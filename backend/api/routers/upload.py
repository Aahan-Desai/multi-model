from fastapi import APIRouter, Depends, File, status, UploadFile

from backend.api.routers.dependencies import get_ingestion_service
from backend.infrastructure.ingestion import IngestionService
from backend.models.ingestion_result import IngestionResult

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
    return await ingestion_service.ingest(file)