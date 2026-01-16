"""Basic research agent example."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import ResearchAgent


def main():
    """Run basic research example."""
    print("=" * 60)
    print("Research Agent - Basic Example")
    print("=" * 60)

    # Initialize agent
    print("\n1. Initializing research agent...")
    agent = ResearchAgent()

    # Step 1: Ingest documents
    print("\n2. Ingesting sample documents...")
    print("   Note: Add documents to data/documents/ folder first")

    # Example documents paths
    documents_dir = Path("data/documents")

    if documents_dir.exists() and any(documents_dir.iterdir()):
        count = agent.ingest_documents([documents_dir])
        print(f"   Successfully ingested {count} document chunks")
    else:
        print("   Warning: No documents found in data/documents/")
        print("   The agent will only use general knowledge")

    # Step 2: Research queries
    print("\n3. Running research queries...")

    queries = [
        "What is machine learning?",
        "Explain neural networks in simple terms",
        "What are the applications of AI?",
    ]

    for i, query in enumerate(queries, 1):
        print(f"\n   Query {i}: {query}")
        print("   " + "-" * 50)

        result = agent.research(query)

        print(f"   Answer: {result['answer'][:200]}...")
        print(f"   Sources: {len(result['sources'])} source(s)")
        print(f"   Documents used: {result['documents_used']}")
        print(f"   Relevance score: {result['relevance_score']:.1f}/10")

    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
