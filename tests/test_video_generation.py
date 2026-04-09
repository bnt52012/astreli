"""Tests for video generation."""
import pytest
from models.enums import SceneType
from models.scene import ScenePipeline


class TestVideoAnimator:
    def test_transition_skipped(self):
        scene = ScenePipeline(index=1, scene_type=SceneType.TRANSITION)
        assert scene.is_transition
        assert not scene.is_personnage

    def test_model_selection_personnage(self):
        from pipeline.config import PIPELINE_DEFAULTS
        scene = ScenePipeline(index=1, scene_type=SceneType.PERSONNAGE)
        model = (
            PIPELINE_DEFAULTS.kling_model_human
            if scene.scene_type == SceneType.PERSONNAGE
            else PIPELINE_DEFAULTS.kling_model_product
        )
        assert model == "kling-video-01"

    def test_model_selection_produit(self):
        from pipeline.config import PIPELINE_DEFAULTS
        scene = ScenePipeline(index=1, scene_type=SceneType.PRODUIT)
        model = (
            PIPELINE_DEFAULTS.kling_model_human
            if scene.scene_type == SceneType.PERSONNAGE
            else PIPELINE_DEFAULTS.kling_model_product
        )
        assert model == "kling-v3"
