"""Tests for LoRA fusion pipeline."""
import pytest
from unittest.mock import patch, MagicMock
from pathlib import Path

from utils.image_utils import create_face_mask, get_aspect_ratio_dimensions


class TestFaceMask:
    def test_default_mask_creation(self):
        mask = create_face_mask((1024, 1024))
        assert mask.size == (1024, 1024)
        assert mask.mode == "L"

    def test_custom_center_mask(self):
        mask = create_face_mask((512, 512), face_center=(256, 128), face_radius=50)
        assert mask.size == (512, 512)


class TestAspectRatio:
    def test_known_ratios(self):
        assert get_aspect_ratio_dimensions("16:9") == (1024, 576)
        assert get_aspect_ratio_dimensions("9:16") == (576, 1024)
        assert get_aspect_ratio_dimensions("1:1") == (1024, 1024)

    def test_unknown_ratio_defaults(self):
        assert get_aspect_ratio_dimensions("3:2") == (1024, 1024)
