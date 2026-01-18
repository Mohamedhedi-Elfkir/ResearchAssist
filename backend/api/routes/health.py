"""Health check endpoints."""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from pathlib import Path
import sys

from backend.database.database import get_db
from src.config import config

router = APIRouter()


@router.get("/health")
async def health_check():
    """Basic health check."""
    return {
        "status": "healthy",
        "service": "Research Agent API",
        "version": "1.0.0"
    }


@router.get("/health/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """Detailed health check with system status."""
    try:
        # Check database connection
        db.execute("SELECT 1")
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"

    # Check if vector store directory exists
    vector_store_path = Path(config.chroma_persist_directory)
    vector_store_status = "exists" if vector_store_path.exists() else "not found"

    # Check if documents directory exists
    documents_path = Path(config.documents_dir)
    documents_status = "exists" if documents_path.exists() else "not found"

    return {
        "status": "healthy",
        "service": "Research Agent API",
        "version": "1.0.0",
        "database": {
            "status": db_status,
            "path": str(Path(__file__).parent.parent.parent.parent / "data" / "research_agent.db")
        },
        "vector_store": {
            "status": vector_store_status,
            "path": str(vector_store_path)
        },
        "documents_directory": {
            "status": documents_status,
            "path": str(documents_path)
        },
        "python_version": sys.version,
        "gemini_api_key_configured": bool(config.gemini_api_key)
    }
