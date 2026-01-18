"""Chat endpoints with SSE streaming."""

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sse_starlette.sse import EventSourceResponse
import logging

from backend.database.database import get_db
from backend.database import crud
from backend.api.schemas.chat import MessageCreate, MessageResponse
from backend.services.streaming_service import get_streaming_service, StreamingService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/sessions/{session_id}/messages", response_model=MessageResponse)
async def send_message(
    session_id: int,
    message_data: MessageCreate,
    db: Session = Depends(get_db)
):
    """
    Send a message (non-streaming fallback).

    Use this endpoint if you want a simple request/response without streaming.
    For streaming, use the /sessions/{session_id}/stream endpoint.
    """
    # Verify session exists
    session = crud.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Save user message
    user_message = crud.create_message(
        db=db,
        session_id=session_id,
        role="user",
        content=message_data.content
    )

    # Get research result (synchronous)
    from backend.services.agent_service import get_agent_service
    agent_service = get_agent_service()

    try:
        result = await agent_service.research_sync(message_data.content)

        # Save assistant message
        assistant_message = crud.create_message(
            db=db,
            session_id=session_id,
            role="assistant",
            content=result.get("answer", ""),
            sources=result.get("sources", []),
            documents_used=result.get("documents_used", 0),
            relevance_score=result.get("relevance_score", 0.0),
            iterations=result.get("iterations", 0)
        )

        return assistant_message

    except Exception as e:
        logger.error(f"Error in send_message: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sessions/{session_id}/stream")
async def stream_chat(
    session_id: int,
    query: str = Query(..., description="The research question"),
    db: Session = Depends(get_db),
    streaming_service: StreamingService = Depends(get_streaming_service)
):
    """
    Stream research response using Server-Sent Events (SSE).

    Events:
    - node_start: Workflow node begins
    - node_complete: Workflow node finishes
    - token: Individual token from LLM
    - synthesis_complete: Final answer ready
    - complete: Message saved to database
    - error: An error occurred
    """
    # Verify session exists
    session = crud.get_session(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    # Save user message
    user_message = crud.create_message(
        db=db,
        session_id=session_id,
        role="user",
        content=query
    )

    logger.info(f"Starting SSE stream for session {session_id}, query: {query}")

    # Create event generator
    async def event_generator():
        try:
            async for event in streaming_service.stream_research(query, session_id, db):
                yield event
        except Exception as e:
            logger.error(f"Streaming error: {e}")
            yield {
                "event": "error",
                "data": f'{{"error": "{str(e)}"}}'
            }

    return EventSourceResponse(event_generator())
