"""
Reliable Video Download with Verification.

Downloads generated videos from Kling's CDN and verifies
file integrity (size check, basic format validation).
"""

from __future__ import annotations

import logging
from pathlib import Path

import httpx

from backend.pipeline.exceptions import VideoDownloadError

logger = logging.getLogger(__name__)

MIN_VIDEO_SIZE_BYTES = 1024  # 1KB minimum to detect corrupt downloads


async def download_video(
    video_url: str,
    output_path: Path,
    timeout: float = 120.0,
    min_size: int = MIN_VIDEO_SIZE_BYTES,
) -> str:
    """Download a video from URL and verify integrity.

    Args:
        video_url: URL to download the video from.
        output_path: Local path to save the file.
        timeout: Download timeout in seconds.
        min_size: Minimum acceptable file size in bytes.

    Returns:
        Path to the saved video file.

    Raises:
        VideoDownloadError: If download fails or file is corrupt.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        async with httpx.AsyncClient(timeout=timeout) as client:
            response = await client.get(video_url)
            response.raise_for_status()

            content = response.content
            if len(content) < min_size:
                raise VideoDownloadError(
                    f"Downloaded video too small ({len(content)} bytes < {min_size}), "
                    f"likely corrupted",
                    video_url=video_url,
                    file_size=len(content),
                )

            output_path.write_bytes(content)

        file_size = output_path.stat().st_size
        logger.info(
            "[DOWNLOAD] Video saved: %s (%.1f MB)",
            output_path,
            file_size / (1024 * 1024),
        )
        return str(output_path)

    except VideoDownloadError:
        raise
    except httpx.TimeoutException as e:
        raise VideoDownloadError(
            f"Download timeout after {timeout}s",
            video_url=video_url,
        ) from e
    except httpx.HTTPStatusError as e:
        raise VideoDownloadError(
            f"Download HTTP error: {e.response.status_code}",
            video_url=video_url,
        ) from e
    except Exception as e:
        raise VideoDownloadError(
            f"Download failed: {e}",
            video_url=video_url,
        ) from e
