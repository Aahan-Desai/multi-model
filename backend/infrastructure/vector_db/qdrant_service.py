from __future__ import annotations

import uuid

from qdrant_client import QdrantClient
from qdrant_client.http.models import Filter, PointStruct

from backend.core.clients import get_qdrant_client
from backend.core.logging import get_logger
from backend.models.document_chunk import DocumentChunk
from backend.models.retrieved_chunk import RetrievedChunk

logger = get_logger(__name__)


class QdrantService:
    """
    Service responsible for interacting with Qdrant.

    This class encapsulates all vector storage and retrieval operations,
    providing a clean interface for the rest of the application while
    hiding direct interactions with the Qdrant SDK.
    """

    def __init__(self, client: QdrantClient | None = None) -> None:
        """
        Initialize the Qdrant service.

        Args:
            client:
                Optional Qdrant client instance. Primarily intended for testing.
                If omitted, the shared application client is used.
        """
        self._client = client or get_qdrant_client()

    def upsert(
        self,
        *,
        collection_name: str,
        points: list[PointStruct],
    ) -> None:
        """
        Insert or update vectors in a collection.

        Args:
            collection_name:
                Name of the target Qdrant collection.

            points:
                List of Qdrant PointStruct objects.

        Raises:
            Exception:
                Propagates any exception raised by the Qdrant SDK.
        """

        logger.info(
            "Upserting %d point(s) into collection '%s'.",
            len(points),
            collection_name,
        )

        self._client.upsert(
            collection_name=collection_name,
            points=points,
        )

        logger.debug(
            "Successfully upserted %d point(s).",
            len(points),
        )

    def upsert_embeddings(
        self,
        *,
        collection_name: str,
        chunks: list[DocumentChunk],
        embeddings: list[list[float]],
    ) -> None:
        """
        Convert document chunks and embeddings into Qdrant points and
        upload them to the collection.

        Args:
            collection_name:
                Target collection.

            chunks:
                Document chunks.

            embeddings:
                Embeddings corresponding to each chunk.
        """

        if len(chunks) != len(embeddings):
            raise ValueError(
                "The number of chunks and embeddings must match."
            )

        points: list[PointStruct] = []

        for chunk, embedding in zip(chunks, embeddings, strict=True):
            payload = dict(chunk.metadata)
            payload["text"] = chunk.text

            points.append(
                PointStruct(
                    id=str(uuid.uuid4()),
                    vector=embedding,
                    payload=payload,
                )
            )

        self.upsert(
            collection_name=collection_name,
            points=points,
        )

    def search(
        self,
        *,
        collection_name: str,
        query_vector: list[float],
        limit: int = 5,
        query_filter: Filter | None = None,
    ) -> list[RetrievedChunk]:
        """
        Search for the nearest vectors in a collection.

        Args:
            collection_name:
                Name of the collection.

            query_vector:
                Embedding vector representing the query.

            limit:
                Maximum number of results to return.

            query_filter:
                Optional filter to apply during search.

        Returns:
            A list of normalized retrieved chunks.

        Raises:
            Exception:
                Propagates any exception raised by the Qdrant SDK.
        """

        logger.info(
            "Searching collection '%s' (limit=%d).",
            collection_name,
            limit,
        )

        response = self._client.query_points(
            collection_name=collection_name,
            query=query_vector,
            query_filter=query_filter,
            limit=limit,
            with_payload=True,
            with_vectors=False,
        )

        logger.debug(
            "Retrieved %d search result(s).",
            len(response.points),
        )

        retrieved_chunks: list[RetrievedChunk] = []

        for point in response.points:
            payload = point.payload or {}

            retrieved_chunks.append(
                RetrievedChunk(
                    id=str(point.id),
                    score=point.score,
                    content=str(payload.get("text", "")),
                    metadata={
                        key: str(value)
                        for key, value in payload.items()
                        if key != "text"
                    },
                )
            )

        return retrieved_chunks

    def delete(
        self,
        *,
        collection_name: str,
        point_ids: list[str],
    ) -> None:
        """
        Delete vectors from a collection.

        Args:
            collection_name:
                Name of the collection.

            point_ids:
                List of point IDs to delete.

        Raises:
            Exception:
                Propagates any exception raised by the Qdrant SDK.
        """

        logger.info(
            "Deleting %d point(s) from collection '%s'.",
            len(point_ids),
            collection_name,
        )

        self._client.delete(
            collection_name=collection_name,
            points_selector=point_ids,
        )

        logger.debug(
            "Successfully deleted %d point(s).",
            len(point_ids),
        )