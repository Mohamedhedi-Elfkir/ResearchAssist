"""Document management endpoints."""

from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database import crud
from backend.api.schemas.document import DocumentResponse, DocumentListResponse, DocumentStatsResponse
from backend.services.document_service import get_document_service, DocumentService

router = APIRouter()


@router.post("/upload", response_model=DocumentResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    document_service: DocumentService = Depends(get_document_service)
):
    """Upload a document and ingest it into the vector store."""
    return await document_service.upload_document(db, file)


@router.get("", response_model=DocumentListResponse)
async def list_documents(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """List all documents."""
    documents = crud.get_documents(db, skip=skip, limit=limit)
    total = len(documents)  # For simplicity; in production, use a count query
    return DocumentListResponse(documents=documents, total=total)


@router.get("/stats", response_model=DocumentStatsResponse)
async def get_document_stats(db: Session = Depends(get_db)):
    """Get document statistics."""
    stats = crud.get_document_stats(db)
    return DocumentStatsResponse(**stats)


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(document_id: int, db: Session = Depends(get_db)):
    """Get a specific document."""
    document = crud.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/{document_id}")
async def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    document_service: DocumentService = Depends(get_document_service)
):
    """Delete a document."""
    success = await document_service.delete_document(db, document_id)
    return {"success": success, "message": "Document deleted successfully"}
