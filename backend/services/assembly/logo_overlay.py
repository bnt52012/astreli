"""
Brand Logo Overlay.

Handles logo positioning, scaling, and FFmpeg overlay filter generation.
Logo is placed in the top-right corner with configurable padding and scale.
"""

from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def build_logo_filter(
    logo_input_index: int,
    video_label: str,
    output_label: str,
    scale_width: int = 120,
    padding: int = 30,
    position: str = "top_right",
) -> str:
    """Build FFmpeg filter for logo overlay.

    Args:
        logo_input_index: FFmpeg input index for the logo file.
        video_label: Label of the video stream to overlay on.
        output_label: Label for the output stream.
        scale_width: Logo width in pixels (height auto-calculated).
        padding: Distance from edge in pixels.
        position: One of "top_right", "top_left", "bottom_right", "bottom_left".

    Returns:
        FFmpeg filter string.
    """
    # Position mapping
    positions = {
        "top_right": f"W-w-{padding}:{padding}",
        "top_left": f"{padding}:{padding}",
        "bottom_right": f"W-w-{padding}:H-h-{padding}",
        "bottom_left": f"{padding}:H-h-{padding}",
    }
    pos = positions.get(position, positions["top_right"])

    return (
        f"[{logo_input_index}:v]scale={scale_width}:-1[logo];"
        f"[{video_label}][logo]overlay={pos}[{output_label}]"
    )
