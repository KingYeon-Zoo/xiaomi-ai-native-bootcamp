from app.services.control_center_metrics import (
    ControlCenterMetricsService,
    build_control_center_snapshot,
)


def test_demo_snapshot_compares_agent_and_ml_on_same_evaluation_set():
    snapshot = build_control_center_snapshot()

    assert snapshot["agent"]["total"] == snapshot["ml"]["total"]
    assert snapshot["agent"]["precision"] > snapshot["ml"]["precision"]
    assert snapshot["agent"]["avg_latency_ms"] > snapshot["ml"]["avg_latency_ms"]
    assert snapshot["comparison"]["same_evaluation_set"] == snapshot["agent"]["total"]


def test_agent_snapshot_contains_real_architecture_stages():
    snapshot = build_control_center_snapshot()
    stages = {item["name"] for item in snapshot["agent"]["pipeline"]}

    assert {"文本取证", "视觉取证", "风险路由", "质疑与仲裁", "策略裁决"} <= stages
    assert snapshot["agent"]["models"][1]["name"] == "Doubao Seed 2.0 Lite"


def test_service_falls_back_to_deterministic_snapshot_without_database():
    snapshot = ControlCenterMetricsService().get_snapshot(hours=24)

    assert snapshot["window_hours"] == 24
    assert snapshot["source"] == "deterministic_demo_snapshot"
