from __future__ import annotations

from collections.abc import Iterable

from app.agents.schemas import (
    AgentAssessment,
    ModerationDecision,
    ModerationStatus,
    ModerationVerdict,
    RiskRoute,
)


class RiskRouter:
    """Select the fast path or the critic/arbitrator path."""

    def __init__(
        self,
        *,
        confidence_threshold: float = 0.75,
        high_risk_threshold: float = 0.6,
    ) -> None:
        self.confidence_threshold = confidence_threshold
        self.high_risk_threshold = high_risk_threshold

    def route(self, assessments: Iterable[AgentAssessment]) -> RiskRoute:
        items = list(assessments)
        reasons: list[str] = []
        recommendations = {item.recommendation for item in items}

        if len(recommendations) > 1:
            reasons.append("conflicting_recommendations")
        if any(item.confidence < self.confidence_threshold for item in items):
            reasons.append("low_confidence")
        if any(item.unavailable or item.error for item in items):
            reasons.append("agent_unavailable")
        if any(
            evidence.severity >= self.high_risk_threshold
            for item in items
            for evidence in item.evidences
        ):
            reasons.append("high_risk_evidence")

        return RiskRoute(
            requires_debate=bool(reasons),
            reasons=list(dict.fromkeys(reasons)),
        )


class ModerationPolicy:
    """Deterministic final authority that an LLM recommendation cannot bypass."""

    TRUSTED_HARD_POLICY_SOURCES = {"rule", "attack_tool"}

    def decide(
        self,
        *,
        assessments: Iterable[AgentAssessment],
        required_sources: set[str],
        arbitration: ModerationVerdict | None,
    ) -> ModerationDecision:
        items = list(assessments)
        evidences = [evidence for item in items for evidence in item.evidences]

        hard_block_evidence = [
            evidence
            for evidence in evidences
            if evidence.source in self.TRUSTED_HARD_POLICY_SOURCES
            and any(code.startswith("HARD_BLOCK_") for code in evidence.policy_codes)
        ]
        if hard_block_evidence:
            return ModerationDecision(
                verdict=ModerationVerdict.BLOCK,
                status=ModerationStatus.COMPLETED,
                confidence=max(item.confidence for item in hard_block_evidence),
                reasons=["hard_policy_violation"],
                policy_codes=self._policy_codes(hard_block_evidence),
                evidence_ids=[item.evidence_id for item in hard_block_evidence],
            )

        available_sources = {
            source
            for item in items
            if not item.unavailable and not item.error
            for source in ({item.agent_name} | {e.source for e in item.evidences})
        }
        missing_sources = sorted(required_sources - available_sources)
        if missing_sources:
            return self._human_review(
                f"missing required evidence: {', '.join(missing_sources)}",
                evidences,
            )

        if any(item.unavailable or item.error for item in items):
            return self._human_review("required agent unavailable", evidences)

        if arbitration is ModerationVerdict.HUMAN_REVIEW:
            return self._human_review("arbitration requires human review", evidences)

        recommendations = {item.recommendation for item in items}
        if len(recommendations) > 1 and arbitration is None:
            return self._human_review("conflicting recommendations", evidences)

        verdict = arbitration or (
            ModerationVerdict.BLOCK
            if ModerationVerdict.BLOCK in recommendations
            else ModerationVerdict.ALLOW
        )
        status = (
            ModerationStatus.WAITING_HUMAN
            if verdict is ModerationVerdict.HUMAN_REVIEW
            else ModerationStatus.COMPLETED
        )
        confidence = min((item.confidence for item in items), default=0.0)
        return ModerationDecision(
            verdict=verdict,
            status=status,
            confidence=confidence,
            reasons=["evidence_consensus"],
            policy_codes=self._policy_codes(evidences),
            evidence_ids=[item.evidence_id for item in evidences],
        )

    @staticmethod
    def _policy_codes(evidences) -> list[str]:
        return list(
            dict.fromkeys(
                code for evidence in evidences for code in evidence.policy_codes
            )
        )

    def _human_review(self, reason: str, evidences) -> ModerationDecision:
        return ModerationDecision(
            verdict=ModerationVerdict.HUMAN_REVIEW,
            status=ModerationStatus.WAITING_HUMAN,
            confidence=0.0,
            reasons=[reason],
            policy_codes=self._policy_codes(evidences),
            evidence_ids=[item.evidence_id for item in evidences],
        )
