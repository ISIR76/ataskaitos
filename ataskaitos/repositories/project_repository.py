"""Project repository for data access operations."""

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from ataskaitos.models.database import Project


class ProjectRepository:
    """Repository for Project data access operations."""

    def __init__(self, session: Session):
        """Initialize repository with database session.

        Args:
            session: SQLAlchemy session
        """
        self.session = session

    def create(self, name: str, project_type: str, user_id: int) -> Project:
        """Create a new project.

        Args:
            name: Project name (must be unique)
            project_type: Type of project ("straipsnis" or "ataskaita")
            user_id: ID of the user who owns this project

        Returns:
            Created Project instance
        """
        project = Project(name=name, project_type=project_type, user_id=user_id)
        self.session.add(project)
        self.session.flush()  # Get the ID without committing
        return project

    def get_by_id(self, project_id: int, load_versions: bool = False) -> Project | None:
        """Get project by ID.

        Args:
            project_id: Project ID
            load_versions: Whether to eager load versions

        Returns:
            Project instance or None if not found
        """
        query = select(Project).where(Project.id == project_id)

        if load_versions:
            query = query.options(selectinload(Project.versions))

        result = self.session.execute(query)
        return result.scalar_one_or_none()

    def get_by_name(self, name: str) -> Project | None:
        """Get project by name.

        Args:
            name: Project name

        Returns:
            Project instance or None if not found
        """
        query = select(Project).where(Project.name == name)
        result = self.session.execute(query)
        return result.scalar_one_or_none()

    def list_all(self, skip: int = 0, limit: int = 100) -> list[Project]:
        """List all projects with pagination.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Project instances
        """
        query = (
            select(Project)
            .options(selectinload(Project.versions))
            .order_by(Project.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = self.session.execute(query)
        return list(result.scalars().all())

    def list_by_user(self, user_id: int, skip: int = 0, limit: int = 100) -> list[Project]:
        """List projects for a specific user with pagination.

        Args:
            user_id: User ID to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of Project instances owned by the user
        """
        query = (
            select(Project)
            .where(Project.user_id == user_id)
            .options(selectinload(Project.versions))
            .order_by(Project.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = self.session.execute(query)
        return list(result.scalars().all())

    def update_active_version(self, project_id: int, version_id: int | None) -> Project:
        """Update the active version for a project.

        Args:
            project_id: Project ID
            version_id: Version ID to set as active (or None to clear)

        Returns:
            Updated Project instance

        Raises:
            ValueError: If project not found
        """
        project = self.get_by_id(project_id)
        if not project:
            raise ValueError(f"Project {project_id} not found")

        project.active_version_id = version_id
        project.updated_at = datetime.utcnow()
        self.session.flush()
        return project

    def delete(self, project_id: int) -> bool:
        """Delete a project and all its versions (cascade).

        Args:
            project_id: Project ID

        Returns:
            True if deleted, False if not found
        """
        project = self.get_by_id(project_id)
        if not project:
            return False

        self.session.delete(project)
        self.session.flush()
        return True

    def count(self) -> int:
        """Count total number of projects.

        Returns:
            Total count of projects
        """
        from sqlalchemy import func

        query = select(func.count(Project.id))
        result = self.session.execute(query)
        return result.scalar_one()
