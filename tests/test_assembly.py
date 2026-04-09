"""Tests for video assembly."""
import pytest
from services.assembly.transitions import TransitionBuilder
from services.assembly.audio_mixer import AudioMixer
from services.assembly.logo_overlay import LogoOverlay
from models.enums import TransitionType


class TestTransitionBuilder:
    def setup_method(self):
        self.builder = TransitionBuilder()

    def test_cut_returns_empty(self):
        assert self.builder.build_filter(TransitionType.CUT) == ""

    def test_fade_returns_filter(self):
        result = self.builder.build_filter(TransitionType.FADE, duration=0.5, offset=3.0)
        assert "fade" in result

    def test_xfade_dissolve(self):
        result = self.builder.build_xfade(TransitionType.DISSOLVE, duration=0.5, offset=3.0)
        assert "dissolve" in result
        assert "xfade" in result


class TestAudioMixer:
    def test_fade_filter(self):
        mixer = AudioMixer()
        result = mixer.build_fade_filter(total_duration=30.0, fade_in=1.0, fade_out=2.0, volume=0.3)
        assert "volume=0.3" in result
        assert "afade=t=in" in result
        assert "afade=t=out" in result


class TestLogoOverlay:
    def test_build_filter(self):
        overlay = LogoOverlay()
        result = overlay.build_filter("/tmp/logo.png", position="top_right")
        assert "overlay" in result
        assert "[logo]" in result
