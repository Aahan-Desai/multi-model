from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class DocumentChunk:
    """
    Represents a single chunk extracted from a processed document.
    """

    chunk_id: int
    text: str
    metadata: dict[str, str] = field(default_factory=dict)