from __future__ import annotations

import re

from app.agents.schemas import AgentAssessment, Evidence, ModerationVerdict


class RuleEvidenceTool:
    """Expose the legacy deterministic detector as structured agent evidence."""

    _INJECTION_PATTERN = re.compile(
        r"(ignore|disregard|forget).{0,32}(previous|system|developer|instruction)"
        r"|(?:approve|allow|block|reject).{0,24}(?:this|the).{0,12}(?:post|content)",
        re.IGNORECASE,
    )

    def __init__(self, rule_engine) -> None:
        self.rule_engine = rule_engine

    def __call__(self, text: str) -> AgentAssessment:
        result = self.rule_engine.check_rules(text)
        score = float(result.get("rule_score", 0.0))
        injection = bool(self._INJECTION_PATTERN.search(text))

        if injection:
            evidence = Evidence(
                evidence_id="attack-prompt-injection",
                source="attack_tool",
                category="prompt_injection",
                severity=0.65,
                confidence=0.95,
                summary="Content contains instructions attempting to influence moderation.",
                policy_codes=["REVIEW_PROMPT_INJECTION"],
            )
            return AgentAssessment(
                agent_name="rule",
                recommendation=ModerationVerdict.HUMAN_REVIEW,
                confidence=0.95,
                evidences=[evidence],
            )

        hard_block = score >= 0.8
        category = "rule_violation" if score > 0 else "rule_clear"
        codes = ["HARD_BLOCK_RULE"] if hard_block else (
            ["REVIEW_RULE_SIGNAL"] if score > 0 else []
        )
        summary = (
            ", ".join(result.get("violations", []))
            if score > 0
            else "No deterministic rule violation detected."
        )
        evidence = Evidence(
            evidence_id="rule-precheck",
            source="rule",
            category=category,
            severity=score,
            confidence=1.0,
            summary=summary,
            policy_codes=codes,
            text_spans=list(result.get("banned_keywords", [])),
        )
        recommendation = (
            ModerationVerdict.BLOCK
            if hard_block
            else ModerationVerdict.HUMAN_REVIEW
            if score > 0
            else ModerationVerdict.ALLOW
        )
        return AgentAssessment(
            agent_name="rule",
            recommendation=recommendation,
            confidence=1.0,
            evidences=[evidence],
        )
