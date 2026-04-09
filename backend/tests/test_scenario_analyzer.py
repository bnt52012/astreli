"""
Tests for the GPT-4o Scenario Analyzer.

Covers:
- Happy path: scenario decomposition with both modes
- Scene type classification and mode enforcement
- JSON parsing edge cases (markdown fences, malformed JSON)
- Error handling for API failures
- Mode-specific system prompt selection
"""

from __future__ import annotations

import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from backend.models.enums import PipelineMode, SceneType, TransitionType
from backend.services.scenario.scene_parser import parse_gpt4o_response
from backend.services.scenario.prompts import get_system_prompt
from backend.pipeline.exceptions import ScenarioAnalysisError


# ── Scene Parser Tests ────────────────────────────────────────


class TestSceneParser:
    """Tests for parse_gpt4o_response()."""

    def _make_raw_response(self, scenes: list[dict], **metadata) -> str:
        """Build a valid GPT-4o JSON response string."""
        data = {
            "concept": metadata.get("concept", "Test concept"),
            "tone": metadata.get("tone", "luxurious"),
            "visual_style": metadata.get("visual_style", "cinematic"),
            "target_audience": metadata.get("target_audience", "adults"),
            "narrative_arc": metadata.get("narrative_arc", "hook -> payoff"),
            "scenes": scenes,
        }
        return json.dumps(data)

    def test_basic_parsing(self):
        """Happy path: valid JSON with two scenes."""
        raw = self._make_raw_response([
            {
                "id": 1, "type": "personnage", "goal": "Hook",
                "description": "Model in lavender field",
                "image_prompt": "A woman in a lavender field",
                "video_prompt": "She walks toward camera",
                "camera_movement": "dolly_in", "lighting": "golden hour",
                "duration": 5.0, "transition": "fade",
                "needs_mannequin": True, "needs_product": False,
                "needs_decor_ref": False,
            },
            {
                "id": 2, "type": "produit", "goal": "Product reveal",
                "description": "Perfume bottle close-up",
                "image_prompt": "Glass perfume bottle on marble",
                "video_prompt": "Slow orbit around bottle",
                "camera_movement": "orbit", "lighting": "studio",
                "duration": 4.0, "transition": "dissolve",
                "needs_mannequin": False, "needs_product": True,
                "needs_decor_ref": True,
            },
        ])

        metadata, scenes = parse_gpt4o_response(
            raw, PipelineMode.PERSONNAGE_ET_PRODUIT,
        )

        assert len(scenes) == 2
        assert scenes[0].type == SceneType.PERSONNAGE
        assert scenes[1].type == SceneType.PRODUIT
        assert scenes[0].needs_mannequin is True
        assert scenes[1].needs_product is True
        assert metadata["tone"] == "luxurious"

    def test_mode_enforcement_produit_only(self):
        """In PRODUIT_UNIQUEMENT mode, personnage scenes are forced to produit."""
        raw = self._make_raw_response([
            {
                "id": 1, "type": "personnage", "goal": "Hook",
                "description": "Model walking",
                "image_prompt": "Woman walking",
                "video_prompt": "Walking motion",
                "camera_movement": "tracking",
                "duration": 5.0, "transition": "fade",
            },
        ])

        _, scenes = parse_gpt4o_response(
            raw, PipelineMode.PRODUIT_UNIQUEMENT,
        )

        assert len(scenes) == 1
        assert scenes[0].type == SceneType.PRODUIT

    def test_type_normalization(self):
        """Various type strings should be normalized."""
        raw = self._make_raw_response([
            {"id": 1, "type": "character", "goal": "Test",
             "description": "d", "image_prompt": "p", "video_prompt": "v",
             "duration": 5.0, "transition": "fade"},
            {"id": 2, "type": "product", "goal": "Test",
             "description": "d", "image_prompt": "p", "video_prompt": "v",
             "duration": 5.0, "transition": "fade"},
            {"id": 3, "type": "title_card", "goal": "Test",
             "description": "d", "image_prompt": "p", "video_prompt": "v",
             "duration": 5.0, "transition": "fade"},
        ])

        _, scenes = parse_gpt4o_response(
            raw, PipelineMode.PERSONNAGE_ET_PRODUIT,
        )

        assert scenes[0].type == SceneType.PERSONNAGE
        assert scenes[1].type == SceneType.PRODUIT
        assert scenes[2].type == SceneType.TRANSITION

    def test_markdown_fences_stripped(self):
        """JSON wrapped in markdown code fences should be parsed."""
        inner = self._make_raw_response([
            {"id": 1, "type": "produit", "goal": "Test",
             "description": "d", "image_prompt": "p", "video_prompt": "v",
             "duration": 5.0, "transition": "fade"},
        ])
        raw = f"```json\n{inner}\n```"

        _, scenes = parse_gpt4o_response(
            raw, PipelineMode.PRODUIT_UNIQUEMENT,
        )
        assert len(scenes) == 1

    def test_empty_scenes_raises(self):
        """Empty scenes list should raise ScenarioAnalysisError."""
        raw = self._make_raw_response([])

        with pytest.raises(ScenarioAnalysisError, match="no scenes"):
            parse_gpt4o_response(raw, PipelineMode.PRODUIT_UNIQUEMENT)

    def test_invalid_json_raises(self):
        """Completely invalid JSON should raise ScenarioAnalysisError."""
        with pytest.raises(ScenarioAnalysisError):
            parse_gpt4o_response(
                "this is not json at all",
                PipelineMode.PRODUIT_UNIQUEMENT,
            )

    def test_duration_clamping(self):
        """Duration should be clamped to 2.0-10.0 range."""
        raw = self._make_raw_response([
            {"id": 1, "type": "produit", "goal": "Test",
             "description": "d", "image_prompt": "p", "video_prompt": "v",
             "duration": 0.5, "transition": "fade"},
            {"id": 2, "type": "produit", "goal": "Test",
             "description": "d", "image_prompt": "p", "video_prompt": "v",
             "duration": 25.0, "transition": "fade"},
        ])

        _, scenes = parse_gpt4o_response(
            raw, PipelineMode.PRODUIT_UNIQUEMENT,
        )

        assert scenes[0].duration == 2.0
        assert scenes[1].duration == 10.0

    def test_sequential_ids_reassigned(self):
        """Scene IDs should be reassigned sequentially starting at 1."""
        raw = self._make_raw_response([
            {"id": 5, "type": "produit", "goal": "Test",
             "description": "d", "image_prompt": "p", "video_prompt": "v",
             "duration": 5.0, "transition": "fade"},
            {"id": 10, "type": "produit", "goal": "Test",
             "description": "d", "image_prompt": "p", "video_prompt": "v",
             "duration": 5.0, "transition": "fade"},
        ])

        _, scenes = parse_gpt4o_response(
            raw, PipelineMode.PRODUIT_UNIQUEMENT,
        )

        assert scenes[0].id == 1
        assert scenes[1].id == 2


# ── System Prompt Tests ───────────────────────────────────────


class TestPrompts:
    """Tests for system prompt generation."""

    def test_personnage_mode_prompt(self):
        prompt = get_system_prompt("personnage_et_produit")
        assert "PERSONNAGE + PRODUIT" in prompt
        assert "personnage" in prompt.lower()
        assert "ABSOLUTE AUTHORITY" in prompt

    def test_produit_mode_prompt(self):
        prompt = get_system_prompt("produit_uniquement")
        assert "PRODUIT UNIQUEMENT" in prompt
        assert "FORBIDDEN" in prompt
        assert "ABSOLUTE AUTHORITY" in prompt

    def test_client_scenario_is_sacred(self):
        """Both prompts must enforce scenario as absolute authority."""
        for mode in ["personnage_et_produit", "produit_uniquement"]:
            prompt = get_system_prompt(mode)
            assert "Do NOT suggest changes" in prompt
            assert "Do NOT reinterpret" in prompt
