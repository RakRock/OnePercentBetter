from __future__ import annotations

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.api.deps import get_current_user, get_db
from app.api.v1.schemas import LearningPathOut, ProgressOut, ProjectOut
from app.models import Checkpoint, LearningPath, Project, User, UserProgress

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/paths", response_model=list[LearningPathOut])
async def list_paths(db: AsyncSession = Depends(get_db)) -> list[LearningPath]:
    result = await db.execute(select(LearningPath).order_by(LearningPath.order_index))
    return list(result.scalars().all())


@router.get("", response_model=list[ProjectOut])
async def list_projects(db: AsyncSession = Depends(get_db)) -> list[Project]:
    result = await db.execute(
        select(Project)
        .options(selectinload(Project.checkpoints))
        .order_by(Project.order_index)
    )
    return list(result.scalars().all())


@router.get("/progress/me", response_model=list[ProgressOut])
async def my_progress(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> list[UserProgress]:
    result = await db.execute(select(UserProgress).where(UserProgress.user_id == user.id))
    return list(result.scalars().all())


@router.get("/{slug}", response_model=ProjectOut)
async def get_project(slug: str, db: AsyncSession = Depends(get_db)) -> Project:
    result = await db.execute(
        select(Project)
        .where(Project.slug == slug)
        .options(selectinload(Project.checkpoints))
    )
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project


@router.get("/{slug}/scaffold")
async def get_scaffold(slug: str, db: AsyncSession = Depends(get_db)) -> dict:
    result = await db.execute(select(Project).where(Project.slug == slug))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {
        "slug": project.slug,
        "files": project.scaffold_files,
        "readme": project.scaffold_files.get("README.md", ""),
        "architecture": project.scaffold_files.get("architecture.md", ""),
        "deployment": project.scaffold_files.get("deployment.md", ""),
    }


@router.post("/{slug}/checkpoints/{checkpoint_id}/complete", response_model=ProgressOut)
async def complete_checkpoint(
    slug: str,
    checkpoint_id: uuid.UUID,
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> UserProgress:
    result = await db.execute(select(Project).where(Project.slug == slug))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    cp = await db.get(Checkpoint, checkpoint_id)
    if not cp or cp.project_id != project.id:
        raise HTTPException(status_code=404, detail="Checkpoint not found")

    prog_result = await db.execute(
        select(UserProgress).where(
            UserProgress.user_id == user.id,
            UserProgress.project_id == project.id,
        )
    )
    progress = prog_result.scalar_one_or_none()
    if not progress:
        progress = UserProgress(user_id=user.id, project_id=project.id)
        db.add(progress)

    completed = list(progress.completed_checkpoints or [])
    cp_id = str(checkpoint_id)
    if cp_id not in completed:
        completed.append(cp_id)
    progress.completed_checkpoints = completed

    total = await db.execute(
        select(Checkpoint).where(Checkpoint.project_id == project.id)
    )
    total_cps = len(list(total.scalars().all()))
    progress.percent_complete = int((len(completed) / max(total_cps, 1)) * 100)

    await db.commit()
    await db.refresh(progress)
    return progress
