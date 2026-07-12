from dataclasses import dataclass
from pathlib import Path
from typing import Literal

@dataclass(slots=True, frozen=True)
class MediaData:
    file_path: Path
    filename: str
    mime_type: str
    file_size: int
    media_type: Literal["image", "video"]