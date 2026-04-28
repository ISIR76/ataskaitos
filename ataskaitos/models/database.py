"""Database models using SQLAlchemy 2.0+ with MappedAsDataclass."""

from datetime import datetime
from typing import TYPE_CHECKING

from fastapi_users.db import SQLAlchemyBaseUserTable
from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship

if TYPE_CHECKING:
    pass


# Use single DeclarativeBase for all models (FastAPI-Users requires non-dataclass base)
class Base(DeclarativeBase):
    """Base class for all database models."""

    pass


class User(SQLAlchemyBaseUserTable[int], Base):
    """User model for authentication with FastAPI-Users.

    Inherits from SQLAlchemyBaseUserTable which provides email, hashed_password,
    is_active, is_superuser, and is_verified fields.
    """

    __tablename__ = "users"

    # Primary key (required, not provided by SQLAlchemyBaseUserTable)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # Relationships
    projects: Mapped[list["Project"]] = relationship(back_populates="user", cascade="all, delete-orphan", lazy="selectin")


class Project(Base):
    """Project model - container for document versions."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    project_type: Mapped[str] = mapped_column(String)  # "straipsnis" or "ataskaita"
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), index=True)
    active_version_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("document_versions.id", use_alter=True), default=None
    )
    is_marked_good: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user: Mapped["User"] = relationship(back_populates="projects")
    versions: Mapped[list["DocumentVersion"]] = relationship(
        back_populates="project",
        foreign_keys="DocumentVersion.project_id",
        cascade="all, delete-orphan",
    )
    active_version: Mapped["DocumentVersion | None"] = relationship(
        foreign_keys=[active_version_id], viewonly=True
    )


class DocumentVersion(Base):
    """Document version model - represents a single version of a document."""

    __tablename__ = "document_versions"
    __table_args__ = (
        UniqueConstraint("project_id", "version_number", name="uq_project_version"),
        Index("ix_document_versions_project_id", "project_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"))
    version_number: Mapped[int] = mapped_column(Integer)
    original_filename: Mapped[str] = mapped_column(String)
    file_extension: Mapped[str] = mapped_column(String)
    original_file_path: Mapped[str] = mapped_column(String)  # Relative path
    markdown_file_path: Mapped[str] = mapped_column(String)  # Relative path
    character_count: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationships
    project: Mapped["Project"] = relationship(back_populates="versions", foreign_keys=[project_id])
    evaluations: Mapped[list["Evaluation"]] = relationship(
        back_populates="document_version", cascade="all, delete-orphan"
    )


class Evaluator(Base):
    """User-editable evaluator definition.

    Defaults are seeded from JSON files on startup with ``source='default'``;
    user-created entries use ``source='custom'``.
    """

    __tablename__ = "evaluators"
    __table_args__ = (
        UniqueConstraint("name", "document_type", name="uq_evaluator_name_type"),
        Index("ix_evaluators_document_type", "document_type"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, index=True)
    document_type: Mapped[str] = mapped_column(String)  # "article" | "report"
    rubric: Mapped[str] = mapped_column(Text)
    has_assertion: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    source: Mapped[str] = mapped_column(String, default="custom")  # "default" | "custom"
    extra_metadata: Mapped[str] = mapped_column(String, default="{}")  # JSON string
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)


class Evaluation(Base):
    """Evaluation model - stores evaluation results for a document version."""

    __tablename__ = "evaluations"
    __table_args__ = (
        Index("ix_evaluations_evaluation_id", "evaluation_id"),
        Index("ix_evaluations_document_version_id", "document_version_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    evaluation_id: Mapped[str] = mapped_column(String)  # UUID
    document_version_id: Mapped[int] = mapped_column(Integer, ForeignKey("document_versions.id"))
    evaluation_type: Mapped[str] = mapped_column(String)  # "scoring" or "agent"
    evaluators_used: Mapped[str] = mapped_column(String)  # JSON array string
    results_json: Mapped[str] = mapped_column(String)  # Full results serialized
    status: Mapped[str] = mapped_column(String)
    error_message: Mapped[str | None] = mapped_column(String, default=None)
    duration_seconds: Mapped[float] = mapped_column(default=0.0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    # Relationships
    document_version: Mapped["DocumentVersion"] = relationship(back_populates="evaluations")
