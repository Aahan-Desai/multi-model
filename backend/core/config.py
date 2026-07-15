from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
   
    # Application
   
    app_name: str
    environment: str
    debug: bool
    log_level: str

    # Groq (Orchestrator + RAG)
    
    groq_api_key: str

    orchestrator_model: str
    rag_model: str
    
    # Google Gemini (Vision)
    
    gemini_api_key: str
    gemini_vision_model: str
    
    # Gemini Vision Processing

    gemini_video_processing_timeout: int = 60
    gemini_video_poll_interval: int = 2
    
    # Ollama (Embeddings)
    ollama_base_url: str
    ollama_embedding_model: str
    
    # Embeddings
    
    embedding_provider: str
    embedding_model: str
    embedding_dimension: int
    
    # Qdrant Vector Database
    
    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection_name: str
    qdrant_distance_metric: str = "COSINE"
    
    # Tavily Web Search
    
    tavily_api_key: str
    
    # Storage
    
    storage_path: Path
    
    # Document Processing
    
    max_upload_size_mb: int
    
         
    supported_document_extensions: set[str] = {
        ".pdf",
        ".docx",
        ".txt",
        ".md",
        ".csv",
        ".xlsx",
        ".pptx",
    }

    supported_image_extensions: set[str] = {
        ".png",
        ".jpg",
        ".jpeg",
        ".webp",
    }

    supported_video_extensions: set[str] = {
        ".mp4",
        ".mov",
        ".avi",
        ".mkv",
    }

    # Chunking
    
    chunk_size: int
    chunk_overlap: int
    
    # Code Execution
    
    python_execution_timeout: int = 10

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",  
    
    )
settings = Settings()