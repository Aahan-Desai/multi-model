from __future__ import annotations

from ollama import Client

from backend.core.config import settings
from backend.core.logging import get_logger

logger = get_logger(__name__)


class EmbeddingService:
    """
    Service responsible for generating embeddings using Ollama.

    This service provides a provider-agnostic interface for embedding
    generation. The rest of the application should depend only on this
    service rather than the Ollama SDK.
    """

    def __init__(self, client: Client | None = None) -> None:
        self._client = client or Client(host=settings.ollama_base_url)
        self._model = settings.ollama_embedding_model

    def embed_text(self, text: str) -> list[float]:
        """
        Generate an embedding for a single text.

        Args:
            text:
                Input text.

        Returns:
            Embedding vector.
        """
        text = text.strip()

        if not text:
            raise ValueError("Input text cannot be empty.")

        return self.embed_texts([text])[0]

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts:
                List of input texts.

        Returns:
            List of embedding vectors.
        """
        if not texts:
            return []

        texts = [text.strip() for text in texts]

        if any(not text for text in texts):
            raise ValueError(
                "Input texts cannot contain empty strings."
            )

        logger.info(
            "Generating embeddings for %d text(s).",
            len(texts),
        )

        response = self._client.embed(
            model=self._model,
            input=texts,
        )

        embeddings = response.embeddings

        if len(embeddings) != len(texts):
            raise RuntimeError(
                "The embedding service returned an unexpected number of embeddings."
            )

        for embedding in embeddings:
            if len(embedding) != settings.embedding_dimension:
                raise ValueError(
                    f"Expected embedding dimension "
                    f"{settings.embedding_dimension}, "
                    f"received {len(embedding)}."
                )

        logger.info(
            "Generated %d embedding(s).",
            len(embeddings),
        )

        return embeddings