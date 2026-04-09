"""Tests for scenario analysis."""
import pytest
from unittest.mock import patch, MagicMock

from models.enums import PipelineMode
from services.scenario.scene_parser import SceneParser
from services.scenario.prompts import SYSTEM_PROMPT_MIXED, SYSTEM_PROMPT_PRODUCT_ONLY


class TestSceneParser:
    def setup_method(self):
        self.parser = SceneParser()

    def test_valid_scene_parsing(self):
        raw = {
            "scenes": [
                {
                    "scene_number": 1,
                    "scene_type": "personnage",
                    "prompt_image": "A woman walking in a field",
                    "prompt_video": "Walking forward motion",
                    "duration_seconds": 4.0,
                    "camera_movement": "tracking",
                    "transition": "dissolve",
                    "needs_mannequin": True,
                    "needs_decor_ref": True,
                    "original_text": "Sophie walks...",
                },
                {
                    "scene_number": 2,
                    "scene_type": "produit",
                    "prompt_image": "Perfume bottle on marble",
                    "prompt_video": "Slow orbit",
                    "duration_seconds": 3.5,
                    "camera_movement": "orbit",
                    "transition": "cut",
                    "needs_mannequin": False,
                    "needs_decor_ref": False,
                },
            ]
        }
        result = self.parser.parse_and_validate(raw, PipelineMode.PERSONNAGE_ET_PRODUIT)
        assert result["total_scenes"] == 2
        assert result["scenes"][0]["scene_type"] == "personnage"
        assert result["scenes"][1]["scene_type"] == "produit"

    def test_force_produit_in_product_only_mode(self):
        raw = {
            "scenes": [
                {
                    "scene_number": 1,
                    "scene_type": "personnage",  # GPT-4o mistake
                    "prompt_image": "test",
                    "prompt_video": "test",
                    "duration_seconds": 4.0,
                }
            ]
        }
        result = self.parser.parse_and_validate(raw, PipelineMode.PRODUIT_UNIQUEMENT)
        assert result["scenes"][0]["scene_type"] == "produit"
        assert result["scenes"][0]["needs_mannequin"] is False

    def test_invalid_scene_type_defaults_to_produit(self):
        raw = {
            "scenes": [
                {
                    "scene_number": 1,
                    "scene_type": "INVALID",
                    "prompt_image": "test",
                    "prompt_video": "test",
                    "duration_seconds": 4.0,
                }
            ]
        }
        result = self.parser.parse_and_validate(raw, PipelineMode.PRODUIT_UNIQUEMENT)
        assert result["scenes"][0]["scene_type"] == "produit"

    def test_duration_clamping(self):
        raw = {
            "scenes": [
                {"scene_type": "produit", "prompt_image": "t", "prompt_video": "t", "duration_seconds": 0.5},
                {"scene_type": "produit", "prompt_image": "t", "prompt_video": "t", "duration_seconds": 99.0},
            ]
        }
        result = self.parser.parse_and_validate(raw, PipelineMode.PRODUIT_UNIQUEMENT)
        assert result["scenes"][0]["duration_seconds"] == 2.0
        assert result["scenes"][1]["duration_seconds"] == 8.0

    def test_empty_scenes_raises(self):
        from pipeline.exceptions import NoScenesError
        with pytest.raises(NoScenesError):
            self.parser.parse_and_validate({"scenes": []}, PipelineMode.PRODUIT_UNIQUEMENT)

    def test_invalid_camera_defaults_to_static(self):
        raw = {"scenes": [{"scene_type": "produit", "prompt_image": "t", "prompt_video": "t", "duration_seconds": 4, "camera_movement": "INVALID"}]}
        result = self.parser.parse_and_validate(raw, PipelineMode.PRODUIT_UNIQUEMENT)
        assert result["scenes"][0]["camera_movement"] == "static"


class TestSystemPrompts:
    def test_mixed_prompt_contains_personnage(self):
        assert "personnage" in SYSTEM_PROMPT_MIXED
        assert "SACRED" in SYSTEM_PROMPT_MIXED

    def test_product_prompt_excludes_personnage(self):
        assert "NEVER use \"personnage\"" in SYSTEM_PROMPT_PRODUCT_ONLY
        assert "SACRED" in SYSTEM_PROMPT_PRODUCT_ONLY
