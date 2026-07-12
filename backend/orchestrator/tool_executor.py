from __future__ import annotations

from pathlib import Path

from backend.specialists.math_service import MathService
from backend.specialists.rag_service import RAGService
from backend.specialists.vision_service import VisionService
from backend.specialists.websearch_service import WebSearchService


class ToolExecutor:
    """
    Executes specialist capabilities selected by the orchestrator.

    This class is responsible for dispatching tool calls returned by the
    orchestrator LLM to the appropriate specialist.
    """

    def __init__(
        self,
        rag_service: RAGService | None = None,
        vision_service: VisionService | None = None,
        web_search_service: WebSearchService | None = None,
        math_service: MathService | None = None,
    ) -> None:
        self._rag_service = rag_service or RAGService()
        self._vision_service = vision_service or VisionService()
        self._web_search_service = (
            web_search_service or WebSearchService()
        )
        self._math_service = math_service or MathService()

    def execute(
        self,
        *,
        tool_name: str,
        arguments: dict[str, object],
        media_path: Path | None = None,
    ) -> str:
        """
        Execute a tool selected by the orchestrator.

        Args:
            tool_name:
                Name of the selected tool.

            arguments:
                Parsed tool arguments.

            media_path:
                Optional media path used for vision analysis.

        Returns:
            The specialist response.

        Raises:
            ValueError:
                If the tool is unknown or required arguments are missing.
        """

        match tool_name:
            case "rag_search":
                question = arguments.get("question")

                if not isinstance(question, str):
                    raise ValueError(
                        "RAG search requires a valid question."
                    )

                return self._rag_service.answer(question)

            case "web_search":
                query = arguments.get("query")

                if not isinstance(query, str):
                    raise ValueError(
                        "Web search requires a valid query."
                    )

                return self._web_search_service.search(query)

            case "solve_math":
                problem = arguments.get("problem")

                if not isinstance(problem, str):
                    raise ValueError(
                        "Math solver requires a valid problem."
                    )

                return self._math_service.solve(problem)

            case "vision_analysis":
                if media_path is None:
                    return (
                        "No image or video file was provided. "
                        "Please select or upload an image/video in the Vision panel on the right and click 'Upload & Analyze' to inspect visual content."
                    )

                prompt = arguments.get("prompt")

                if not isinstance(prompt, str):
                    raise ValueError(
                        "Vision analysis requires a valid prompt."
                    )

                return self._vision_service.analyze(
                    media_path=media_path,
                    prompt=prompt,
                )

            case _:
                raise ValueError(
                    f"Unsupported tool '{tool_name}'."
                )