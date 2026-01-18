"""Session management endpoints."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.database.database import get_db
from backend.database import crud
from backend.api.schemas.session import (
    SessionCreate,
    SessionUpdate,
    SessionResponse,
    SessionListResponse
)
from backend.api.schemas.chat import SessionDetailResponse

router = APIRouter()


@router.post("/sessions", response_model=SessionResponse)
async def create_session(
    session_data: SessionCreate,
    db: Session = Depends(get_db)
):
    """Create a new chat session."""
    session = crud.create_session(db, title=session_data.title)

    # Add message count
    response = SessionResponse.from_orm(session)
    response.message_count = 0
    return response


@router.get("/sessions", response_model=SessionListResponse)
async def list_sessions(
    skip: int = 0,
    limit: int = 100,
    include_archived: bool = False,
    db: Session = Depends(get_db)
):
    """List all sessions."""
    sessions = crud.get_sessions(db, skip=skip, limit=limit, include_archived=include_archived)

    # Add message counts
    session_responses = []
    for session in sessions:
        response = SessionResponse.from_orm(session)
        response.message_count = len(session.messages)
        session_responses.append(response)

    return SessionListResponse(sessions=session_responses, total=len(sessions))


@router.get("/sessions/{session_id}", response_model=SessionDetailResponse)
async def get_session(session_id: int, db: Session = Depends(get_db)):
    """Get a session with all its messages."""
    session = crud.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    messages = crud.get_messages(db, session_id)

    return SessionDetailResponse(
        id=session.id,
        title=session.title,
        created_at=session.created_at,
        updated_at=session.updated_at,
        is_archived=session.is_archived,
        messages=messages
    )


@router.patch("/sessions/{session_id}", response_model=SessionResponse)
async def update_session(
    session_id: int,
    session_data: SessionUpdate,
    db: Session = Depends(get_db)
):
    """Update a session."""
    session = crud.update_session(
        db,
        session_id,
        title=session_data.title,
        is_archived=session_data.is_archived
    )
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    response = SessionResponse.from_orm(session)
    response.message_count = len(session.messages)
    return response


@router.delete("/sessions/{session_id}")
async def delete_session(session_id: int, db: Session = Depends(get_db)):
    """Delete a session and all its messages."""
    success = crud.delete_session(db, session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")

    return {"success": True, "message": "Session deleted successfully"}
