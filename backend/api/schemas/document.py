"""Pydantic schemas for documents."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class DocumentResponse(BaseModel):
    """Schema for document response."""
    id: int
    filename: str
    original_filename: str
    file_type: str
    file_size: int
    chunks_count: Optional[int] = None
    uploaded_at: datetime
    is_ingested: bool
    ingestion_status: str
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


class DocumentListResponse(BaseModel):
    """Schema for listing documents."""
    documents: list[DocumentResponse]
    total: int


class DocumentStatsResponse(BaseModel):
    """Schema for document statistics."""
    total_documents: int
    total_size_mb: float
    total_chunks: int
    by_type: dict[str, int]
