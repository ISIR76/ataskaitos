"""Tests for DocumentService."""

from io import BytesIO
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException, UploadFile

from ataskaitos.services.document_service import DocumentService

pytestmark = pytest.mark.anyio


@pytest.fixture
def document_service():
    """Create a DocumentService instance."""
    return DocumentService()


@pytest.fixture
def mock_markdown_result():
    """Mock MarkItDown conversion result."""
    result = MagicMock()
    result.text_content = "# Test Document\n\nThis is test content."
    return result


class TestDocumentService:
    """Test DocumentService functionality."""

    def test_init(self):
        """Test service initialization."""
        service = DocumentService()
        assert service.converter is not None
        assert service.SUPPORTED_FORMATS == {".docx", ".pdf", ".doc", ".txt", ".md"}

    async def test_convert_to_markdown_success(self, document_service, mock_markdown_result):
        """Test successful file conversion to markdown."""
        # Create mock upload file
        file_content = b"fake docx content"
        upload_file = UploadFile(filename="test.docx", file=BytesIO(file_content))

        # Mock the converter
        with patch.object(document_service.converter, "convert", return_value=mock_markdown_result):
            result = await document_service.convert_to_markdown(upload_file)

        assert result == "# Test Document\n\nThis is test content."

    async def test_convert_to_markdown_no_filename(self, document_service):
        """Test conversion fails when no filename provided."""
        upload_file = UploadFile(filename=None, file=BytesIO(b"content"))

        with pytest.raises(HTTPException) as exc_info:
            await document_service.convert_to_markdown(upload_file)

        assert exc_info.value.status_code == 400
        assert "No file provided" in exc_info.value.detail

    async def test_convert_to_markdown_unsupported_format(self, document_service):
        """Test conversion fails with unsupported file format."""
        upload_file = UploadFile(filename="test.xyz", file=BytesIO(b"content"))

        with pytest.raises(HTTPException) as exc_info:
            await document_service.convert_to_markdown(upload_file)

        assert exc_info.value.status_code == 400
        assert "Unsupported file format" in exc_info.value.detail

    @pytest.mark.parametrize("extension", [".docx", ".pdf", ".doc", ".txt", ".md"])
    async def test_convert_to_markdown_supported_formats(self, document_service, mock_markdown_result, extension):
        """Test all supported file formats."""
        upload_file = UploadFile(filename=f"test{extension}", file=BytesIO(b"content"))

        with patch.object(document_service.converter, "convert", return_value=mock_markdown_result):
            result = await document_service.convert_to_markdown(upload_file)

        assert result == "# Test Document\n\nThis is test content."

    def test_convert_file_to_markdown_sync_success(self, document_service, mock_markdown_result, tmp_path):
        """Test synchronous file conversion."""
        # Create a temporary file
        test_file = tmp_path / "test.txt"
        test_file.write_text("Test content")

        with patch.object(document_service.converter, "convert", return_value=mock_markdown_result):
            result = document_service.convert_file_to_markdown(test_file)

        assert result == "# Test Document\n\nThis is test content."

    def test_convert_file_to_markdown_file_not_found(self, document_service):
        """Test sync conversion fails when file doesn't exist."""
        with pytest.raises(ValueError) as exc_info:
            document_service.convert_file_to_markdown("/nonexistent/file.docx")

        assert "File not found" in str(exc_info.value)

    def test_convert_file_to_markdown_unsupported_format_sync(self, document_service, tmp_path):
        """Test sync conversion fails with unsupported format."""
        test_file = tmp_path / "test.xyz"
        test_file.write_text("content")

        with pytest.raises(ValueError) as exc_info:
            document_service.convert_file_to_markdown(test_file)

        assert "Unsupported file format" in str(exc_info.value)

    async def test_convert_to_markdown_conversion_error(self, document_service):
        """Test handling of conversion errors."""
        upload_file = UploadFile(filename="test.docx", file=BytesIO(b"content"))

        with patch.object(document_service.converter, "convert", side_effect=Exception("Conversion failed")):
            with pytest.raises(HTTPException) as exc_info:
                await document_service.convert_to_markdown(upload_file)

            assert exc_info.value.status_code == 500
            assert "Error converting file" in exc_info.value.detail
