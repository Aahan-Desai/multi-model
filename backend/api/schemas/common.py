from pydantic import BaseModel, ConfigDict, Field


class BaseResponse(BaseModel):
    """
    Base schema for all API responses.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    success: bool = Field(
        description="Indicates whether the request completed successfully."
    )

    message: str = Field(
        description="Human-readable response message."
    )