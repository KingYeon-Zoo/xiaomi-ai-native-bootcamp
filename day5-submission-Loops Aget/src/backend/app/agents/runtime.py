from __future__ import annotations

import asyncio
from contextlib import suppress
from typing import Any, Awaitable, Callable

from langgraph.types import Command

from app.agents.repositories import RunRepository
from app.agents.schemas import (
    ModerationRun,
    ModerationStatus,
    ModerationVerdict,
)


class ModerationRuntime:
    """Single-process durable queue backed by a run repository and checkpoints."""

    TERMINAL_STATUSES = {
        ModerationStatus.COMPLETED,
        ModerationStatus.FAILED,
        ModerationStatus.WAITING_HUMAN,
    }

    def __init__(
        self,
        *,
        graph,
        repository: RunRepository,
        result_handler: Callable[
            [ModerationRun], Awaitable[None]
        ] | None = None,
    ) -> None:
        self.graph = graph
        self.repository = repository
        self.result_handler = result_handler
        self._queue: asyncio.Queue[
            tuple[str, dict[str, str] | None] | None
        ] = asyncio.Queue()
        self._worker: asyncio.Task | None = None

    async def start(self) -> None:
        if self._worker and not self._worker.done():
            return
        for run in await self.repository.list_recoverable():
            await self._queue.put((run.run_id, None))
        self._worker = asyncio.create_task(
            self._work_loop(),
            name="moderation-agent-worker",
        )

    async def stop(self) -> None:
        if not self._worker:
            return
        await self._queue.put(None)
        with suppress(asyncio.CancelledError):
            await self._worker
        self._worker = None

    async def enqueue(
        self,
        *,
        post_id: str,
        text: str,
        image_path: str | None,
    ) -> ModerationRun:
        run = await self.repository.create(
            post_id=post_id,
            text=text,
            image_path=image_path,
        )
        await self._queue.put((run.run_id, None))
        return run

    async def resume(
        self,
        run_id: str,
        *,
        decision: str,
        reviewer_id: str,
        reason: str,
    ) -> ModerationRun:
        run = await self.repository.get(run_id)
        if run is None:
            raise KeyError(run_id)
        if run.status is not ModerationStatus.WAITING_HUMAN:
            raise ValueError("only waiting_human runs can be resumed")
        if decision not in {"approve", "reject"}:
            raise ValueError("decision must be approve or reject")

        updated = await self.repository.update(
            run_id,
            status=ModerationStatus.QUEUED,
            error=None,
        )
        await self._queue.put(
            (
                run_id,
                {
                    "decision": decision,
                    "reviewer_id": reviewer_id,
                    "reason": reason,
                },
            )
        )
        return updated

    async def get_run(self, run_id: str) -> ModerationRun | None:
        return await self.repository.get(run_id)

    async def wait_for_terminal(
        self,
        run_id: str,
        *,
        timeout: float,
        poll_interval: float = 0.01,
    ) -> ModerationRun:
        async def wait() -> ModerationRun:
            while True:
                run = await self.repository.get(run_id)
                if run is None:
                    raise KeyError(run_id)
                if run.status in self.TERMINAL_STATUSES:
                    return run
                await asyncio.sleep(poll_interval)

        return await asyncio.wait_for(wait(), timeout=timeout)

    async def _work_loop(self) -> None:
        while True:
            job = await self._queue.get()
            try:
                if job is None:
                    return
                run_id, resume_payload = job
                await self._process(run_id, resume_payload=resume_payload)
            finally:
                self._queue.task_done()

    async def _process(
        self,
        run_id: str,
        *,
        resume_payload: dict[str, str] | None = None,
    ) -> None:
        run = await self.repository.get(run_id)
        if run is None:
            return
        await self.repository.update(
            run_id,
            status=ModerationStatus.RUNNING,
            error=None,
        )
        try:
            input_value: dict[str, Any] | Command
            if resume_payload is not None:
                input_value = Command(resume=resume_payload)
            else:
                input_value = {
                    "run_id": run.run_id,
                    "post_id": run.post_id,
                    "text": run.text,
                    "image_path": run.image_path,
                    "assessments": [],
                    "trace": [],
                }
            result = await self.graph.ainvoke(
                input_value,
                config={"configurable": {"thread_id": run.run_id}},
                durability="sync",
            )
            decision: dict[str, Any] | None = result.get("decision")
            if decision is None:
                raise RuntimeError("graph completed without a decision")
            status = ModerationStatus(decision["status"])
            verdict = ModerationVerdict(decision["verdict"])
            completed = await self.repository.update(
                run_id,
                status=status,
                verdict=verdict,
                decision=decision,
                trace=result.get("trace", []),
            )
            if self.result_handler is not None:
                await self.result_handler(completed)
        except Exception as exc:
            await self.repository.update(
                run_id,
                status=ModerationStatus.FAILED,
                verdict=None,
                error=str(exc),
            )
