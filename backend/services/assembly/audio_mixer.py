"""
Audio Mixing for Background Music.

Handles music integration with:
- Audio fade in/out
- Duration trimming to match video length
- Volume normalization
"""

from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


def build_audio_filter(
    audio_input_index: int,
    total_duration: float,
    fade_in: float = 1.5,
    fade_out: float = 2.0,
    volume: float = 0.8,
) -> tuple[str, str]:
    """Build FFmpeg audio filter for background music.

    Args:
        audio_input_index: FFmpeg input index for the audio file.
        total_duration: Total video duration in seconds.
        fade_in: Audio fade-in duration.
        fade_out: Audio fade-out duration.
        volume: Volume level (0.0-1.0).

    Returns:
        Tuple of (filter_string, output_label).
    """
    fade_out_start = max(0, total_duration - fade_out)

    filter_str = (
        f"[{audio_input_index}:a]"
        f"volume={volume},"
        f"afade=t=in:d={fade_in},"
        f"afade=t=out:st={fade_out_start:.2f}:d={fade_out},"
        f"atrim=0:{total_duration:.2f}"
        f"[aout]"
    )

    return filter_str, "aout"
