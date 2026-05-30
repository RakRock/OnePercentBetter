import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.db_types import JsonCol, UuidCol


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UuidCol, primary_key=True, default=uuid.uuid4)
    external_id: Mapped[str | None] = mapped_column(String(128), unique=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(120))
    learning_profile: Mapped[dict] = mapped_column(JsonCol, default=dict)
    github_username: Mapped[str | None] = mapped_column(String(120))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    progress: Mapped[list["UserProgress"]] = relationship(back_populates="user")
    conversations: Mapped[list["Conversation"]] = relationship(back_populates="user")


class UserProgress(Base):
    __tablename__ = "user_progress"

    id: Mapped[uuid.UUID] = mapped_column(UuidCol, primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"), index=True)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), index=True)
    completed_checkpoints: Mapped[list] = mapped_column(JsonCol, default=list)
    strengths: Mapped[list] = mapped_column(JsonCol, default=list)
    weaknesses: Mapped[list] = mapped_column(JsonCol, default=list)
    percent_complete: Mapped[int] = mapped_column(default=0)
    notes: Mapped[str | None] = mapped_column(Text)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="progress")
