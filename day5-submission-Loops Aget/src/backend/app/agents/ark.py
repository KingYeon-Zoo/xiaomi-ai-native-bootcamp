from __future__ import annotations

import asyncio
import base64
import json
import mimetypes
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeVar

from openai import AsyncOpenAI
from PIL import Image
from pydantic import BaseModel


ResponseModel = TypeVar("ResponseModel", bound=BaseModel)


class ArkResponseError(RuntimeError):
    pass


@dataclass(frozen=True)
class ArkConfig:
    base_url: str
    api_key: str
    text_model: str
    vision_model: str
    critic_model: str
    arbiter_model: str
    timeout_seconds: float

    @classmethod
    def from_env(cls) -> "ArkConfig":
        text_model = os.getenv(
            "AGENT_TEXT_MODEL",
            os.getenv("LLM_MODEL", "deepseek-v4-flash-260425"),
        ).strip()
        return cls(
            base_url=os.getenv(
                "ARK_BASE_URL",
                os.getenv(
                    "LLM_BASE_URL",
                    "https://ark.cn-beijing.volces.com/api/v3",
                ),
            ).strip().rstrip("/"),
            api_key=(
                os.getenv("ARK_API_KEY", "").strip()
                or os.getenv("LLM_API_KEY", "").strip()
            ),
            text_model=text_model,
            vision_model=os.getenv(
                "AGENT_VISION_MODEL",
                "doubao-seed-2-0-lite-260428",
            ).strip(),
            critic_model=os.getenv("AGENT_CRITIC_MODEL", text_model).strip(),
            arbiter_model=os.getenv("AGENT_ARBITER_MODEL", text_model).strip(),
            timeout_seconds=float(os.getenv("AGENT_TIMEOUT", "20")),
        )


class ArkResponsesClient:
    """Small adapter around the OpenAI SDK Responses API used by Ark."""

    def __init__(
        self,
        *,
        config: ArkConfig | None = None,
        client: Any | None = None,
        max_attempts: int = 2,
        retry_delay_seconds: float = 0.2,
    ) -> None:
        self.config = config or ArkConfig.from_env()
        self.max_attempts = max(1, max_attempts)
        self.retry_delay_seconds = max(0.0, retry_delay_seconds)
        self._client = client

        if self._client is None and self.config.api_key:
            self._client = AsyncOpenAI(
                base_url=self.config.base_url,
                api_key=self.config.api_key,
                timeout=self.config.timeout_seconds,
                max_retries=0,
            )

    async def parse(
        self,
        *,
        model: str,
        instructions: str,
        input_items: list[dict[str, Any]],
        response_model: type[ResponseModel],
    ) -> ResponseModel:
        if self._client is None:
            raise ArkResponseError(
                "ARK_API_KEY/LLM_API_KEY is not configured; cloud evidence is unavailable"
            )

        last_error: Exception | None = None
        for attempt in range(self.max_attempts):
            try:
                response = await self._client.responses.parse(
                    model=model,
                    instructions=instructions,
                    input=input_items,
                    text_format=response_model,
                )
                return self._extract_parsed(response, response_model)
            except Exception as exc:
                last_error = exc
                if self._json_schema_unsupported(exc):
                    try:
                        response = await self._client.responses.create(
                            model=model,
                            instructions=(
                                f"{instructions}\nReturn one JSON object matching "
                                f"this schema exactly: "
                                f"{json.dumps(response_model.model_json_schema(), ensure_ascii=False)}"
                            ),
                            input=input_items,
                            text={"format": {"type": "json_object"}},
                        )
                        return self._extract_parsed(response, response_model)
                    except Exception as fallback_exc:
                        last_error = fallback_exc
                if attempt + 1 < self.max_attempts and self.retry_delay_seconds:
                    await asyncio.sleep(
                        self.retry_delay_seconds * (2**attempt)
                    )

        raise ArkResponseError(
            f"Ark returned no valid {response_model.__name__} after "
            f"{self.max_attempts} attempt(s): {last_error}"
        ) from last_error

    @staticmethod
    def _json_schema_unsupported(error: Exception) -> bool:
        message = str(error).lower()
        return "json_schema" in message and (
            "not supported" in message or "not valid" in message
        )

    @staticmethod
    def _extract_parsed(
        response: Any,
        response_model: type[ResponseModel],
    ) -> ResponseModel:
        for output in getattr(response, "output", []):
            if getattr(output, "type", None) != "message":
                continue
            for content in getattr(output, "content", []):
                parsed = getattr(content, "parsed", None)
                if parsed is not None:
                    if isinstance(parsed, response_model):
                        return parsed
                    return response_model.model_validate(parsed)

        output_text = getattr(response, "output_text", "")
        if output_text:
            return response_model.model_validate_json(output_text)
        raise ValueError("response contained neither parsed output nor output_text")


class ImageInputAdapter:
    """Validate a local upload and convert it into an inline image data URL."""

    def __init__(
        self,
        *,
        base_dir: str | Path | None = None,
        max_bytes: int = 8 * 1024 * 1024,
    ) -> None:
        self.base_dir = Path(base_dir or Path.cwd()).resolve()
        self.max_bytes = max_bytes

    def to_data_url(self, image_path: str | Path) -> str:
        path = self._resolve(image_path)
        if not path.is_file():
            raise ValueError(f"image file does not exist: {path}")
        if path.stat().st_size > self.max_bytes:
            raise ValueError(f"image exceeds {self.max_bytes} byte limit")

        mime_type = mimetypes.guess_type(path.name)[0]
        if mime_type not in {"image/jpeg", "image/png", "image/webp"}:
            raise ValueError(f"unsupported image type: {mime_type or 'unknown'}")

        try:
            with Image.open(path) as image:
                image.verify()
        except Exception as exc:
            raise ValueError("image is corrupt or unreadable") from exc

        encoded = base64.b64encode(path.read_bytes()).decode("ascii")
        return f"data:{mime_type};base64,{encoded}"

    def _resolve(self, image_path: str | Path) -> Path:
        path = Path(image_path)
        if path.is_absolute() and path.exists():
            return path.resolve()
        return (self.base_dir / str(image_path).lstrip("/")).resolve()
