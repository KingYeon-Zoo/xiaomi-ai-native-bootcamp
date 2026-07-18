from __future__ import annotations

import asyncio

import pytest
from langgraph.types import Command

from app.agents.repositories import InMemoryRunRepository
from app.agents.runtime import ModerationRuntime
from app.agents.schemas import ModerationStatus, ModerationVerdict


class CompletingGraph:
    async def ainvoke(self, input_value, *, config, **kwargs):
        return {
            "run_id": input_value["run_id"],
            "post_id": input_value["post_id"],
            "decision": {
                "verdict": ModerationVerdict.ALLOW.value,
                "status": ModerationStatus.COMPLETED.value,
                "confidence": 0.93,
                "reasons": ["evidence_consensus"],
                "policy_codes": ["TECH_RELEVANT"],
                "evidence_ids": ["text-1"],
            },
            "trace": [
                {
                    "node": "policy_gate",
                    "status": "completed",
                    "summary": "allow",
                    "timestamp": "2026-07-17T00:00:00+00:00",
                }
            ],
        }


class FailingGraph:
    async def ainvoke(self, input_value, *, config, **kwargs):
        raise RuntimeError("graph exploded")


class PausingGraph:
    async def ainvoke(self, input_value, *, config, **kwargs):
        if isinstance(input_value, Command):
            return {
                "decision": {
                    "verdict": ModerationVerdict.BLOCK.value,
                    "status": ModerationStatus.COMPLETED.value,
                    "confidence": 1.0,
                    "reasons": [input_value.resume["reason"]],
                    "policy_codes": [],
                    "evidence_ids": ["vision-1"],
                },
                "trace": [{"node": "finalize_human"}],
                "human_decision": input_value.resume,
            }
        return {
            "decision": {
                "verdict": ModerationVerdict.HUMAN_REVIEW.value,
                "status": ModerationStatus.WAITING_HUMAN.value,
                "confidence": 0.0,
                "reasons": ["conflicting evidence"],
                "policy_codes": [],
                "evidence_ids": ["vision-1"],
            },
            "trace": [{"node": "human_review"}],
            "__interrupt__": [{"value": {"allowed_actions": ["approve", "reject"]}}],
        }


@pytest.mark.asyncio
async def test_enqueued_run_completes_in_background():
    repository = InMemoryRunRepository()
    runtime = ModerationRuntime(graph=CompletingGraph(), repository=repository)
    await runtime.start()
    try:
        queued = await runtime.enqueue(
            post_id="post-1",
            text="PostgreSQL index tuning",
            image_path=None,
        )
        assert queued.status is ModerationStatus.QUEUED

        completed = await runtime.wait_for_terminal(queued.run_id, timeout=1)

        assert completed.status is ModerationStatus.COMPLETED
        assert completed.verdict is ModerationVerdict.ALLOW
        assert completed.decision["evidence_ids"] == ["text-1"]
        assert completed.trace[0]["node"] == "policy_gate"
    finally:
        await runtime.stop()


@pytest.mark.asyncio
async def test_graph_failure_is_recorded_instead_of_silently_allowing():
    repository = InMemoryRunRepository()
    runtime = ModerationRuntime(graph=FailingGraph(), repository=repository)
    await runtime.start()
    try:
        queued = await runtime.enqueue(
            post_id="post-2",
            text="hello",
            image_path=None,
        )

        failed = await runtime.wait_for_terminal(queued.run_id, timeout=1)

        assert failed.status is ModerationStatus.FAILED
        assert failed.verdict is None
        assert "graph exploded" in failed.error
    finally:
        await runtime.stop()


@pytest.mark.asyncio
async def test_start_requeues_runs_left_queued_before_restart():
    repository = InMemoryRunRepository()
    stale = await repository.create(
        post_id="post-recover",
        text="recover me",
        image_path=None,
    )
    runtime = ModerationRuntime(graph=CompletingGraph(), repository=repository)

    await runtime.start()
    try:
        recovered = await runtime.wait_for_terminal(stale.run_id, timeout=1)
        assert recovered.status is ModerationStatus.COMPLETED
    finally:
        await runtime.stop()


@pytest.mark.asyncio
async def test_human_decision_resumes_the_same_run():
    repository = InMemoryRunRepository()
    runtime = ModerationRuntime(graph=PausingGraph(), repository=repository)
    await runtime.start()
    try:
        queued = await runtime.enqueue(
            post_id="post-review",
            text="image conflict",
            image_path="/uploads/conflict.png",
        )
        paused = await runtime.wait_for_terminal(queued.run_id, timeout=1)
        assert paused.status is ModerationStatus.WAITING_HUMAN

        await runtime.resume(
            queued.run_id,
            decision="reject",
            reviewer_id="admin-1",
            reason="Credential exposure confirmed",
        )
        completed = await runtime.wait_for_terminal(queued.run_id, timeout=1)

        assert completed.run_id == queued.run_id
        assert completed.status is ModerationStatus.COMPLETED
        assert completed.verdict is ModerationVerdict.BLOCK
        assert completed.decision["reasons"] == ["Credential exposure confirmed"]
    finally:
        await runtime.stop()
