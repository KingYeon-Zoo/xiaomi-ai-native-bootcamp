from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.agents.container import get_agent_runtime
from app.agents.schemas import ModerationRun, ModerationStatus, ModerationVerdict
from app.api.agent_moderation import router


class FakeRuntime:
    def __init__(self):
        self.run = ModerationRun(
            run_id="run-1",
            post_id="post-1",
            text="private post text",
            status=ModerationStatus.WAITING_HUMAN,
            verdict=ModerationVerdict.HUMAN_REVIEW,
            decision={"reasons": ["conflict"]},
            trace=[{"node": "policy_gate", "summary": "human_review"}],
            created_at=datetime.now(timezone.utc),
            updated_at=datetime.now(timezone.utc),
        )

    async def get_run(self, run_id):
        return self.run if run_id == self.run.run_id else None

    async def resume(self, run_id, **payload):
        if run_id != self.run.run_id:
            raise KeyError(run_id)
        self.run = self.run.model_copy(
            update={"status": ModerationStatus.QUEUED}
        )
        return self.run


def make_client():
    app = FastAPI()
    app.include_router(router, prefix="/api/moderation")
    runtime = FakeRuntime()
    app.dependency_overrides[get_agent_runtime] = lambda: runtime
    return TestClient(app), runtime


def test_public_run_status_hides_post_text_and_internal_trace():
    client, _ = make_client()

    response = client.get("/api/moderation/runs/run-1")

    assert response.status_code == 200
    assert response.json()["status"] == "waiting_human"
    assert "text" not in response.json()
    assert "trace" not in response.json()


def test_admin_trace_returns_structured_nodes_not_hidden_reasoning():
    client, _ = make_client()

    response = client.get("/api/moderation/runs/run-1/trace")

    assert response.status_code == 200
    assert response.json()["trace"][0]["node"] == "policy_gate"


def test_human_decision_is_accepted_for_paused_run():
    client, runtime = make_client()

    response = client.post(
        "/api/moderation/runs/run-1/human-decision",
        json={
            "decision": "reject",
            "reviewer_id": "admin-1",
            "reason": "Confirmed violation",
        },
    )

    assert response.status_code == 202
    assert runtime.run.status is ModerationStatus.QUEUED


def test_missing_run_returns_404():
    client, _ = make_client()

    response = client.get("/api/moderation/runs/missing")

    assert response.status_code == 404
