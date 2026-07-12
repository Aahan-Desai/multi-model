from __future__ import annotations

# Storage

UPLOAD_DIRECTORY = "uploads"

# Tool Names

TOOL_RAG = "rag"
TOOL_VISION = "vision"
TOOL_MATH = "math"
TOOL_WEBSEARCH = "websearch"

# Supported Document Formats

SUPPORTED_DOCUMENT_EXTENSIONS = frozenset(
    {
        ".pdf",
        ".docx",
        ".txt",
        ".md",
    }
)

# Supported Image Formats

SUPPORTED_IMAGE_EXTENSIONS = frozenset(
    {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
    }
)

# Supported Video Formats

SUPPORTED_VIDEO_EXTENSIONS = frozenset(
    {
        ".mp4",
        ".mov",
        ".avi",
        ".mkv",
    }
)