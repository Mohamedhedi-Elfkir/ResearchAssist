"""Pydantic schemas for chat/messages."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class MessageCreate(BaseModel):
    """Schema for creating a message."""
    content: str = Field(..., min_length=1, max_length=10000)
    stream: bool = Field(default=True, description="Whether to stream response")


class MessageResponse(BaseModel):
    """Schema for message response."""
    id: int
    session_id: int
    role: str
    content: str
    created_at: datetime
    sources: Optional[list[str]] = None
    documents_used: Optional[int] = None
    relevance_score: Optional[float] = None
    iterations: Optional[int] = None

    class Config:
        from_attributes = True


class SessionDetailResponse(BaseModel):
    """Schema for session with messages."""
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    is_archived: bool
    messages: list[MessageResponse]

    class Config:
        from_attributes = True
