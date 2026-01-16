"""Document retrieval logic."""

from typing import List, Optional, Dict, Any

from langchain_core.documents import Document

from src.config import config
from src.rag.vector_store import VectorStore
from src.utils.logger import logger


class DocumentRetriever:
    """Retrieve relevant documents from vector store."""

    def __init__(
        self,
        vector_store: VectorStore,
        top_k: Optional[int] = None,
        use_mmr: bool = True,
    ):
        """
        Initialize document retriever.

        Args:
            vector_store: Vector store instance
            top_k: Number of documents to retrieve
            use_mmr: Whether to use MMR for diverse results
        """
        self.vector_store = vector_store
        self.top_k = top_k or config.retrieval_top_k
        self.use_mmr = use_mmr

        logger.info(
            f"Initialized retriever with top_k={self.top_k}, use_mmr={self.use_mmr}"
        )

    def retrieve(
        self,
        query: str,
        top_k: Optional[int] = None,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
        """
        Retrieve relevant documents for a query.

        Args:
            query: Query string
            top_k: Number of documents to retrieve
            filter: Optional metadata filter

        Returns:
            List of relevant documents
        """
        k = top_k or self.top_k

        try:
            if self.use_mmr:
                # Use MMR for diverse results
                documents = self.vector_store.max_marginal_relevance_search(
                    query=query,
                    k=k,
                    fetch_k=k * 4,  # Fetch more for diversity
                    lambda_mult=0.5,  # Balance relevance and diversity
                    filter=filter,
                )
            else:
                # Use standard similarity search
                documents = self.vector_store.similarity_search(
                    query=query,
                    k=k,
                    filter=filter,
                )

            logger.info(f"Retrieved {len(documents)} documents for query: {query[:50]}...")
            return documents

        except Exception as e:
            logger.error(f"Error retrieving documents: {e}")
            raise

    def retrieve_with_scores(
        self,
        query: str,
        top_k: Optional[int] = None,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[tuple[Document, float]]:
        """
        Retrieve relevant documents with relevance scores.

        Args:
            query: Query string
            top_k: Number of documents to retrieve
            filter: Optional metadata filter

        Returns:
            List of tuples (document, score)
        """
        k = top_k or self.top_k

        try:
            results = self.vector_store.similarity_search_with_score(
                query=query,
                k=k,
                filter=filter,
            )

            logger.info(f"Retrieved {len(results)} documents with scores")
            return results

        except Exception as e:
            logger.error(f"Error retrieving documents with scores: {e}")
            raise

    def retrieve_relevant(
        self,
        query: str,
        top_k: Optional[int] = None,
        score_threshold: Optional[float] = None,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
        """
        Retrieve only highly relevant documents based on score threshold.

        Args:
            query: Query string
            top_k: Number of documents to retrieve
            score_threshold: Minimum relevance score (lower is more similar)
            filter: Optional metadata filter

        Returns:
            List of relevant documents above threshold
        """
        k = top_k or self.top_k
        threshold = score_threshold if score_threshold is not None else 0.3

        try:
            results = self.retrieve_with_scores(query, top_k=k, filter=filter)

            # Filter by score threshold
            # Note: In Chroma, lower scores mean more similar
            relevant_docs = [
                doc for doc, score in results
                if score <= threshold
            ]

            logger.info(
                f"Retrieved {len(relevant_docs)} relevant documents "
                f"(threshold: {threshold})"
            )
            return relevant_docs

        except Exception as e:
            logger.error(f"Error retrieving relevant documents: {e}")
            raise


def create_retriever(
    vector_store: VectorStore,
    top_k: Optional[int] = None,
    use_mmr: bool = True,
) -> DocumentRetriever:
    """
    Create a document retriever.

    Args:
        vector_store: Vector store instance
        top_k: Number of documents to retrieve
        use_mmr: Whether to use MMR

    Returns:
        DocumentRetriever instance
    """
    return DocumentRetriever(
        vector_store=vector_store,
        top_k=top_k,
        use_mmr=use_mmr,
    )
