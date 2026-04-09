"""Tests for knowledge engine and industry detection."""
import pytest
from knowledge.industry_detector import IndustryDetector
from knowledge.knowledge_engine import KnowledgeEngine


class TestIndustryDetector:
    def setup_method(self):
        self.detector = IndustryDetector()

    def test_detect_luxury(self):
        result = self.detector.detect("A luxurious gold watch on marble surface, heritage craftsmanship")
        assert result.industry == "luxury" or result.industry == "jewelry_watches"
        assert result.confidence > 0.3

    def test_detect_beauty(self):
        result = self.detector.detect("Apply the serum on clean skin for a radiant glow, moisturizer cream")
        assert result.industry == "beauty"

    def test_detect_automotive(self):
        result = self.detector.detect("The car races down the highway, engine roaring, 0-60 in 3 seconds")
        assert result.industry == "automotive"

    def test_detect_food(self):
        result = self.detector.detect("Fresh pasta being prepared by the chef, wine pairing, gourmet cuisine")
        assert result.industry == "food_beverage"

    def test_detect_tech(self):
        result = self.detector.detect("The smartphone features a 120Hz OLED display with AI-powered camera")
        assert result.industry == "tech"

    def test_detect_fragrance(self):
        result = self.detector.detect("A new perfume with top notes of bergamot and base notes of oud and sandalwood")
        assert result.industry == "fragrance"

    def test_default_to_luxury(self):
        result = self.detector.detect("Something completely unrelated with no keywords")
        assert result.industry == "luxury"
        assert result.confidence == 0.3

    def test_hybrid_detection(self):
        results = self.detector.detect_hybrid(
            "A fashion model wearing a luxury dress sprays perfume in a lavender field"
        )
        assert len(results) >= 1


class TestKnowledgeEngine:
    def setup_method(self):
        self.engine = KnowledgeEngine()

    def test_detect_industry(self):
        result = self.engine.detect_industry("luxury perfume campaign")
        assert result.industry in ["luxury", "fragrance"]

    def test_get_patterns(self):
        patterns = self.engine.get_industry_patterns("luxury")
        assert "prompt_modifiers" in patterns
        assert "lighting_preferences" in patterns
        assert len(patterns["prompt_modifiers"]) >= 10

    def test_image_enrichment(self):
        from intelligence.scene_understanding import SceneContext
        ctx = SceneContext(implied_framing="close_up", time_of_day="golden_hour")
        enrichment = self.engine.get_image_enrichment("luxury", ctx, "portrait")
        assert len(enrichment) > 50
        assert "8K" in enrichment
