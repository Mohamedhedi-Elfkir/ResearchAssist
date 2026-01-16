"""Document loaders for local files."""

from pathlib import Path
from typing import List, Union
import os

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader,
)

from src.config import config
from src.utils.logger import logger


class FileLoader:
    """Load documents from local files."""

    SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".markdown"}

    def __init__(self):
        """Initialize file loader."""
        self.max_file_size_bytes = config.max_file_size_mb * 1024 * 1024

    def load_file(self, file_path: Union[str, Path]) -> List[Document]:
        """
        Load a single file.

        Args:
            file_path: Path to file

        Returns:
            List of Document objects
        """
        file_path = Path(file_path)

        # Validate file exists
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Check file size
        file_size = file_path.stat().st_size
        if file_size > self.max_file_size_bytes:
            raise ValueError(
                f"File too large: {file_size / 1024 / 1024:.2f} MB "
                f"(max: {config.max_file_size_mb} MB)"
            )

        # Check extension
        extension = file_path.suffix.lower()
        if extension not in self.SUPPORTED_EXTENSIONS:
            raise ValueError(
                f"Unsupported file type: {extension}. "
                f"Supported types: {', '.join(self.SUPPORTED_EXTENSIONS)}"
            )

        logger.info(f"Loading file: {file_path}")

        try:
            # Load based on file type
            if extension == ".pdf":
                loader = PyPDFLoader(str(file_path))
            elif extension == ".txt":
                loader = TextLoader(str(file_path), encoding="utf-8")
            elif extension in {".md", ".markdown"}:
                loader = UnstructuredMarkdownLoader(str(file_path))
            else:
                raise ValueError(f"Unsupported extension: {extension}")

            documents = loader.load()

            # Add metadata
            for doc in documents:
                doc.metadata.update({
                    "source": str(file_path),
                    "file_name": file_path.name,
                    "file_type": extension,
                    "file_size": file_size,
                })

            logger.info(f"Loaded {len(documents)} documents from {file_path}")
            return documents

        except Exception as e:
            logger.error(f"Error loading file {file_path}: {e}")
            raise

    def load_directory(
        self,
        directory_path: Union[str, Path],
        recursive: bool = True,
    ) -> List[Document]:
        """
        Load all supported files from a directory.

        Args:
            directory_path: Path to directory
            recursive: Whether to search recursively

        Returns:
            List of Document objects
        """
        directory_path = Path(directory_path)

        if not directory_path.is_dir():
            raise ValueError(f"Not a directory: {directory_path}")

        logger.info(f"Loading documents from directory: {directory_path}")

        all_documents = []
        pattern = "**/*" if recursive else "*"

        for file_path in directory_path.glob(pattern):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                try:
                    documents = self.load_file(file_path)
                    all_documents.extend(documents)
                except Exception as e:
                    logger.warning(f"Skipping file {file_path}: {e}")
                    continue

        logger.info(
            f"Loaded {len(all_documents)} total documents from {directory_path}"
        )
        return all_documents

    def load_files(self, file_paths: List[Union[str, Path]]) -> List[Document]:
        """
        Load multiple files.

        Args:
            file_paths: List of file paths

        Returns:
            List of Document objects
        """
        all_documents = []

        for file_path in file_paths:
            try:
                documents = self.load_file(file_path)
                all_documents.extend(documents)
            except Exception as e:
                logger.warning(f"Skipping file {file_path}: {e}")
                continue

        logger.info(f"Loaded {len(all_documents)} total documents from {len(file_paths)} files")
        return all_documents


def load_documents(
    paths: Union[str, Path, List[Union[str, Path]]],
    recursive: bool = True,
) -> List[Document]:
    """
    Load documents from file(s) or directory.

    Args:
        paths: Single path or list of paths (files or directories)
        recursive: Whether to search directories recursively

    Returns:
        List of Document objects
    """
    loader = FileLoader()

    # Convert single path to list
    if isinstance(paths, (str, Path)):
        paths = [paths]

    all_documents = []

    for path in paths:
        path = Path(path)

        if path.is_file():
            documents = loader.load_file(path)
            all_documents.extend(documents)
        elif path.is_dir():
            documents = loader.load_directory(path, recursive=recursive)
            all_documents.extend(documents)
        else:
            logger.warning(f"Path does not exist: {path}")

    return all_documents
