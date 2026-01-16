"""LangGraph workflow nodes."""

import re
from typing import Dict, Any

from langchain_core.messages import HumanMessage, AIMessage

from src.graph.state import AgentState
from src.llm.gemini_client import GeminiClient
from src.llm.prompts import (
    QUERY_ANALYSIS_PROMPT,
    RELEVANCE_CHECK_PROMPT,
    SYNTHESIS_PROMPT,
    RESEARCH_PLANNING_PROMPT,
    format_documents_for_prompt,
)
from src.rag.vector_store import VectorStore
from src.rag.retriever import DocumentRetriever
from src.loaders.web_scraper import WebScraper
from src.config import config
from src.utils.logger import logger


# Global instances (initialized by workflow)
_llm_client = None
_vector_store = None
_retriever = None
_web_scraper = None


def initialize_nodes(
    llm_client: GeminiClient,
    vector_store: VectorStore,
    retriever: DocumentRetriever,
    web_scraper: WebScraper,
):
    """Initialize global instances for nodes."""
    global _llm_client, _vector_store, _retriever, _web_scraper
    _llm_client = llm_client
    _vector_store = vector_store
    _retriever = retriever
    _web_scraper = web_scraper


def query_analysis_node(state: AgentState) -> Dict[str, Any]:
    """
    Analyze the query and determine research strategy.

    Args:
        state: Current agent state

    Returns:
        Updated state
    """
    logger.info("Running query analysis node")

    query = state["query"]

    # Generate analysis prompt
    prompt = QUERY_ANALYSIS_PROMPT.format(query=query)

    # Get LLM response
    response = _llm_client.generate(prompt)

    # Parse response
    local_search = "yes" in response.lower().split("local_search:")[1].split("\n")[0].lower()
    web_search = "yes" in response.lower().split("web_search:")[1].split("\n")[0].lower()

    # Extract sub-questions
    sub_questions = []
    if "sub_questions:" in response.lower():
        sub_q_section = response.split("SUB_QUESTIONS:")[1] if "SUB_QUESTIONS:" in response else ""
        sub_questions = [
            line.strip("- ").strip()
            for line in sub_q_section.split("\n")
            if line.strip().startswith("-")
        ]

    # Determine next action
    if local_search and web_search:
        next_action = "both"
    elif local_search:
        next_action = "rag"
    elif web_search:
        next_action = "web"
    else:
        next_action = "rag"  # Default to RAG

    logger.info(f"Analysis: local={local_search}, web={web_search}, next={next_action}")

    return {
        "research_plan": sub_questions or [query],
        "next_action": next_action,
        "messages": [HumanMessage(content=query)],
    }


def research_planning_node(state: AgentState) -> Dict[str, Any]:
    """
    Create a detailed research plan.

    Args:
        state: Current agent state

    Returns:
        Updated state
    """
    logger.info("Running research planning node")

    query = state["query"]

    # Generate planning prompt
    prompt = RESEARCH_PLANNING_PROMPT.format(query=query)

    # Get LLM response
    response = _llm_client.generate(prompt)

    # Parse sub-questions
    sub_questions = []
    if "sub_questions:" in response.lower():
        sub_q_section = response.split("SUB_QUESTIONS:")[1] if "SUB_QUESTIONS:" in response else ""
        sub_questions = [
            line.strip("- ").strip()
            for line in sub_q_section.split("\n")
            if line.strip().startswith("-")
        ]

    return {
        "research_plan": sub_questions or [query],
    }


def rag_retrieval_node(state: AgentState) -> Dict[str, Any]:
    """
    Retrieve documents from vector store.

    Args:
        state: Current agent state

    Returns:
        Updated state
    """
    logger.info("Running RAG retrieval node")

    query = state["query"]
    research_plan = state.get("research_plan", [query])

    all_retrieved_docs = []

    # Retrieve for main query
    docs = _retriever.retrieve(query, top_k=config.retrieval_top_k)
    all_retrieved_docs.extend(docs)

    # Retrieve for sub-questions
    for sub_q in research_plan:
        if sub_q.lower() != query.lower():
            docs = _retriever.retrieve(sub_q, top_k=3)
            all_retrieved_docs.extend(docs)

    # Deduplicate
    seen = set()
    unique_docs = []
    for doc in all_retrieved_docs:
        doc_hash = hash(doc.page_content)
        if doc_hash not in seen:
            seen.add(doc_hash)
            unique_docs.append(doc)

    logger.info(f"Retrieved {len(unique_docs)} unique documents")

    return {
        "retrieved_documents": unique_docs,
        "all_documents": unique_docs,
    }


def web_scraping_node(state: AgentState) -> Dict[str, Any]:
    """
    Scrape web content.

    Args:
        state: Current agent state

    Returns:
        Updated state
    """
    logger.info("Running web scraping node")

    # Placeholder: In production, integrate with search API
    # For now, return empty results and force synthesis
    logger.warning("Web scraping is a placeholder. Integrate with search API for production.")
    logger.warning("Skipping web search and moving to synthesis with available documents.")

    web_results = []

    # Combine with existing documents
    all_docs = state.get("retrieved_documents", []) + web_results

    # Since we can't actually web scrape, force synthesis to prevent infinite loop
    return {
        "web_results": web_results,
        "all_documents": all_docs,
        "next_action": "synthesize",  # Force synthesis to prevent infinite loop
    }


def relevance_check_node(state: AgentState) -> Dict[str, Any]:
    """
    Check if retrieved documents are sufficient.

    Args:
        state: Current agent state

    Returns:
        Updated state
    """
    logger.info("Running relevance check node")

    query = state["query"]
    documents = state.get("all_documents", [])

    if not documents:
        logger.warning("No documents available for relevance check")
        return {
            "relevance_score": 0.0,
            "next_action": "web" if state.get("iteration_count", 0) < config.max_iterations else "synthesize",
        }

    # Format documents for prompt
    docs_text = format_documents_for_prompt(documents[:5])  # Limit to top 5

    # Generate relevance check prompt
    prompt = RELEVANCE_CHECK_PROMPT.format(query=query, documents=docs_text)

    # Get LLM response
    response = _llm_client.generate(prompt)

    # Parse relevance score
    relevance_score = 5.0  # Default
    if "relevance_score:" in response.lower():
        try:
            score_text = response.lower().split("relevance_score:")[1].split("\n")[0].strip()
            relevance_score = float(re.findall(r'\d+\.?\d*', score_text)[0])
        except:
            pass

    logger.info(f"Relevance score: {relevance_score}")

    # Determine next action based on score and iterations
    iteration_count = state.get("iteration_count", 0)

    # Increment iteration count first
    new_iteration_count = iteration_count + 1

    logger.info(f"Iteration count: {new_iteration_count}/{config.max_iterations}")

    if relevance_score >= config.relevance_threshold:
        next_action = "synthesize"
        logger.info("Documents are sufficient, moving to synthesis")
    elif new_iteration_count >= config.max_iterations:
        next_action = "synthesize"
        logger.info(f"Max iterations reached ({config.max_iterations}), forcing synthesis")
    else:
        next_action = "web"  # Try web search if RAG insufficient
        logger.info("Documents insufficient, trying web search")

    return {
        "relevance_score": relevance_score,
        "next_action": next_action,
        "iteration_count": new_iteration_count,
    }


def synthesis_node(state: AgentState) -> Dict[str, Any]:
    """
    Synthesize final answer from retrieved documents.

    Args:
        state: Current agent state

    Returns:
        Updated state
    """
    logger.info("Running synthesis node")

    query = state["query"]
    documents = state.get("all_documents", [])

    if not documents:
        synthesis = "I apologize, but I couldn't find relevant information to answer your query. Please try rephrasing your question or adding documents to the knowledge base."
        sources = []
    else:
        # Format documents for prompt
        docs_text = format_documents_for_prompt(documents)

        # Generate synthesis prompt
        prompt = SYNTHESIS_PROMPT.format(query=query, documents=docs_text)

        # Get LLM response
        synthesis = _llm_client.generate(prompt)

        # Extract sources
        sources = list(set([
            doc.metadata.get("source", "Unknown")
            for doc in documents
        ]))

    logger.info("Synthesis complete")

    return {
        "synthesis": synthesis,
        "sources": sources,
        "next_action": "end",
        "messages": [AIMessage(content=synthesis)],
    }
