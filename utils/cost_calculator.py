"""
Cost estimation per API call and per pipeline run.
"""
from __future__ import annotations

import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# ── Unit costs (USD) ───────────────────────────────────────────────

@dataclass(frozen=True)
class APICosts:
    # OpenAI GPT-4o
    gpt4o_input_per_1k: float = 0.005
    gpt4o_output_per_1k: float = 0.015
    gpt4o_estimated_per_call: float = 0.05

    # Gemini Flash (image generation)
    gemini_flash_per_image: float = 0.02

    # Replicate LoRA SDXL
    replicate_lora_per_image: float = 0.05

    # Replicate Inpainting
    replicate_inpaint_per_image: float = 0.04

    # Kling Video
    kling_per_second: float = 0.10
    kling_min_per_clip: float = 0.30

    # Gemini quality check
    gemini_quality_check: float = 0.005


COSTS = APICosts()


class CostCalculator:
    """Estimate costs before and track costs during a pipeline run."""

    def __init__(self) -> None:
        self.costs = COSTS
        self._tracked: dict[str, float] = {}

    def estimate_pipeline(
        self,
        total_scenes: int,
        personnage_scenes: int,
        produit_scenes: int,
        transition_scenes: int,
        avg_duration: float = 4.0,
    ) -> dict[str, float]:
        """Pre-run cost estimation."""
        breakdown: dict[str, float] = {}

        # Step 1: Scenario analysis
        breakdown["scenario_analysis"] = self.costs.gpt4o_estimated_per_call

        # Step 2: Image generation
        # Personnage: 3 passes (Gemini + LoRA + Inpainting) + quality check
        personnage_cost = personnage_scenes * (
            self.costs.gemini_flash_per_image  # Pass 1: scene
            + self.costs.replicate_lora_per_image  # Pass 2: mannequin
            + self.costs.replicate_inpaint_per_image  # Pass 3: fusion
            + self.costs.gemini_quality_check  # Quality check
        )
        breakdown["personnage_images"] = personnage_cost

        # Produit: 1 pass (Gemini only)
        breakdown["produit_images"] = produit_scenes * self.costs.gemini_flash_per_image

        # Step 3: Video animation
        animated_scenes = personnage_scenes + produit_scenes
        video_cost = animated_scenes * max(
            avg_duration * self.costs.kling_per_second,
            self.costs.kling_min_per_clip,
        )
        breakdown["video_animation"] = video_cost

        # Step 4: Assembly (free, local FFmpeg)
        breakdown["assembly"] = 0.0

        breakdown["total"] = sum(breakdown.values())

        logger.info("Cost estimate: $%.2f for %d scenes", breakdown["total"], total_scenes)
        return breakdown

    def track(self, category: str, amount: float) -> None:
        """Track actual cost during pipeline run."""
        self._tracked[category] = self._tracked.get(category, 0.0) + amount

    def get_tracked(self) -> dict[str, float]:
        total = sum(self._tracked.values())
        return {**self._tracked, "total": total}
