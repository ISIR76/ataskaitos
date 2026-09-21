"""Google Cloud Storage service for managing uploaded documents."""

from pathlib import Path

from fastapi import UploadFile

try:
    from google.cloud import storage
    from google.oauth2 import service_account
except ImportError:
    storage = None  # type: ignore
    service_account = None  # type: ignore

from ataskaitos.services.storage_service import StoredDocumentPaths
from ataskaitos.settings import settings


class GCSStorageService:
    """Handles file storage operations using Google Cloud Storage."""

    def __init__(
        self,
        bucket_name: str | None = None,
        project_id: str | None = None,
        credentials_path: str | None = None,
        base_path: str = "ataskaitos",
    ):
        """Initialize GCS storage service.

        Args:
            bucket_name: GCS bucket name (defaults to settings)
            project_id: GCP project ID (defaults to settings)
            credentials_path: Path to service account JSON (defaults to settings)
            base_path: Base path within bucket (defaults to settings)
        """
        if storage is None:
            raise ImportError(
                "google-cloud-storage is not installed. "
                "Install it with: uv add google-cloud-storage"
            )

        self.bucket_name = bucket_name or settings.gcs_bucket_name
        self.project_id = project_id or settings.gcs_project_id
        self.credentials_path = credentials_path or settings.gcs_credentials_path
        self.base_path = base_path or settings.gcs_base_path

        if not self.bucket_name:
            raise ValueError("GCS bucket name must be provided")

        # Initialize GCS client
        if self.credentials_path:
            if service_account is None:
                raise ImportError(
                    "google-cloud-storage is not installed. "
                    "Install it with: uv add google-cloud-storage"
                )
            credentials = service_account.Credentials.from_service_account_file(
                self.credentials_path
            )
            self.client = storage.Client(
                project=self.project_id, credentials=credentials
            )
        else:
            # Use default credentials (for Cloud Run, GCE, etc.)
            self.client = storage.Client(project=self.project_id)

        self.bucket = self.client.bucket(self.bucket_name)

    def _get_blob_path(self, project_id: int, version_number: int, filename: str) -> str:
        """Get blob path for a file.

        Args:
            project_id: Project ID
            version_number: Version number
            filename: Filename (e.g., "original.docx" or "converted.md")

        Returns:
            Full blob path
        """
        return f"{self.base_path}/projects/{project_id}/v{version_number}/{filename}"

    async def save_document_files(
        self,
        project_id: int,
        version_number: int,
        original_file: UploadFile,
        markdown_content: str,
    ) -> StoredDocumentPaths:
        """Save original file and markdown content to GCS.

        Args:
            project_id: Project ID
            version_number: Version number
            original_file: Uploaded file object
            markdown_content: Converted markdown text

        Returns:
            StoredDocumentPaths with GCS URLs (gs:// format)
        """
        # Determine file extension
        filename = original_file.filename or "document"
        extension = Path(filename).suffix or ".bin"

        # Save original file
        original_blob_path = self._get_blob_path(
            project_id, version_number, f"original{extension}"
        )
        original_blob = self.bucket.blob(original_blob_path)

        # Read file content
        content = await original_file.read()
        original_blob.upload_from_string(
            content,
            content_type=original_file.content_type or "application/octet-stream",
        )

        # Save markdown file
        markdown_blob_path = self._get_blob_path(
            project_id, version_number, "converted.md"
        )
        markdown_blob = self.bucket.blob(markdown_blob_path)
        markdown_blob.upload_from_string(
            markdown_content, content_type="text/markdown; charset=utf-8"
        )

        # Return GCS paths (gs:// format)
        original_gcs_path = f"gs://{self.bucket_name}/{original_blob_path}"
        markdown_gcs_path = f"gs://{self.bucket_name}/{markdown_blob_path}"

        return StoredDocumentPaths(
            original_file_path=original_gcs_path,
            markdown_file_path=markdown_gcs_path,
        )

    def get_original_file_content(self, project_id: int, version_number: int) -> bytes:
        """Get original file content from GCS.

        Args:
            project_id: Project ID
            version_number: Version number

        Returns:
            File content as bytes

        Raises:
            FileNotFoundError: If file not found
        """
        # List blobs with the prefix to find the original file
        prefix = f"{self.base_path}/projects/{project_id}/v{version_number}/original"
        blobs = list(self.client.list_blobs(self.bucket_name, prefix=prefix))

        if not blobs:
            raise FileNotFoundError(
                f"Original file not found for project {project_id} v{version_number}"
            )

        # Get the first matching blob
        blob = blobs[0]
        return blob.download_as_bytes()

    def get_markdown_content(self, project_id: int, version_number: int) -> str:
        """Get markdown content from GCS.

        Args:
            project_id: Project ID
            version_number: Version number

        Returns:
            Markdown content as string

        Raises:
            FileNotFoundError: If file not found
        """
        markdown_blob_path = self._get_blob_path(
            project_id, version_number, "converted.md"
        )
        blob = self.bucket.blob(markdown_blob_path)

        if not blob.exists():
            raise FileNotFoundError(
                f"Markdown file not found for project {project_id} v{version_number}"
            )

        return blob.download_as_text(encoding="utf-8")

    def delete_version_files(self, project_id: int, version_number: int) -> None:
        """Delete all files for a specific version from GCS.

        Args:
            project_id: Project ID
            version_number: Version number
        """
        prefix = f"{self.base_path}/projects/{project_id}/v{version_number}/"
        blobs = self.client.list_blobs(self.bucket_name, prefix=prefix)

        for blob in blobs:
            blob.delete()

    def delete_project_files(self, project_id: int) -> None:
        """Delete all files for a project from GCS (all versions).

        Args:
            project_id: Project ID
        """
        prefix = f"{self.base_path}/projects/{project_id}/"
        blobs = self.client.list_blobs(self.bucket_name, prefix=prefix)

        for blob in blobs:
            blob.delete()

    def get_download_url(
        self, project_id: int, version_number: int, expiration_minutes: int = 60
    ) -> str:
        """Generate a signed URL for downloading the original file.

        Args:
            project_id: Project ID
            version_number: Version number
            expiration_minutes: URL expiration time in minutes

        Returns:
            Signed download URL
        """
        # Find the original file
        prefix = f"{self.base_path}/projects/{project_id}/v{version_number}/original"
        blobs = list(self.client.list_blobs(self.bucket_name, prefix=prefix))

        if not blobs:
            raise FileNotFoundError(
                f"Original file not found for project {project_id} v{version_number}"
            )

        blob = blobs[0]
        return blob.generate_signed_url(
            version="v4",
            expiration=expiration_minutes * 60,  # Convert to seconds
            method="GET",
        )


# Global GCS storage service instance (initialized only when needed)
_gcs_storage_service: GCSStorageService | None = None


def get_gcs_storage_service() -> GCSStorageService:
    """Get or create GCS storage service instance.

    Returns:
        GCS storage service instance

    Raises:
        ValueError: If GCS is not properly configured
    """
    global _gcs_storage_service

    if _gcs_storage_service is None:
        _gcs_storage_service = GCSStorageService()

    return _gcs_storage_service
