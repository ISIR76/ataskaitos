"""Document processing and conversion service."""

from pathlib import Path
from tempfile import NamedTemporaryFile

from fastapi import HTTPException, UploadFile
from markitdown import MarkItDown


class DocumentService:
    """Service for document processing and conversion."""

    SUPPORTED_FORMATS = {".docx", ".pdf", ".doc", ".txt", ".md"}

    def __init__(self):
        self.converter = MarkItDown()

    async def convert_to_markdown(self, file: UploadFile) -> str:
        """Convert uploaded file to markdown text.

        Args:
            file: Uploaded file from FastAPI

        Returns:
            Markdown text content

        Raises:
            HTTPException: If file is invalid or conversion fails
        """
        if not file.filename:
            raise HTTPException(status_code=400, detail="No file provided")

        # Check file extension
        file_ext = Path(file.filename).suffix.lower()

        if file_ext not in self.SUPPORTED_FORMATS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file format: {file_ext}. "
                f"Supported formats: {', '.join(self.SUPPORTED_FORMATS)}",
            )

        try:
            # Save uploaded file to temporary location
            with NamedTemporaryFile(delete=False, suffix=file_ext) as tmp_file:
                content = await file.read()
                tmp_file.write(content)
                tmp_path = Path(tmp_file.name)

            # Convert to markdown
            try:
                result = self.converter.convert(str(tmp_path))
                return result.text_content
            finally:
                # Clean up temp file
                tmp_path.unlink(missing_ok=True)

        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error converting file to markdown: {str(e)}"
            )

    def convert_file_to_markdown(self, file_path: str | Path) -> str:
        """Convert a file path to markdown (sync version for CLI/scripts).

        Args:
            file_path: Path to the file to convert

        Returns:
            Markdown text content

        Raises:
            ValueError: If file doesn't exist or has unsupported format
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise ValueError(f"File not found: {file_path}")

        file_ext = file_path.suffix.lower()
        if file_ext not in self.SUPPORTED_FORMATS:
            raise ValueError(
                f"Unsupported file format: {file_ext}. "
                f"Supported formats: {', '.join(self.SUPPORTED_FORMATS)}"
            )

        try:
            result = self.converter.convert(str(file_path))
            return result.text_content
        except Exception as e:
            raise ValueError(f"Error converting file to markdown: {str(e)}")
