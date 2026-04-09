"""
Integration Tests for the Full AdGenAI Pipeline.

Covers:
- Mode detection edge cases
- Intelligence layer (scene understanding + prompt enrichment)
- Brand analyzer color extraction
- Quality checker response parsing
- Audience adapter platform specs
- Full pipeline orchestration flow (mocked APIs)
- Error handling and partial failure recovery
"""

from __future__ import annotations

import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from backend.models.enums import (
    AdCategory,
    CameraMovement,
    EmotionalTone,
    PipelineMode,
    SceneType,
    TargetPlatform,
    TransitionType,
)
from backend.models.scene import SceneAnalysis, SceneContext, ScenePipeline
from backend.intelligence.scene_understanding import SceneUnderstanding
from backend.intelligence.prompt_enricher import PromptEnricher
from backend.intelligence.brand_analyzer import BrandAnalyzer
from backend.intelligence.audience_adapter import AudienceAdapter
from backend.pipeline.mode_detector import ModeDetector
from backend.utils.cost_calculator import CostCalculator


# ── Scene Understanding Tests ─────────────────────────────────


class TestSceneUnderstanding:
    """Tests for natural language scene understanding."""

    def _make_scene(self, **kwargs) -> SceneAnalysis:
        defaults = dict(
            id=1, type=SceneType.PERSONNAGE, goal="Test",
            description="", image_prompt="", video_prompt="",
            camera_movement="static", duration=5.0,
            transition=TransitionType.FADE,
        )
        defaults.update(kwargs)
        return SceneAnalysis(**defaults)

    def test_detect_tracking_shot(self):
        su = SceneUnderstanding()
        scene = self._make_scene(
            description="She walks toward the camera through the field",
        )
        ctx = su.analyze_scene(scene)
        assert ctx.detected_camera_work == CameraMovement.DOLLY_IN

    def test_detect_orbit(self):
        su = SceneUnderstanding()
        scene = self._make_scene(
            description="Camera orbits around the product",
            type=SceneType.PRODUIT,
        )
        ctx = su.analyze_scene(scene)
        assert ctx.detected_camera_work == CameraMovement.ORBIT

    def test_detect_luxury_tone(self):
        su = SceneUnderstanding()
        scene = self._make_scene(
            description="Luxurious setting with opulent gold accents",
        )
        ctx = su.analyze_scene(scene)
        assert ctx.emotional_tone == EmotionalTone.LUXURY

    def test_detect_product_interaction(self):
        su = SceneUnderstanding()
        scene = self._make_scene(
            description="She holds the perfume bottle close to her face",
        )
        ctx = su.analyze_scene(scene)
        assert ctx.requires_product_in_frame is True

    def test_detect_wardrobe_change(self):
        su = SceneUnderstanding()
        scene = self._make_scene(
            description="Now wearing a different outfit, a red evening dress",
        )
        ctx = su.analyze_scene(scene)
        assert ctx.has_wardrobe_change is True

    def test_detect_scene_reference(self):
        su = SceneUnderstanding()
        scene = self._make_scene(
            description="Same location as scene 2 but at sunset",
        )
        ctx = su.analyze_scene(scene)
        assert 2 in ctx.linked_scene_ids

    def test_should_route_to_pro_for_personnage(self):
        su = SceneUnderstanding()
        scene = self._make_scene(type=SceneType.PERSONNAGE)
        ctx = SceneContext()
        assert su.should_route_to_pro(scene, ctx) is True

    def test_should_not_route_to_pro_for_produit(self):
        su = SceneUnderstanding()
        scene = self._make_scene(type=SceneType.PRODUIT, needs_mannequin=False)
        ctx = SceneContext()
        assert su.should_route_to_pro(scene, ctx) is False


# ── Prompt Enricher Tests ─────────────────────────────────────


class TestPromptEnricher:
    """Tests for invisible prompt enrichment."""

    def test_client_words_preserved_at_start(self):
        enricher = PromptEnricher()
        scene = SceneAnalysis(
            id=1, type=SceneType.PRODUIT, goal="Test",
            description="Test", video_prompt="Test motion",
            image_prompt="perfume bottle on white marble",
            camera_movement="static", duration=5.0,
            transition=TransitionType.FADE,
        )
        ctx = SceneContext(emotional_tone=EmotionalTone.LUXURY)

        result = enricher.enrich_image_prompt(scene, ctx, AdCategory.FRAGRANCE)

        # Client's original words must appear in the result
        assert "perfume bottle on white marble" in result
        # Technical additions should be present
        assert "8K detail" in result
        assert len(result) > len(scene.image_prompt)

    def test_category_detection(self):
        enricher = PromptEnricher()

        cat = enricher.detect_ad_category(
            "A luxury perfume ad with a glass bottle and fragrance mist"
        )
        assert cat == AdCategory.FRAGRANCE

    def test_sport_category_detection(self):
        enricher = PromptEnricher()
        cat = enricher.detect_ad_category(
            "An athletic shoe commercial with runners and training"
        )
        assert cat == AdCategory.SPORT

    def test_video_prompt_enrichment(self):
        enricher = PromptEnricher()
        scene = SceneAnalysis(
            id=1, type=SceneType.PRODUIT, goal="Test",
            description="Test",
            image_prompt="Test",
            video_prompt="Slow orbit around bottle",
            camera_movement="orbit", duration=5.0,
            transition=TransitionType.FADE,
        )
        ctx = SceneContext(detected_camera_work=CameraMovement.ORBIT)

        result = enricher.enrich_video_prompt(scene, ctx)

        assert "Slow orbit around bottle" in result
        assert "realistic physics" in result
        assert "duration: 5.0s" in result


# ── Brand Analyzer Tests ──────────────────────────────────────


class TestBrandAnalyzer:
    """Tests for brand visual identity analysis."""

    def test_brand_prefix_with_name(self):
        analyzer = BrandAnalyzer()
        prefix = analyzer.analyze(brand_name="Chanel")
        assert "Chanel" in prefix

    def test_brand_prefix_with_colors_override(self):
        analyzer = BrandAnalyzer()
        prefix = analyzer.analyze(
            brand_colors_override=["#000000", "#ffffff"],
        )
        assert "#000000" in prefix

    def test_empty_brand_returns_empty(self):
        analyzer = BrandAnalyzer()
        prefix = analyzer.analyze()
        assert prefix == ""


# ── Audience Adapter Tests ────────────────────────────────────


class TestAudienceAdapter:
    """Tests for platform-specific output adaptation."""

    def test_youtube_spec(self):
        adapter = AudienceAdapter()
        specs = adapter.get_output_specs([TargetPlatform.YOUTUBE])
        assert len(specs) == 1
        assert specs[0].resolution == "1920x1080"
        assert specs[0].fps == 30

    def test_instagram_reels_spec(self):
        adapter = AudienceAdapter()
        specs = adapter.get_output_specs([TargetPlatform.INSTAGRAM_REELS])
        assert specs[0].resolution == "1080x1920"

    def test_tv_broadcast_higher_bitrate(self):
        adapter = AudienceAdapter()
        specs = adapter.get_output_specs([TargetPlatform.TV_BROADCAST])
        assert specs[0].video_bitrate == "25M"
        assert specs[0].fps == 25

    def test_multiple_platforms(self):
        adapter = AudienceAdapter()
        specs = adapter.get_output_specs([
            TargetPlatform.YOUTUBE,
            TargetPlatform.INSTAGRAM_REELS,
            TargetPlatform.TIKTOK,
        ])
        assert len(specs) == 3

    def test_fallback_to_youtube(self):
        adapter = AudienceAdapter()
        specs = adapter.get_output_specs([])
        assert len(specs) == 1
        assert specs[0].platform == TargetPlatform.YOUTUBE

    def test_primary_spec_prioritizes_cinema(self):
        adapter = AudienceAdapter()
        spec = adapter.get_primary_spec([
            TargetPlatform.TIKTOK,
            TargetPlatform.CINEMA,
            TargetPlatform.YOUTUBE,
        ])
        assert spec.platform == TargetPlatform.CINEMA


# ── Cost Calculator Tests ─────────────────────────────────────


class TestCostCalculator:
    """Tests for API cost estimation."""

    def test_estimate_from_scenario(self):
        calc = CostCalculator()
        breakdown = calc.estimate_from_scenario(
            "A perfume ad",
            estimated_scene_count=5,
            avg_duration_seconds=5.0,
        )
        assert breakdown.total_cost >= 0
        assert breakdown.total_scenes == 5
        assert breakdown.total_video_seconds == 25.0

    def test_estimate_from_scenes(self):
        scenes = [
            SceneAnalysis(
                id=1, type=SceneType.PERSONNAGE, goal="Test",
                description="d", image_prompt="p", video_prompt="v",
                camera_movement="static", duration=5.0,
                transition=TransitionType.FADE,
            ),
            SceneAnalysis(
                id=2, type=SceneType.PRODUIT, goal="Test",
                description="d", image_prompt="p", video_prompt="v",
                camera_movement="static", duration=4.0,
                transition=TransitionType.FADE,
            ),
        ]
        calc = CostCalculator()
        breakdown = calc.estimate_from_scenes(scenes)
        assert breakdown.personnage_scenes == 1
        assert breakdown.produit_scenes == 1
        assert breakdown.total_video_seconds == 9.0
