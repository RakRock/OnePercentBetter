"""Evaluation engine (Phase 1 — Claude rubric scorer)."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user, get_db
from app.api.v1.schemas import EvaluationRequest
from app.models import Evaluation, Project, Submission, User
from app.services.llm.provider import LLMProvider

router = APIRouter(prefix="/evaluation", tags=["evaluation"])


@router.post("/submit")
async def evaluate_submission(
    body: EvaluationRequest,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> dict:
    result = await db.execute(select(Project).where(Project.id == body.project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    submission = Submission(
        user_id=user.id,
        project_id=project.id,
        artifact=body.artifact,
        notes=body.submission_notes,
    )
    db.add(submission)
    await db.flush()

    llm = LLMProvider()
    rubric = project.rubric or {
        "correctness": 25,
        "architecture": 25,
        "code_quality": 20,
        "performance": 15,
        "deployment_readiness": 15,
    }
    scores = await llm.structured_json(
        [
            {
                "role": "system",
                "content": "You are an AI engineering evaluator. Score fairly using the rubric.",
            },
            {
                "role": "user",
                "content": (
                    f"Project: {project.title}\n"
                    f"Summary: {project.summary}\n"
                    f"Rubric weights: {rubric}\n"
                    f"Submission notes: {body.submission_notes}\n"
                    f"Artifact: {body.artifact}"
                ),
            },
        ],
        schema_hint='{"scores":{"correctness":0-25,...},"overall_score":0-100,"feedback":"string","improvement_plan":["string"]}',
    )

    overall = int(scores.get("overall_score", 70))
    evaluation = Evaluation(
        submission_id=submission.id,
        scores=scores.get("scores", scores),
        feedback=scores.get("feedback", "Good start — keep iterating."),
        improvement_plan=scores.get("improvement_plan", []),
        overall_score=overall,
    )
    db.add(evaluation)
    await db.commit()

    return {
        "submission_id": str(submission.id),
        "evaluation_id": str(evaluation.id),
        "overall_score": overall,
        "feedback": evaluation.feedback,
        "improvement_plan": evaluation.improvement_plan,
        "scores": evaluation.scores,
    }
