from __future__ import annotations

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


class UserOut(BaseModel):
    id: uuid.UUID
    email: str
    display_name: str
    learning_profile: dict = Field(default_factory=dict)

    class Config:
        from_attributes = True


class LearningPathOut(BaseModel):
    id: uuid.UUID
    slug: str
    title: str
    description: str
    difficulty: str

    class Config:
        from_attributes = True


class CheckpointOut(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    tasks: list
    order_index: int

    class Config:
        from_attributes = True


class ProjectOut(BaseModel):
    id: uuid.UUID
    slug: str
    title: str
    summary: str
    difficulty: str
    stack: list
    deployment_checklist: list
    checkpoints: list[CheckpointOut] = Field(default_factory=list)

    class Config:
        from_attributes = True


class MentorChatRequest(BaseModel):
    message: str
    conversation_id: uuid.UUID | None = None
    project_id: uuid.UUID | None = None
    personality: str = "teacher"


class ConversationOut(BaseModel):
    id: uuid.UUID
    mentor_personality: str
    title: str
    created_at: datetime

    class Config:
        from_attributes = True


class MessageOut(BaseModel):
    id: uuid.UUID
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ProgressOut(BaseModel):
    project_id: uuid.UUID
    percent_complete: int
    completed_checkpoints: list
    strengths: list
    weaknesses: list

    class Config:
        from_attributes = True


class EvaluationRequest(BaseModel):
    project_id: uuid.UUID
    submission_notes: str = ""
    artifact: dict = Field(default_factory=dict)
