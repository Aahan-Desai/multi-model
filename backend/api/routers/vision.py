from __future__ import annotations

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from backend.api.routers.dependencies import get_vision_service
from backend.api.schemas.vision import VisionAnalysisResponse
from backend.core.logging import get_logger
from backend.infrastructure.llm.gemini_vision_service import (
    GeminiVisionModelUnavailableError,
)
from backend.infrastructure.vision import UnsupportedMediaError, VisionService

logger = get_logger(__name__)

router = APIRouter(
    prefix="/vision",
    tags=["Vision"],
)


@router.post(
    "/analyze",
    response_model=VisionAnalysisResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze an uploaded image or video",
)
async def analyze_vision_media(
    file: UploadFile = File(...),
    prompt: str | None = Form(default=None),
    vision_service: VisionService = Depends(get_vision_service),
) -> VisionAnalysisResponse:
    """
    Analyze uploaded image or video media through the vision pipeline.

    Args:
        file:
            Uploaded media file to analyze.
        prompt:
            Optional prompt guiding the analysis.
        vision_service:
            Vision business service.

    Returns:
        Structured vision analysis response.
    """
    try:
        result = await vision_service.analyze(
            file=file,
            prompt=prompt,
        )
    except UnsupportedMediaError as exc:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=str(exc),
        ) from exc
    except GeminiVisionModelUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        logger.exception("Unexpected vision analysis failure.")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze uploaded media.",
        ) from exc

    return VisionAnalysisResponse(
        success=True,
        message="Vision analysis completed successfully.",
        **result,
    )
