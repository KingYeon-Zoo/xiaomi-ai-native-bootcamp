from __future__ import annotations

import asyncio
import os
from pathlib import Path

from langgraph.checkpoint.mongodb import MongoDBSaver

from app.agents.ark import ArkConfig, ArkResponsesClient, ImageInputAdapter
from app.agents.graph import build_moderation_graph
from app.agents.moderators import (
    AdversarialReviewAgent,
    ArbitrationAgent,
    TextModerationAgent,
    VisionModerationAgent,
)
from app.agents.policy import ModerationPolicy, RiskRouter
from app.agents.repositories import MongoRunRepository
from app.agents.runtime import ModerationRuntime
from app.agents.tools import RuleEvidenceTool
from app.services.rule_engine import RuleEngine


_runtime: ModerationRuntime | None = None


def get_agent_runtime() -> ModerationRuntime:
    global _runtime
    if _runtime is not None:
        return _runtime

    from app.db.mongodb import mongodb, post_repository

    config = ArkConfig.from_env()
    client = ArkResponsesClient(config=config)
    checkpointer = MongoDBSaver(
        mongodb._client,
        db_name=os.getenv("MONGODB_DB_NAME", "loops_moderation"),
        checkpoint_collection_name="agent_checkpoints",
        writes_collection_name="agent_checkpoint_writes",
    )
    graph = build_moderation_graph(
        rule_tool=RuleEvidenceTool(RuleEngine()),
        text_agent=TextModerationAgent(client=client, model=config.text_model),
        vision_agent=VisionModerationAgent(
            client=client,
            model=config.vision_model,
            image_adapter=ImageInputAdapter(
                base_dir=Path(__file__).resolve().parents[2]
            ),
        ),
        critic_agent=AdversarialReviewAgent(
            client=client,
            model=config.critic_model,
        ),
        arbitrator=ArbitrationAgent(client=client, model=config.arbiter_model),
        risk_router=RiskRouter(),
        policy=ModerationPolicy(),
        checkpointer=checkpointer,
    )

    async def project_result(run) -> None:
        await asyncio.to_thread(post_repository.apply_agent_result, run)

    _runtime = ModerationRuntime(
        graph=graph,
        repository=MongoRunRepository(mongodb._db.moderation_runs),
        result_handler=project_result,
    )
    return _runtime


def peek_agent_runtime() -> ModerationRuntime | None:
    return _runtime
