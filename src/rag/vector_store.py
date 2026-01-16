"""Chroma vector store implementation."""

from typing import List, Optional, Dict, Any
from pathlib import Path

from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

from src.config import config
from src.rag.embeddings import get_embeddings_model
from src.utils.logger import logger


class VectorStore:
    """Chroma vector store for document embeddings."""

    def __init__(
        self,
        collection_name: str = "research_agent",
        persist_directory: Optional[str] = None,
    ):
        """
        Initialize vector store.

        Args:
            collection_name: Name of the collection
            persist_directory: Directory to persist the vector store
        """
        self.collection_name = collection_name
        self.persist_directory = persist_directory or config.chroma_persist_directory

        # Ensure directory exists
        Path(self.persist_directory).mkdir(parents=True, exist_ok=True)

        # Get embeddings model
        self.embeddings = get_embeddings_model()

        # Initialize Chroma
        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory,
        )

        logger.info(
            f"Initialized Chroma vector store: {self.collection_name} "
            f"at {self.persist_directory}"
        )

    def add_documents(
        self,
        documents: List[Document],
        ids: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Add documents to vector store.

        Args:
            documents: List of documents to add
            ids: Optional list of IDs for documents

        Returns:
            List of document IDs
        """
        if not documents:
            logger.warning("No documents to add")
            return []

        try:
            doc_ids = self.vector_store.add_documents(documents, ids=ids)
            logger.info(f"Added {len(documents)} documents to vector store")
            return doc_ids
        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            raise

    def similarity_search(
        self,
        query: str,
        k: int = 5,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
        """
        Search for similar documents.

        Args:
            query: Query string
            k: Number of results to return
            filter: Optional metadata filter

        Returns:
            List of similar documents
        """
        try:
            results = self.vector_store.similarity_search(
                query,
                k=k,
                filter=filter,
            )
            logger.info(f"Found {len(results)} similar documents for query")
            return results
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            raise

    def similarity_search_with_score(
        self,
        query: str,
        k: int = 5,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[tuple[Document, float]]:
        """
        Search for similar documents with relevance scores.

        Args:
            query: Query string
            k: Number of results to return
            filter: Optional metadata filter

        Returns:
            List of tuples (document, score)
        """
        try:
            results = self.vector_store.similarity_search_with_score(
                query,
                k=k,
                filter=filter,
            )
            logger.info(f"Found {len(results)} similar documents with scores")
            return results
        except Exception as e:
            logger.error(f"Error in similarity search with score: {e}")
            raise

    def max_marginal_relevance_search(
        self,
        query: str,
        k: int = 5,
        fetch_k: int = 20,
        lambda_mult: float = 0.5,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Document]:
        """
        Search using Maximal Marginal Relevance (MMR).

        MMR balances relevance and diversity in results.

        Args:
            query: Query string
            k: Number of results to return
            fetch_k: Number of documents to fetch for MMR
            lambda_mult: Diversity parameter (0=max diversity, 1=max relevance)
            filter: Optional metadata filter

        Returns:
            List of documents
        """
        try:
            results = self.vector_store.max_marginal_relevance_search(
                query,
                k=k,
                fetch_k=fetch_k,
                lambda_mult=lambda_mult,
                filter=filter,
            )
            logger.info(f"Found {len(results)} documents using MMR")
            return results
        except Exception as e:
            logger.error(f"Error in MMR search: {e}")
            raise

    def delete_collection(self) -> None:
        """Delete the entire collection."""
        try:
            self.vector_store.delete_collection()
            logger.info(f"Deleted collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error deleting collection: {e}")
            raise

    def get_collection_size(self) -> int:
        """
        Get the number of documents in the collection.

        Returns:
            Number of documents
        """
        try:
            collection = self.vector_store._collection
            count = collection.count()
            logger.info(f"Collection size: {count} documents")
            return count
        except Exception as e:
            logger.error(f"Error getting collection size: {e}")
            return 0

    def as_retriever(self, search_kwargs: Optional[Dict[str, Any]] = None):
        """
        Get a retriever interface.

        Args:
            search_kwargs: Search parameters

        Returns:
            Retriever instance
        """
        search_kwargs = search_kwargs or {"k": config.retrieval_top_k}
        return self.vector_store.as_retriever(search_kwargs=search_kwargs)


def create_vector_store(
    collection_name: str = "research_agent",
    persist_directory: Optional[str] = None,
) -> VectorStore:
    """
    Create a vector store instance.

    Args:
        collection_name: Name of the collection
        persist_directory: Directory to persist the vector store

    Returns:
        VectorStore instance
    """
    return VectorStore(
        collection_name=collection_name,
        persist_directory=persist_directory,
    )
