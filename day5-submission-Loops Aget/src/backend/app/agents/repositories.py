from __future__ import annotations

import asyncio
import uuid
from datetime import datetime, timezone
from typing import Any, Protocol

from app.agents.schemas import ModerationRun, ModerationStatus


class RunRepository(Protocol):
    async def create(
        self,
        *,
        post_id: str,
        text: str,
        image_path: str | None,
    ) -> ModerationRun: ...

    async def get(self, run_id: str) -> ModerationRun | None: ...

    async def update(self, run_id: str, **changes: Any) -> ModerationRun: ...

    async def list_recoverable(self) -> list[ModerationRun]: ...


class InMemoryRunRepository:
    def __init__(self) -> None:
        self._runs: dict[str, ModerationRun] = {}
        self._lock = asyncio.Lock()

    async def create(
        self,
        *,
        post_id: str,
        text: str,
        image_path: str | None,
    ) -> ModerationRun:
        run = ModerationRun(
            run_id=f"run_{uuid.uuid4().hex}",
            post_id=post_id,
            text=text,
            image_path=image_path,
        )
        async with self._lock:
            self._runs[run.run_id] = run
        return run.model_copy(deep=True)

    async def get(self, run_id: str) -> ModerationRun | None:
        async with self._lock:
            run = self._runs.get(run_id)
            return run.model_copy(deep=True) if run else None

    async def update(self, run_id: str, **changes: Any) -> ModerationRun:
        async with self._lock:
            current = self._runs.get(run_id)
            if current is None:
                raise KeyError(run_id)
            payload = current.model_dump()
            payload.update(changes)
            payload["updated_at"] = datetime.now(timezone.utc)
            updated = ModerationRun.model_validate(payload)
            self._runs[run_id] = updated
            return updated.model_copy(deep=True)

    async def list_recoverable(self) -> list[ModerationRun]:
        async with self._lock:
            return [
                run.model_copy(deep=True)
                for run in self._runs.values()
                if run.status in {ModerationStatus.QUEUED, ModerationStatus.RUNNING}
            ]


class MongoRunRepository:
    """PyMongo-backed run store; sync driver calls are isolated in threads."""

    def __init__(self, collection) -> None:
        self.collection = collection

    async def create(
        self,
        *,
        post_id: str,
        text: str,
        image_path: str | None,
    ) -> ModerationRun:
        run = ModerationRun(
            run_id=f"run_{uuid.uuid4().hex}",
            post_id=post_id,
            text=text,
            image_path=image_path,
        )
        document = run.model_dump(mode="python")
        document["_id"] = run.run_id
        await asyncio.to_thread(self.collection.insert_one, document)
        return run

    async def get(self, run_id: str) -> ModerationRun | None:
        document = await asyncio.to_thread(
            self.collection.find_one,
            {"_id": run_id},
        )
        if document is None:
            return None
        document.pop("_id", None)
        return ModerationRun.model_validate(document)

    async def update(self, run_id: str, **changes: Any) -> ModerationRun:
        changes["updated_at"] = datetime.now(timezone.utc)
        await asyncio.to_thread(
            self.collection.update_one,
            {"_id": run_id},
            {"$set": changes},
        )
        run = await self.get(run_id)
        if run is None:
            raise KeyError(run_id)
        return run

    async def list_recoverable(self) -> list[ModerationRun]:
        def fetch():
            return list(
                self.collection.find(
                    {
                        "status": {
                            "$in": [
                                ModerationStatus.QUEUED.value,
                                ModerationStatus.RUNNING.value,
                            ]
                        }
                    }
                )
            )

        documents = await asyncio.to_thread(fetch)
        runs = []
        for document in documents:
            document.pop("_id", None)
            runs.append(ModerationRun.model_validate(document))
        return runs
