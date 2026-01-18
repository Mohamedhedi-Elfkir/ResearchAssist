"""Document downloader utility."""

import os
import requests
from pathlib import Path
from typing import Optional, List
from urllib.parse import urlparse
from tqdm import tqdm

from src.config import config
from src.utils.logger import logger


class DocumentDownloader:
    """Download documents from URLs."""

    def __init__(self, download_dir: Optional[str] = None):
        """
        Initialize document downloader.

        Args:
            download_dir: Directory to save downloaded files
        """
        self.download_dir = Path(download_dir or config.documents_dir)
        self.download_dir.mkdir(parents=True, exist_ok=True)

    def download_file(
        self,
        url: str,
        filename: Optional[str] = None,
        chunk_size: int = 8192,
    ) -> Optional[str]:
        """
        Download a file from URL.

        Args:
            url: URL to download from
            filename: Optional custom filename
            chunk_size: Chunk size for streaming download

        Returns:
            Path to downloaded file or None if failed
        """
        try:
            logger.info(f"Downloading from: {url}")

            # Get filename from URL if not provided
            if not filename:
                parsed_url = urlparse(url)
                filename = os.path.basename(parsed_url.path)
                if not filename:
                    filename = "downloaded_file"

            # Full path
            file_path = self.download_dir / filename

            # Check if file already exists
            if file_path.exists():
                logger.warning(f"File already exists: {file_path}")
                response = input(f"Overwrite {filename}? (y/n): ")
                if response.lower() != 'y':
                    logger.info("Download cancelled")
                    return str(file_path)

            # Stream download with progress bar
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()

            # Get total file size
            total_size = int(response.headers.get('content-length', 0))

            # Download with progress bar
            with open(file_path, 'wb') as f:
                if total_size == 0:
                    # No content-length header
                    f.write(response.content)
                else:
                    # Show progress bar
                    with tqdm(
                        total=total_size,
                        unit='B',
                        unit_scale=True,
                        desc=filename
                    ) as pbar:
                        for chunk in response.iter_content(chunk_size=chunk_size):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))

            logger.info(f"Downloaded successfully: {file_path}")
            return str(file_path)

        except requests.exceptions.RequestException as e:
            logger.error(f"Error downloading {url}: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error downloading {url}: {e}")
            return None

    def download_multiple(
        self,
        urls: List[str],
        filenames: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Download multiple files.

        Args:
            urls: List of URLs to download
            filenames: Optional list of custom filenames

        Returns:
            List of downloaded file paths
        """
        downloaded_files = []

        for i, url in enumerate(urls):
            filename = filenames[i] if filenames and i < len(filenames) else None
            file_path = self.download_file(url, filename)
            if file_path:
                downloaded_files.append(file_path)

        logger.info(f"Downloaded {len(downloaded_files)} out of {len(urls)} files")
        return downloaded_files


def download_documents(
    urls: List[str],
    download_dir: Optional[str] = None,
    filenames: Optional[List[str]] = None,
) -> List[str]:
    """
    Download documents from URLs.

    Args:
        urls: List of URLs to download
        download_dir: Directory to save files
        filenames: Optional list of custom filenames

    Returns:
        List of downloaded file paths
    """
    downloader = DocumentDownloader(download_dir)
    return downloader.download_multiple(urls, filenames)
