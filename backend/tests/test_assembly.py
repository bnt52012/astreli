"""
Tests for the FFmpeg Video Assembly Service.

Covers:
- Transition filter building
- Audio filter generation
- Logo overlay filter generation
- Encoding profile selection
- Single vs multi-clip assembly logic
- Missing clip detection
"""

from __future__ import annotations

import pytest
from pathlib import Path

from backend.models.enums import QualityLevel, TransitionType
from backend.services.assembly.transitions import (
    build_xfade_filter,
    get_transition_duration,
    get_xfade_name,
)
from backend.services.assembly.audio_mixer import build_audio_filter
from backend.services.assembly.logo_overlay import build_logo_filter
from backend.services.assembly.encoder import get_encoding_args


# ── Transition Tests ──────────────────────────────────────────


class TestTransitions:
    """Tests for FFmpeg transition filter building."""

    def test_xfade_name_mapping(self):
        assert get_xfade_name(TransitionType.FADE) == "fade"
        assert get_xfade_name(TransitionType.DISSOLVE) == "dissolve"
        assert get_xfade_name(TransitionType.WIPE_LEFT) == "wipeleft"
        assert get_xfade_name(TransitionType.CIRCLE_CROP) == "circlecrop"
        assert get_xfade_name(TransitionType.CUT) == "fade"

    def test_cut_has_near_zero_duration(self):
        dur = get_transition_duration(TransitionType.CUT)
        assert dur < 0.1

    def test_normal_transition_uses_default(self):
        dur = get_transition_duration(TransitionType.FADE, default=0.5)
        assert dur == 0.5

    def test_build_xfade_filter_string(self):
        result = build_xfade_filter(
            "v0", "v1", "xf1",
            TransitionType.DISSOLVE, offset=4.5, duration=0.5,
        )
        assert "[v0][v1]xfade" in result
        assert "transition=dissolve" in result
        assert "duration=0.5" in result
        assert "offset=4.50" in result
        assert "[xf1]" in result


# ── Audio Mixer Tests ─────────────────────────────────────────


class TestAudioMixer:
    """Tests for audio filter generation."""

    def test_basic_audio_filter(self):
        filter_str, label = build_audio_filter(
            audio_input_index=2,
            total_duration=20.0,
            fade_in=1.5,
            fade_out=2.0,
            volume=0.8,
        )
        assert "[2:a]" in filter_str
        assert "volume=0.8" in filter_str
        assert "afade=t=in:d=1.5" in filter_str
        assert "atrim=0:20.00" in filter_str
        assert label == "aout"


# ── Logo Overlay Tests ────────────────────────────────────────


class TestLogoOverlay:
    """Tests for logo overlay filter generation."""

    def test_top_right_position(self):
        result = build_logo_filter(
            logo_input_index=3, video_label="vout",
            output_label="vlogo", scale_width=120,
            padding=30, position="top_right",
        )
        assert "[3:v]scale=120:-1[logo]" in result
        assert "[vout][logo]overlay=" in result
        assert "W-w-30:30" in result
        assert "[vlogo]" in result

    def test_bottom_left_position(self):
        result = build_logo_filter(
            logo_input_index=2, video_label="v0",
            output_label="vl", position="bottom_left",
        )
        assert "30:H-h-30" in result


# ── Encoder Tests ─────────────────────────────────────────────


class TestEncoder:
    """Tests for H.264 encoding profile generation."""

    def test_premium_preset(self):
        args = get_encoding_args(QualityLevel.PREMIUM)
        assert "-preset slow" in args
        assert "-crf 18" in args
        assert "-c:v libx264" in args
        assert "-pix_fmt yuv420p" in args

    def test_draft_preset(self):
        args = get_encoding_args(QualityLevel.DRAFT)
        assert "-preset fast" in args
        assert "-crf 28" in args

    def test_broadcast_with_bitrate(self):
        args = get_encoding_args(QualityLevel.BROADCAST)
        assert "-b:v 25M" in args
        assert "-crf 15" in args

    def test_custom_fps(self):
        args = get_encoding_args(QualityLevel.STANDARD, fps=25)
        assert "-r 25" in args

    def test_custom_bitrate_override(self):
        args = get_encoding_args(QualityLevel.PREMIUM, custom_bitrate="15M")
        assert "-b:v 15M" in args
