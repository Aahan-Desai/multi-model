from __future__ import annotations

from fastapi import UploadFile
from pathlib import Path

from backend.core.config import settings
from backend.core.logging import get_logger
from backend.infrastructure.document_processing.document_processor import (
    DocumentProcessor,
)
from backend.infrastructure.llm.embedding_service import EmbeddingService
from backend.infrastructure.storage.storage_service import StorageService
from backend.infrastructure.vector_db.collection_manager import CollectionManager
from backend.infrastructure.vector_db.qdrant_service import QdrantService
from backend.models.ingestion_result import IngestionResult
from backend.processing.chunking_service import ChunkingService

logger = get_logger(__name__)


class IngestionService:
    """
    Coordinates the complete RAG ingestion pipeline.

    Workflow:
        UploadFile
            ↓
        Storage
            ↓
        Document Processing
            ↓
        Chunking
            ↓
        Embedding
            ↓
        Collection Management
            ↓
        Qdrant Upsert
    """

    def __init__(
        self,
        storage_service: StorageService | None = None,
        document_processor: DocumentProcessor | None = None,
        chunking_service: ChunkingService | None = None,
        embedding_service: EmbeddingService | None = None,
        collection_manager: CollectionManager | None = None,
        qdrant_service: QdrantService | None = None,
    ) -> None:
        self._storage_service = storage_service or StorageService()
        self._document_processor = (
            document_processor or DocumentProcessor()
        )
        self._chunking_service = (
            chunking_service or ChunkingService()
        )
        self._embedding_service = (
            embedding_service or EmbeddingService()
        )
        self._collection_manager = (
            collection_manager or CollectionManager()
        )
        self._qdrant_service = qdrant_service or QdrantService()

    async def ingest(
        self,
        file: UploadFile,
    ) -> IngestionResult:
            """
                 Ingest a document into Qdrant.

                    Args:
                        file:
                          Uploaded document.
                    Returns:
                            Summary of the ingestion process.
             """

            extension = Path(file.filename or "").suffix.lower()

            if extension not in settings.supported_document_extensions:
                raise ValueError(
                    f"Unsupported file type: '{extension}'. "
                    f"Supported types: {', '.join(sorted(settings.supported_document_extensions))}"
                )
            logger.info("Starting ingestion for '%s'.", file.filename)

            # Step 1: Store file
            file_path = await self._storage_service.save_file(file)

            # Step 2: Extract document
            document = self._document_processor.extract_document(file_path)

            # Step 3: Chunk document
            chunks = self._chunking_service.chunk_document(document)

            if not chunks:
                raise ValueError("No chunks were generated from the document.")

            # Step 4: Generate embeddings
            embeddings = self._embedding_service.embed_texts(
                [chunk.text for chunk in chunks]
            )

            # Step 5: Ensure collection exists
            self._collection_manager.create(
                settings.qdrant_collection_name
            )

            # Step 6: Upload embeddings to Qdrant
            self._qdrant_service.upsert_embeddings(
                collection_name=settings.qdrant_collection_name,
                chunks=chunks,
                embeddings=embeddings,
            )

            logger.info(
                "Successfully ingested '%s' (%d chunk(s)).",
                file.filename,
                len(chunks),
            )

            return IngestionResult(
                filename=file.filename or file_path.name,
                chunks_created=len(chunks),
                vectors_uploaded=len(chunks),
            )