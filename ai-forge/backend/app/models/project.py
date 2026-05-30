import uuid
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.core.db_types import JsonCol, UuidCol


class LearningPath(Base):
    __tablename__ = "learning_paths"

    id: Mapped[uuid.UUID] = mapped_column(UuidCol, primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    difficulty: Mapped[str] = mapped_column(String(32), default="beginner")
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    lessons: Mapped[list["Lesson"]] = relationship(back_populates="path")
    projects: Mapped[list["Project"]] = relationship(back_populates="path")


class Lesson(Base):
    __tablename__ = "lessons"

    id: Mapped[uuid.UUID] = mapped_column(UuidCol, primary_key=True, default=uuid.uuid4)
    path_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("learning_paths.id"), index=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    concept_markdown: Mapped[str] = mapped_column(Text)
    architecture_mermaid: Mapped[str] = mapped_column(Text, default="")
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    path: Mapped["LearningPath"] = relationship(back_populates="lessons")


class Project(Base):
    __tablename__ = "projects"

    id: Mapped[uuid.UUID] = mapped_column(UuidCol, primary_key=True, default=uuid.uuid4)
    path_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("learning_paths.id"), nullable=True)
    slug: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    summary: Mapped[str] = mapped_column(Text)
    difficulty: Mapped[str] = mapped_column(String(32), default="intermediate")
    stack: Mapped[list] = mapped_column(JsonCol, default=list)
    rubric: Mapped[dict] = mapped_column(JsonCol, default=dict)
    deployment_checklist: Mapped[list] = mapped_column(JsonCol, default=list)
    scaffold_files: Mapped[dict] = mapped_column(JsonCol, default=dict)
    order_index: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)

    path: Mapped["LearningPath | None"] = relationship(back_populates="projects")
    checkpoints: Mapped[list["Checkpoint"]] = relationship(back_populates="project")


class Checkpoint(Base):
    __tablename__ = "checkpoints"

    id: Mapped[uuid.UUID] = mapped_column(UuidCol, primary_key=True, default=uuid.uuid4)
    project_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("projects.id"), index=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    tasks: Mapped[list] = mapped_column(JsonCol, default=list)
    order_index: Mapped[int] = mapped_column(Integer, default=0)

    project: Mapped["Project"] = relationship(back_populates="checkpoints")
