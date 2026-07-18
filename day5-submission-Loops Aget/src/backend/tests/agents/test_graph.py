from __future__ import annotations

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
import pytest

from app.agents.graph import build_moderation_graph
from app.agents.moderators import ArbitrationPayload
from app.agents.policy import ModerationPolicy, RiskRouter
from app.agents.schemas import (
    AgentAssessment,
    Evidence,
    ModerationStatus,
    ModerationVerdict,
)


def make_assessment(
    agent_name: str,
    verdict: ModerationVerdict,
    *,
    evidence_id: str | None = None,
    severity: float = 0.05,
    confidence: float = 0.95,
    policy_codes: list[str] | None = None,
    unavailable: bool = False,
) -> AgentAssessment:
    return AgentAssessment(
        agent_name=agent_name,
        recommendation=verdict,
        confidence=confidence,
        unavailable=unavailable,
        evidences=[
            Evidence(
                evidence_id=evidence_id or f"{agent_name}-1",
                source=agent_name,
                category="test",
                severity=severity,
                confidence=confidence,
                summary=f"{agent_name} finding",
                policy_codes=policy_codes or [],
            )
        ],
    )


class StubTextAgent:
    def __init__(self, result):
        self.result = result
        self.calls = 0

    async def analyze(self, text):
        self.calls += 1
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


class StubVisionAgent:
    def __init__(self, result):
        self.result = result
        self.calls = 0

    async def analyze(self, *, text, image_path):
        self.calls += 1
        if isinstance(self.result, Exception):
            raise self.result
        return self.result


class StubCritic:
    def __init__(self, result):
        self.result = result
        self.calls = 0

    async def review(self, text, assessments):
        self.calls += 1
        return self.result


class StubArbitrator:
    def __init__(self, result):
        self.result = result
        self.calls = 0

    async def arbitrate(self, *, text, assessments):
        self.calls += 1
        return self.result


def graph_with(
    *,
    rule,
    text,
    vision=None,
    critic=None,
    arbitration=ModerationVerdict.ALLOW,
):
    text_agent = StubTextAgent(text)
    vision_agent = StubVisionAgent(
        vision
        or make_assessment("vision_agent", ModerationVerdict.ALLOW)
    )
    critic_agent = StubCritic(
        critic
        or make_assessment("critic_agent", ModerationVerdict.ALLOW)
    )
    arbitrator = StubArbitrator(
        ArbitrationPayload(
            recommendation=arbitration,
            confidence=0.9,
            summary="bounded arbitration",
            evidence_ids=[],
        )
    )
    graph = build_moderation_graph(
        rule_tool=lambda _: rule,
        text_agent=text_agent,
        vision_agent=vision_agent,
        critic_agent=critic_agent,
        arbitrator=arbitrator,
        risk_router=RiskRouter(),
        policy=ModerationPolicy(),
        checkpointer=InMemorySaver(),
    )
    return graph, text_agent, vision_agent, critic_agent, arbitrator


def initial_state(*, image_path=None):
    return {
        "run_id": "run-1",
        "post_id": "post-1",
        "text": "PostgreSQL index tuning",
        "image_path": image_path,
        "assessments": [],
        "trace": [],
    }


@pytest.mark.asyncio
async def test_fast_path_skips_vision_critic_and_arbitrator_for_text_only_post():
    graph, text, vision, critic, arbitrator = graph_with(
        rule=make_assessment("rule", ModerationVerdict.ALLOW),
        text=make_assessment("text_agent", ModerationVerdict.ALLOW),
    )

    result = await graph.ainvoke(
        initial_state(),
        config={"configurable": {"thread_id": "run-1"}},
    )

    assert result["decision"]["verdict"] == ModerationVerdict.ALLOW.value
    assert text.calls == 1
    assert vision.calls == 0
    assert critic.calls == 0
    assert arbitrator.calls == 0
    assert {"precheck", "text_agent", "risk_route", "policy_gate"} <= {
        item["node"] for item in result["trace"]
    }


@pytest.mark.asyncio
async def test_hard_rule_block_short_circuits_all_cloud_agents():
    graph, text, vision, critic, arbitrator = graph_with(
        rule=make_assessment(
            "rule",
            ModerationVerdict.BLOCK,
            severity=0.99,
            policy_codes=["HARD_BLOCK_VIOLENCE"],
        ),
        text=make_assessment("text_agent", ModerationVerdict.ALLOW),
    )

    result = await graph.ainvoke(
        initial_state(image_path="/uploads/image.png"),
        config={"configurable": {"thread_id": "run-hard-block"}},
    )

    assert result["decision"]["verdict"] == ModerationVerdict.BLOCK.value
    assert text.calls == vision.calls == critic.calls == arbitrator.calls == 0


@pytest.mark.asyncio
async def test_conflict_runs_critic_and_arbitrator_then_interrupts_for_human():
    graph, text, vision, critic, arbitrator = graph_with(
        rule=make_assessment("rule", ModerationVerdict.ALLOW),
        text=make_assessment("text_agent", ModerationVerdict.ALLOW),
        vision=make_assessment(
            "vision_agent",
            ModerationVerdict.BLOCK,
            severity=0.72,
        ),
        critic=make_assessment(
            "critic_agent",
            ModerationVerdict.HUMAN_REVIEW,
            severity=0.68,
        ),
        arbitration=ModerationVerdict.HUMAN_REVIEW,
    )
    config = {"configurable": {"thread_id": "run-conflict"}}

    paused = await graph.ainvoke(
        initial_state(image_path="/uploads/image.png"),
        config=config,
    )

    assert paused["decision"]["status"] == ModerationStatus.WAITING_HUMAN.value
    assert "__interrupt__" in paused
    assert critic.calls == 1
    assert arbitrator.calls == 1

    resumed = await graph.ainvoke(
        Command(
            resume={
                "decision": "reject",
                "reviewer_id": "admin-1",
                "reason": "Credential exposure confirmed",
            }
        ),
        config=config,
    )

    assert resumed["decision"]["verdict"] == ModerationVerdict.BLOCK.value
    assert resumed["decision"]["status"] == ModerationStatus.COMPLETED.value
    assert resumed["human_decision"]["reviewer_id"] == "admin-1"
