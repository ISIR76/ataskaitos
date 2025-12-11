"""Database models using SQLAlchemy 2.0+ with MappedAsDataclass."""

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Index, Integer, String, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship

if TYPE_CHECKING:
    pass


class Base(MappedAsDataclass, DeclarativeBase):
    """Base class for all database models with dataclass functionality."""

    pass


class Project(Base):
    """Project model - container for document versions."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False, autoincrement=True)
    name: Mapped[str] = mapped_column(String, unique=True, index=True)
    project_type: Mapped[str] = mapped_column(String)  # "straipsnis" or "ataskaita"
    active_version_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("document_versions.id", use_alter=True), default=None, init=False
    )
    created_at: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow, init=False)
    updated_at: Mapped[datetime] = mapped_column(
        default_factory=datetime.utcnow, onupdate=datetime.utcnow, init=False
    )

    # Relationships
    versions: Mapped[list["DocumentVersion"]] = relationship(
        back_populates="project",
        foreign_keys="DocumentVersion.project_id",
        default_factory=list,
        init=False,
        cascade="all, delete-orphan",
    )
    active_version: Mapped["DocumentVersion | None"] = relationship(
        foreign_keys=[active_version_id], init=False, default=None, viewonly=True
    )


class DocumentVersion(Base):
    """Document version model - represents a single version of a document."""

    __tablename__ = "document_versions"
    __table_args__ = (
        UniqueConstraint("project_id", "version_number", name="uq_project_version"),
        Index("ix_document_versions_project_id", "project_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id"))
    version_number: Mapped[int] = mapped_column(Integer)
    original_filename: Mapped[str] = mapped_column(String)
    file_extension: Mapped[str] = mapped_column(String)
    original_file_path: Mapped[str] = mapped_column(String)  # Relative path
    markdown_file_path: Mapped[str] = mapped_column(String)  # Relative path
    character_count: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow, init=False)

    # Relationships
    project: Mapped["Project"] = relationship(
        back_populates="versions", foreign_keys=[project_id], init=False
    )
    evaluations: Mapped[list["Evaluation"]] = relationship(
        back_populates="document_version", default_factory=list, init=False, cascade="all, delete-orphan"
    )


class Evaluation(Base):
    """Evaluation model - stores evaluation results for a document version."""

    __tablename__ = "evaluations"
    __table_args__ = (
        Index("ix_evaluations_evaluation_id", "evaluation_id"),
        Index("ix_evaluations_document_version_id", "document_version_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, init=False, autoincrement=True)
    evaluation_id: Mapped[str] = mapped_column(String)  # UUID
    document_version_id: Mapped[int] = mapped_column(Integer, ForeignKey("document_versions.id"))
    evaluation_type: Mapped[str] = mapped_column(String)  # "scoring" or "agent"
    evaluators_used: Mapped[str] = mapped_column(String)  # JSON array string
    results_json: Mapped[str] = mapped_column(String)  # Full results serialized
    status: Mapped[str] = mapped_column(String)
    error_message: Mapped[str | None] = mapped_column(String, default=None)
    duration_seconds: Mapped[float] = mapped_column(default=0.0)
    created_at: Mapped[datetime] = mapped_column(default_factory=datetime.utcnow, init=False)

    # Relationships
    document_version: Mapped["DocumentVersion"] = relationship(back_populates="evaluations", init=False)
