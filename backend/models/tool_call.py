from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class ToolCall:
    name: str
    arguments: dict[str, object]