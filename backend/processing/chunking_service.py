from __future__ import annotations

from backend.core.config import settings
from backend.core.logging import get_logger
from backend.models.document_chunk import DocumentChunk
from backend.models.processed_document import ProcessedDocument

logger = get_logger(__name__)


class ChunkingService:
    """
    Splits processed documents into overlapping word-based chunks.
    """

    def chunk_document(
        self,
        document: ProcessedDocument,
    ) -> list[DocumentChunk]:
        """
        Split a processed document into overlapping chunks.

        Args:
            document:
                Processed document.

        Returns:
            List of document chunks.
        """

        text = document.text.strip()

        if not text:
            logger.warning("Received empty document for chunking.")
            return []

        words = text.split()

        chunk_size = settings.chunk_size
        overlap = settings.chunk_overlap

        if overlap >= chunk_size:
            raise ValueError(
                "CHUNK_OVERLAP must be smaller than CHUNK_SIZE."
            )

        chunks: list[DocumentChunk] = []

        step = chunk_size - overlap

        start = 0

        while start < len(words):
            end = min(start + chunk_size, len(words))

            chunk_text = " ".join(words[start:end])

            chunks.append(
                DocumentChunk(
                    chunk_id=len(chunks),
                    text=chunk_text,
                    metadata=document.metadata.copy(),
                )
            )

            if end == len(words):
                break

            start += step

        total_chunks = len(chunks)

        for chunk in chunks:
            chunk.metadata["chunk_id"] = str(chunk.chunk_id)
            chunk.metadata["total_chunks"] = str(total_chunks)

        logger.info(
            "Generated %d chunk(s).",
            total_chunks,
        )

        return chunks