"""FastAPI application entry point."""

import sys
from pathlib import Path

# Add parent directory to path to import from src
sys.path.insert(0, str(Path(__file__).parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from backend.api.routes import health, documents, sessions, chat
from backend.database.database import init_db
from backend.middleware.error_handler import add_error_handlers

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown."""
    # Startup
    logger.info("Starting Research Agent API...")
    init_db()
    logger.info("API server ready")
    yield
    # Shutdown
    logger.info("Shutting down Research Agent API...")


app = FastAPI(
    title="Research Agent API",
    description="API for NotebookLM-like Research Agent with RAG and LangGraph",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - Allow frontend to access API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:5174",  # Vite dev server (alt port)
        "http://localhost:5175",  # Vite dev server (alt port)
        "http://localhost:5176",  # Vite dev server (alt port)
        "http://localhost:3000",  # Alternative React dev server
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175",
        "http://127.0.0.1:5176",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add error handlers
add_error_handlers(app)

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(documents.router, prefix="/api/v1/documents", tags=["documents"])
app.include_router(sessions.router, prefix="/api/v1/chat", tags=["sessions"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Research Agent API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
