"""Service for document management."""

from pathlib import Path
import shutil
from datetime import datetime
from typing import Optional
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
import logging

from backend.database import crud
from backend.services.agent_service import get_agent_service

logger = logging.getLogger(__name__)


class DocumentService:
    """Service for document management."""

    def __init__(self):
        """Initialize document service."""
        # Create upload directory
        self.upload_dir = Path(__file__).parent.parent.parent / "data" / "uploads"
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Document upload directory: {self.upload_dir}")

    async def upload_document(self, db: Session, file: UploadFile):
        """
        Upload and ingest a document.

        Args:
            db: Database session
            file: Uploaded file

        Returns:
            Created document record
        """
        # Validate file type
        file_extension = Path(file.filename).suffix.lower().lstrip(".")
        if file_extension not in ["pdf", "txt", "md"]:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_extension}. Supported types: pdf, txt, md"
            )

        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_filename = "".join(c for c in file.filename if c.isalnum() or c in "._- ")
        filename = f"{timestamp}_{safe_filename}"
        file_path = self.upload_dir / filename

        # Save file to disk
        try:
            with file_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            logger.info(f"File saved: {file_path}")
        except Exception as e:
            logger.error(f"Error saving file: {e}")
            raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

        # Get file info
        file_size = file_path.stat().st_size

        # Validate file size (50MB limit)
        max_size = 50 * 1024 * 1024  # 50MB
        if file_size > max_size:
            file_path.unlink()  # Delete the file
            raise HTTPException(
                status_code=400,
                detail=f"File too large: {file_size / (1024*1024):.2f}MB. Max size: 50MB"
            )

        # Create database record
        document = crud.create_document(
            db=db,
            filename=filename,
            original_filename=file.filename,
            file_path=str(file_path),
            file_type=file_extension,
            file_size=file_size,
            ingestion_status="processing"
        )

        # Ingest document in background
        try:
            agent_service = get_agent_service()
            chunks_count = await agent_service.ingest_documents([str(file_path)], recursive=False)

            # Update document status
            crud.update_document(
                db=db,
                document_id=document.id,
                is_ingested=True,
                ingestion_status="completed",
                chunks_count=chunks_count
            )

            logger.info(f"Document ingested successfully: {filename} ({chunks_count} chunks)")

        except Exception as e:
            logger.error(f"Document ingestion failed: {e}")
            crud.update_document(
                db=db,
                document_id=document.id,
                ingestion_status="failed",
                error_message=str(e)
            )
            raise HTTPException(status_code=500, detail=f"Document ingestion failed: {str(e)}")

        # Refresh to get updated data
        db.refresh(document)
        return document

    async def delete_document(self, db: Session, document_id: int) -> bool:
        """
        Delete a document from disk and database.

        Args:
            db: Database session
            document_id: Document ID

        Returns:
            True if successful
        """
        document = crud.get_document(db, document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")

        # Delete file from disk
        file_path = Path(document.file_path)
        if file_path.exists():
            try:
                file_path.unlink()
                logger.info(f"File deleted: {file_path}")
            except Exception as e:
                logger.error(f"Error deleting file: {e}")

        # Delete from database
        success = crud.delete_document(db, document_id)
        if not success:
            raise HTTPException(status_code=404, detail="Document not found in database")

        logger.info(f"Document deleted: {document.filename}")
        return True


# Global document service instance
_document_service: Optional[DocumentService] = None


def get_document_service() -> DocumentService:
    """Get or create the global document service instance."""
    global _document_service
    if _document_service is None:
        _document_service = DocumentService()
    return _document_service
