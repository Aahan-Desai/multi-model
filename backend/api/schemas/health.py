from typing import Literal

from pydantic import BaseModel, ConfigDict


class HealthResponse(BaseModel):
    """
    Health check response.
    """

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
    )

    status: Literal["healthy"]