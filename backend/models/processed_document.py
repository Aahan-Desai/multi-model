from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class ProcessedDocument:
    """
    Internal representation of a processed document.

    This model isolates the rest of the application from the
    underlying document processing library.
    """

    text: str
    metadata: dict[str, str] = field(default_factory=dict)