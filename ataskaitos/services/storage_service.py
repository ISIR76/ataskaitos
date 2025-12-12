"""File storage service for managing uploaded documents."""

import shutil
from pathlib import Path
from typing import NamedTuple, Protocol

from fastapi import UploadFile

from ataskaitos.settings import settings


class StoredDocumentPaths(NamedTuple):
    """Paths to stored document files."""

    original_file_path: str
    """Path to the original uploaded file (local path or gs:// URL)"""

    markdown_file_path: str
    """Path to the converted markdown file (local path or gs:// URL)"""


class StorageBackend(Protocol):
    """Protocol for storage backends."""

    async def save_document_files(
        self,
        project_id: int,
        version_number: int,
        original_file: UploadFile,
        markdown_content: str,
    ) -> StoredDocumentPaths:
        """Save original file and markdown content."""
        ...

    def get_markdown_content(self, project_id: int, version_number: int) -> str:
        """Get markdown content."""
        ...

    def delete_version_files(self, project_id: int, version_number: int) -> None:
        """Delete all files for a version."""
        ...

    def delete_project_files(self, project_id: int) -> None:
        """Delete all files for a project."""
        ...


class LocalStorageService:
    """Handles file storage operations for project documents."""

    def __init__(self, base_path: str = "data/uploads"):
        """Initialize storage service.

        Args:
            base_path: Base directory for file uploads
        """
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def _get_version_dir(self, project_id: int, version_number: int) -> Path:
        """Get directory path for a specific version.

        Args:
            project_id: Project ID
            version_number: Version number

        Returns:
            Path to version directory
        """
        return self.base_path / "projects" / str(project_id) / f"v{version_number}"

    async def save_document_files(
        self,
        project_id: int,
        version_number: int,
        original_file: UploadFile,
        markdown_content: str,
    ) -> StoredDocumentPaths:
        """Save original file and markdown content.

        Args:
            project_id: Project ID
            version_number: Version number
            original_file: Uploaded file object
            markdown_content: Converted markdown text

        Returns:
            StoredDocumentPaths with relative paths to saved files
        """
        version_dir = self._get_version_dir(project_id, version_number)
        version_dir.mkdir(parents=True, exist_ok=True)

        # Determine file extension
        filename = original_file.filename or "document"
        extension = Path(filename).suffix or ".bin"

        # Save original file
        original_path = version_dir / f"original{extension}"
        with original_path.open("wb") as f:
            content = await original_file.read()
            f.write(content)

        # Save markdown file
        markdown_path = version_dir / "converted.md"
        markdown_path.write_text(markdown_content, encoding="utf-8")

        # Return relative paths
        original_rel = str(original_path.relative_to(self.base_path))
        markdown_rel = str(markdown_path.relative_to(self.base_path))

        return StoredDocumentPaths(
            original_file_path=original_rel,
            markdown_file_path=markdown_rel,
        )

    def get_original_file_path(self, project_id: int, version_number: int) -> Path:
        """Get path to original file.

        Args:
            project_id: Project ID
            version_number: Version number

        Returns:
            Absolute path to original file
        """
        version_dir = self._get_version_dir(project_id, version_number)
        # Find the original file (could be .docx, .pdf, etc.)
        for file in version_dir.glob("original.*"):
            return file
        raise FileNotFoundError(f"Original file not found for project {project_id} v{version_number}")

    def get_markdown_content(self, project_id: int, version_number: int) -> str:
        """Get markdown content for a version.

        Args:
            project_id: Project ID
            version_number: Version number

        Returns:
            Markdown content as string
        """
        version_dir = self._get_version_dir(project_id, version_number)
        markdown_path = version_dir / "converted.md"

        if not markdown_path.exists():
            raise FileNotFoundError(f"Markdown file not found for project {project_id} v{version_number}")

        return markdown_path.read_text(encoding="utf-8")

    def delete_version_files(self, project_id: int, version_number: int) -> None:
        """Delete all files for a specific version.

        Args:
            project_id: Project ID
            version_number: Version number
        """
        version_dir = self._get_version_dir(project_id, version_number)
        if version_dir.exists():
            shutil.rmtree(version_dir)

    def delete_project_files(self, project_id: int) -> None:
        """Delete all files for a project (all versions).

        Args:
            project_id: Project ID
        """
        project_dir = self.base_path / "projects" / str(project_id)
        if project_dir.exists():
            shutil.rmtree(project_dir)


# Factory function to get the appropriate storage service
def get_storage_service() -> StorageBackend:
    """Get the configured storage service (local or GCS).

    Returns:
        Storage service instance based on configuration
    """
    if settings.use_gcs:
        from ataskaitos.services.gcs_storage_service import get_gcs_storage_service

        return get_gcs_storage_service()
    else:
        return LocalStorageService(base_path=settings.uploads_directory)


# Global storage service instance
storage_service = get_storage_service()
