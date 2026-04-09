"""
Cost estimation for AdGenAI pipeline runs.

Calculates expected API costs BEFORE running the pipeline
so clients can approve or adjust before committing resources.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from backend.models.enums import SceneType
from backend.models.scene import SceneAnalysis
from backend.pipeline.config import APICostRates, DEFAULT_COST_RATES

logger = logging.getLogger(__name__)


@dataclass
class CostBreakdown:
    """Itemized cost estimate for a pipeline run."""

    # Per-step costs (USD)
    scenario_analysis_cost: float = 0.0
    prompt_enrichment_cost: float = 0.0
    image_generation_cost: float = 0.0
    video_generation_cost: float = 0.0
    quality_check_cost: float = 0.0

    # Scene counts
    total_scenes: int = 0
    personnage_scenes: int = 0
    produit_scenes: int = 0
    transition_scenes: int = 0

    # Video seconds
    total_video_seconds: float = 0.0

    @property
    def total_cost(self) -> float:
        """Total estimated cost in USD."""
        return (
            self.scenario_analysis_cost
            + self.prompt_enrichment_cost
            + self.image_generation_cost
            + self.video_generation_cost
            + self.quality_check_cost
        )

    def to_dict(self) -> dict:
        """Serialize for API response or report."""
        return {
            "total_cost_usd": round(self.total_cost, 4),
            "breakdown": {
                "scenario_analysis": round(self.scenario_analysis_cost, 4),
                "prompt_enrichment": round(self.prompt_enrichment_cost, 4),
                "image_generation": round(self.image_generation_cost, 4),
                "video_generation": round(self.video_generation_cost, 4),
                "quality_check": round(self.quality_check_cost, 4),
            },
            "scenes": {
                "total": self.total_scenes,
                "personnage": self.personnage_scenes,
                "produit": self.produit_scenes,
                "transition": self.transition_scenes,
            },
            "total_video_seconds": round(self.total_video_seconds, 1),
        }


class CostCalculator:
    """Estimates pipeline costs based on scene analysis.

    Call estimate_from_scenes() after GPT-4o analysis to get a cost
    breakdown before committing to image/video generation.
    """

    def __init__(self, rates: APICostRates | None = None) -> None:
        self.rates = rates or DEFAULT_COST_RATES

    def estimate_from_scenario(
        self,
        scenario_text: str,
        estimated_scene_count: int = 5,
        avg_duration_seconds: float = 5.0,
        quality_check_enabled: bool = True,
    ) -> CostBreakdown:
        """Quick estimate before scenario analysis runs.

        Uses rough estimates since we don't have scene breakdown yet.

        Args:
            scenario_text: The client's scenario text.
            estimated_scene_count: Estimated number of scenes.
            avg_duration_seconds: Average scene duration.
            quality_check_enabled: Whether quality checks will run.

        Returns:
            Rough cost breakdown.
        """
        breakdown = CostBreakdown()
        breakdown.total_scenes = estimated_scene_count

        # Scenario analysis: ~500 input tokens + ~2000 output tokens
        breakdown.scenario_analysis_cost = (
            0.5 * self.rates.gpt4o_input_per_1k_tokens
            + 2.0 * self.rates.gpt4o_output_per_1k_tokens
        )

        # Prompt enrichment: ~200 input + ~300 output per scene, x2 (image+video)
        per_scene_enrich = (
            0.2 * self.rates.gpt4o_input_per_1k_tokens
            + 0.3 * self.rates.gpt4o_output_per_1k_tokens
        ) * 2
        breakdown.prompt_enrichment_cost = per_scene_enrich * estimated_scene_count

        # Image generation (Gemini - currently free)
        breakdown.image_generation_cost = (
            self.rates.gemini_flash_per_image * estimated_scene_count
        )

        # Video generation
        total_seconds = estimated_scene_count * avg_duration_seconds
        breakdown.total_video_seconds = total_seconds
        breakdown.video_generation_cost = (
            total_seconds * self.rates.kling_per_second_v3
        )

        # Quality check: one Gemini call per scene
        if quality_check_enabled:
            breakdown.quality_check_cost = (
                self.rates.gemini_flash_per_image * estimated_scene_count
            )

        return breakdown

    def estimate_from_scenes(
        self,
        scenes: list[SceneAnalysis],
        quality_check_enabled: bool = True,
    ) -> CostBreakdown:
        """Precise estimate after GPT-4o scene analysis.

        Args:
            scenes: Analyzed scenes from GPT-4o.
            quality_check_enabled: Whether quality checks will run.

        Returns:
            Detailed cost breakdown.
        """
        breakdown = CostBreakdown()
        breakdown.total_scenes = len(scenes)

        for scene in scenes:
            if scene.type == SceneType.PERSONNAGE:
                breakdown.personnage_scenes += 1
            elif scene.type == SceneType.PRODUIT:
                breakdown.produit_scenes += 1
            else:
                breakdown.transition_scenes += 1

        # Scenario analysis (already done, but include for total)
        breakdown.scenario_analysis_cost = (
            0.5 * self.rates.gpt4o_input_per_1k_tokens
            + 2.0 * self.rates.gpt4o_output_per_1k_tokens
        )

        # Prompt enrichment per generatable scene
        generatable = breakdown.personnage_scenes + breakdown.produit_scenes
        per_scene_enrich = (
            0.2 * self.rates.gpt4o_input_per_1k_tokens
            + 0.3 * self.rates.gpt4o_output_per_1k_tokens
        ) * 2
        breakdown.prompt_enrichment_cost = per_scene_enrich * generatable

        # Image generation
        breakdown.image_generation_cost = (
            self.rates.gemini_pro_per_image * breakdown.personnage_scenes
            + self.rates.gemini_flash_per_image * breakdown.produit_scenes
        )

        # Video generation (model-specific rates)
        for scene in scenes:
            if scene.type == SceneType.TRANSITION:
                continue
            breakdown.total_video_seconds += scene.duration
            if scene.type == SceneType.PERSONNAGE:
                breakdown.video_generation_cost += (
                    scene.duration * self.rates.kling_per_second_video01
                )
            else:
                breakdown.video_generation_cost += (
                    scene.duration * self.rates.kling_per_second_v3
                )

        # Quality checks
        if quality_check_enabled:
            breakdown.quality_check_cost = (
                self.rates.gemini_flash_per_image * generatable
            )

        logger.info(
            "[COST] Estimated total: $%.4f for %d scenes (%.1fs video)",
            breakdown.total_cost,
            breakdown.total_scenes,
            breakdown.total_video_seconds,
        )

        return breakdown
