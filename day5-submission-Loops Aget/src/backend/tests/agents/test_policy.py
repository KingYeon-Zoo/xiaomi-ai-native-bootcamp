from app.agents.policy import ModerationPolicy, RiskRouter
from app.agents.schemas import (
    AgentAssessment,
    Evidence,
    ModerationStatus,
    ModerationVerdict,
)


def evidence(
    evidence_id: str,
    source: str,
    *,
    category: str = "safe",
    severity: float = 0.05,
    confidence: float = 0.95,
    policy_codes: list[str] | None = None,
) -> Evidence:
    return Evidence(
        evidence_id=evidence_id,
        source=source,
        category=category,
        severity=severity,
        confidence=confidence,
        summary=f"{source} evidence",
        policy_codes=policy_codes or [],
    )


def assessment(
    name: str,
    recommendation: ModerationVerdict,
    item: Evidence,
    *,
    confidence: float = 0.9,
    unavailable: bool = False,
) -> AgentAssessment:
    return AgentAssessment(
        agent_name=name,
        recommendation=recommendation,
        confidence=confidence,
        evidences=[item],
        unavailable=unavailable,
    )


def test_hard_block_evidence_cannot_be_overridden_by_allow_recommendation():
    policy = ModerationPolicy()
    hard_block = evidence(
        "rule-1",
        "rule",
        category="self_harm",
        severity=0.98,
        policy_codes=["HARD_BLOCK_SELF_HARM"],
    )

    decision = policy.decide(
        assessments=[
            assessment("text_agent", ModerationVerdict.ALLOW, hard_block),
        ],
        required_sources={"rule", "text_agent"},
        arbitration=ModerationVerdict.ALLOW,
    )

    assert decision.verdict is ModerationVerdict.BLOCK
    assert decision.status is ModerationStatus.COMPLETED
    assert decision.evidence_ids == ["rule-1"]
    assert "HARD_BLOCK_SELF_HARM" in decision.policy_codes


def test_llm_cannot_grant_itself_hard_policy_authority():
    policy = ModerationPolicy()
    untrusted_code = evidence(
        "text-1",
        "text_agent",
        category="violence",
        severity=0.9,
        policy_codes=["HARD_BLOCK_VIOLENCE"],
    )

    decision = policy.decide(
        assessments=[
            assessment(
                "text_agent",
                ModerationVerdict.ALLOW,
                untrusted_code,
            ),
        ],
        required_sources={"text_agent"},
        arbitration=ModerationVerdict.ALLOW,
    )

    assert decision.verdict is ModerationVerdict.ALLOW


def test_missing_required_vision_evidence_routes_to_human_review():
    policy = ModerationPolicy()
    text = evidence("text-1", "text_agent")

    decision = policy.decide(
        assessments=[
            assessment("text_agent", ModerationVerdict.ALLOW, text),
        ],
        required_sources={"rule", "text_agent", "vision_agent"},
        arbitration=ModerationVerdict.ALLOW,
    )

    assert decision.verdict is ModerationVerdict.HUMAN_REVIEW
    assert decision.status is ModerationStatus.WAITING_HUMAN
    assert "vision_agent" in decision.reasons[0]


def test_consistent_high_confidence_evidence_can_be_allowed():
    policy = ModerationPolicy()
    rule = evidence("rule-1", "rule")
    text = evidence("text-1", "text_agent")
    vision = evidence("vision-1", "vision_agent")

    decision = policy.decide(
        assessments=[
            assessment("rule", ModerationVerdict.ALLOW, rule),
            assessment("text_agent", ModerationVerdict.ALLOW, text),
            assessment("vision_agent", ModerationVerdict.ALLOW, vision),
        ],
        required_sources={"rule", "text_agent", "vision_agent"},
        arbitration=ModerationVerdict.ALLOW,
    )

    assert decision.verdict is ModerationVerdict.ALLOW
    assert decision.status is ModerationStatus.COMPLETED
    assert set(decision.evidence_ids) == {"rule-1", "text-1", "vision-1"}


def test_risk_router_escalates_conflicting_agent_recommendations():
    router = RiskRouter()
    text = assessment(
        "text_agent",
        ModerationVerdict.ALLOW,
        evidence("text-1", "text_agent"),
    )
    vision = assessment(
        "vision_agent",
        ModerationVerdict.BLOCK,
        evidence(
            "vision-1",
            "vision_agent",
            category="credentials",
            severity=0.72,
        ),
    )

    route = router.route([text, vision])

    assert route.requires_debate is True
    assert "conflicting_recommendations" in route.reasons


def test_risk_router_keeps_consistent_low_risk_content_on_fast_path():
    router = RiskRouter()
    text = assessment(
        "text_agent",
        ModerationVerdict.ALLOW,
        evidence("text-1", "text_agent"),
    )

    route = router.route([text])

    assert route.requires_debate is False
    assert route.reasons == []
