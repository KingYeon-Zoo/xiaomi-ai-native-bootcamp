from __future__ import annotations

from types import SimpleNamespace

import pytest
from PIL import Image

from app.agents.ark import ArkConfig, ArkResponsesClient, ImageInputAdapter
from app.agents.moderators import (
    AdversarialReviewAgent,
    ArbitrationAgent,
    ArbitrationPayload,
    ModelAssessmentPayload,
    ModelFinding,
    TextModerationAgent,
    VisionModerationAgent,
)
from app.agents.schemas import ModerationVerdict


class FakeResponses:
    def __init__(self, outcomes, create_outcomes=None):
        self.outcomes = list(outcomes)
        self.create_outcomes = list(create_outcomes or [])
        self.calls = []
        self.create_calls = []

    async def parse(self, **kwargs):
        self.calls.append(kwargs)
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome

    async def create(self, **kwargs):
        self.create_calls.append(kwargs)
        outcome = self.create_outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


class FakeOpenAI:
    def __init__(self, outcomes, create_outcomes=None):
        self.responses = FakeResponses(outcomes, create_outcomes)


def parsed_response(payload):
    return SimpleNamespace(
        output=[
            SimpleNamespace(
                type="message",
                content=[
                    SimpleNamespace(
                        type="output_text",
                        parsed=payload,
                        text=payload.model_dump_json(),
                    )
                ],
            )
        ],
        output_text=payload.model_dump_json(),
    )


def safe_payload() -> ModelAssessmentPayload:
    return ModelAssessmentPayload(
        recommendation=ModerationVerdict.ALLOW,
        confidence=0.94,
        findings=[
            ModelFinding(
                category="technology",
                severity=0.03,
                confidence=0.96,
                summary="The post discusses PostgreSQL indexing.",
                policy_codes=["TECH_RELEVANT"],
                text_spans=["PostgreSQL index"],
            )
        ],
    )


def test_config_prefers_ark_key_and_falls_back_to_legacy_llm_key(monkeypatch):
    monkeypatch.setenv("ARK_API_KEY", "ark-key")
    monkeypatch.setenv("LLM_API_KEY", "legacy-key")
    assert ArkConfig.from_env().api_key == "ark-key"

    monkeypatch.delenv("ARK_API_KEY")
    assert ArkConfig.from_env().api_key == "legacy-key"


@pytest.mark.asyncio
async def test_structured_request_retries_once_after_invalid_response():
    payload = safe_payload()
    fake = FakeOpenAI([ValueError("invalid structured output"), parsed_response(payload)])
    client = ArkResponsesClient(client=fake, max_attempts=2, retry_delay_seconds=0)

    result = await client.parse(
        model="text-model",
        instructions="Return moderation evidence.",
        input_items=[{"role": "user", "content": "hello"}],
        response_model=ModelAssessmentPayload,
    )

    assert result == payload
    assert len(fake.responses.calls) == 2


@pytest.mark.asyncio
async def test_falls_back_to_json_object_when_model_rejects_json_schema():
    payload = safe_payload()
    fake = FakeOpenAI(
        [ValueError("response_format.type json_schema is not supported")],
        [parsed_response(payload)],
    )
    client = ArkResponsesClient(client=fake, max_attempts=1)

    result = await client.parse(
        model="ark-model",
        instructions="Return moderation evidence.",
        input_items=[{"role": "user", "content": "hello"}],
        response_model=ModelAssessmentPayload,
    )

    assert result == payload
    assert fake.responses.create_calls[0]["text"]["format"]["type"] == "json_object"


def test_image_adapter_converts_local_upload_to_data_url(tmp_path):
    image_path = tmp_path / "safe.png"
    Image.new("RGB", (8, 8), color="navy").save(image_path)

    data_url = ImageInputAdapter(max_bytes=1024).to_data_url(image_path)

    assert data_url.startswith("data:image/png;base64,")


@pytest.mark.asyncio
async def test_text_agent_returns_versioned_structured_evidence():
    payload = safe_payload()
    fake = FakeOpenAI([parsed_response(payload)])
    client = ArkResponsesClient(client=fake, max_attempts=1)
    agent = TextModerationAgent(client=client, model="deepseek-test")

    result = await agent.analyze("How do I optimize a PostgreSQL index?")

    assert result.agent_name == "text_agent"
    assert result.recommendation is ModerationVerdict.ALLOW
    assert result.evidences[0].source == "text_agent"
    assert result.evidences[0].model_name == "deepseek-test"
    assert result.evidences[0].prompt_version == "text-v1"
    call = fake.responses.calls[0]
    assert call["model"] == "deepseek-test"
    assert "untrusted content" in call["instructions"].lower()


@pytest.mark.asyncio
async def test_vision_agent_sends_image_and_text_to_doubao():
    payload = safe_payload()
    fake = FakeOpenAI([parsed_response(payload)])
    client = ArkResponsesClient(client=fake, max_attempts=1)
    adapter = SimpleNamespace(
        to_data_url=lambda _: "data:image/png;base64,aW1hZ2U="
    )
    agent = VisionModerationAgent(
        client=client,
        model="doubao-test",
        image_adapter=adapter,
    )

    result = await agent.analyze(
        text="PostgreSQL execution plan",
        image_path="/uploads/plan.png",
    )

    assert result.agent_name == "vision_agent"
    call = fake.responses.calls[0]
    content = call["input"][0]["content"]
    assert content[0] == {
        "type": "input_image",
        "image_url": "data:image/png;base64,aW1hZ2U=",
    }
    assert content[1]["type"] == "input_text"
    assert "PostgreSQL execution plan" in content[1]["text"]


@pytest.mark.asyncio
async def test_critic_turns_counter_evidence_into_a_versioned_assessment():
    payload = ModelAssessmentPayload(
        recommendation=ModerationVerdict.HUMAN_REVIEW,
        confidence=0.82,
        findings=[
            ModelFinding(
                category="credential_exposure",
                severity=0.68,
                confidence=0.79,
                summary="The screenshot may expose a connection string.",
                policy_codes=["REVIEW_CREDENTIAL_EXPOSURE"],
            )
        ],
    )
    fake = FakeOpenAI([parsed_response(payload)])
    client = ArkResponsesClient(client=fake, max_attempts=1)
    critic = AdversarialReviewAgent(client=client, model="deepseek-critic")
    prior = [
        TextModerationAgent(client=client, model="unused")._to_assessment(
            safe_payload(), latency_ms=10
        )
    ]

    result = await critic.review("PostgreSQL screenshot", prior)

    assert result.agent_name == "critic_agent"
    assert result.recommendation is ModerationVerdict.HUMAN_REVIEW
    assert result.evidences[0].prompt_version == "critic-v1"


@pytest.mark.asyncio
async def test_arbitrator_returns_bounded_verdict_with_evidence_references():
    payload = ArbitrationPayload(
        recommendation=ModerationVerdict.HUMAN_REVIEW,
        confidence=0.88,
        summary="Conflicting image evidence requires a person.",
        evidence_ids=["text-1", "vision-1"],
    )
    fake = FakeOpenAI([parsed_response(payload)])
    client = ArkResponsesClient(client=fake, max_attempts=1)
    arbitrator = ArbitrationAgent(client=client, model="deepseek-arbiter")

    result = await arbitrator.arbitrate(
        text="PostgreSQL screenshot",
        assessments=[],
    )

    assert result.recommendation is ModerationVerdict.HUMAN_REVIEW
    assert result.evidence_ids == ["text-1", "vision-1"]
