"""Tests for image generation engine."""
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock

from models.enums import SceneType, CameraMovement, TransitionType
from models.scene import ScenePipeline
from services.image_generation.engine import ImageGenerationEngine
from services.image_generation.cache import ImageCache


class TestImageCache:
    def test_compute_key(self):
        cache = ImageCache(enabled=False)
        key1 = cache.compute_key("test prompt 1")
        key2 = cache.compute_key("test prompt 2")
        key3 = cache.compute_key("test prompt 1")
        assert key1 != key2
        assert key1 == key3

    def test_cache_disabled(self):
        cache = ImageCache(enabled=False)
        assert cache.get("key") is None
        cache.put("key", Path("/tmp/test.png"))
        assert cache.get("key") is None


class TestImageGenerationEngine:
    def test_transition_skipped(self):
        engine = ImageGenerationEngine()
        scene = ScenePipeline(index=1, scene_type=SceneType.TRANSITION)
        import asyncio
        result = asyncio.run(
            engine.generate_scene_image(scene, Path("/tmp"))
        )
        assert result is None

    def test_mannequin_prompt_building(self):
        engine = ImageGenerationEngine(lora_model_id="test/model:v1", lora_trigger_word="SOPHIE")
        prompt = engine._build_mannequin_prompt(
            "A woman sitting in a cafe with golden hour warm light, close-up", ScenePipeline()
        )
        assert "SOPHIE" in prompt
        assert "sitting" in prompt.lower()


class TestReferenceManager:
    def test_empty_references(self):
        from services.image_generation.reference_manager import ReferenceManager
        mgr = ReferenceManager()
        result = mgr.prepare_references(None, None)
        assert result == []
