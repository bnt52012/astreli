"""
FFmpeg Transition Filter Builders.

Implements 15+ transition types using FFmpeg xfade filter.
Each transition maps to an xfade transition name and optional parameters.
"""

from __future__ import annotations

from backend.models.enums import TransitionType

# Mapping from our TransitionType enum to FFmpeg xfade transition names
XFADE_MAP: dict[TransitionType, str] = {
    TransitionType.FADE: "fade",
    TransitionType.DISSOLVE: "dissolve",
    TransitionType.WIPE_LEFT: "wipeleft",
    TransitionType.WIPE_RIGHT: "wiperight",
    TransitionType.WIPE_UP: "wipeup",
    TransitionType.WIPE_DOWN: "wipedown",
    TransitionType.SLIDE_LEFT: "slideleft",
    TransitionType.SLIDE_RIGHT: "slideright",
    TransitionType.CIRCLE_CROP: "circlecrop",
    TransitionType.RADIAL: "radial",
    TransitionType.SMOOTHLEFT: "smoothleft",
    TransitionType.SMOOTHRIGHT: "smoothright",
    TransitionType.SMOOTHUP: "smoothup",
    TransitionType.SMOOTHDOWN: "smoothdown",
    TransitionType.CUT: "fade",  # Hard cut: zero-duration fade
}


def get_xfade_name(transition: TransitionType) -> str:
    """Get the FFmpeg xfade transition name for a TransitionType."""
    return XFADE_MAP.get(transition, "fade")


def get_transition_duration(transition: TransitionType, default: float = 0.5) -> float:
    """Get the appropriate duration for a transition type.

    Hard cuts get zero duration, everything else uses the default.
    """
    if transition == TransitionType.CUT:
        return 0.05  # Near-instant but avoids FFmpeg filter issues
    return default


def build_xfade_filter(
    input_a: str,
    input_b: str,
    output: str,
    transition: TransitionType,
    offset: float,
    duration: float = 0.5,
) -> str:
    """Build an FFmpeg xfade filter string.

    Args:
        input_a: Label of the first input stream.
        input_b: Label of the second input stream.
        output: Label for the output stream.
        transition: Transition type.
        offset: Time offset in seconds where transition begins.
        duration: Transition duration in seconds.

    Returns:
        FFmpeg filter string like "[v0][v1]xfade=transition=fade:duration=0.5:offset=4.5[xf1]"
    """
    xfade_name = get_xfade_name(transition)
    actual_duration = get_transition_duration(transition, duration)

    return (
        f"[{input_a}][{input_b}]xfade=transition={xfade_name}"
        f":duration={actual_duration}:offset={offset:.2f}[{output}]"
    )
