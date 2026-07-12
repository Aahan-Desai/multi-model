from __future__ import annotations

import mimetypes
from pathlib import Path
from typing import Literal, TypedDict

from fastapi import UploadFile

from backend.core.config import settings
from backend.core.logging import get_logger
from backend.infrastructure.llm.gemini_vision_service import (
    GeminiVisionModelUnavailableError,
    GeminiVisionService,
)
from backend.infrastructure.storage.storage_service import StorageService
from backend.models.media_data import MediaData

logger = get_logger(__name__)


class VisionAnalysisResult(TypedDict):
    """Structured response returned by the vision business layer."""

    filename: str
    media_type: Literal["image", "video"]
    mime_type: str
    file_size: int
    analysis: str


class UnsupportedMediaError(ValueError):
    """Raised when an uploaded media file is not supported."""


class VisionService:
    """
    Coordinates media upload validation, storage, and vision analysis.

    This service owns the business workflow for image and video analysis
    while delegating persistence and Gemini SDK calls to infrastructure
    services.
    """

    def __init__(
        self,
        storage_service: StorageService | None = None,
        gemini_vision_service: GeminiVisionService | None = None,
    ) -> None:
        self._storage_service = storage_service or StorageService()
        self._gemini_vision_service = (
            gemini_vision_service or GeminiVisionService()
        )

    async def analyze(
        self,
        file: UploadFile,
        prompt: str | None = None,
    ) -> VisionAnalysisResult:
        """
        Validate, persist, and analyze uploaded media.

        Args:
            file:
                Uploaded image or video file.
            prompt:
                Optional user prompt to guide the analysis.

        Returns:
            Structured analysis result.

        Raises:
            UnsupportedMediaError:
                If the uploaded file extension is not supported.

            RuntimeError:
                If storage or Gemini processing fails.
        """
        filename = file.filename or ""
        extension = self._get_extension(filename)

        logger.info("Vision upload received for '%s'.", filename)

        self._validate_extension(extension)

        try:
            file_path = await self._storage_service.save_file(file)
        except Exception as exc:  # pragma: no cover - defensive fallback
            logger.exception(
                "Vision upload failed while saving '%s'.",
                filename,
            )
            raise RuntimeError("Failed to save uploaded media.") from exc

        logger.info("Vision file saved to '%s'.", file_path)

        media = self._build_media_data(file_path=file_path, original_name=filename)

        logger.info(
            "Detected media type '%s' for '%s'.",
            media.media_type,
            media.filename,
        )
        logger.info("Starting Gemini vision request for '%s'.", media.filename)

        try:
            analysis = self._gemini_vision_service.generate_content(
                media=media,
                prompt=prompt or "Describe this media in detail.",
            )
        except GeminiVisionModelUnavailableError:
            logger.exception(
                "Configured Gemini vision model is unavailable for '%s'.",
                media.filename,
            )
            raise
        except Exception as exc:
            logger.exception(
                "Gemini vision analysis failed for '%s'.",
                media.filename,
            )
            raise RuntimeError("Vision analysis failed.") from exc

        logger.info("Gemini vision completed for '%s'.", media.filename)

        return VisionAnalysisResult(
            filename=media.filename,
            media_type=media.media_type,
            mime_type=media.mime_type,
            file_size=media.file_size,
            analysis=analysis,
        )

    def _get_extension(self, filename: str) -> str:
        """
        Extract the normalized file extension from an uploaded filename.

        Args:
            filename:
                Original uploaded filename.

        Returns:
            Lowercase file extension.
        """
        return Path(filename).suffix.lower()

    def _validate_extension(self, extension: str) -> None:
        """
        Ensure the uploaded file extension is supported for vision analysis.

        Args:
            extension:
                Lowercase file extension.

        Raises:
            UnsupportedMediaError:
                If the extension is not a supported image or video format.
        """
        supported_extensions = (
            settings.supported_image_extensions
            | settings.supported_video_extensions
        )

        if extension not in supported_extensions:
            supported_list = ", ".join(sorted(supported_extensions))
            raise UnsupportedMediaError(
                f"Unsupported media type: '{extension}'. "
                f"Supported media types: {supported_list}"
            )

    def _build_media_data(
        self,
        file_path: Path,
        original_name: str,
    ) -> MediaData:
        """
        Build strongly typed media metadata from a stored file.

        Args:
            file_path:
                Location of the saved upload.
            original_name:
                Original filename supplied by the client.

        Returns:
            Validated media metadata for Gemini processing.

        Raises:
            UnsupportedMediaError:
                If the stored file extension is unsupported.

            RuntimeError:
                If the MIME type cannot be determined.
        """
        extension = file_path.suffix.lower()
        media_type = self._detect_media_type(extension)

        mime_type, _ = mimetypes.guess_type(original_name or file_path.name)
        if mime_type is None:
            mime_type, _ = mimetypes.guess_type(file_path.name)

        if mime_type is None:
            raise RuntimeError(
                f"Unable to determine MIME type for '{original_name or file_path.name}'."
            )

        return MediaData(
            file_path=file_path,
            filename=original_name or file_path.name,
            mime_type=mime_type,
            file_size=file_path.stat().st_size,
            media_type=media_type,
        )

    def _detect_media_type(self, extension: str) -> Literal["image", "video"]:
        """
        Detect the media type from the file extension.

        Args:
            extension:
                Lowercase file extension.

        Returns:
            Either ``"image"`` or ``"video"``.

        Raises:
            UnsupportedMediaError:
                If the extension does not belong to a supported media type.
        """
        if extension in settings.supported_image_extensions:
            return "image"

        if extension in settings.supported_video_extensions:
            return "video"

        raise UnsupportedMediaError(f"Unsupported media type: '{extension}'.")
