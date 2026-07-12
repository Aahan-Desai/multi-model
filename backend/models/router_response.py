from dataclasses import dataclass

from backend.models.tool_call import ToolCall


@dataclass(slots=True, frozen=True)
class RouterResponse:
    """
    Normalized response returned by the orchestrator model.
    """

    content: str
    tool_call: ToolCall | None