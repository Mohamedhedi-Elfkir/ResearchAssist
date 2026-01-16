"""LangGraph state definitions."""

from typing import List, TypedDict, Annotated, Sequence
import operator

from langchain_core.messages import BaseMessage
from langchain_core.documents import Document


class AgentState(TypedDict):
    """State for the research agent workflow."""

    # Messages in the conversation
    messages: Annotated[Sequence[BaseMessage], operator.add]

    # User's research query
    query: str

    # Research plan (sub-questions)
    research_plan: List[str]

    # Retrieved documents from vector store
    retrieved_documents: List[Document]

    # Web scraping results
    web_results: List[Document]

    # All documents combined
    all_documents: List[Document]

    # Final synthesized answer
    synthesis: str

    # Iteration counter
    iteration_count: int

    # Sources used for the answer
    sources: List[str]

    # Next action to take
    next_action: str  # "rag", "web", "both", "synthesize", "end"

    # Relevance score (0-10)
    relevance_score: float
