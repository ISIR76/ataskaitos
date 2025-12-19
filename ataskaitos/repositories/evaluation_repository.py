"""Evaluation repository for data access operations."""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ataskaitos.models.database import Evaluation


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
        from ataskaitos.models.database import DocumentVersion

        query = (
            select(Evaluation)
            .join(DocumentVersion)
            .where(DocumentVersion.project_id == project_id)
            .order_by(Evaluation.created_at.desc())
        )
        result = await self.session.execute(query)
        return list(result.scalars().all())

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
