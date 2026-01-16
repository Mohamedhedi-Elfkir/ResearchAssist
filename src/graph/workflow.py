"""LangGraph workflow construction."""

from typing import Dict, Any, Literal

from langgraph.graph import StateGraph, END

from src.graph.state import AgentState
from src.graph.nodes import (
    query_analysis_node,
    research_planning_node,
    rag_retrieval_node,
    web_scraping_node,
    relevance_check_node,
    synthesis_node,
    initialize_nodes,
)
from src.llm.gemini_client import GeminiClient
from src.rag.vector_store import VectorStore
from src.rag.retriever import DocumentRetriever
from src.loaders.web_scraper import WebScraper
from src.utils.logger import logger


def route_after_analysis(state: AgentState) -> Literal["rag_retrieval", "web_scraping", "research_planning"]:
    """
    Route based on query analysis.

    Args:
        state: Current state

    Returns:
        Next node name
    """
    next_action = state.get("next_action", "rag")

    if next_action == "rag":
        return "rag_retrieval"
    elif next_action == "web":
        return "web_scraping"
    else:  # "both"
        return "research_planning"


def route_after_relevance_check(state: AgentState) -> Literal["synthesis", "web_scraping"]:
    """
    Route based on relevance check.

    Args:
        state: Current state

    Returns:
        Next node name
    """
    next_action = state.get("next_action", "synthesize")

    if next_action == "synthesize":
        return "synthesis"
    else:
        return "web_scraping"


def create_workflow(
    llm_client: GeminiClient,
    vector_store: VectorStore,
    retriever: DocumentRetriever,
    web_scraper: WebScraper,
):
    """
    Create the research agent workflow.

    Args:
        llm_client: LLM client instance
        vector_store: Vector store instance
        retriever: Document retriever instance
        web_scraper: Web scraper instance

    Returns:
        Compiled workflow
    """
    logger.info("Creating research agent workflow")

    # Initialize nodes with dependencies
    initialize_nodes(llm_client, vector_store, retriever, web_scraper)

    # Create state graph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("query_analysis", query_analysis_node)
    workflow.add_node("research_planning", research_planning_node)
    workflow.add_node("rag_retrieval", rag_retrieval_node)
    workflow.add_node("web_scraping", web_scraping_node)
    workflow.add_node("relevance_check", relevance_check_node)
    workflow.add_node("synthesis", synthesis_node)

    # Set entry point
    workflow.set_entry_point("query_analysis")

    # Add conditional edges
    workflow.add_conditional_edges(
        "query_analysis",
        route_after_analysis,
        {
            "rag_retrieval": "rag_retrieval",
            "web_scraping": "web_scraping",
            "research_planning": "research_planning",
        }
    )

    # After research planning, go to RAG retrieval
    workflow.add_edge("research_planning", "rag_retrieval")

    # After RAG retrieval, check relevance
    workflow.add_edge("rag_retrieval", "relevance_check")

    # After web scraping, go directly to synthesis (since web scraping is a placeholder)
    # In production, this should go to relevance_check
    workflow.add_edge("web_scraping", "synthesis")

    # After relevance check, route to synthesis or web scraping
    workflow.add_conditional_edges(
        "relevance_check",
        route_after_relevance_check,
        {
            "synthesis": "synthesis",
            "web_scraping": "web_scraping",
        }
    )

    # Synthesis is the end
    workflow.add_edge("synthesis", END)

    # Compile the workflow
    compiled_workflow = workflow.compile()

    logger.info("Workflow created successfully")

    return compiled_workflow


class ResearchWorkflow:
    """Research agent workflow wrapper."""

    def __init__(
        self,
        vector_store: VectorStore,
    ):
        """
        Initialize research workflow.

        Args:
            vector_store: Vector store instance
        """
        self.vector_store = vector_store

        # Initialize components
        self.llm_client = GeminiClient()
        self.retriever = DocumentRetriever(vector_store)
        self.web_scraper = WebScraper()

        # Create workflow
        self.workflow = create_workflow(
            self.llm_client,
            self.vector_store,
            self.retriever,
            self.web_scraper,
        )

    def run(self, query: str) -> Dict[str, Any]:
        """
        Run the research workflow.

        Args:
            query: Research query

        Returns:
            Research results
        """
        logger.info(f"Running workflow for query: {query}")

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

        # Run workflow
        result = self.workflow.invoke(initial_state)

        # Extract results
        output = {
            "query": query,
            "answer": result.get("synthesis", "No answer generated."),
            "sources": result.get("sources", []),
            "documents_used": len(result.get("all_documents", [])),
            "relevance_score": result.get("relevance_score", 0.0),
            "iterations": result.get("iteration_count", 0),
        }

        logger.info("Workflow completed successfully")

        return output
