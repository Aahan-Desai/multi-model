from __future__ import annotations

import uuid
from pathlib import Path

import aiofiles
from fastapi import UploadFile

from backend.core.config import settings
from backend.core.logging import get_logger

logger = get_logger(__name__)


class StorageService:
    """
    Handles persistence of uploaded files.

    This service is responsible only for storing files on disk.
    """

    def __init__(self, upload_dir: Path | None = None) -> None:
        self._upload_dir = upload_dir or settings.storage_path
        self._upload_dir.mkdir(parents=True, exist_ok=True)

    async def save_file(self, file: UploadFile) -> Path:
        """
        Save an uploaded file to local storage.

        Args:
            file:
                The uploaded file.

        Returns:
            Path to the saved file.
        """

        extension = Path(file.filename or "").suffix

        filename = f"{uuid.uuid4()}{extension}"

        destination = self._upload_dir / filename

        logger.info(
            "Saving uploaded file '%s' to '%s'.",
            file.filename,
            destination,
        )

        async with aiofiles.open(destination, "wb") as out_file:
            while chunk := await file.read(1024 * 1024):
                await out_file.write(chunk)

        logger.info(
            "File saved successfully: %s",
            destination,
        )

        return destination