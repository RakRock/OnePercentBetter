import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base
from app.core.db_types import JsonCol, UuidCol


class Submission(Base):
    __tablename__ = "submissions"

    id: Mapped[uuid.UUID] = mapped_column(UuidCol, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), index=True)
    checkpoint_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("checkpoints.id"), nullable=True)
    artifact: Mapped[dict] = mapped_column(JsonCol, default=dict)
    notes: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)


class Evaluation(Base):
    __tablename__ = "evaluations"

    id: Mapped[uuid.UUID] = mapped_column(UuidCol, primary_key=True, default=uuid.uuid4)
    submission_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("submissions.id"), index=True)
    scores: Mapped[dict] = mapped_column(JsonCol, default=dict)
    feedback: Mapped[str] = mapped_column(Text)
    improvement_plan: Mapped[list] = mapped_column(JsonCol, default=list)
    overall_score: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
