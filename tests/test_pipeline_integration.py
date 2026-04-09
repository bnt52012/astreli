"""Integration tests for pipeline components."""
import pytest
from models.enums import PipelineMode
from models.scene import ScenePipeline, SceneType
from pipeline.mode_detector import ModeDetector
from pipeline.config import PIPELINE_DEFAULTS
from utils.cost_calculator import CostCalculator


class TestModeDetector:
    def test_detect_personnage_mode(self):
        mode = ModeDetector.detect("owner/model:version123")
        assert mode == PipelineMode.PERSONNAGE_ET_PRODUIT

    def test_detect_product_mode(self):
        mode = ModeDetector.detect(None)
        assert mode == PipelineMode.PRODUIT_UNIQUEMENT

    def test_detect_empty_string(self):
        mode = ModeDetector.detect("")
        assert mode == PipelineMode.PRODUIT_UNIQUEMENT

    def test_force_produit(self):
        result = ModeDetector.should_force_produit("personnage", PipelineMode.PRODUIT_UNIQUEMENT)
        assert result == "produit"

    def test_no_force_in_mixed_mode(self):
        result = ModeDetector.should_force_produit("personnage", PipelineMode.PERSONNAGE_ET_PRODUIT)
        assert result == "personnage"


class TestScenePipeline:
    def test_scene_properties(self):
        scene = ScenePipeline(index=1, scene_type=SceneType.PERSONNAGE)
        assert scene.is_personnage
        assert not scene.is_produit
        assert not scene.is_transition

    def test_mark_failed(self):
        scene = ScenePipeline(index=1)
        scene.mark_failed("test error")
        assert scene.failed
        assert scene.failure_reason == "test error"

    def test_to_dict(self):
        scene = ScenePipeline(index=1, scene_type=SceneType.PRODUIT, duration_seconds=3.5)
        d = scene.to_dict()
        assert d["index"] == 1
        assert d["scene_type"] == "produit"
        assert d["duration_seconds"] == 3.5

    def test_cost_tracking(self):
        scene = ScenePipeline(index=1, cost_image=0.05, cost_video=0.30)
        assert scene.total_cost == 0.35


class TestCostCalculator:
    def test_estimate(self):
        calc = CostCalculator()
        costs = calc.estimate_pipeline(
            total_scenes=5,
            personnage_scenes=2,
            produit_scenes=2,
            transition_scenes=1,
        )
        assert "total" in costs
        assert costs["total"] > 0
        assert costs["personnage_images"] > costs["produit_images"]

    def test_tracking(self):
        calc = CostCalculator()
        calc.track("images", 0.50)
        calc.track("images", 0.30)
        calc.track("videos", 1.20)
        tracked = calc.get_tracked()
        assert tracked["images"] == 0.80
        assert tracked["videos"] == 1.20
        assert tracked["total"] == 2.00


class TestPipelineDefaults:
    def test_defaults_exist(self):
        assert PIPELINE_DEFAULTS.openai_model == "gpt-4o"
        assert PIPELINE_DEFAULTS.kling_model_human == "kling-video-01"
        assert PIPELINE_DEFAULTS.kling_model_product == "kling-v3"
        assert PIPELINE_DEFAULTS.ffmpeg_crf == 18
        assert PIPELINE_DEFAULTS.quality_threshold == 7.0
        assert PIPELINE_DEFAULTS.max_quality_retries == 3
