"""Document chunking strategies."""

from typing import List, Optional

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

from src.config import config
from src.utils.logger import logger


class DocumentChunker:
    """Chunk documents into smaller pieces."""

    def __init__(
        self,
        chunk_size: Optional[int] = None,
        chunk_overlap: Optional[int] = None,
    ):
        """
        Initialize document chunker.

        Args:
            chunk_size: Size of each chunk in characters
            chunk_overlap: Overlap between chunks in characters
        """
        self.chunk_size = chunk_size or config.chunk_size
        self.chunk_overlap = chunk_overlap or config.chunk_overlap

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", " ", ""],
        )

        logger.info(
            f"Initialized chunker with chunk_size={self.chunk_size}, "
            f"chunk_overlap={self.chunk_overlap}"
        )

    def chunk_documents(self, documents: List[Document]) -> List[Document]:
        """
        Chunk documents into smaller pieces.

        Args:
            documents: List of documents to chunk

        Returns:
            List of chunked documents
        """
        logger.info(f"Chunking {len(documents)} documents")

        chunked_docs = self.text_splitter.split_documents(documents)

        logger.info(
            f"Created {len(chunked_docs)} chunks from {len(documents)} documents "
            f"(avg {len(chunked_docs) / len(documents) if documents else 0:.1f} chunks per doc)"
        )

        return chunked_docs

    def chunk_text(self, text: str, metadata: Optional[dict] = None) -> List[Document]:
        """
        Chunk a single text string.

        Args:
            text: Text to chunk
            metadata: Optional metadata for chunks

        Returns:
            List of document chunks
        """
        chunks = self.text_splitter.split_text(text)

        documents = [
            Document(
                page_content=chunk,
                metadata=metadata or {},
            )
            for chunk in chunks
        ]

        logger.info(f"Created {len(documents)} chunks from text")
        return documents


def chunk_documents(
    documents: List[Document],
    chunk_size: Optional[int] = None,
    chunk_overlap: Optional[int] = None,
) -> List[Document]:
    """
    Chunk documents into smaller pieces.

    Args:
        documents: List of documents to chunk
        chunk_size: Size of each chunk
        chunk_overlap: Overlap between chunks

    Returns:
        List of chunked documents
    """
    chunker = DocumentChunker(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return chunker.chunk_documents(documents)
