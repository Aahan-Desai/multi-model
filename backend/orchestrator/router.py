from __future__ import annotations

from pathlib import Path

from backend.core.config import settings
from backend.infrastructure.llm.chat_service import ChatService
from backend.models.router_response import RouterResponse
from backend.orchestrator.tool_executor import ToolExecutor
from backend.orchestrator.tool_schemas import TOOLS
from backend.prompts.router_prompt import ROUTER_SYSTEM_PROMPT
from backend.core.logging import get_logger

logger = get_logger(__name__)

class Router:
    """
    Routes user requests to the appropriate specialist using LLM tool calling.
    """

    def __init__(
        self,
        chat_service: ChatService | None = None,
        tool_executor: ToolExecutor | None = None,
    ) -> None:
        self._chat_service = chat_service or ChatService()
        self._tool_executor = tool_executor or ToolExecutor()

    def route(
        self,
        *,
        prompt: str,
        media_path: Path | None = None,
    ) -> str:
        """
        Route a user request to the appropriate specialist.

        Args:
            prompt:
                User request.

            media_path:
                Optional uploaded image/video.

        Returns:
            Final response.
        """

        prompt = prompt.strip()

        if not prompt:
            raise ValueError("Prompt cannot be empty.")

        response: RouterResponse = (
        self._chat_service.generate_with_tools(
            model=settings.orchestrator_model,
            system_prompt=ROUTER_SYSTEM_PROMPT,
            user_prompt=prompt,
            tools=TOOLS,
        )
    )


        if response.tool_call is None:
            return response.content

        return self._tool_executor.execute(
            tool_name=response.tool_call.name,
            arguments=response.tool_call.arguments,
            media_path=media_path,
        )