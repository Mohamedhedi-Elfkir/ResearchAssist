"""Configuration management for the research agent."""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from pydantic import BaseModel, Field

# Load environment variables from .env file
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).parent.parent


class Config(BaseModel):
    """Application configuration."""

    # Google Gemini API
    gemini_api_key: str = Field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))

    # Vector Store
    chroma_persist_directory: str = Field(
        default_factory=lambda: os.getenv(
            "CHROMA_PERSIST_DIRECTORY",
            str(BASE_DIR / "data" / "chroma_db")
        )
    )

    # Document Processing
    chunk_size: int = Field(default_factory=lambda: int(os.getenv("CHUNK_SIZE", "1000")))
    chunk_overlap: int = Field(default_factory=lambda: int(os.getenv("CHUNK_OVERLAP", "200")))
    max_file_size_mb: int = Field(default_factory=lambda: int(os.getenv("MAX_FILE_SIZE_MB", "50")))

    # Agent Configuration
    max_iterations: int = Field(default_factory=lambda: int(os.getenv("MAX_ITERATIONS", "3")))
    retrieval_top_k: int = Field(default_factory=lambda: int(os.getenv("RETRIEVAL_TOP_K", "5")))
    relevance_threshold: float = Field(default_factory=lambda: float(os.getenv("RELEVANCE_THRESHOLD", "7.0")))

    # LLM Configuration
    gemini_model: str = Field(default_factory=lambda: os.getenv("GEMINI_MODEL", "gemini-1.5-flash-latest"))
    temperature: float = Field(default_factory=lambda: float(os.getenv("TEMPERATURE", "0.7")))
    max_tokens: int = Field(default_factory=lambda: int(os.getenv("MAX_TOKENS", "8192")))

    # Web Scraping
    user_agent: str = Field(default_factory=lambda: os.getenv("USER_AGENT", "ResearchAgent/1.0"))
    request_timeout: int = Field(default_factory=lambda: int(os.getenv("REQUEST_TIMEOUT", "30")))
    rate_limit_delay: float = Field(default_factory=lambda: float(os.getenv("RATE_LIMIT_DELAY", "1.0")))

    # Logging
    log_level: str = Field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    log_file: str = Field(default_factory=lambda: os.getenv("LOG_FILE", str(BASE_DIR / "logs" / "agent.log")))

    # Data directories
    data_dir: str = Field(default=str(BASE_DIR / "data"))
    documents_dir: str = Field(default=str(BASE_DIR / "data" / "documents"))
    cache_dir: str = Field(default=str(BASE_DIR / "data" / "cache"))

    class Config:
        """Pydantic config."""
        arbitrary_types_allowed = True

    def validate(self) -> bool:
        """Validate configuration."""
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY is required. Please set it in .env file.")
        return True

    def ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        directories = [
            self.chroma_persist_directory,
            self.data_dir,
            self.documents_dir,
            self.cache_dir,
            os.path.dirname(self.log_file),
        ]
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)


# Global configuration instance
config = Config()
