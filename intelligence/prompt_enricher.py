"""
Prompt Enricher — adds professional photography precision to prompts.

NEVER changes the client's intent. The client's words are always preserved
at the beginning. Enrichment is APPENDED invisibly.

Example:
  Client: "Sophie walks in a lavender field, white dress, wind in her hair"
  Enriched: "Sophie walks in a lavender field, white dress, wind in her hair.
             Fashion editorial photography, 85mm f/1.4 lens, golden hour..."
"""
from __future__ import annotations

import logging
from typing import Any

from intelligence.scene_understanding import SceneContext, SceneUnderstanding
from knowledge.knowledge_engine import KnowledgeEngine

logger = logging.getLogger(__name__)

# Lazy singleton for dataset access (avoids loading 65K files on import)
_dataset_loader = None


def _get_dataset():
    global _dataset_loader
    if _dataset_loader is None:
        try:
            from load_dataset import DatasetLoader
            _dataset_loader = DatasetLoader()
        except Exception as e:
            logger.warning("Could not load dataset: %s", e)
            _dataset_loader = False  # type: ignore[assignment]
    return _dataset_loader if _dataset_loader else None


class PromptEnricher:
    """Enriches prompts with professional photography knowledge."""

    def __init__(self) -> None:
        self.knowledge = KnowledgeEngine()
        self.scene_understanding = SceneUnderstanding()

    def enrich_image_prompt(
        self,
        original_prompt: str,
        scene_context: SceneContext,
        industry: str = "luxury",
        brand_prefix: str = "",
        scene_type: str = "lifestyle",
    ) -> str:
        """Enrich an image generation prompt.

        Client's words are ALWAYS preserved first. Technical additions appended.

        Args:
            original_prompt: The client's original prompt (sacred).
            scene_context: Technical understanding from SceneUnderstanding.
            industry: Detected industry.
            brand_prefix: Brand visual identity prefix.
            scene_type: Scene archetype.

        Returns:
            Enriched prompt with photography directives appended.
        """
        # Get enrichment from knowledge engine
        enrichment = self.knowledge.get_image_enrichment(
            industry=industry,
            scene_context=scene_context,
            scene_type=scene_type,
        )

        # Build the enriched prompt
        parts = []

        # Brand prefix first (if exists)
        if brand_prefix:
            parts.append(brand_prefix)

        # Client's original words (SACRED — never modified)
        parts.append(original_prompt.strip())

        # Technical enrichment appended
        if enrichment:
            parts.append(enrichment)

        enriched = ". ".join(p.rstrip(".") for p in parts if p)

        logger.debug(
            "Enriched prompt: original=%d chars, enriched=%d chars, industry=%s",
            len(original_prompt), len(enriched), industry,
        )
        return enriched

    def enrich_video_prompt(
        self,
        original_prompt: str,
        scene_context: SceneContext,
        industry: str = "luxury",
    ) -> str:
        """Enrich a video animation prompt.

        Args:
            original_prompt: Client's video prompt.
            scene_context: Scene technical understanding.
            industry: Detected industry.

        Returns:
            Enriched video prompt.
        """
        enrichment = self.knowledge.get_video_enrichment(
            industry=industry,
            scene_context=scene_context,
        )

        parts = [original_prompt.strip()]
        if enrichment:
            parts.append(enrichment)

        # Add Kling-specific hints from scene understanding
        kling_hints = scene_context.kling_hints
        if kling_hints.get("motion_prompt"):
            parts.append(kling_hints["motion_prompt"])
        if kling_hints.get("speed_modifier"):
            parts.append(kling_hints["speed_modifier"])
        if kling_hints.get("camera_prompt"):
            parts.append(kling_hints["camera_prompt"])
        if kling_hints.get("atmosphere"):
            parts.append(kling_hints["atmosphere"])

        return ". ".join(p.rstrip(".") for p in parts if p)

    def enrich_mannequin_prompt(
        self,
        base_scene_prompt: str,
        scene_context: SceneContext,
        trigger_word: str = "MANNEQUIN",
    ) -> str:
        """Build LoRA mannequin prompt that matches the base scene.

        Analyzes the base scene to extract pose, angle, lighting
        and includes them in the LoRA prompt.
        """
        pose_parts = [trigger_word, "portrait photograph"]

        # Framing
        framing_map = {
            "close_up": "close-up head and shoulders portrait",
            "wide": "full body portrait, head to toe",
            "medium": "medium shot, waist up",
        }
        pose_parts.append(framing_map.get(scene_context.implied_framing, "medium shot"))

        # Lighting
        lighting_map = {
            "backlit": "backlit with rim light, face partially in shadow",
            "side": "dramatic side lighting, Rembrandt pattern",
            "top": "overhead lighting, subtle shadows under eyes",
            "front": "soft frontal lighting, even illumination",
        }
        pose_parts.append(lighting_map.get(scene_context.implied_lighting_direction, "soft frontal lighting"))

        # Subject pose/motion
        motion_map = {
            "walking": "walking pose, mid-stride, dynamic body position",
            "turning": "head turned slightly, three-quarter view angle",
            "reaching": "hands extended, reaching gesture",
            "static": "standing pose, relaxed and natural",
        }
        pose_parts.append(motion_map.get(scene_context.implied_subject_motion, "natural relaxed pose"))

        # Time of day lighting
        if scene_context.time_of_day == "golden_hour":
            pose_parts.append("warm golden hour sunlight")
        elif scene_context.time_of_day == "night":
            pose_parts.append("dramatic artificial lighting")

        # Quality modifiers
        pose_parts.extend([
            "photorealistic", "8K detail", "natural skin texture",
            "sharp focus on face", "professional photography",
        ])

        return ", ".join(pose_parts)

    # ── High-level scene enrichment API ─────────────────────────────

    def enrich_scene(
        self,
        scene_data: dict[str, Any],
        industry: str = "luxury",
        brand_name: str | None = None,
    ) -> dict[str, Any]:
        """Enrich a single scene dict with professional prompts.

        Bridges knowledge engine + dataset + scene understanding.

        Args:
            scene_data: dict with keys like description, prompt_image,
                        prompt_video, scene_type, archetype.
            industry: Detected industry key.
            brand_name: Optional brand name for brand DNA loading.

        Returns:
            Copy of scene_data with enriched prompt_image and prompt_video.
        """
        result = dict(scene_data)

        # 1. Analyze the scene description for technical context
        description = scene_data.get("description", "") or scene_data.get("prompt_image", "")
        scene_context = self.scene_understanding.analyze(description)

        # 2. Get brand prefix if brand is known
        brand_prefix = ""
        if brand_name:
            ds = _get_dataset()
            if ds:
                profile = ds.get_brand_profile(brand_name)
                if profile:
                    brand_prefix = profile.get("prompt_prefix", "")
                    logger.debug("Loaded brand prefix for %s", brand_name)

        # 3. Detect archetype
        archetype = scene_data.get("archetype", "")
        if not archetype:
            archetype = self.knowledge.detect_archetype(description)

        # 4. Enrich image prompt
        original_image = scene_data.get("prompt_image", description)
        result["prompt_image"] = self.enrich_image_prompt(
            original_prompt=original_image,
            scene_context=scene_context,
            industry=industry,
            brand_prefix=brand_prefix,
            scene_type=archetype,
        )

        # 5. Enrich video prompt
        original_video = scene_data.get("prompt_video", "")
        if original_video:
            result["prompt_video"] = self.enrich_video_prompt(
                original_prompt=original_video,
                scene_context=scene_context,
                industry=industry,
            )

        # 6. Store archetype and context for downstream pipeline
        result["archetype"] = archetype
        result["scene_context"] = {
            "framing": scene_context.implied_framing,
            "lighting": scene_context.implied_lighting_direction,
            "camera": scene_context.implied_camera_movement,
            "motion": scene_context.implied_subject_motion,
            "speed": scene_context.implied_speed,
            "time_of_day": scene_context.time_of_day,
            "environment": scene_context.environment_type,
        }

        return result

    def enrich_all_scenes(
        self,
        scenes: list[dict[str, Any]],
        industry: str = "luxury",
        brand_name: str | None = None,
    ) -> list[dict[str, Any]]:
        """Enrich every scene in a list.

        Args:
            scenes: List of scene dicts.
            industry: Detected industry key.
            brand_name: Optional brand name.

        Returns:
            List of enriched scene dicts.
        """
        enriched = []
        for i, scene in enumerate(scenes):
            try:
                enriched.append(self.enrich_scene(scene, industry, brand_name))
            except Exception as e:
                logger.warning("Failed to enrich scene %d: %s", i + 1, e)
                enriched.append(scene)  # Pass through unchanged
        logger.info("Enriched %d/%d scenes for industry=%s", len(enriched), len(scenes), industry)
        return enriched
