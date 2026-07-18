"""
LLM Text Moderator — OpenAI-compatible Chat Completions API

Zero ML dependencies. Talks to any OpenAI-compatible endpoint
(DeepSeek / 通义千问 / 智谱 / Moonshot / OpenAI itself) over plain HTTP.

The LLM only judges ONE thing: is the post genuinely about technology?
All harm detection (abuse / spam / scam / threats) is handled upstream by
the deterministic RuleEngine, so we keep the prompt short and cheap.

Config via environment variables (see backend/.env):
    LLM_BASE_URL   e.g. https://api.deepseek.com   (no trailing /v1)
    LLM_API_KEY    your provider API key
    LLM_MODEL      e.g. deepseek-chat
"""

import requests
import json
import os
import sys
import re
import time
import hashlib
from typing import Dict, Any

LLM_BASE_URL = os.getenv("LLM_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3").strip().rstrip("/")
LLM_API_KEY = os.getenv("LLM_API_KEY", "").strip()
LLM_MODEL = os.getenv("LLM_MODEL", "deepseek-v4-flash-260425").strip()
LLM_MAX_INPUT = int(os.getenv("LLM_MAX_INPUT", "1000"))
LLM_MAX_TOKENS = int(os.getenv("LLM_MAX_TOKENS", "100"))
LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", "20"))


class LLMModerator:
    """Judges tech-relevance of a post via an OpenAI-compatible LLM API."""

    def __init__(self):
        self.base_url = LLM_BASE_URL
        self.api_key = LLM_API_KEY
        self.model = LLM_MODEL
        self.max_input = LLM_MAX_INPUT
        self.max_tokens = LLM_MAX_TOKENS
        self.timeout = LLM_TIMEOUT
        self._cache: Dict[str, Any] = {}
        self._cache_hits = 0
        self._cache_misses = 0

        print(f"🔥 LLMModerator initialized — model: {self.model} @ {self.base_url}")
        sys.stdout.flush()

        self._available = self._check_availability()
        if not self._available:
            print("⚠️ LLM API not configured/reachable. Falling back to keyword scoring.")
        sys.stdout.flush()

    def _check_availability(self) -> bool:
        """Available only if an API key is present. We avoid a network
        probe on startup so the server boots instantly; connection errors
        during analyze() degrade gracefully to the keyword fallback."""
        if not self.api_key:
            print("⚠️ LLM_API_KEY is empty — set it in backend/.env")
            sys.stdout.flush()
            return False
        return True

    def _get_cache_key(self, text: str) -> str:
        return hashlib.md5(text[:200].encode()).hexdigest()

    def _call_llm(self, text: str) -> str:
        """Call the OpenAI-compatible /v1/chat/completions endpoint.

        Returns the raw assistant message content, or "" on any failure.
        """
        if not self._available:
            return ""

        system_prompt = (
            "You are a strict content classifier for a developer-only social "
            "platform that ONLY allows technology content (coding, software, "
            "DevOps, ML, architecture, open-source). Judge whether a post is "
            "genuinely about technology. Reply with ONLY a JSON object, no prose."
        )
        user_prompt = (
            'Return ONLY: {"tech_relevance": <float 0.0-1.0>, "reason": "<short>"}\n'
            "1.0 = clearly a software/tech topic. 0.0 = not tech at all.\n"
            'Examples: "how to optimize a Postgres index" -> 0.95; '
            '"my favorite pizza topping" -> 0.05; '
            '"python is a great snake and language" -> 0.4\n\n'
            f"Post: {text[:self.max_input]}"
        )

        try:
            # base_url already includes the API version segment
            # (ARK: /api/v3, DeepSeek: append /v1 in the env value).
            resp = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.1,
                    "max_tokens": self.max_tokens,
                    "response_format": {"type": "json_object"},
                    "stream": False,
                },
                timeout=self.timeout,
            )
            if resp.status_code == 200:
                data = resp.json()
                return data.get("choices", [{}])[0].get("message", {}).get("content", "")
            print(f"⚠️ LLM API returned {resp.status_code}: {resp.text[:200]}")
            sys.stdout.flush()
        except Exception as e:
            print(f"⚠️ LLM API error: {e}")
            sys.stdout.flush()
        return ""

    def analyze(self, text: str) -> Dict[str, Any]:
        """Return the same result shape as OllamaModerator.analyze()."""
        start = time.time()

        if not text or not text.strip():
            return self._fallback("")

        cache_key = self._get_cache_key(text)
        if cache_key in self._cache:
            self._cache_hits += 1
            return self._cache[cache_key]
        self._cache_misses += 1

        response = self._call_llm(text)

        try:
            # response_format=json_object should give clean JSON, but some
            # providers wrap it in prose — extract the first JSON object.
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                tech_score = max(0.0, min(1.0, float(data.get("tech_relevance", 0.5))))
                tech_zone = self._zone(tech_score)

                result = {
                    "scores": {
                        "tech_relevance": tech_score,
                        # Harm dimensions are handled by the RuleEngine upstream,
                        # so the LLM path reports them as 0.
                        "toxicity": 0.0, "sexual": 0.0, "self_harm": 0.0,
                        "violence": 0.0, "drugs": 0.0, "threats": 0.0,
                    },
                    "flagged_categories": [],
                    "is_harmful": False,
                    "is_tech_relevant": tech_score > 0.45,
                    "primary_category": "tech" if tech_score > 0.45 else "safe",
                    "tech_zone": tech_zone,
                    "reason": str(data.get("reason", ""))[:200],
                    "processing_time_ms": int((time.time() - start) * 1000),
                }

                if len(self._cache) < 200:
                    self._cache[cache_key] = result

                print(f"✅ LLM result: tech={tech_score:.3f} zone={tech_zone}")
                sys.stdout.flush()
                return result
        except Exception as e:
            print(f"⚠️ LLM parse error: {e}")
            sys.stdout.flush()

        return self._fallback(text)

    @staticmethod
    def _zone(tech_score: float) -> str:
        if tech_score > 0.45:
            return "tech"
        if tech_score > 0.25:
            return "review"
        return "off_topic"

    def _fallback(self, text: str) -> Dict[str, Any]:
        """Keyword-based tech scoring when the LLM API is unavailable.
        Mirrors OllamaModerator._fallback so downstream behaviour is identical."""
        text_lower = text.lower()
        tech_keywords = [
            'python', 'react', 'docker', 'api', 'code', 'database',
            'backend', 'frontend', 'microservices', 'kubernetes',
            'cloud', 'data', 'analytics', 'insights', 'algorithm',
            'programming', 'software', 'developer', 'engineering',
        ]
        tech_score = min(sum(1 for kw in tech_keywords if kw in text_lower) * 0.1, 0.9)
        tech_zone = self._zone(tech_score)

        return {
            "scores": {
                "tech_relevance": tech_score,
                "toxicity": 0.0, "sexual": 0.0, "self_harm": 0.0,
                "violence": 0.0, "drugs": 0.0, "threats": 0.0,
            },
            "flagged_categories": [],
            "is_harmful": False,
            "is_tech_relevant": tech_score > 0.45,
            "primary_category": "tech" if tech_score > 0.45 else "safe",
            "tech_zone": tech_zone,
            "reason": "keyword fallback (LLM API unavailable)",
            "processing_time_ms": 3,
        }


_llm_moderator = None


def get_llm_moderator() -> LLMModerator:
    global _llm_moderator
    if _llm_moderator is None:
        _llm_moderator = LLMModerator()
    return _llm_moderator
