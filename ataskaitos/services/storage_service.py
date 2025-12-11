"""File storage service for managing uploaded documents."""

import shutil
from pathlib import Path

from fastapi import UploadFile


class StorageService:
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
    ) -> tuple[str, str]:
        """Save original file and markdown content.

        Args:
            project_id: Project ID
            version_number: Version number
            original_file: Uploaded file object
            markdown_content: Converted markdown text

        Returns:
            Tuple of (original_file_path, markdown_file_path) as relative paths
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

        return original_rel, markdown_rel

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


# Global storage service instance
storage_service = StorageService()
