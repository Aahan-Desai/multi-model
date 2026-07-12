from __future__ import annotations

from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

from backend.core.clients import get_qdrant_client
from backend.core.config import settings
from backend.core.logging import get_logger

logger = get_logger(__name__)


class CollectionManager:
    """
    Manages the lifecycle of Qdrant collections.

    This service is responsible only for collection management.
    It intentionally does not perform vector CRUD operations,
    which belong in QdrantService.
    """

    def __init__(self, client: QdrantClient | None = None) -> None:
        """
        Initialize the collection manager.

        Args:
            client:
                Optional Qdrant client instance.
                Primarily intended for testing.
        """
        self._client = client or get_qdrant_client()

    def exists(self, collection_name: str) -> bool:
        """
        Check whether a collection exists.

        Args:
            collection_name:
                Name of the collection.

        Returns:
            True if the collection exists, otherwise False.
        """
        collections = self._client.get_collections().collections

        return any(
            collection.name == collection_name
            for collection in collections
        )

    def create(self, collection_name: str) -> None:
        """
        Create a new collection if it does not already exist.

        Args:
            collection_name:
                Name of the collection.
        """
        if self.exists(collection_name):
            logger.info(
                "Collection '%s' already exists.",
                collection_name,
            )
            return

        logger.info(
            "Creating collection '%s'.",
            collection_name,
        )

        self._client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(
                size=settings.embedding_dimension,
                distance=Distance.COSINE,
            ),
        )

        logger.info(
            "Collection '%s' created successfully.",
            collection_name,
        )

    def delete(self, collection_name: str) -> None:
        """
        Delete a collection.

        Args:
            collection_name:
                Name of the collection.
        """
        if not self.exists(collection_name):
            logger.info(
                "Collection '%s' does not exist.",
                collection_name,
            )
            return

        logger.info(
            "Deleting collection '%s'.",
            collection_name,
        )

        self._client.delete_collection(
            collection_name=collection_name,
        )

        logger.info(
            "Collection '%s' deleted successfully.",
            collection_name,
        )

    def recreate(self, collection_name: str) -> None:
        """
        Delete and recreate a collection.

        Useful during development when rebuilding the vector store.

        Args:
            collection_name:
                Name of the collection.
        """
        logger.info(
            "Recreating collection '%s'.",
            collection_name,
        )

        if self.exists(collection_name):
            self.delete(collection_name)

        self.create(collection_name)