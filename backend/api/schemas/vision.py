from pydantic import ConfigDict, Field

from backend.api.schemas.common import BaseResponse


class VisionAnalysisResponse(BaseResponse):
    """Response returned after successfully analyzing uploaded media."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    filename: str = Field(
        description="Original uploaded filename."
    )

    media_type: str = Field(
        description="Detected media category for the uploaded file."
    )

    mime_type: str = Field(
        description="Resolved MIME type of the uploaded media."
    )

    file_size: int = Field(
        ge=0,
        description="Size of the uploaded media in bytes."
    )

    analysis: str = Field(
        description="Vision model analysis of the uploaded media."
    )
