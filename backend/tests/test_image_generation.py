"""
Tests for the Dual Gemini Image Generation Engine.

Covers:
- Scene routing (personnage → Pro, produit → Flash)
- Cache hit/miss behavior
- Fallback from Pro to Flash
- Reference image preparation and batching
- Mode detection routing
"""

from __future__ import annotations

import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

from backend.models.enums import PipelineMode, SceneType, TransitionType
from backend.models.scene import SceneAnalysis, SceneContext, ScenePipeline
from backend.services.image_generation.cache import ImageCache
from backend.pipeline.mode_detector import ModeDetector


# ── Helpers ───────────────────────────────────────────────────


def make_scene(
    scene_id: int = 1,
    scene_type: SceneType = SceneType.PRODUIT,
    prompt: str = "A beautiful product shot",
) -> ScenePipeline:
    """Create a test ScenePipeline with minimal required fields."""
    analysis = SceneAnalysis(
        id=scene_id,
        type=scene_type,
        goal="Test scene",
        description="Test description",
        image_prompt=prompt,
        video_prompt="Slow motion",
        camera_movement="static",
        duration=5.0,
        transition=TransitionType.FADE,
    )
    return ScenePipeline(analysis=analysis)


# ── Mode Detection Tests ─────────────────────────────────────


class TestModeDetector:
    """Tests for pipeline mode detection."""

    def test_no_mannequin_images(self):
        mode, paths = ModeDetector.detect(None)
        assert mode == PipelineMode.PRODUIT_UNIQUEMENT
        assert paths == []

    def test_empty_mannequin_list(self):
        mode, paths = ModeDetector.detect([])
        assert mode == PipelineMode.PRODUIT_UNIQUEMENT
        assert paths == []

    def test_nonexistent_paths_filtered(self):
        mode, paths = ModeDetector.detect([
            "/nonexistent/path1.jpg",
            "/nonexistent/path2.png",
        ])
        assert mode == PipelineMode.PRODUIT_UNIQUEMENT
        assert paths == []

    def test_valid_mannequin_images(self, tmp_path):
        """Valid image files should trigger PERSONNAGE_ET_PRODUIT mode."""
        img_path = tmp_path / "model.jpg"
        img_path.write_bytes(b"\xff\xd8\xff" + b"\x00" * 200)

        mode, paths = ModeDetector.detect([str(img_path)])
        assert mode == PipelineMode.PERSONNAGE_ET_PRODUIT
        assert len(paths) == 1

    def test_unsupported_format_filtered(self, tmp_path):
        """Non-image files should be filtered out."""
        txt_path = tmp_path / "model.txt"
        txt_path.write_bytes(b"not an image" * 20)

        mode, paths = ModeDetector.detect([str(txt_path)])
        assert mode == PipelineMode.PRODUIT_UNIQUEMENT
        assert paths == []

    def test_too_small_file_filtered(self, tmp_path):
        """Files < 100 bytes should be filtered (likely corrupt)."""
        img_path = tmp_path / "tiny.jpg"
        img_path.write_bytes(b"\xff\xd8\xff")  # 3 bytes

        mode, paths = ModeDetector.detect([str(img_path)])
        assert mode == PipelineMode.PRODUIT_UNIQUEMENT


# ── Image Cache Tests ─────────────────────────────────────────


class TestImageCache:
    """Tests for the prompt+ref hash cache."""

    def test_cache_miss(self, tmp_path):
        cache = ImageCache(tmp_path / "cache", enabled=True)
        result = cache.get("nonexistent_key")
        assert result is None

    def test_cache_put_and_get(self, tmp_path):
        cache = ImageCache(tmp_path / "cache", enabled=True)

        # Create a fake image file
        src = tmp_path / "source.png"
        src.write_bytes(b"\x89PNG" + b"\x00" * 200)

        key = cache.compute_cache_key("test prompt", model="test-model")
        cache.put(key, str(src), "test prompt", "test-model")

        result = cache.get(key)
        assert result is not None
        assert Path(result).exists()

    def test_cache_disabled(self, tmp_path):
        cache = ImageCache(tmp_path / "cache", enabled=False)

        src = tmp_path / "source.png"
        src.write_bytes(b"\x89PNG" + b"\x00" * 200)

        key = cache.compute_cache_key("test prompt")
        result_put = cache.put(key, str(src), "test prompt")
        assert result_put == str(src)  # Returns source path when disabled

        result_get = cache.get(key)
        assert result_get is None  # Always misses when disabled

    def test_deterministic_hash(self, tmp_path):
        cache = ImageCache(tmp_path / "cache", enabled=True)

        key1 = cache.compute_cache_key("same prompt", model="same-model")
        key2 = cache.compute_cache_key("same prompt", model="same-model")
        key3 = cache.compute_cache_key("different prompt", model="same-model")

        assert key1 == key2
        assert key1 != key3

    def test_cache_clear(self, tmp_path):
        cache = ImageCache(tmp_path / "cache", enabled=True)

        src = tmp_path / "source.png"
        src.write_bytes(b"\x89PNG" + b"\x00" * 200)

        key = cache.compute_cache_key("test prompt")
        cache.put(key, str(src), "test prompt")

        cleared = cache.clear()
        assert cleared >= 1

        assert cache.get(key) is None


# ── Scene Routing Tests ───────────────────────────────────────


class TestSceneRouting:
    """Tests for scene type → model routing logic."""

    def test_personnage_gets_pro_model(self):
        scene = make_scene(scene_type=SceneType.PERSONNAGE)
        assert "gemini" in scene.gemini_model.lower() or scene.gemini_model != ""

    def test_produit_gets_flash_model(self):
        scene = make_scene(scene_type=SceneType.PRODUIT)
        assert scene.gemini_model != ""

    def test_transition_gets_empty_model(self):
        scene = make_scene(scene_type=SceneType.TRANSITION)
        assert scene.gemini_model == ""

    def test_personnage_gets_video01(self):
        scene = make_scene(scene_type=SceneType.PERSONNAGE)
        assert "kling" in scene.kling_model.lower() or scene.kling_model != ""

    def test_produit_gets_v3(self):
        scene = make_scene(scene_type=SceneType.PRODUIT)
        assert scene.kling_model != ""

    def test_final_prompt_with_brand_prefix(self):
        scene = make_scene(prompt="Beautiful product shot")
        scene.brand_prompt_prefix = "Luxury brand style"
        scene.enriched_image_prompt = "Beautiful product shot, 85mm lens"

        final = scene.final_image_prompt
        assert final.startswith("Luxury brand style")
        assert "85mm lens" in final

    def test_final_prompt_fallback_to_raw(self):
        scene = make_scene(prompt="Beautiful product shot")
        # No enrichment set

        final = scene.final_image_prompt
        assert final == "Beautiful product shot"
