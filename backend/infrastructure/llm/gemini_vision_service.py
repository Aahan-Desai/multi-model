from __future__ import annotations

import time

from google import genai
from google.genai import errors, types

from backend.core.clients import get_gemini_client
from backend.core.config import settings
from backend.core.logging import get_logger
from backend.models.media_data import MediaData

logger = get_logger(__name__)


class GeminiVisionError(RuntimeError):
    """Base exception for Gemini vision failures."""


class GeminiVisionModelUnavailableError(GeminiVisionError):
    """Raised when the configured Gemini vision model is unavailable."""


class GeminiVisionService:
    """
    Infrastructure service for interacting with Google's Gemini vision APIs.

    This class encapsulates all Google GenAI SDK usage and exposes a single
    provider-agnostic interface for generating content from validated media.
    """

    def __init__(self, client: genai.Client | None = None) -> None:
        self._client = client or get_gemini_client()
        self._model_name = settings.gemini_vision_model

    def generate_content(
        self,
        media: MediaData,
        prompt: str,
    ) -> str:
        """
        Generate content from the provided media using Gemini.

        Args:
            media:
                A validated media payload produced by the media processing layer.

            prompt:
                The text prompt to send alongside the media.

        Returns:
            The generated response text as plain text.

        Raises:
            RuntimeError:
                If the upload or generation flow fails.

            TimeoutError:
                If a video upload remains in a non-active state beyond the
                configured timeout.
        """
        uploaded_file = None

        try:
            uploaded_file = self._upload_file(media)

            if media.media_type == "video":
                self._wait_until_active(uploaded_file)

            response_text = self._generate(uploaded_file, prompt)
            logger.info("Generation completed.")
            return response_text
        except (GeminiVisionError, RuntimeError, TimeoutError):
            raise
        except Exception as exc:  # pragma: no cover - defensive fallback
            raise RuntimeError("Gemini vision generation failed.") from exc
        finally:
            if uploaded_file is not None:
                self._cleanup_file(uploaded_file)

    def _upload_file(self, media: MediaData) -> types.File:
        logger.info("Uploading media to Gemini.")

        try:
            uploaded_file = self._client.files.upload(
                file=media.file_path,
                config={"mime_type": media.mime_type},
            )
        except Exception as exc:
            raise RuntimeError("Failed to upload media to Gemini.") from exc

        logger.info("Upload completed.")
        return uploaded_file

    def _wait_until_active(self, uploaded_file: types.File,) -> None:
        logger.info("Waiting for uploaded video to become active.")

        deadline = time.monotonic() + settings.gemini_video_processing_timeout
        

        while time.monotonic() < deadline:
            try:
                file_info = self._client.files.get(name=self._get_file_name(uploaded_file))
            except Exception as exc:
                raise RuntimeError("Failed to inspect uploaded video status.") from exc

            state = self._normalize_state(getattr(file_info, "state", None))

            if state == "ACTIVE":
                return

            if state in {"FAILED", "ERROR"}:
                raise RuntimeError("Gemini video processing failed.")

            time.sleep(settings.gemini_video_poll_interval)

        raise TimeoutError(
            "Timed out waiting for Gemini video processing to complete."
        )

    def _generate(self, uploaded_file: types.File, prompt: str) -> str:
        try:
            response: types.GenerateContentResponse = (
                self._client.models.generate_content(
                    model=self._model_name,
                    contents=[prompt, uploaded_file],
                )
            )
        except errors.ClientError as exc:
            if self._is_model_unavailable_error(exc):
                raise GeminiVisionModelUnavailableError(
                    self._build_model_unavailable_message()
                ) from exc
            raise RuntimeError("Failed to generate content with Gemini.") from exc
        except Exception as exc:
            raise RuntimeError("Failed to generate content with Gemini.") from exc

        text = self._extract_text(response)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")

        return text.strip()

    def _cleanup_file(self, uploaded_file: types.File,) -> None:
        file_name = self._get_file_name(uploaded_file)
        if not file_name:
            return

        try:
            self._client.files.delete(name=file_name)
        except Exception as exc:
            logger.warning("Failed to cleanup uploaded Gemini file: %s", exc)

    def _extract_text(
    self,
    response: types.GenerateContentResponse,
) -> str:
        if not response.text:
            raise RuntimeError("Gemini returned an empty response.")

        return response.text.strip()

    def _normalize_state(self, state: object,) -> str:
        if state is None:
            return "UNKNOWN"

        name = getattr(state, "name", None)
        if isinstance(name, str) and name:
            return name.upper()

        if isinstance(state, str):
            return state.upper()

        return str(state).upper()

    def _get_file_name(self, uploaded_file: types.File) -> str | None:
        file_name = getattr(uploaded_file, "name", None)
        if isinstance(file_name, str) and file_name:
            return file_name
        return None

    def _is_model_unavailable_error(self, exc: errors.ClientError) -> bool:
        """
        Return whether a Gemini client error indicates model unavailability.

        Args:
            exc:
                Client error raised by the Gemini SDK.

        Returns:
            True if the error reflects a missing or retired model.
        """
        status_code = getattr(exc, "code", None)
        if status_code != 404:
            return False

        message = str(exc).lower()
        return (
            "model" in message
            and (
                "no longer available" in message
                or "not found" in message
                or "not available" in message
            )
        )

    def _build_model_unavailable_message(self) -> str:
        """
        Build a safe, actionable message for unavailable Gemini models.

        Returns:
            Human-readable remediation guidance.
        """
        return (
            "Configured Gemini vision model "
            f"'{self._model_name}' is unavailable. "
            "Update GEMINI_VISION_MODEL to a currently supported Gemini model."
        )
