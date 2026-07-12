from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class IngestionResult:
    """
    Result returned after successfully ingesting a document.
    """

    filename: str
    chunks_created: int
    vectors_uploaded: int