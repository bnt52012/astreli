"""
H.264 Encoding Profiles.

Provides encoding parameter sets for different quality levels
and target platforms.
"""

from __future__ import annotations

from backend.models.enums import QualityLevel
from backend.pipeline.config import QUALITY_PRESETS


def get_encoding_args(
    quality: QualityLevel = QualityLevel.PREMIUM,
    resolution: str = "1920x1080",
    fps: int = 30,
    custom_bitrate: str | None = None,
) -> str:
    """Build FFmpeg encoding arguments string.

    Args:
        quality: Quality level preset.
        resolution: Output resolution (WxH).
        fps: Output frame rate.
        custom_bitrate: Override bitrate (e.g., "25M").

    Returns:
        FFmpeg encoding arguments string.
    """
    preset = QUALITY_PRESETS.get(quality, QUALITY_PRESETS[QualityLevel.PREMIUM])

    parts = [
        f"-c:v libx264",
        f"-preset {preset.preset}",
        f"-crf {preset.crf}",
        f"-pix_fmt yuv420p",
        f"-movflags +faststart",
        f"-r {fps}",
    ]

    # Bitrate override
    bitrate = custom_bitrate or preset.video_bitrate
    if bitrate:
        parts.append(f"-b:v {bitrate}")
        parts.append(f"-maxrate {bitrate}")
        parts.append(f"-bufsize {bitrate}")

    # Audio encoding
    parts.append("-c:a aac")
    parts.append("-b:a 192k")

    return " ".join(parts)
