from openai import OpenAI
from google import genai
from qdrant_client import QdrantClient
from tavily import TavilyClient

from backend.core.config import settings


_GROQ_BASE_URL = "https://api.groq.com/openai/v1"


_groq_client: OpenAI | None = None
_gemini_client: genai.Client | None = None
_qdrant_client: QdrantClient | None = None
_tavily_client: TavilyClient | None = None


def get_groq_client() -> OpenAI:
    """
    Returns a singleton Groq client using the OpenAI-compatible SDK.
    """
    global _groq_client

    if _groq_client is None:
        _groq_client = OpenAI(
            api_key=settings.groq_api_key,
            base_url=_GROQ_BASE_URL,
        )

    return _groq_client


def get_gemini_client() -> genai.Client:
    """
    Returns a singleton Google Gemini client.
    """
    global _gemini_client

    if _gemini_client is None:
        _gemini_client = genai.Client(
            api_key=settings.gemini_api_key,
        )

    return _gemini_client


def get_qdrant_client() -> QdrantClient:
    """
    Returns a singleton Qdrant client.
    """
    global _qdrant_client

    if _qdrant_client is None:
        _qdrant_client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            check_compatibility=False,
        )

    return _qdrant_client


def get_tavily_client() -> TavilyClient:
    """
    Returns a singleton Tavily client.
    """
    global _tavily_client

    if _tavily_client is None:
        _tavily_client = TavilyClient(
            api_key=settings.tavily_api_key,
        )

    return _tavily_client