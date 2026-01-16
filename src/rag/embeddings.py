"""Embedding generation for documents."""

from typing import List

from langchain_google_genai import GoogleGenerativeAIEmbeddings

from src.config import config
from src.utils.logger import logger


class EmbeddingsGenerator:
    """Generate embeddings for text."""

    def __init__(self):
        """Initialize embeddings generator."""
        self.embeddings_model = GoogleGenerativeAIEmbeddings(
            model="models/text-embedding-004",
            google_api_key=config.gemini_api_key,
        )

        logger.info("Initialized Google Embeddings (text-embedding-004)")

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple documents.

        Args:
            texts: List of text strings

        Returns:
            List of embedding vectors
        """
        try:
            embeddings = self.embeddings_model.embed_documents(texts)
            logger.info(f"Generated embeddings for {len(texts)} documents")
            return embeddings
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            raise

    def embed_query(self, text: str) -> List[float]:
        """
        Generate embedding for a query.

        Args:
            text: Query text

        Returns:
            Embedding vector
        """
        try:
            embedding = self.embeddings_model.embed_query(text)
            logger.debug(f"Generated embedding for query: {text[:50]}...")
            return embedding
        except Exception as e:
            logger.error(f"Error generating query embedding: {e}")
            raise

    def get_embeddings_model(self) -> GoogleGenerativeAIEmbeddings:
        """
        Get the underlying embeddings model.

        Returns:
            Embeddings model instance
        """
        return self.embeddings_model


def get_embeddings_model() -> GoogleGenerativeAIEmbeddings:
    """
    Get embeddings model instance.

    Returns:
        Configured embeddings model
    """
    generator = EmbeddingsGenerator()
    return generator.get_embeddings_model()
