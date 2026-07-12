from pydantic import ConfigDict, Field

from backend.api.schemas.common import BaseResponse


class UploadResponse(BaseResponse):
    """
    Response returned after document ingestion.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    documents_processed: int = Field(
        ge=0,
        description="Number of successfully processed documents."
    )

    chunks_created: int = Field(
        ge=0,
        description="Number of chunks indexed."
    )