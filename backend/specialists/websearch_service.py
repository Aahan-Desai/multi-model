from __future__ import annotations

from typing import Any

from backend.core.config import settings
from backend.core.logging import get_logger
from backend.infrastructure.llm.chat_service import ChatService
from backend.infrastructure.websearch.tavily_service import TavilyService

logger = get_logger(__name__)


class WebSearchService:
    """
    Specialist responsible for answering user questions using
    fresh information retrieved from the web.

    Workflow:
        1. Search the web using Tavily.
        2. Build a structured context from the search results.
        3. Ask the LLM to synthesize an answer grounded only in
           those results.
    """

    _DEFAULT_MAX_RESULTS = 5

    _SYSTEM_PROMPT = """
You are a web research assistant.

Answer the user's question using ONLY the provided search results.

Rules:
- Base your answer only on the supplied search results.
- If the search results do not contain enough information,
  explicitly say so.
- Do not fabricate facts.
- Produce a concise, well-structured response.
"""

    def __init__(
        self,
        chat_service: ChatService | None = None,
        tavily_service: TavilyService | None = None,
    ) -> None:
        self._chat_service = chat_service or ChatService()
        self._tavily_service = tavily_service or TavilyService()

    def search(self, query: str) -> str:
        """
        Answer a user query using web search.

        Args:
            query: User's search query.

        Returns:
            A synthesized answer grounded in the retrieved search results.
        """
        logger.info("Processing web search request.")

        results = self._tavily_service.search(
            query=query,
            max_results=self._DEFAULT_MAX_RESULTS,
        )

        if not results:
            logger.info("No search results found.")
            return "I couldn't find relevant information for your query."

        context = self._build_search_context(results)

        prompt = (
            f"User Question:\n{query}\n\n"
            f"Search Results:\n{context}"
        )

        return self._chat_service.generate(
            model=settings.rag_model,
            system_prompt=self._SYSTEM_PROMPT,
            user_prompt=prompt,
        )

    @staticmethod
    def _build_search_context(
        results: list[dict[str, Any]],
    ) -> str:
        """
        Convert normalized search results into a structured
        prompt context for the LLM.
        """
        sections: list[str] = []

        for index, result in enumerate(results, start=1):
            title = result.get("title", "Unknown")
            url = result.get("url", "Unknown")
            content = result.get("content", "")

            sections.append(
                "\n".join(
                    [
                        f"Source {index}",
                        f"Title: {title}",
                        f"URL: {url}",
                        f"Content: {content}",
                    ]
                )
            )

        return "\n\n".join(sections)