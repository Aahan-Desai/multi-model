from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class RetrievedChunk:
    """
    Represents a normalized retrieval result returned by the vector database.

    This model forms the contract between the infrastructure layer and the
    specialist layer. It intentionally hides provider-specific SDK objects
    (e.g. Qdrant's ScoredPoint) behind a provider-agnostic representation.
    """

    id: str
    score: float
    content: str
    metadata: dict[str, str]