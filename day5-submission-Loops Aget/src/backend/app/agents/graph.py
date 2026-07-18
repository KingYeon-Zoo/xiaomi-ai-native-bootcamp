from __future__ import annotations

import operator
from datetime import datetime, timezone
from typing import Annotated, Any

from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt
from typing_extensions import TypedDict

from app.agents.moderators import ArbitrationPayload
from app.agents.policy import ModerationPolicy, RiskRouter
from app.agents.schemas import (
    AgentAssessment,
    Evidence,
    ModerationDecision,
    ModerationStatus,
    ModerationVerdict,
)


class ModerationState(TypedDict, total=False):
    run_id: str
    post_id: str
    text: str
    image_path: str | None
    assessments: Annotated[list[dict[str, Any]], operator.add]
    trace: Annotated[list[dict[str, Any]], operator.add]
    requires_debate: bool
    route_reasons: list[str]
    arbitration: dict[str, Any] | None
    decision: dict[str, Any] | None
    human_decision: dict[str, Any] | None


def _trace(node: str, summary: str, *, status: str = "completed") -> dict[str, Any]:
    return {
        "node": node,
        "status": status,
        "summary": summary,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


def _assessment_dict(item: AgentAssessment) -> dict[str, Any]:
    return item.model_dump(mode="json")


def _assessments(state: ModerationState) -> list[AgentAssessment]:
    return [
        item
        if isinstance(item, AgentAssessment)
        else AgentAssessment.model_validate(item)
        for item in state.get("assessments", [])
    ]


def _unavailable(agent_name: str, error: Exception) -> AgentAssessment:
    return AgentAssessment(
        agent_name=agent_name,
        recommendation=ModerationVerdict.HUMAN_REVIEW,
        confidence=0.0,
        unavailable=True,
        error=str(error),
        evidences=[
            Evidence(
                evidence_id=f"{agent_name}-unavailable",
                source=agent_name,
                category="agent_unavailable",
                severity=0.5,
                confidence=1.0,
                summary=f"{agent_name} failed to produce required evidence.",
                policy_codes=["REVIEW_AGENT_UNAVAILABLE"],
            )
        ],
    )


def build_moderation_graph(
    *,
    rule_tool,
    text_agent,
    vision_agent,
    critic_agent,
    arbitrator,
    risk_router: RiskRouter,
    policy: ModerationPolicy,
    checkpointer,
):
    async def precheck(state: ModerationState) -> dict[str, Any]:
        try:
            result = rule_tool(state.get("text", ""))
            if hasattr(result, "__await__"):
                result = await result
            assessment = (
                result
                if isinstance(result, AgentAssessment)
                else AgentAssessment.model_validate(result)
            )
        except Exception as exc:
            assessment = _unavailable("rule", exc)
        return {
            "assessments": [_assessment_dict(assessment)],
            "trace": [_trace("precheck", "Deterministic rule evidence collected")],
        }

    def route_precheck(state: ModerationState) -> str:
        for assessment in _assessments(state):
            for evidence in assessment.evidences:
                if (
                    evidence.source in policy.TRUSTED_HARD_POLICY_SOURCES
                    and any(
                        code.startswith("HARD_BLOCK_")
                        for code in evidence.policy_codes
                    )
                ):
                    return "hard_block"
        return "analyze"

    async def dispatch(_: ModerationState) -> dict[str, Any]:
        return {"trace": [_trace("dispatch", "Expert evidence collection started")]}

    async def analyze_text(state: ModerationState) -> dict[str, Any]:
        try:
            assessment = await text_agent.analyze(state.get("text", ""))
        except Exception as exc:
            assessment = _unavailable("text_agent", exc)
        return {
            "assessments": [_assessment_dict(assessment)],
            "trace": [_trace("text_agent", assessment.recommendation.value)],
        }

    async def analyze_vision(state: ModerationState) -> dict[str, Any]:
        image_path = state.get("image_path")
        if not image_path:
            return {
                "trace": [_trace("vision_agent", "Skipped: no image", status="skipped")]
            }
        try:
            assessment = await vision_agent.analyze(
                text=state.get("text", ""),
                image_path=image_path,
            )
        except Exception as exc:
            assessment = _unavailable("vision_agent", exc)
        return {
            "assessments": [_assessment_dict(assessment)],
            "trace": [_trace("vision_agent", assessment.recommendation.value)],
        }

    async def risk_route(state: ModerationState) -> dict[str, Any]:
        route = risk_router.route(_assessments(state))
        return {
            "requires_debate": route.requires_debate,
            "route_reasons": route.reasons,
            "trace": [
                _trace(
                    "risk_route",
                    "debate" if route.requires_debate else "fast_path",
                )
            ],
        }

    def route_risk(state: ModerationState) -> str:
        return "debate" if state.get("requires_debate") else "fast_path"

    async def critic(state: ModerationState) -> dict[str, Any]:
        try:
            assessment = await critic_agent.review(
                state.get("text", ""),
                _assessments(state),
            )
        except Exception as exc:
            assessment = _unavailable("critic_agent", exc)
        return {
            "assessments": [_assessment_dict(assessment)],
            "trace": [_trace("critic_agent", assessment.recommendation.value)],
        }

    async def arbitrate(state: ModerationState) -> dict[str, Any]:
        try:
            result = await arbitrator.arbitrate(
                text=state.get("text", ""),
                assessments=_assessments(state),
            )
        except Exception as exc:
            result = ArbitrationPayload(
                recommendation=ModerationVerdict.HUMAN_REVIEW,
                confidence=0.0,
                summary=f"Arbitrator unavailable: {exc}",
                evidence_ids=[],
            )
        return {
            "arbitration": result.model_dump(mode="json"),
            "trace": [_trace("arbitrator", result.recommendation.value)],
        }

    async def policy_gate(state: ModerationState) -> dict[str, Any]:
        assessments = _assessments(state)
        has_trusted_hard_block = any(
            evidence.source in policy.TRUSTED_HARD_POLICY_SOURCES
            and any(code.startswith("HARD_BLOCK_") for code in evidence.policy_codes)
            for assessment in assessments
            for evidence in assessment.evidences
        )
        required_sources = (
            {"rule"}
            if has_trusted_hard_block
            else {"rule", "text_agent"}
            | ({"vision_agent"} if state.get("image_path") else set())
        )
        arbitration_payload = state.get("arbitration")
        arbitration = (
            ModerationVerdict(arbitration_payload["recommendation"])
            if arbitration_payload
            else None
        )
        decision = policy.decide(
            assessments=assessments,
            required_sources=required_sources,
            arbitration=arbitration,
        )
        return {
            "decision": decision.model_dump(mode="json"),
            "trace": [_trace("policy_gate", decision.verdict.value)],
        }

    def route_policy(state: ModerationState) -> str:
        decision = ModerationDecision.model_validate(state["decision"])
        return (
            "human"
            if decision.status is ModerationStatus.WAITING_HUMAN
            else "complete"
        )

    async def human_review(state: ModerationState) -> dict[str, Any]:
        response = interrupt(
            {
                "run_id": state["run_id"],
                "post_id": state["post_id"],
                "decision": state["decision"],
                "allowed_actions": ["approve", "reject"],
            }
        )
        if response.get("decision") not in {"approve", "reject"}:
            raise ValueError("human decision must be approve or reject")
        return {
            "human_decision": response,
            "trace": [_trace("human_review", response["decision"])],
        }

    async def finalize_human(state: ModerationState) -> dict[str, Any]:
        human = state["human_decision"]
        previous = ModerationDecision.model_validate(state["decision"])
        verdict = (
            ModerationVerdict.ALLOW
            if human["decision"] == "approve"
            else ModerationVerdict.BLOCK
        )
        decision = ModerationDecision(
            verdict=verdict,
            status=ModerationStatus.COMPLETED,
            confidence=1.0,
            reasons=[human.get("reason") or f"human_{human['decision']}"],
            policy_codes=previous.policy_codes,
            evidence_ids=previous.evidence_ids,
        )
        return {
            "decision": decision.model_dump(mode="json"),
            "trace": [_trace("finalize_human", verdict.value)],
        }

    builder = StateGraph(ModerationState)
    builder.add_node("precheck", precheck)
    builder.add_node("dispatch", dispatch)
    builder.add_node("text_agent", analyze_text)
    builder.add_node("vision_agent", analyze_vision)
    builder.add_node("risk_route", risk_route)
    builder.add_node("critic_agent", critic)
    builder.add_node("arbitrator", arbitrate)
    builder.add_node("policy_gate", policy_gate)
    builder.add_node("human_review", human_review)
    builder.add_node("finalize_human", finalize_human)

    builder.add_edge(START, "precheck")
    builder.add_conditional_edges(
        "precheck",
        route_precheck,
        {"hard_block": "policy_gate", "analyze": "dispatch"},
    )
    builder.add_edge("dispatch", "text_agent")
    builder.add_edge("dispatch", "vision_agent")
    builder.add_edge(["text_agent", "vision_agent"], "risk_route")
    builder.add_conditional_edges(
        "risk_route",
        route_risk,
        {"debate": "critic_agent", "fast_path": "policy_gate"},
    )
    builder.add_edge("critic_agent", "arbitrator")
    builder.add_edge("arbitrator", "policy_gate")
    builder.add_conditional_edges(
        "policy_gate",
        route_policy,
        {"human": "human_review", "complete": END},
    )
    builder.add_edge("human_review", "finalize_human")
    builder.add_edge("finalize_human", END)
    return builder.compile(checkpointer=checkpointer)
