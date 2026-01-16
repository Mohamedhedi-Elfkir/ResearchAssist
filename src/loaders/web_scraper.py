"""Web scraping functionality."""

import time
from typing import List, Optional
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from langchain_core.documents import Document

from src.config import config
from src.utils.logger import logger


class WebScraper:
    """Scrape web content and convert to documents."""

    def __init__(
        self,
        user_agent: Optional[str] = None,
        timeout: Optional[int] = None,
        rate_limit_delay: Optional[float] = None,
    ):
        """
        Initialize web scraper.

        Args:
            user_agent: User agent string
            timeout: Request timeout in seconds
            rate_limit_delay: Delay between requests in seconds
        """
        self.user_agent = user_agent or config.user_agent
        self.timeout = timeout or config.request_timeout
        self.rate_limit_delay = rate_limit_delay or config.rate_limit_delay
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": self.user_agent})

    def _validate_url(self, url: str) -> bool:
        """
        Validate URL format.

        Args:
            url: URL to validate

        Returns:
            True if valid
        """
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False

    def _extract_text(self, html: str, url: str) -> str:
        """
        Extract clean text from HTML.

        Args:
            html: HTML content
            url: Source URL

        Returns:
            Extracted text
        """
        try:
            soup = BeautifulSoup(html, "lxml")

            # Remove script and style elements
            for element in soup(["script", "style", "nav", "footer", "header"]):
                element.decompose()

            # Get text
            text = soup.get_text(separator="\n", strip=True)

            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            text = "\n".join(line for line in lines if line)

            return text

        except Exception as e:
            logger.error(f"Error extracting text from {url}: {e}")
            return ""

    def scrape_url(self, url: str) -> Optional[Document]:
        """
        Scrape a single URL.

        Args:
            url: URL to scrape

        Returns:
            Document object or None if failed
        """
        # Validate URL
        if not self._validate_url(url):
            logger.error(f"Invalid URL: {url}")
            return None

        logger.info(f"Scraping URL: {url}")

        try:
            # Make request
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()

            # Extract text
            text = self._extract_text(response.text, url)

            if not text:
                logger.warning(f"No text extracted from {url}")
                return None

            # Create document
            document = Document(
                page_content=text,
                metadata={
                    "source": url,
                    "url": url,
                    "title": self._extract_title(response.text),
                    "status_code": response.status_code,
                    "content_type": response.headers.get("content-type", ""),
                },
            )

            logger.info(f"Successfully scraped {url} ({len(text)} characters)")

            # Rate limiting
            time.sleep(self.rate_limit_delay)

            return document

        except requests.exceptions.Timeout:
            logger.error(f"Timeout scraping {url}")
            return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error scraping {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error scraping {url}: {e}")
            return None

    def scrape_urls(self, urls: List[str]) -> List[Document]:
        """
        Scrape multiple URLs.

        Args:
            urls: List of URLs to scrape

        Returns:
            List of Document objects
        """
        documents = []

        for url in urls:
            document = self.scrape_url(url)
            if document:
                documents.append(document)

        logger.info(
            f"Scraped {len(documents)} documents from {len(urls)} URLs"
        )
        return documents

    def _extract_title(self, html: str) -> str:
        """
        Extract page title from HTML.

        Args:
            html: HTML content

        Returns:
            Page title or empty string
        """
        try:
            soup = BeautifulSoup(html, "lxml")
            title_tag = soup.find("title")
            return title_tag.get_text(strip=True) if title_tag else ""
        except Exception:
            return ""

    def search_and_scrape(
        self,
        query: str,
        num_results: int = 5,
    ) -> List[Document]:
        """
        Search the web and scrape results.

        Note: This is a placeholder. In production, integrate with
        a search API (Google Custom Search, Bing, DuckDuckGo, etc.)

        Args:
            query: Search query
            num_results: Number of results to scrape

        Returns:
            List of Document objects
        """
        logger.warning(
            "search_and_scrape is a placeholder. "
            "Integrate with a search API for production use."
        )

        # Placeholder implementation
        # In production, use Google Custom Search API, Bing API, etc.
        return []


def scrape_web(urls: List[str]) -> List[Document]:
    """
    Scrape web pages from URLs.

    Args:
        urls: List of URLs to scrape

    Returns:
        List of Document objects
    """
    scraper = WebScraper()
    return scraper.scrape_urls(urls)
