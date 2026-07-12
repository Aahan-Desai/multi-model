from __future__ import annotations

from pathlib import Path

from docling.document_converter import DocumentConverter

from backend.core.logging import get_logger
from backend.models.processed_document import ProcessedDocument

logger = get_logger(__name__)


class DocumentProcessor:
    """
    Handles document parsing and text extraction using Docling.

    This service converts supported document formats into the
    application's internal ProcessedDocument model.
    """

    def __init__(self, converter: DocumentConverter | None = None) -> None:
        self._converter = converter or DocumentConverter()

    def extract_document(
        self,
        file_path: Path,
    ) -> ProcessedDocument:
        """
        Extract text from a document.

        Args:
            file_path:
                Path to the stored document.

        Returns:
            ProcessedDocument containing the extracted text.

        Raises:
            Exception:
                Propagates any exception raised by Docling.
        """

        logger.info(
            "Processing document: %s",
            file_path,
        )

        result = self._converter.convert(file_path)

        text = result.document.export_to_markdown().strip()

        logger.info(
            "Successfully processed document: %s",
            file_path,
        )

        return ProcessedDocument(
            text=text,
            metadata={
                "filename": file_path.name,
                "source_path": str(file_path),
            },
        )