from fastapi import Request

from backend.infrastructure.ingestion import IngestionService
from backend.infrastructure.vision import VisionService
from backend.orchestrator.router import Router


def get_router(request: Request) -> Router:
    """
    Retrieve the application Router instance.

    The Router is created once during application startup and stored
    on the FastAPI application state.
    """
    return request.app.state.router


def get_ingestion_service(request: Request) -> IngestionService:
    """
    Retrieve the application IngestionService instance.

    The service is created once during application startup and stored
    on the FastAPI application state.
    """
    return request.app.state.ingestion_service


def get_vision_service(request: Request) -> VisionService:
    """
    Retrieve the application VisionService instance.

    The service is created once during application startup and stored
    on the FastAPI application state.
    """
    return request.app.state.vision_service
