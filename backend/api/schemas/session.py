"""Pydantic schemas for sessions."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class SessionCreate(BaseModel):
    """Schema for creating a session."""
    title: Optional[str] = Field(default="New Research Session", max_length=255)


class SessionUpdate(BaseModel):
    """Schema for updating a session."""
    title: Optional[str] = Field(default=None, max_length=255)
    is_archived: Optional[bool] = None


class SessionResponse(BaseModel):
    """Schema for session response."""
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    is_archived: bool
    message_count: int = 0

    class Config:
        from_attributes = True


class SessionListResponse(BaseModel):
    """Schema for listing sessions."""
    sessions: list[SessionResponse]
    total: int
