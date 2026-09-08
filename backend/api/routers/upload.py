from fastapi import APIRouter, Depends, File, HTTPException, status, UploadFile

from backend.api.routers.dependencies import get_ingestion_service
from backend.core.logging import get_logger
from backend.infrastructure.ingestion import IngestionService
from backend.models.ingestion_result import IngestionResult

logger = get_logger(__name__)

router = APIRouter(
    prefix="/upload",
    tags=["Upload"],
)


@router.post(
    "",
    response_model=IngestionResult,
    status_code=status.HTTP_201_CREATED,
    summary="Upload and ingest a document",
)
async def upload_document(
    file: UploadFile = File(...),
    ingestion_service: IngestionService = Depends(get_ingestion_service),
) -> IngestionResult:
    """
    Upload a document and ingest it into the retrieval system.

    Args:
        file: Document to ingest.
        ingestion_service: Document ingestion service.

    Returns:
        Result of the ingestion process.
    """
    try:
        return await ingestion_service.ingest(file)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        logger.exception("Failed to ingest document '%s'.", file.filename)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to ingest document: {exc}",
        ) from exc