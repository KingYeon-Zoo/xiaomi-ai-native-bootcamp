from __future__ import annotations

from enum import Enum
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class ModerationStatus(str, Enum):
    QUEUED = "queued"
    RUNNING = "running"
    WAITING_HUMAN = "waiting_human"
    COMPLETED = "completed"
    FAILED = "failed"


class ModerationVerdict(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"
    HUMAN_REVIEW = "human_review"


class Evidence(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    evidence_id: str
    source: str
    category: str
    severity: float = Field(ge=0.0, le=1.0)
    confidence: float = Field(ge=0.0, le=1.0)
    summary: str
    policy_codes: list[str] = Field(default_factory=list)
    text_spans: list[str] = Field(default_factory=list)
    image_regions: list[dict[str, Any]] = Field(default_factory=list)
    model_name: str | None = None
    prompt_version: str | None = None
    latency_ms: int | None = Field(default=None, ge=0)


class AgentAssessment(BaseModel):
    agent_name: str
    recommendation: ModerationVerdict
    confidence: float = Field(ge=0.0, le=1.0)
    evidences: list[Evidence] = Field(default_factory=list)
    unavailable: bool = False
    error: str | None = None


class ModerationDecision(BaseModel):
    verdict: ModerationVerdict
    status: ModerationStatus
    confidence: float = Field(ge=0.0, le=1.0)
    reasons: list[str] = Field(default_factory=list)
    policy_codes: list[str] = Field(default_factory=list)
    evidence_ids: list[str] = Field(default_factory=list)


class RiskRoute(BaseModel):
    requires_debate: bool
    reasons: list[str] = Field(default_factory=list)


class ModerationRun(BaseModel):
    run_id: str
    post_id: str
    text: str
    image_path: str | None = None
    status: ModerationStatus = ModerationStatus.QUEUED
    verdict: ModerationVerdict | None = None
    decision: dict[str, Any] | None = None
    trace: list[dict[str, Any]] = Field(default_factory=list)
    error: str | None = None
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
