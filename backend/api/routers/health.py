from fastapi import APIRouter, status

from backend.api.schemas.health import HealthResponse

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get(
    "",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check",
)
async def health_check() -> HealthResponse:
    """
    Check whether the API is running.

    Returns:
        HealthResponse indicating the application is healthy.
    """
    return HealthResponse(status="healthy")