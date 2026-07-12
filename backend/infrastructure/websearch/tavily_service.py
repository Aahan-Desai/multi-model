from __future__ import annotations

from typing import Any

from tavily import TavilyClient

from backend.core.clients import get_tavily_client
from backend.core.logging import get_logger

logger = get_logger(__name__)


class TavilyService:
    """
    Infrastructure service responsible for interacting with the Tavily Search API.

    This service encapsulates all communication with Tavily and exposes a clean,
    provider-agnostic interface to the rest of the application.
    """

    def __init__(self, client: TavilyClient | None = None) -> None:
        self._client = client or get_tavily_client()

    def search(
        self,
        query: str,
        max_results: int = 5,
    ) -> list[dict[str, Any]]:
        """
        Execute a web search using Tavily.

        Args:
            query: Search query.
            max_results: Maximum number of results to return.

        Returns:
            A list of normalized search results.
        """
        query = query.strip()

        if not query:
            raise ValueError("Search query cannot be empty.")

        if max_results <= 0:
            raise ValueError("max_results must be greater than zero.")

        logger.info(
            "Searching Tavily | query='%s' | max_results=%d",
            query,
            max_results,
        )

        try:
            response = self._client.search(
                query=query,
                max_results=max_results,
            )

            results = response.get("results", [])

            normalized_results = [
                {
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", ""),
                    "score": result.get("score"),
                }
                for result in results
            ]

            logger.info(
                "Tavily returned %d result(s).",
                len(normalized_results),
            )

            return normalized_results

        except Exception:
            logger.exception("Tavily search failed.")
            raise