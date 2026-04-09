"""
Reliable video download with verification.
"""
from __future__ import annotations

import logging
from pathlib import Path

from utils.http_client import create_session

logger = logging.getLogger(__name__)


class VideoDownloader:
    """Downloads and verifies video files."""

    def __init__(self, min_file_size: int = 1024) -> None:
        self.min_file_size = min_file_size
        self.session = create_session(timeout=120)

    def download(self, url: str, output_path: Path, retries: int = 3) -> Path:
        """Download video with retry and verification.

        Args:
            url: Video URL.
            output_path: Local path to save.
            retries: Number of retry attempts.

        Returns:
            Path to verified video file.

        Raises:
            IOError if download fails or file is corrupted.
        """
        output_path.parent.mkdir(parents=True, exist_ok=True)
        last_error: Exception | None = None

        for attempt in range(1, retries + 1):
            try:
                resp = self.session.get(url, stream=True, timeout=120)
                resp.raise_for_status()

                with open(output_path, "wb") as f:
                    for chunk in resp.iter_content(chunk_size=8192):
                        f.write(chunk)

                size = output_path.stat().st_size
                if size < self.min_file_size:
                    raise IOError(f"File too small: {size} bytes")

                logger.info("Downloaded video: %s (%d bytes)", output_path, size)
                return output_path

            except Exception as e:
                last_error = e
                logger.warning(
                    "Download attempt %d/%d failed: %s", attempt, retries, e
                )

        raise IOError(f"Failed to download video after {retries} attempts: {last_error}")

    def verify_video(self, path: Path) -> bool:
        """Basic video file verification."""
        if not path.exists():
            return False
        if path.stat().st_size < self.min_file_size:
            return False
        # Check for valid video header bytes
        with open(path, "rb") as f:
            header = f.read(12)
        # MP4 / MOV signature
        if b"ftyp" in header:
            return True
        # AVI
        if header[:4] == b"RIFF":
            return True
        logger.warning("Unknown video format: %s", path)
        return True  # Don't reject unknown formats
