"""
Knowledge Engine — The brain behind AdGenAI's professional quality.

Orchestrates all knowledge modules to transform a client's simple prompt
into a prompt that produces broadcast-quality advertising imagery.

Flow:
1. Receive scenario text
2. Call industry_detector to identify the advertising industry
3. Load ad_patterns for that industry
4. For each scene, identify the archetype (product hero, portrait, etc.)
5. Select: photography style, lighting, lens, color palette, composition, textures
6. Generate enriched prompt = client's original text + industry patterns + photography knowledge
7. Client's words always preserved first, enrichment appended invisibly

CRITICAL: The client's scenario is SACRED. This engine adds expertise.
It NEVER changes, removes, or reinterprets the client's words.
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field

from backend.knowledge.industry_detector import IndustryDetector, DetectionResult
from backend.knowledge.scene_structures.scene_archetypes import (
    SCENE_ARCHETYPES,
    get_archetype,
)
from backend.knowledge.scene_structures.transition_grammar import (
    get_recommended_transition,
    get_transition_duration,
)
from backend.models.enums import AdCategory, SceneArchetype, SceneType

logger = logging.getLogger(__name__)


@dataclass
class EnrichmentResult:
    """Result of knowledge-based prompt enrichment for one scene."""
    enriched_image_prompt: str
    enriched_video_prompt: str
    detected_industry: str
    detected_archetype: str
    photography_modifiers: list[str] = field(default_factory=list)
    video_modifiers: list[str] = field(default_factory=list)
    lighting_setup: str = ""
    lens_choice: str = ""
    color_palette: str = ""
    composition_rule: str = ""
    recommended_transition: str = ""
    recommended_transition_duration: float = 0.5


class KnowledgeEngine:
    """Main knowledge orchestrator for prompt enrichment.

    Usage:
        engine = KnowledgeEngine()
        result = engine.enrich_scene(
            scene_description="Sophie walks in a lavender field...",
            scene_type=SceneType.PERSONNAGE,
            image_prompt="Sophie walks in lavender field, white dress",
            video_prompt="She walks toward camera, wind in hair",
            scenario_text="A luxury perfume ad...",
            duration=5.0,
        )
    """

    def __init__(self) -> None:
        self._detector = IndustryDetector()
        self._patterns_cache: dict[str, dict] = {}
        self._detection_cache: DetectionResult | None = None

    def detect_industry(
        self,
        scenario: str,
        brand_name: str | None = None,
    ) -> DetectionResult:
        """Detect and cache the industry for this scenario."""
        if self._detection_cache is None:
            self._detection_cache = self._detector.detect(scenario, brand_name=brand_name)
            logger.info(
                "[KNOWLEDGE] Industry detected: %s (confidence: %.2f)%s",
                self._detection_cache.primary.industry,
                self._detection_cache.primary.confidence,
                f" + {self._detection_cache.secondary[0].industry}"
                if self._detection_cache.is_hybrid else "",
            )
        return self._detection_cache

    def get_industry_patterns(self, industry: str) -> dict:
        """Load ad patterns for an industry (cached)."""
        if industry not in self._patterns_cache:
            try:
                from backend.knowledge.ad_patterns import PATTERN_REGISTRY
                self._patterns_cache[industry] = PATTERN_REGISTRY.get(industry, {})
            except ImportError:
                logger.warning("[KNOWLEDGE] Ad patterns not loaded for %s", industry)
                self._patterns_cache[industry] = {}
        return self._patterns_cache[industry]

    def detect_archetype(
        self,
        description: str,
        scene_type: SceneType,
        image_prompt: str,
    ) -> str:
        """Identify the scene archetype from description and prompt.

        Returns the archetype name (e.g., 'product_hero', 'portrait').
        """
        text = f"{description} {image_prompt}".lower()

        # Archetype detection rules (ordered by specificity)
        archetype_rules = [
            ("macro_detail", [r"close.?up", r"macro", r"detail", r"texture", r"extreme close"]),
            ("packshot", [r"packshot", r"packaging", r"box shot", r"catalog"]),
            ("endframe", [r"end.?frame", r"final shot", r"logo reveal", r"brand.?shot", r"closing"]),
            ("overhead_flat_lay", [r"flat.?lay", r"top.?down", r"overhead", r"bird.?s?.?eye"]),
            ("unboxing", [r"unbox", r"open.*package", r"reveal.*box", r"unwrap"]),
            ("before_after", [r"before.*after", r"transform", r"comparison"]),
            ("silhouette", [r"silhouette", r"backlit.*outline", r"shadow.*figure"]),
            ("reflection_shot", [r"reflection", r"mirror", r"water.*reflect"]),
            ("hand_detail", [r"hand.*hold", r"hand.*touch", r"fingers", r"applying"]),
            ("360_product", [r"360", r"full rotation", r"all angles", r"turntable"]),
            ("action", [r"running", r"jumping", r"sports", r"dynamic.*motion", r"athletic"]),
            ("walking_tracking", [r"walk", r"stroll", r"stride", r"approach"]),
            ("reveal", [r"reveal", r"emerge", r"appear", r"gradually.*show"]),
            ("ambient", [r"ambient", r"atmosphere", r"abstract", r"smoke", r"mist", r"fog"]),
            ("montage", [r"montage", r"sequence", r"rapid.*cut", r"series of"]),
            ("testimonial", [r"testimonial", r"speak", r"tell", r"recommend"]),
            ("group_shot", [r"group", r"collection", r"lineup", r"range of"]),
            ("split_screen", [r"split", r"side by side", r"dual"]),
            ("establishing", [r"wide shot", r"establish", r"location", r"setting", r"environment"]),
            ("interaction", [r"hold", r"touch", r"apply", r"spray", r"pour", r"drink", r"eat"]),
            ("portrait", [r"portrait", r"face", r"head.?shot", r"close.?up.*person"]),
            ("lifestyle", [r"lifestyle", r"daily", r"morning", r"routine", r"natural"]),
            ("product_hero", [r"product", r"bottle", r"item", r"display"]),
        ]

        for archetype_name, patterns in archetype_rules:
            for pattern in patterns:
                if re.search(pattern, text):
                    return archetype_name

        # Fallback based on scene type
        if scene_type == SceneType.PERSONNAGE:
            return "portrait"
        elif scene_type == SceneType.PRODUIT:
            return "product_hero"
        return "ambient"

    def enrich_scene(
        self,
        scene_description: str,
        scene_type: SceneType,
        image_prompt: str,
        video_prompt: str,
        scenario_text: str,
        duration: float = 5.0,
        camera_movement: str = "static",
        brand_name: str | None = None,
        previous_scene_type: str | None = None,
    ) -> EnrichmentResult:
        """Enrich a single scene's prompts with professional knowledge.

        The client's original prompt words are ALWAYS preserved at the start.
        Knowledge additions are APPENDED after the original text.

        Args:
            scene_description: GPT-4o scene description.
            scene_type: Scene classification.
            image_prompt: Client's raw image prompt.
            video_prompt: Client's raw video prompt.
            scenario_text: Full scenario for industry context.
            duration: Scene duration in seconds.
            camera_movement: Camera movement type.
            brand_name: Optional brand name.
            previous_scene_type: Previous scene's type/archetype for transition.

        Returns:
            EnrichmentResult with enriched prompts and metadata.
        """
        # 1. Detect industry
        detection = self.detect_industry(scenario_text, brand_name)
        industry = detection.primary.industry
        patterns = self.get_industry_patterns(industry)

        # 2. Detect scene archetype
        archetype_name = self.detect_archetype(scene_description, scene_type, image_prompt)
        archetype_data = get_archetype(archetype_name) or {}

        # 3. Gather photography modifiers from industry patterns
        photo_mods = list(patterns.get("prompt_modifiers", []))
        video_mods = list(patterns.get("video_modifiers", []))

        # 4. Select lighting
        lighting_prefs = patterns.get("lighting_preferences", [])
        lighting_setup = ""
        if lighting_prefs:
            # Use archetype's lighting preference if available, else first from industry
            lighting_setup = archetype_data.get("lighting", lighting_prefs[0] if isinstance(lighting_prefs[0], str) else lighting_prefs[0].get("name", ""))

        # 5. Select lens
        lens_prefs = patterns.get("lens_preferences", [])
        lens_choice = archetype_data.get("lens", "")
        if not lens_choice and lens_prefs:
            lens_choice = lens_prefs[0] if isinstance(lens_prefs[0], str) else lens_prefs[0].get("focal_length", "85mm")

        # 6. Get composition
        composition = archetype_data.get("composition", "")

        # 7. Get visual signature
        visual_sig = patterns.get("visual_signature", {})

        # 8. Build enriched IMAGE prompt
        # Client's words FIRST, always preserved
        enriched_parts = [image_prompt]

        # Add archetype-specific keywords
        if archetype_data.get("keywords"):
            enriched_parts.extend(archetype_data["keywords"][:3])

        # Add photography directives
        if lighting_setup:
            enriched_parts.append(lighting_setup)
        if lens_choice:
            enriched_parts.append(f"{lens_choice} lens")
        if composition:
            enriched_parts.append(composition)

        # Add industry-specific modifiers (select top 5 most relevant)
        selected_mods = self._select_relevant_modifiers(
            photo_mods, scene_description, max_count=5,
        )
        enriched_parts.extend(selected_mods)

        # Add visual signature directives
        if visual_sig:
            if visual_sig.get("depth_of_field"):
                enriched_parts.append(visual_sig["depth_of_field"])
            if visual_sig.get("color_temperature"):
                enriched_parts.append(f"color temperature {visual_sig['color_temperature']}")
            if visual_sig.get("grain"):
                enriched_parts.append(visual_sig["grain"])

        # Always add quality keywords
        enriched_parts.extend(["8K detail", "photorealistic", "commercial quality"])

        enriched_image = ", ".join(enriched_parts)

        # 9. Build enriched VIDEO prompt
        video_parts = [video_prompt]

        # Add camera movement description
        camera_desc = self._camera_to_description(camera_movement)
        if camera_desc:
            video_parts.append(camera_desc)

        # Add industry video modifiers
        selected_video_mods = self._select_relevant_modifiers(
            video_mods, scene_description, max_count=3,
        )
        video_parts.extend(selected_video_mods)

        # Add timing
        video_parts.append(f"duration: {duration}s")
        video_parts.append("realistic physics, natural motion")

        enriched_video = ", ".join(video_parts)

        # 10. Determine transition
        from_type = previous_scene_type or "establishing"
        recommended_trans = get_recommended_transition(from_type, archetype_name, industry)
        trans_duration = get_transition_duration(recommended_trans, industry)

        return EnrichmentResult(
            enriched_image_prompt=enriched_image,
            enriched_video_prompt=enriched_video,
            detected_industry=industry,
            detected_archetype=archetype_name,
            photography_modifiers=selected_mods,
            video_modifiers=selected_video_mods,
            lighting_setup=lighting_setup,
            lens_choice=lens_choice,
            composition_rule=composition,
            recommended_transition=recommended_trans,
            recommended_transition_duration=trans_duration,
        )

    def enrich_all_scenes(
        self,
        scenes: list[dict],
        scenario_text: str,
        brand_name: str | None = None,
    ) -> list[EnrichmentResult]:
        """Enrich all scenes in order, tracking previous scene for transitions.

        Args:
            scenes: List of dicts with keys: description, type, image_prompt,
                    video_prompt, duration, camera_movement.
            scenario_text: Full scenario text.
            brand_name: Optional brand name.

        Returns:
            List of EnrichmentResults, one per scene.
        """
        results = []
        prev_archetype = None

        for scene in scenes:
            result = self.enrich_scene(
                scene_description=scene.get("description", ""),
                scene_type=scene.get("type", SceneType.PRODUIT),
                image_prompt=scene.get("image_prompt", ""),
                video_prompt=scene.get("video_prompt", ""),
                scenario_text=scenario_text,
                duration=scene.get("duration", 5.0),
                camera_movement=scene.get("camera_movement", "static"),
                brand_name=brand_name,
                previous_scene_type=prev_archetype,
            )
            results.append(result)
            prev_archetype = result.detected_archetype

        return results

    def _select_relevant_modifiers(
        self,
        modifiers: list[str],
        context: str,
        max_count: int = 5,
    ) -> list[str]:
        """Select the most relevant modifiers based on scene context."""
        if not modifiers:
            return []

        context_lower = context.lower()
        scored = []
        for mod in modifiers:
            # Score by word overlap with context
            words = mod.lower().split()
            overlap = sum(1 for w in words if w in context_lower)
            scored.append((mod, overlap))

        # Sort by relevance, take top N
        scored.sort(key=lambda x: x[1], reverse=True)
        return [mod for mod, _ in scored[:max_count]]

    @staticmethod
    def _camera_to_description(movement: str) -> str:
        """Convert camera movement enum to natural language."""
        descriptions = {
            "static": "locked-off camera, no movement",
            "pan_left": "smooth pan left",
            "pan_right": "smooth pan right",
            "zoom_in": "slow zoom into subject",
            "zoom_out": "slow zoom revealing full scene",
            "tracking": "camera tracking alongside subject movement",
            "orbit": "smooth 360-degree orbit around subject",
            "dolly_in": "dolly pushing in toward subject",
            "dolly_out": "dolly pulling back from subject",
            "crane_up": "crane rising upward revealing scene",
            "crane_down": "crane descending toward subject",
            "tilt_up": "camera tilting upward",
            "tilt_down": "camera tilting downward",
            "handheld": "organic handheld movement, slight shake",
            "steadicam": "smooth steadicam glide",
        }
        return descriptions.get(movement.lower(), "")
