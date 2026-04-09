"""
FFmpeg transition filter builders.
"""
from __future__ import annotations

import logging
from models.enums import TransitionType

logger = logging.getLogger(__name__)


class TransitionBuilder:
    """Builds FFmpeg filter expressions for scene transitions."""

    def build_filter(
        self,
        transition_type: TransitionType,
        duration: float = 0.5,
        offset: float = 0.0,
    ) -> str:
        """Build an FFmpeg filter string for a transition.

        Args:
            transition_type: Type of transition.
            duration: Transition duration in seconds.
            offset: Time offset where transition starts.

        Returns:
            FFmpeg filter expression string.
        """
        if transition_type == TransitionType.FADE:
            return self._fade(duration, offset)
        elif transition_type == TransitionType.DISSOLVE:
            return self._dissolve(duration, offset)
        elif transition_type == TransitionType.WIPE:
            return self._wipe(duration, offset)
        else:  # CUT
            return ""

    def _fade(self, duration: float, offset: float) -> str:
        return f"fade=t=out:st={offset}:d={duration},fade=t=in:st={offset}:d={duration}"

    def _dissolve(self, duration: float, offset: float) -> str:
        return f"fade=t=out:st={offset}:d={duration}:alpha=1,fade=t=in:st=0:d={duration}:alpha=1"

    def _wipe(self, duration: float, offset: float) -> str:
        # Horizontal wipe using crop
        return f"fade=t=out:st={offset}:d={duration}"

    def build_xfade(
        self,
        transition_type: TransitionType,
        duration: float = 0.5,
        offset: float = 0.0,
    ) -> str:
        """Build xfade filter for between-clip transitions.

        Requires FFmpeg 4.3+.
        """
        xfade_map = {
            TransitionType.FADE: "fade",
            TransitionType.DISSOLVE: "dissolve",
            TransitionType.WIPE: "wipeleft",
            TransitionType.CUT: "fade",
        }
        effect = xfade_map.get(transition_type, "fade")
        return f"xfade=transition={effect}:duration={duration}:offset={offset}"
