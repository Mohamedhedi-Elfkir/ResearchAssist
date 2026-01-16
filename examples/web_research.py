"""Web research example using web scraping."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.loaders.web_scraper import WebScraper
from src.rag.vector_store import create_vector_store
from src.rag.chunking import chunk_documents
from src.loaders.document_processor import process_documents


def main():
    """Run web research example."""
    print("=" * 60)
    print("Research Agent - Web Scraping Example")
    print("=" * 60)

    # Initialize web scraper
    print("\n1. Initializing web scraper...")
    scraper = WebScraper()

    # Example URLs to scrape
    urls = [
        "https://en.wikipedia.org/wiki/Machine_learning",
        "https://en.wikipedia.org/wiki/Artificial_intelligence",
    ]

    print(f"\n2. Scraping {len(urls)} URLs...")
    for url in urls:
        print(f"   - {url}")

    # Scrape URLs
    documents = scraper.scrape_urls(urls)

    if not documents:
        print("\n   Warning: No documents scraped")
        print("   This may be due to network issues or rate limiting")
        return

    print(f"\n   Successfully scraped {len(documents)} pages")

    # Process documents
    print("\n3. Processing documents...")
    documents = process_documents(documents)

    # Chunk documents
    print("   Chunking documents...")
    chunks = chunk_documents(documents)
    print(f"   Created {len(chunks)} chunks")

    # Create vector store and add documents
    print("\n4. Adding to vector store...")
    vector_store = create_vector_store(collection_name="web_research_example")
    vector_store.add_documents(chunks)

    # Search the vector store
    print("\n5. Testing retrieval...")
    test_queries = [
        "What is machine learning?",
        "Define artificial intelligence",
    ]

    for query in test_queries:
        print(f"\n   Query: {query}")
        results = vector_store.similarity_search(query, k=3)
        print(f"   Found {len(results)} relevant chunks")

        if results:
            print(f"   Top result preview: {results[0].page_content[:150]}...")

    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
