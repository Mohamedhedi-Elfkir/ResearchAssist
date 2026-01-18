"""Service wrapping the existing ResearchAgent."""

import sys
from pathlib import Path
from typing import Dict, Any, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from main import ResearchAgent
from backend.database import crud
from sqlalchemy.orm import Session

import logging

logger = logging.getLogger(__name__)


class AgentService:
    """Service wrapping the existing ResearchAgent."""

    def __init__(self):
        """Initialize the agent service."""
        try:
            self.agent = ResearchAgent()
            logger.info("ResearchAgent initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize ResearchAgent: {e}")
            raise

    async def research_sync(self, query: str) -> Dict[str, Any]:
        """
        Perform synchronous research (non-streaming).

        Args:
            query: Research question

        Returns:
            Research results dictionary
        """
        try:
            result = self.agent.research(query)
            return result
        except Exception as e:
            logger.error(f"Research error: {e}")
            raise

    async def ingest_documents(self, paths: list[str], recursive: bool = True) -> int:
        """
        Ingest documents into the vector store.

        Args:
            paths: List of file or directory paths
            recursive: Whether to search directories recursively

        Returns:
            Number of chunks ingested
        """
        try:
            count = self.agent.ingest_documents(paths, recursive=recursive)
            logger.info(f"Ingested {count} document chunks from {len(paths)} path(s)")
            return count
        except Exception as e:
            logger.error(f"Document ingestion error: {e}")
            raise

    async def save_message(
        self,
        db: Session,
        session_id: int,
        role: str,
        content: str,
        sources: Optional[list[str]] = None,
        documents_used: Optional[int] = None,
        relevance_score: Optional[float] = None,
        iterations: Optional[int] = None
    ):
        """
        Save a message to the database.

        Args:
            db: Database session
            session_id: Session ID
            role: Message role ("user" or "assistant")
            content: Message content
            sources: List of source file paths
            documents_used: Number of documents used
            relevance_score: Relevance score (0-10)
            iterations: Number of workflow iterations

        Returns:
            Created message
        """
        try:
            message = crud.create_message(
                db=db,
                session_id=session_id,
                role=role,
                content=content,
                sources=sources,
                documents_used=documents_used,
                relevance_score=relevance_score,
                iterations=iterations
            )
            return message
        except Exception as e:
            logger.error(f"Error saving message: {e}")
            raise

    def get_workflow(self):
        """Get the workflow instance for streaming."""
        return self.agent.workflow


# Global agent service instance
_agent_service: Optional[AgentService] = None


def get_agent_service() -> AgentService:
    """
    Get or create the global agent service instance.

    This is a dependency for FastAPI routes.
    """
    global _agent_service
    if _agent_service is None:
        _agent_service = AgentService()
    return _agent_service
