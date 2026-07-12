from pathlib import Path

from backend.infrastructure.llm.gemini_vision_service import GeminiVisionService
from backend.processing.media_processor import MediaProcessor


class VisionService:
    """Business capability for analyzing image and video media."""

    def __init__(
        self,
        media_processor: MediaProcessor | None = None,
        gemini_vision_service: GeminiVisionService | None = None,
    ) -> None:
        self._media_processor = media_processor or MediaProcessor()
        self._gemini_vision_service = (gemini_vision_service or GeminiVisionService())

    def analyze(self, media_path: Path, prompt: str) -> str:
        """
        Analyze an image or video using the configured vision model.

        Args:
            media_path: Path to the media file.
            prompt: User prompt describing the desired analysis.

        Returns:
            The generated text response from the vision model.

        Raises:
            FileNotFoundError:
                If the media file does not exist.

            ValueError:
                If the media file is unsupported or fails validation.

            google.genai.errors.APIError (or provider-specific exceptions):
                Propagated from the infrastructure layer.
        """
        media = self._media_processor.process(media_path)

        return self._gemini_vision_service.generate_content(
            media=media,
            prompt=prompt,
        )