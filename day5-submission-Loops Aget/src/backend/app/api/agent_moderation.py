from typing import Literal

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from app.agents.container import get_agent_runtime
from app.agents.runtime import ModerationRuntime


router = APIRouter()


class HumanDecisionRequest(BaseModel):
    decision: Literal["approve", "reject"]
    reviewer_id: str = Field(min_length=1, max_length=128)
    reason: str = Field(min_length=1, max_length=1000)


@router.get("/runs/{run_id}")
async def get_run(
    run_id: str,
    runtime: ModerationRuntime = Depends(get_agent_runtime),
):
    run = await runtime.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Moderation run not found")
    return run.model_dump(
        mode="json",
        exclude={"text", "trace"},
    )


@router.get("/runs/{run_id}/trace")
async def get_run_trace(
    run_id: str,
    runtime: ModerationRuntime = Depends(get_agent_runtime),
):
    run = await runtime.get_run(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Moderation run not found")
    return {
        "run_id": run.run_id,
        "post_id": run.post_id,
        "status": run.status,
        "verdict": run.verdict,
        "decision": run.decision,
        "trace": run.trace,
        "error": run.error,
    }


@router.post("/runs/{run_id}/human-decision", status_code=202)
async def submit_human_decision(
    run_id: str,
    payload: HumanDecisionRequest,
    runtime: ModerationRuntime = Depends(get_agent_runtime),
):
    try:
        run = await runtime.resume(
            run_id,
            decision=payload.decision,
            reviewer_id=payload.reviewer_id,
            reason=payload.reason,
        )
    except KeyError:
        raise HTTPException(status_code=404, detail="Moderation run not found")
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return run.model_dump(mode="json", exclude={"text", "trace"})
