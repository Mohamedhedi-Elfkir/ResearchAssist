"""Document preprocessing utilities."""

import re
from typing import List

from langchain_core.documents import Document

from src.utils.logger import logger


class DocumentProcessor:
    """Process and clean documents."""

    def __init__(self):
        """Initialize document processor."""
        pass

    def clean_text(self, text: str) -> str:
        """
        Clean and normalize text.

        Args:
            text: Input text

        Returns:
            Cleaned text
        """
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)

        # Remove excessive newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)

        # Strip leading/trailing whitespace
        text = text.strip()

        return text

    def remove_duplicates(self, documents: List[Document]) -> List[Document]:
        """
        Remove duplicate documents based on content.

        Args:
            documents: List of documents

        Returns:
            Deduplicated list
        """
        seen_content = set()
        unique_docs = []

        for doc in documents:
            content_hash = hash(doc.page_content)
            if content_hash not in seen_content:
                seen_content.add(content_hash)
                unique_docs.append(doc)

        if len(unique_docs) < len(documents):
            logger.info(
                f"Removed {len(documents) - len(unique_docs)} duplicate documents"
            )

        return unique_docs

    def filter_short_documents(
        self,
        documents: List[Document],
        min_length: int = 100,
    ) -> List[Document]:
        """
        Filter out documents that are too short.

        Args:
            documents: List of documents
            min_length: Minimum character length

        Returns:
            Filtered list
        """
        filtered = [
            doc for doc in documents
            if len(doc.page_content) >= min_length
        ]

        if len(filtered) < len(documents):
            logger.info(
                f"Filtered out {len(documents) - len(filtered)} short documents"
            )

        return filtered

    def process_documents(
        self,
        documents: List[Document],
        clean: bool = True,
        deduplicate: bool = True,
        filter_short: bool = True,
        min_length: int = 100,
    ) -> List[Document]:
        """
        Process documents with various cleaning operations.

        Args:
            documents: List of documents
            clean: Whether to clean text
            deduplicate: Whether to remove duplicates
            filter_short: Whether to filter short documents
            min_length: Minimum length for filtering

        Returns:
            Processed documents
        """
        logger.info(f"Processing {len(documents)} documents")

        processed = documents.copy()

        # Clean text
        if clean:
            for doc in processed:
                doc.page_content = self.clean_text(doc.page_content)

        # Remove duplicates
        if deduplicate:
            processed = self.remove_duplicates(processed)

        # Filter short documents
        if filter_short:
            processed = self.filter_short_documents(processed, min_length)

        logger.info(f"Processed {len(processed)} documents (from {len(documents)})")
        return processed


def process_documents(
    documents: List[Document],
    clean: bool = True,
    deduplicate: bool = True,
    filter_short: bool = True,
    min_length: int = 100,
) -> List[Document]:
    """
    Process documents with cleaning operations.

    Args:
        documents: List of documents
        clean: Whether to clean text
        deduplicate: Whether to remove duplicates
        filter_short: Whether to filter short documents
        min_length: Minimum length for filtering

    Returns:
        Processed documents
    """
    processor = DocumentProcessor()
    return processor.process_documents(
        documents,
        clean=clean,
        deduplicate=deduplicate,
        filter_short=filter_short,
        min_length=min_length,
    )
