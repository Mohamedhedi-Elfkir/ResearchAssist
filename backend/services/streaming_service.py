"""Service for streaming research responses using SSE."""

from typing import AsyncGenerator, Dict, Any
import json
import logging
from sqlalchemy.orm import Session

from backend.services.agent_service import get_agent_service
from backend.database import crud

logger = logging.getLogger(__name__)


class StreamingService:
    """Service for streaming research responses."""

    def __init__(self):
        """Initialize streaming service."""
        self.agent_service = get_agent_service()

    async def stream_research(
        self,
        query: str,
        session_id: int,
        db: Session
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream research results using LangGraph's astream_events.

        Args:
            query: Research question
            session_id: Session ID
            db: Database session

        Yields:
            SSE-formatted events
        """
        try:
            # Get workflow
            workflow_wrapper = self.agent_service.get_workflow()
            workflow = workflow_wrapper.workflow

            # Initialize state
            initial_state = {
                "query": query,
                "messages": [],
                "research_plan": [],
                "retrieved_documents": [],
                "web_results": [],
                "all_documents": [],
                "synthesis": "",
                "iteration_count": 0,
                "sources": [],
                "next_action": "",
                "relevance_score": 0.0,
            }

            # Track state for final message
            final_state = {}
            current_synthesis = ""
            current_node = ""

            logger.info(f"Starting streaming research for query: {query}")

            # Stream events from workflow
            async for event in workflow.astream_events(initial_state, version="v1"):
                event_type = event.get("event")
                event_name = event.get("name", "")

                # Node lifecycle events
                if event_type == "on_chain_start":
                    if event_name in ["query_analysis", "research_planning", "rag_retrieval",
                                     "web_scraping", "relevance_check", "synthesis"]:
                        current_node = event_name
                        yield {
                            "event": "node_start",
                            "data": json.dumps({"node": event_name})
                        }

                elif event_type == "on_chain_end":
                    if event_name in ["query_analysis", "research_planning", "rag_retrieval",
                                     "web_scraping", "relevance_check", "synthesis"]:
                        # Extract output data
                        output = event.get("data", {}).get("output", {})

                        if event_name == "synthesis":
                            # Synthesis complete, extract final state
                            final_state = output
                            current_synthesis = output.get("synthesis", "")

                            yield {
                                "event": "synthesis_complete",
                                "data": json.dumps({
                                    "content": current_synthesis,
                                    "sources": output.get("sources", []),
                                    "documents_used": len(output.get("all_documents", [])),
                                    "relevance_score": output.get("relevance_score", 0.0),
                                    "iterations": output.get("iteration_count", 0)
                                })
                            }

                        yield {
                            "event": "node_complete",
                            "data": json.dumps({"node": event_name})
                        }

                # LLM streaming tokens (if available)
                elif event_type == "on_chat_model_stream":
                    chunk_data = event.get("data", {}).get("chunk", {})
                    if hasattr(chunk_data, "content") and chunk_data.content:
                        current_synthesis += chunk_data.content
                        yield {
                            "event": "token",
                            "data": json.dumps({
                                "token": chunk_data.content,
                                "partial_response": current_synthesis
                            })
                        }

            # If we don't have a synthesis yet (workflow didn't complete properly),
            # use synchronous fallback
            if not current_synthesis:
                logger.warning("Streaming didn't produce synthesis, falling back to sync")
                result = await self.agent_service.research_sync(query)
                current_synthesis = result.get("answer", "")
                final_state = result

            # Save message to database
            message = crud.create_message(
                db=db,
                session_id=session_id,
                role="assistant",
                content=current_synthesis,
                sources=final_state.get("sources", []),
                documents_used=final_state.get("documents_used", 0),
                relevance_score=final_state.get("relevance_score", 0.0),
                iterations=final_state.get("iterations", 0)
            )

            logger.info(f"Message saved: {message.id}")

            yield {
                "event": "complete",
                "data": json.dumps({"message_id": message.id})
            }

        except Exception as e:
            logger.error(f"Error in streaming research: {e}", exc_info=True)
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)})
            }

    async def stream_research_sync_fallback(
        self,
        query: str,
        session_id: int,
        db: Session
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Fallback to synchronous research with simulated streaming.

        This is used if async streaming fails or is not available.
        """
        try:
            logger.info(f"Using sync fallback for query: {query}")

            # Notify start
            yield {
                "event": "node_start",
                "data": json.dumps({"node": "research"})
            }

            # Perform synchronous research
            result = await self.agent_service.research_sync(query)

            # Simulate token streaming
            answer = result.get("answer", "")
            chunk_size = 20  # Characters per chunk

            for i in range(0, len(answer), chunk_size):
                chunk = answer[i:i + chunk_size]
                yield {
                    "event": "token",
                    "data": json.dumps({
                        "token": chunk,
                        "partial_response": answer[:i + chunk_size]
                    })
                }

            # Send completion
            yield {
                "event": "synthesis_complete",
                "data": json.dumps({
                    "content": answer,
                    "sources": result.get("sources", []),
                    "documents_used": result.get("documents_used", 0),
                    "relevance_score": result.get("relevance_score", 0.0),
                    "iterations": result.get("iterations", 0)
                })
            }

            # Save message
            message = crud.create_message(
                db=db,
                session_id=session_id,
                role="assistant",
                content=answer,
                sources=result.get("sources", []),
                documents_used=result.get("documents_used", 0),
                relevance_score=result.get("relevance_score", 0.0),
                iterations=result.get("iterations", 0)
            )

            yield {
                "event": "complete",
                "data": json.dumps({"message_id": message.id})
            }

        except Exception as e:
            logger.error(f"Error in sync fallback: {e}", exc_info=True)
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)})
            }


# Global streaming service instance
_streaming_service = None


def get_streaming_service() -> StreamingService:
    """Get or create the global streaming service instance."""
    global _streaming_service
    if _streaming_service is None:
        _streaming_service = StreamingService()
    return _streaming_service
