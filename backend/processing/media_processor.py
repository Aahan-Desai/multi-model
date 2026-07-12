from __future__ import annotations

import mimetypes
from pathlib import Path
from typing import Literal

from backend.core.logging import get_logger
from backend.models.media_data import MediaData

logger = get_logger(__name__)


class MediaProcessor:
    """
    Processes uploaded media (images and videos) into a strongly typed
    MediaData model suitable for downstream vision and analysis services.

    Supports both image and video formats with automatic type detection
    and validation based on file extension.
    """

    _SUPPORTED_IMAGE_EXTENSIONS = frozenset(
        {
            ".jpg",
            ".jpeg",
            ".png",
            ".gif",
            ".webp",
            ".bmp",
            ".tiff",
        }
    )

    _SUPPORTED_VIDEO_EXTENSIONS = frozenset(
        {
            ".mp4",
            ".mov",
            ".avi",
            ".mkv",
            ".webm",
            ".mpeg",
            ".mpg",
        }
    )

    def process(self, media_path: Path) -> MediaData:
        """
        Validate and prepare media (image or video) for analysis.

        Args:
            media_path: Path to the uploaded media file.

        Returns:
            A MediaData instance containing validated metadata and
            automatically detected media type.

        Raises:
            FileNotFoundError:
                If the media file does not exist.

            ValueError:
                If the media format is unsupported or the MIME type
                cannot be determined.
        """
        logger.info("Processing media: %s", media_path.name)

        if not media_path.exists():
            raise FileNotFoundError(f"Media not found: {media_path}")

        extension = media_path.suffix.lower()

        # Determine media type from validated extension (source of truth)
        media_type: Literal["image", "video"] | None = None

        if extension in self._SUPPORTED_IMAGE_EXTENSIONS:
            media_type = "image"
        elif extension in self._SUPPORTED_VIDEO_EXTENSIONS:
            media_type = "video"
        else:
            raise ValueError(
                f"Unsupported media format: {extension}"
            )

        # Determine MIME type
        mime_type, _ = mimetypes.guess_type(media_path)

        if mime_type is None:
            raise ValueError(
                f"Unable to determine MIME type for '{media_path.name}'."
            )

        # Validate MIME type matches determined media type
        mime_category = mime_type.split("/")[0]
        if mime_category != media_type:
            logger.warning(
                "MIME type category '%s' does not match detected media type '%s' "
                "for '%s'. Using extension-based detection.",
                mime_category,
                media_type,
                media_path.name,
            )

        file_size = media_path.stat().st_size

        return MediaData(
            file_path=media_path,
            filename=media_path.name,
            mime_type=mime_type,
            file_size=file_size,
            media_type=media_type,
        )
