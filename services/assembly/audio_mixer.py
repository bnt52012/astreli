"""
Audio mixing — background music integration with fade in/out.
"""
from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class AudioMixer:
    """Builds FFmpeg audio filter expressions."""

    def build_fade_filter(
        self,
        total_duration: float,
        fade_in: float = 1.0,
        fade_out: float = 2.0,
        volume: float = 0.3,
    ) -> str:
        """Build audio fade filter string.

        Args:
            total_duration: Total video duration.
            fade_in: Fade in duration.
            fade_out: Fade out duration.
            volume: Background music volume (0.0-1.0).

        Returns:
            FFmpeg audio filter string.
        """
        fade_out_start = max(0, total_duration - fade_out)
        return (
            f"volume={volume},"
            f"afade=t=in:st=0:d={fade_in},"
            f"afade=t=out:st={fade_out_start}:d={fade_out}"
        )

    def build_mix_filter(
        self,
        original_audio: bool = False,
        music_volume: float = 0.3,
        voice_volume: float = 1.0,
    ) -> str:
        """Build audio mix filter for combining original audio with music."""
        if original_audio:
            return (
                f"[1:a]volume={music_volume}[music];"
                f"[0:a]volume={voice_volume}[voice];"
                f"[voice][music]amix=inputs=2:duration=first[aout]"
            )
        return f"volume={music_volume}"
