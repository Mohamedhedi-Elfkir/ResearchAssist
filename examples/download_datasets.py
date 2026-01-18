"""Example: Download large datasets and documents."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.utils.downloader import DocumentDownloader
from main import ResearchAgent


def main():
    """Download example datasets and ingest them."""
    print("=" * 60)
    print("Research Agent - Large Dataset Download Example")
    print("=" * 60)

    # Initialize downloader
    downloader = DocumentDownloader()

    # Example URLs for large documents/datasets
    # These are just examples - replace with actual URLs you want to download
    example_urls = {
        "AI Research Papers": [
            # Example: ArXiv papers (replace with actual paper URLs)
            # "https://arxiv.org/pdf/1706.03762.pdf",  # Attention Is All You Need
            # "https://arxiv.org/pdf/2005.14165.pdf",  # GPT-3
        ],
        "Documentation": [
            # Example: Technical documentation (replace with actual URLs)
            # "https://docs.python.org/3/archives/python-3.11.0-docs-pdf-a4.zip",
        ],
        "Books": [
            # Example: Public domain books (replace with actual URLs)
            # "https://www.gutenberg.org/files/1342/1342-0.txt",  # Pride and Prejudice
        ]
    }

    print("\n" + "=" * 60)
    print("EXAMPLE DATASETS TO DOWNLOAD")
    print("=" * 60)
    print("\nHere are some examples of large datasets you can download:\n")

    print("1. Research Papers (ArXiv):")
    print("   https://arxiv.org/pdf/[paper-id].pdf")
    print("   Example: https://arxiv.org/pdf/1706.03762.pdf (Attention Is All You Need)")

    print("\n2. Books (Project Gutenberg):")
    print("   https://www.gutenberg.org/files/[book-id]/[book-id]-0.txt")
    print("   Example: https://www.gutenberg.org/files/1342/1342-0.txt (Pride and Prejudice)")

    print("\n3. Documentation:")
    print("   Python Docs: https://docs.python.org/3/archives/")
    print("   Django Docs: https://media.readthedocs.org/pdf/django/latest/django.pdf")

    print("\n4. Wikipedia Articles (as PDF):")
    print("   Use https://en.wikipedia.org/api/rest_v1/page/pdf/[Article_Name]")

    print("\n5. GitHub README files:")
    print("   https://raw.githubusercontent.com/[user]/[repo]/main/README.md")

    print("\n" + "=" * 60)
    print("DOWNLOAD INSTRUCTIONS")
    print("=" * 60)

    print("\nTo download and ingest documents, use:")
    print("\n  python main.py download --url <URL> --auto-ingest")

    print("\nExamples:")
    print("\n  # Download a single document")
    print("  python main.py download --url https://arxiv.org/pdf/1706.03762.pdf --auto-ingest")

    print("\n  # Download multiple documents")
    print("  python main.py download --url")
    print("    https://arxiv.org/pdf/1706.03762.pdf")
    print("    https://arxiv.org/pdf/2005.14165.pdf")
    print("    --auto-ingest")

    print("\n  # Download with custom filename")
    print("  python main.py download --url https://example.com/doc.pdf --filename my_document.pdf")

    print("\n" + "=" * 60)
    print("PROGRAMMATIC USAGE")
    print("=" * 60)

    print("\nOr use Python code:")
    print("""
from src.utils.downloader import DocumentDownloader
from main import ResearchAgent

# Download documents
downloader = DocumentDownloader()
files = downloader.download_multiple([
    "https://arxiv.org/pdf/1706.03762.pdf",
    "https://arxiv.org/pdf/2005.14165.pdf",
])

# Ingest into research agent
agent = ResearchAgent()
agent.ingest_documents(files)

# Research
result = agent.research("What is attention mechanism in transformers?")
print(result["answer"])
    """)

    print("\n" + "=" * 60)
    print("INTERACTIVE DEMO")
    print("=" * 60)

    response = input("\nWould you like to download a sample document? (y/n): ")

    if response.lower() == 'y':
        # Download a sample public domain book
        sample_url = "https://www.gutenberg.org/files/1342/1342-0.txt"
        print(f"\nDownloading sample: Pride and Prejudice by Jane Austen")
        print(f"URL: {sample_url}")

        files = downloader.download_multiple(
            [sample_url],
            filenames=["pride_and_prejudice.txt"]
        )

        if files:
            print(f"\nDownloaded successfully: {files[0]}")

            ingest_response = input("\nWould you like to ingest this into the research agent? (y/n): ")

            if ingest_response.lower() == 'y':
                agent = ResearchAgent()
                count = agent.ingest_documents(files)
                print(f"\nIngested {count} document chunks!")

                print("\nYou can now query the document:")
                print('  python main.py query "Who are the main characters in Pride and Prejudice?"')
        else:
            print("\nDownload failed. Please check your internet connection.")
    else:
        print("\nSkipping download demo.")

    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
