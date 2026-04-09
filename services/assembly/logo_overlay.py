"""
Brand logo overlay positioning.
"""
from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class LogoOverlay:
    """Builds FFmpeg filter for logo overlay."""

    def build_filter(
        self,
        logo_path: str,
        position: str = "top_right",
        margin: int = 30,
        opacity: float = 0.7,
        max_height: int = 60,
    ) -> str:
        """Build FFmpeg overlay filter for brand logo.

        Args:
            logo_path: Path to logo image.
            position: Position: top_right, top_left, bottom_right, bottom_left.
            margin: Margin from edges in pixels.
            opacity: Logo opacity (0.0-1.0).
            max_height: Maximum logo height in pixels.

        Returns:
            FFmpeg filter_complex expression.
        """
        # Position mapping
        positions = {
            "top_right": f"W-w-{margin}:{margin}",
            "top_left": f"{margin}:{margin}",
            "bottom_right": f"W-w-{margin}:H-h-{margin}",
            "bottom_left": f"{margin}:H-h-{margin}",
        }
        pos = positions.get(position, positions["top_right"])

        # Scale logo + set opacity
        return (
            f"[1:v]scale=-1:{max_height},format=rgba,"
            f"colorchannelmixer=aa={opacity}[logo];"
            f"[main][logo]overlay={pos}[out]"
        )
