from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routers.chat import router as chat_router
from backend.api.routers.health import router as health_router
from backend.api.routers.upload import router as upload_router
from backend.api.routers.vision import router as vision_router

from backend.core.config import settings

from backend.infrastructure.llm.chat_service import ChatService
from backend.infrastructure.llm.embedding_service import EmbeddingService
from backend.infrastructure.llm.gemini_vision_service import GeminiVisionService
from backend.infrastructure.vision import VisionService as ApiVisionService
from backend.infrastructure.vector_db.qdrant_service import QdrantService
from backend.infrastructure.websearch.tavily_service import TavilyService
from backend.infrastructure.execution.python_executor import PythonExecutor
from backend.infrastructure.storage.storage_service import StorageService
from backend.infrastructure.document_processing.document_processor import DocumentProcessor
from backend.infrastructure.vector_db.collection_manager import CollectionManager
from backend.infrastructure.ingestion import IngestionService

from backend.processing.chunking_service import ChunkingService
from backend.processing.media_processor import MediaProcessor

from backend.specialists.rag_service import RAGService
from backend.specialists.vision_service import VisionService as SpecialistVisionService
from backend.specialists.websearch_service import WebSearchService
from backend.specialists.math_service import MathService

from backend.orchestrator.tool_executor import ToolExecutor
from backend.orchestrator.router import Router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Create all application services once and store them on app.state.
    """

    # Infrastructure

    chat_service = ChatService()
    embedding_service = EmbeddingService()
    gemini_vision_service = GeminiVisionService()
    qdrant_service = QdrantService()
    tavily_service = TavilyService()
    python_executor = PythonExecutor()

    storage_service = StorageService()
    document_processor = DocumentProcessor()
    collection_manager = CollectionManager()

    # Processing

    chunking_service = ChunkingService()
    media_processor = MediaProcessor()

    # Specialists

    rag_service = RAGService(
        chat_service=chat_service,
        embedding_service=embedding_service,
        qdrant_service=qdrant_service,
    )

    vision_service = SpecialistVisionService(
        media_processor=media_processor,
        gemini_vision_service=gemini_vision_service,
    )

    api_vision_service = ApiVisionService(
        storage_service=storage_service,
        gemini_vision_service=gemini_vision_service,
    )

    web_search_service = WebSearchService(
        chat_service=chat_service,
        tavily_service=tavily_service,
    )

    math_service = MathService(
        chat_service=chat_service,
        python_executor=python_executor,
    )

    ingestion_service = IngestionService(
        storage_service=storage_service,
        document_processor=document_processor,
        chunking_service=chunking_service,
        embedding_service=embedding_service,
        collection_manager=collection_manager,
        qdrant_service=qdrant_service,
    )

    tool_executor = ToolExecutor(
        rag_service=rag_service,
        vision_service=vision_service,
        web_search_service=web_search_service,
        math_service=math_service,
    )

    router = Router(
        chat_service=chat_service,
        tool_executor=tool_executor,
    )

    app.state.router = router
    app.state.ingestion_service = ingestion_service
    app.state.vision_service = api_vision_service

    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(chat_router)
app.include_router(upload_router)
app.include_router(vision_router)
