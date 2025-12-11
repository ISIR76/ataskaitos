"""Document version repository for data access operations."""

from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from ataskaitos.models.database import DocumentVersion


class DocumentVersionRepository:
    """Repository for DocumentVersion data access operations."""

    def __init__(self, session: Session):
        """Initialize repository with database session.

        Args:
            session: SQLAlchemy session
        """
        self.session = session

    def create(
        self,
        project_id: int,
        version_number: int,
        original_filename: str,
        file_extension: str,
        original_file_path: str,
        markdown_file_path: str,
        character_count: int,
    ) -> DocumentVersion:
        """Create a new document version.

        Args:
            project_id: Project ID
            version_number: Version number (auto-incremented per project)
            original_filename: Original filename
            file_extension: File extension (e.g., ".docx")
            original_file_path: Relative path to original file
            markdown_file_path: Relative path to markdown file
            character_count: Number of characters in document

        Returns:
            Created DocumentVersion instance
        """
        version = DocumentVersion(
            project_id=project_id,
            version_number=version_number,
            original_filename=original_filename,
            file_extension=file_extension,
            original_file_path=original_file_path,
            markdown_file_path=markdown_file_path,
            character_count=character_count,
        )
        self.session.add(version)
        self.session.flush()
        return version

    def get_by_id(self, version_id: int, load_evaluations: bool = False) -> DocumentVersion | None:
        """Get document version by ID.

        Args:
            version_id: Version ID
            load_evaluations: Whether to eager load evaluations

        Returns:
            DocumentVersion instance or None if not found
        """
        query = select(DocumentVersion).where(DocumentVersion.id == version_id)

        if load_evaluations:
            query = query.options(selectinload(DocumentVersion.evaluations))

        result = self.session.execute(query)
        return result.scalar_one_or_none()

    def get_by_version(self, project_id: int, version_number: int) -> DocumentVersion | None:
        """Get document version by project and version number.

        Args:
            project_id: Project ID
            version_number: Version number

        Returns:
            DocumentVersion instance or None if not found
        """
        query = select(DocumentVersion).where(
            DocumentVersion.project_id == project_id, DocumentVersion.version_number == version_number
        )
        result = self.session.execute(query)
        return result.scalar_one_or_none()

    def list_by_project(self, project_id: int, load_evaluations: bool = False) -> list[DocumentVersion]:
        """List all versions for a project.

        Args:
            project_id: Project ID
            load_evaluations: Whether to eager load evaluations

        Returns:
            List of DocumentVersion instances ordered by version number
        """
        query = (
            select(DocumentVersion)
            .where(DocumentVersion.project_id == project_id)
            .order_by(DocumentVersion.version_number.desc())
        )

        if load_evaluations:
            query = query.options(selectinload(DocumentVersion.evaluations))

        result = self.session.execute(query)
        return list(result.scalars().all())

    def get_next_version_number(self, project_id: int) -> int:
        """Get the next version number for a project.

        Args:
            project_id: Project ID

        Returns:
            Next version number (1 if no versions exist)
        """
        query = select(func.max(DocumentVersion.version_number)).where(DocumentVersion.project_id == project_id)
        result = self.session.execute(query)
        max_version = result.scalar_one_or_none()

        return (max_version or 0) + 1

    def delete(self, version_id: int) -> bool:
        """Delete a document version.

        Args:
            version_id: Version ID

        Returns:
            True if deleted, False if not found
        """
        version = self.get_by_id(version_id)
        if not version:
            return False

        self.session.delete(version)
        self.session.flush()
        return True

    def count_by_project(self, project_id: int) -> int:
        """Count versions for a project.

        Args:
            project_id: Project ID

        Returns:
            Number of versions
        """
        query = select(func.count(DocumentVersion.id)).where(DocumentVersion.project_id == project_id)
        result = self.session.execute(query)
        return result.scalar_one()
