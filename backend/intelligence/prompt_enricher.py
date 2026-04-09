"""
Invisible Prompt Enrichment Engine v3.0.

Transforms simple client scene descriptions into world-class photography
prompts by calling the Knowledge Engine for industry-specific enrichment,
then adding scene-specific technical precision.

PHILOSOPHY:
    Client writes: "Sophie walks in a lavender field, white dress, wind in hair"
    We silently produce: "Sophie walks in a lavender field, white dress, wind
    in her hair, fashion editorial photography, 85mm f/1.4 lens, golden hour
    sunlight from the left, shallow depth of field, Provence landscape, warm
    color grading 5800K, natural skin texture, flowing fabric captured
    mid-movement, cinematic atmosphere, film grain, 8K detail"

    The client's words are ALWAYS preserved as-is at the beginning.
    We NEVER change the MEANING of what the client wrote.
    We ONLY add technical precision that a professional photographer would know.

v3.0 changes:
- Delegates to KnowledgeEngine for industry-specific enrichment
- Maintains backward compatibility with direct enrichment methods
- Added mannequin prompt generation for LoRA fusion workflow
"""

from __future__ import annotations

import logging

from backend.knowledge.knowledge_engine import KnowledgeEngine, EnrichmentResult
from backend.models.enums import AdCategory, EmotionalTone, SceneType
from backend.models.scene import SceneAnalysis, SceneContext

logger = logging.getLogger(__name__)


# Emotional tone -> prompt additions (INVISIBLE to the client)
TONE_ENRICHMENTS: dict[EmotionalTone, list[str]] = {
    EmotionalTone.LUXURY: [
        "soft golden light from the left",
        "shallow depth of field",
        "film grain reminiscent of Kodak Portra 800",
    ],
    EmotionalTone.ENERGETIC: [
        "dynamic angle",
        "high contrast",
        "sharp focus",
        "motion blur on background elements",
    ],
    EmotionalTone.INTIMATE: [
        "warm tones",
        "close framing",
        "bokeh background",
        "soft diffusion",
    ],
    EmotionalTone.DRAMATIC: [
        "chiaroscuro lighting",
        "deep shadows",
        "high contrast",
        "cinematic aspect ratio feel",
    ],
    EmotionalTone.PLAYFUL: [
        "bright saturated colors",
        "high-key lighting",
        "dynamic composition",
        "cheerful color palette",
    ],
    EmotionalTone.MINIMALIST: [
        "clean negative space",
        "single-source soft lighting",
        "monochromatic palette",
        "geometric precision",
    ],
    EmotionalTone.NOSTALGIC: [
        "warm tungsten color temperature",
        "soft diffusion filter",
        "slightly lifted blacks",
        "desaturated pastel tones",
    ],
    EmotionalTone.POWERFUL: [
        "heroic low angle",
        "strong rim light",
        "high contrast dramatic shadows",
        "bold composition",
    ],
    EmotionalTone.SERENE: [
        "soft overcast natural light",
        "gentle pastel color palette",
        "smooth gradients",
        "calm balanced composition",
    ],
    EmotionalTone.MYSTERIOUS: [
        "low-key lighting",
        "deep shadows with isolated light pools",
        "cool blue-teal color shift",
        "atmospheric haze",
    ],
    EmotionalTone.JOYFUL: [
        "bright natural sunlight",
        "warm golden tones",
        "vibrant saturated colors",
        "high-key with fill flash",
    ],
    EmotionalTone.ELEGANT: [
        "Rembrandt lighting pattern",
        "neutral warm color temperature",
        "subtle fill reducing shadow density",
        "refined classical composition",
    ],
}


class PromptEnricher:
    """Silently enriches scene prompts with professional photography knowledge.

    Integrates with the KnowledgeEngine for industry-specific patterns,
    then adds scene-specific emotional and technical enrichments.

    The client's original words are ALWAYS preserved at the beginning.
    Technical enrichments are APPENDED, never replacing intent.
    """

    def __init__(self) -> None:
        self._knowledge = KnowledgeEngine()
        self._scenario_text: str = ""
        self._brand_name: str | None = None

    def set_scenario_context(
        self,
        scenario_text: str,
        brand_name: str | None = None,
    ) -> str:
        """Cache the scenario context and detect industry.

        Should be called once per pipeline run before enriching scenes.

        Returns:
            Detected industry name.
        """
        self._scenario_text = scenario_text
        self._brand_name = brand_name
        detection = self._knowledge.detect_industry(scenario_text, brand_name)
        return detection.primary.industry

    def detect_ad_category(self, full_scenario: str) -> AdCategory:
        """Auto-detect the advertising category from the full scenario text.

        Delegates to the KnowledgeEngine industry detector for consistency.
        """
        industry = self._knowledge.detect_industry(full_scenario).primary.industry
        # Map knowledge engine industry names to AdCategory enum
        mapping = {
            "luxury": AdCategory.LUXURY,
            "beauty": AdCategory.BEAUTY,
            "fashion": AdCategory.FASHION,
            "sport": AdCategory.SPORT,
            "food_beverage": AdCategory.FOOD_BEVERAGE,
            "automotive": AdCategory.AUTOMOTIVE,
            "tech": AdCategory.TECH,
            "travel": AdCategory.TRAVEL,
            "real_estate": AdCategory.REAL_ESTATE,
            "jewelry_watches": AdCategory.JEWELRY_WATCHES,
            "fragrance": AdCategory.FRAGRANCE,
            "health": AdCategory.HEALTH,
        }
        return mapping.get(industry, AdCategory.GENERAL)

    def enrich_image_prompt(
        self,
        scene: SceneAnalysis,
        context: SceneContext,
        category: AdCategory | None = None,
        brand_style_prefix: str = "",
    ) -> str:
        """Enrich an image prompt with invisible professional photography directives.

        Uses the KnowledgeEngine for industry patterns, then adds
        scene-specific emotional and technical enrichments.

        The client's original image_prompt is preserved verbatim at the start.
        """
        # Use knowledge engine for primary enrichment
        enrichment = self._knowledge.enrich_scene(
            scene_description=scene.description,
            scene_type=scene.type,
            image_prompt=scene.image_prompt,
            video_prompt=scene.video_prompt,
            scenario_text=self._scenario_text or scene.description,
            duration=scene.duration,
            camera_movement=scene.camera_movement,
            brand_name=self._brand_name,
        )

        # Start with knowledge-enriched prompt
        parts: list[str] = []

        # 1. Brand style prefix
        if brand_style_prefix:
            parts.append(brand_style_prefix)

        # 2. Knowledge-enriched image prompt (already preserves client words)
        parts.append(enrichment.enriched_image_prompt)

        # 3. Emotional tone enrichments (add if not already in knowledge output)
        tone_additions = TONE_ENRICHMENTS.get(context.emotional_tone, [])
        for addition in tone_additions[:2]:
            if addition.lower() not in enrichment.enriched_image_prompt.lower():
                parts.append(addition)

        # 4. Scene-specific additions
        if context.has_wardrobe_change:
            parts.append(
                "the same person as before but in a different outfit, "
                "maintain exact face and body consistency"
            )

        if scene.type == SceneType.PERSONNAGE:
            parts.append("natural skin texture, realistic proportions")

        enriched = ", ".join(parts)

        logger.debug(
            "[ENRICHER] Scene %d image: %d → %d chars (archetype: %s)",
            scene.id, len(scene.image_prompt), len(enriched),
            enrichment.detected_archetype,
        )

        return enriched

    def enrich_video_prompt(
        self,
        scene: SceneAnalysis,
        context: SceneContext,
    ) -> str:
        """Enrich a video prompt with precise motion and physics directives.

        Uses the KnowledgeEngine for industry video patterns, then adds
        scene-specific pacing and physics constraints.
        """
        enrichment = self._knowledge.enrich_scene(
            scene_description=scene.description,
            scene_type=scene.type,
            image_prompt=scene.image_prompt,
            video_prompt=scene.video_prompt,
            scenario_text=self._scenario_text or scene.description,
            duration=scene.duration,
            camera_movement=scene.camera_movement,
            brand_name=self._brand_name,
        )

        # Start with knowledge-enriched video prompt
        parts: list[str] = [enrichment.enriched_video_prompt]

        # Add emotional pacing if not already included
        pacing_map: dict[EmotionalTone, str] = {
            EmotionalTone.LUXURY: "slow, deliberate movement, elegant pacing",
            EmotionalTone.ENERGETIC: "dynamic movement, fast-paced, high energy",
            EmotionalTone.INTIMATE: "gentle, slow movement, intimate pacing",
            EmotionalTone.DRAMATIC: "building intensity, dramatic timing",
            EmotionalTone.SERENE: "very slow, meditative movement",
            EmotionalTone.PLAYFUL: "bouncy, light movement with surprise",
        }
        pacing = pacing_map.get(context.emotional_tone, "")
        if pacing and pacing.lower() not in enrichment.enriched_video_prompt.lower():
            parts.append(pacing)

        return ", ".join(parts)

    def build_scene_base_prompt(
        self,
        scene: SceneAnalysis,
        context: SceneContext,
        category: AdCategory | None = None,
        brand_style_prefix: str = "",
    ) -> str:
        """Build the Pass 1 prompt for Nano Banana scene base generation.

        For personnage scenes: replaces the specific mannequin reference with
        a generic human figure placeholder while keeping everything else.

        For produit scenes: returns the standard enriched prompt.
        """
        if scene.type != SceneType.PERSONNAGE:
            return self.enrich_image_prompt(scene, context, category, brand_style_prefix)

        # For personnage: modify to use generic figure placeholder
        import re

        prompt = scene.image_prompt

        # Replace specific mannequin references with generic person
        replacements = [
            (r"\b(the mannequin|mannequin|the model|our model)\b",
             "a person"),
            (r"\b(she|he)\b(?!\s+is\s+holding)",
             "the person"),
        ]
        modified_prompt = prompt
        for pattern, replacement in replacements:
            modified_prompt = re.sub(pattern, replacement, modified_prompt, flags=re.IGNORECASE)

        # Add instruction for generic placeholder
        modified_prompt += (
            ", generic human figure in the correct pose and position, "
            "placeholder face (will be replaced), matching clothing and body type"
        )

        # Enrich with knowledge engine
        temp_scene = scene.model_copy(update={"image_prompt": modified_prompt})
        return self.enrich_image_prompt(temp_scene, context, category, brand_style_prefix)

    def build_mannequin_prompt(
        self,
        scene: SceneAnalysis,
        base_analysis: dict,
        trigger_word: str = "MANNEQUIN",
    ) -> str:
        """Build the Pass 2 prompt for LoRA SDXL mannequin generation.

        Describes the mannequin in the EXACT same pose, angle, and lighting
        as the base scene from Pass 1.

        Args:
            scene: Original scene analysis.
            base_analysis: Pose analysis from the base scene image.
            trigger_word: LoRA trigger word for the mannequin.

        Returns:
            Prompt string for LoRA generation.
        """
        parts = [
            f"A photo of {trigger_word}",
            f"{base_analysis.get('body_pose', 'standing')}",
            f"head {base_analysis.get('head_angle', 'facing forward')}",
            f"lighting from {base_analysis.get('lighting_direction', 'the left')}",
        ]

        # Add clothing from scenario
        clothing = base_analysis.get("clothing_description", "")
        if clothing:
            parts.append(f"wearing {clothing}")

        # Add technical quality
        parts.extend([
            "portrait photography",
            "natural skin texture",
            "sharp focus on face",
            "matching the scene's lighting exactly",
            "photorealistic, 8K detail",
        ])

        return ", ".join(parts)
