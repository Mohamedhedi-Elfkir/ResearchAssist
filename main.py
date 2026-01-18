"""Main entry point for the research agent."""

import argparse
import sys
from pathlib import Path

from src.config import config
from src.utils.logger import logger
from src.utils.downloader import DocumentDownloader
from src.rag.vector_store import create_vector_store
from src.graph.workflow import ResearchWorkflow
from src.loaders.file_loader import load_documents
from src.loaders.document_processor import process_documents
from src.rag.chunking import chunk_documents


class ResearchAgent:
    """Research agent with RAG and web scraping capabilities."""

    def __init__(self):
        """Initialize research agent."""
        # Validate and setup configuration
        config.validate()
        config.ensure_directories()

        # Initialize vector store
        self.vector_store = create_vector_store()

        # Initialize workflow
        self.workflow = ResearchWorkflow(self.vector_store)

        logger.info("Research agent initialized successfully")

    def ingest_documents(
        self,
        paths: list,
        recursive: bool = True,
    ) -> int:
        """
        Ingest documents into the vector store.

        Args:
            paths: List of file or directory paths
            recursive: Whether to search directories recursively

        Returns:
            Number of documents ingested
        """
        logger.info(f"Ingesting documents from {len(paths)} path(s)")

        # Load documents
        documents = load_documents(paths, recursive=recursive)

        if not documents:
            logger.warning("No documents loaded")
            return 0

        # Process documents
        documents = process_documents(documents)

        # Chunk documents
        chunks = chunk_documents(documents)

        # Add to vector store
        self.vector_store.add_documents(chunks)

        logger.info(f"Successfully ingested {len(chunks)} chunks from {len(documents)} documents")

        return len(chunks)

    def research(self, query: str) -> dict:
        """
        Perform research on a query.

        Args:
            query: Research question

        Returns:
            Research results
        """
        logger.info(f"Researching: {query}")

        result = self.workflow.run(query)

        return result


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Research Agent with RAG and LangGraph",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download documents
  python main.py download --url https://example.com/paper.pdf --auto-ingest

  # Ingest documents
  python main.py ingest --path data/documents

  # Research query
  python main.py query "What is machine learning?"

  # Interactive mode
  python main.py interactive
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # Ingest command
    ingest_parser = subparsers.add_parser("ingest", help="Ingest documents into vector store")
    ingest_parser.add_argument(
        "--path",
        nargs="+",
        required=True,
        help="Path(s) to files or directories"
    )
    ingest_parser.add_argument(
        "--no-recursive",
        action="store_true",
        help="Don't search directories recursively"
    )

    # Query command
    query_parser = subparsers.add_parser("query", help="Research a query")
    query_parser.add_argument(
        "query",
        nargs="+",
        help="Research query"
    )

    # Interactive command
    subparsers.add_parser("interactive", help="Interactive mode")

    # Download command
    download_parser = subparsers.add_parser("download", help="Download documents from URLs")
    download_parser.add_argument(
        "--url",
        nargs="+",
        required=True,
        help="URL(s) to download documents from"
    )
    download_parser.add_argument(
        "--filename",
        nargs="+",
        help="Optional custom filename(s)"
    )
    download_parser.add_argument(
        "--auto-ingest",
        action="store_true",
        help="Automatically ingest downloaded documents"
    )

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    try:
        # Initialize agent
        agent = ResearchAgent()

        if args.command == "ingest":
            # Ingest documents
            count = agent.ingest_documents(
                args.path,
                recursive=not args.no_recursive
            )
            print(f"\nSuccessfully ingested {count} document chunks.")

        elif args.command == "query":
            # Research query
            query = " ".join(args.query)
            result = agent.research(query)

            # Print results
            print(f"\nQuery: {result['query']}")
            print(f"\nAnswer:\n{result['answer']}")
            print(f"\nSources:")
            for source in result['sources']:
                print(f"  - {source}")
            print(f"\nDocuments used: {result['documents_used']}")
            print(f"Relevance score: {result['relevance_score']:.1f}/10")

        elif args.command == "download":
            # Download documents
            downloader = DocumentDownloader()
            downloaded_files = downloader.download_multiple(
                args.url,
                filenames=args.filename
            )

            if downloaded_files:
                print(f"\nSuccessfully downloaded {len(downloaded_files)} file(s):")
                for file in downloaded_files:
                    print(f"  - {file}")

                # Auto-ingest if requested
                if args.auto_ingest:
                    print("\nAuto-ingesting downloaded documents...")
                    count = agent.ingest_documents(downloaded_files)
                    print(f"Successfully ingested {count} document chunks.")
            else:
                print("\nNo files were downloaded.")

        elif args.command == "interactive":
            # Interactive mode
            print("\nResearch Agent - Interactive Mode")
            print("Type 'exit' or 'quit' to end the session\n")

            while True:
                try:
                    query = input("Query: ").strip()

                    if not query:
                        continue

                    if query.lower() in ["exit", "quit"]:
                        print("Goodbye!")
                        break

                    # Research
                    result = agent.research(query)

                    # Print results
                    print(f"\nAnswer:\n{result['answer']}\n")
                    print(f"Sources: {', '.join(result['sources'])}")
                    print(f"Relevance: {result['relevance_score']:.1f}/10\n")

                except KeyboardInterrupt:
                    print("\n\nGoodbye!")
                    break
                except Exception as e:
                    logger.error(f"Error: {e}")
                    print(f"\nError: {e}\n")

    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
