"""Evaluation repository for data access operations."""

import json
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ataskaitos.models.database import DocumentVersion, Evaluation, Project

logger = logging.getLogger(__name__)


class EvaluationRepository:
    """Repository for Evaluation data access operations."""

    def __init__(self, session: AsyncSession):
        """Initialize repository with database session.

        Args:
            session: SQLAlchemy session
        """
        self.session = session

    async def create(
        self,
        evaluation_id: str,
        document_version_id: int,
        evaluation_type: str,
        evaluators_used: str,
        results_json: str,
        status: str,
        duration_seconds: float,
        error_message: str | None = None,
    ) -> Evaluation:
        """Create a new evaluation record.

        Args:
            evaluation_id: Unique evaluation ID (UUID)
            document_version_id: Document version ID
            evaluation_type: Type of evaluation ("scoring" or "agent")
            evaluators_used: JSON string of evaluators used
            results_json: JSON string of evaluation results
            status: Status of evaluation
            duration_seconds: Duration of evaluation
            error_message: Optional error message

        Returns:
            Created Evaluation instance
        """
        evaluation = Evaluation(
            evaluation_id=evaluation_id,
            document_version_id=document_version_id,
            evaluation_type=evaluation_type,
            evaluators_used=evaluators_used,
            results_json=results_json,
            status=status,
            duration_seconds=duration_seconds,
            error_message=error_message,
        )
        self.session.add(evaluation)
        await self.session.flush()
        return evaluation

    async def get_by_id(self, id: int) -> Evaluation | None:
        """Get evaluation by database ID.

        Args:
            id: Evaluation database ID

        Returns:
            Evaluation instance or None if not found
        """
        query = select(Evaluation).where(Evaluation.id == id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def get_by_uuid(self, evaluation_id: str) -> Evaluation | None:
        """Get evaluation by UUID.

        Args:
            evaluation_id: Evaluation UUID

        Returns:
            Evaluation instance or None if not found
        """
        query = select(Evaluation).where(Evaluation.evaluation_id == evaluation_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def list_by_version(self, document_version_id: int) -> list[Evaluation]:
        """List all evaluations for a document version.

        Args:
            document_version_id: Document version ID

        Returns:
            List of Evaluation instances ordered by creation date (newest first)
        """
        query = (
            select(Evaluation)
            .where(Evaluation.document_version_id == document_version_id)
            .order_by(Evaluation.created_at.desc())
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def list_by_project(self, project_id: int) -> list[Evaluation]:
        """List all evaluations for a project (across all versions).

        Args:
            project_id: Project ID

        Returns:
            List of Evaluation instances ordered by creation date (newest first)
        """
        query = (
            select(Evaluation)
            .join(DocumentVersion)
            .where(DocumentVersion.project_id == project_id)
            .order_by(Evaluation.created_at.desc())
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def get_latest_scoring_per_project(
        self, user_id: int, project_type: str
    ) -> list[dict]:
        """Aggregate the most recent ``scoring`` evaluation per project for the user.

        Walks the user's projects, finds the active version for each, then picks the
        newest scoring evaluation on that version. Parses ``results_json`` and pulls
        the ``cases[0].scores`` mapping (matching what the frontend already renders).

        Returns one row per project (including projects with no scoring evaluation,
        which carry an empty scores dict). Each row::

            {
                "project_id": int,
                "project_name": str,
                "project_type": str,
                "is_marked_good": bool,
                "active_version_id": int | None,
                "active_version_number": int | None,
                "evaluation_id": str | None,
                "evaluated_at": datetime | None,
                "scores": dict[str, float],
            }
        """
        projects_q = (
            select(Project)
            .where(Project.user_id == user_id, Project.project_type == project_type)
            .order_by(Project.created_at.desc())
        )
        projects_result = await self.session.execute(projects_q)
        projects = list(projects_result.scalars().all())

        rows: list[dict] = []
        for project in projects:
            row: dict = {
                "project_id": project.id,
                "project_name": project.name,
                "project_type": project.project_type,
                "is_marked_good": bool(getattr(project, "is_marked_good", False)),
                "active_version_id": project.active_version_id,
                "active_version_number": None,
                "evaluation_id": None,
                "evaluated_at": None,
                "scores": {},
            }

            if project.active_version_id is None:
                rows.append(row)
                continue

            version_q = select(DocumentVersion).where(
                DocumentVersion.id == project.active_version_id
            )
            version = (await self.session.execute(version_q)).scalar_one_or_none()
            if version is None:
                rows.append(row)
                continue
            row["active_version_number"] = version.version_number

            eval_q = (
                select(Evaluation)
                .where(
                    Evaluation.document_version_id == version.id,
                    Evaluation.evaluation_type == "scoring",
                    Evaluation.status == "success",
                )
                .order_by(Evaluation.created_at.desc())
                .limit(1)
            )
            evaluation = (await self.session.execute(eval_q)).scalar_one_or_none()
            if evaluation is None:
                rows.append(row)
                continue

            row["evaluation_id"] = evaluation.evaluation_id
            row["evaluated_at"] = evaluation.created_at

            scores: dict[str, float] = {}
            try:
                payload = json.loads(evaluation.results_json or "{}")
                cases = payload.get("cases") or []
                if cases:
                    raw_scores = cases[0].get("scores") or {}
                    for name, value in raw_scores.items():
                        if isinstance(value, dict) and "value" in value:
                            try:
                                scores[name] = float(value["value"])
                            except (TypeError, ValueError):
                                continue
                        elif isinstance(value, (int, float)):
                            scores[name] = float(value)
            except (json.JSONDecodeError, TypeError, KeyError) as exc:
                logger.warning(
                    "Failed to parse results_json for evaluation %s: %s",
                    evaluation.evaluation_id,
                    exc,
                )

            row["scores"] = scores
            rows.append(row)

        return rows

    async def delete(self, id: int) -> bool:
        """Delete an evaluation.

        Args:
            id: Evaluation database ID

        Returns:
            True if deleted, False if not found
        """
        evaluation = await self.get_by_id(id)
        if not evaluation:
            return False

        await self.session.delete(evaluation)
        await self.session.flush()
        return True
