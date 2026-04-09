"""
Knowledge Engine — the main orchestrator for prompt enrichment.

1. Receives a scene's original prompt + scenario context
2. Calls industry_detector to identify industry
3. Loads the right ad_patterns file
4. Identifies the scene archetype from scene_archetypes.py
5. Selects: best lighting, lens, color palette, composition, textures
6. Builds enriched prompt = original client text + all technical additions
7. Has enrich_image_prompt() and enrich_video_prompt()
8. Client's words ALWAYS preserved first, enrichment appended invisibly

Designed to be compatible with future data sources:
  - Phase 1: 50K scenarios (dataset/scenarios/)
  - Phase 2: 5K storyboards (dataset/storyboards/)
  - Phase 4: 500 brand profiles (dataset/brand_profiles/)
  - Phase 5: 10K performance data (dataset/performance/)
"""
from __future__ import annotations

import logging
import random
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from intelligence.scene_understanding import SceneContext

from knowledge.industry_detector import IndustryDetector, IndustryMatch

logger = logging.getLogger(__name__)


# ── Archetype detection keywords ────────────────────────────────────────
# Maps keywords in scene descriptions to archetype keys in scene_archetypes.py

_ARCHETYPE_SIGNALS: dict[str, list[str]] = {
    "product_hero_shot": [
        "hero shot", "product shot", "product hero", "showcase product",
        "display product", "present product", "product reveal",
        "product floating", "product center", "product isolated",
    ],
    "lifestyle_context": [
        "lifestyle", "everyday", "daily life", "in context", "real life",
        "using product", "at home", "in use", "candid moment",
    ],
    "model_portrait_closeup": [
        "close-up", "closeup", "close up", "portrait", "face",
        "headshot", "gros plan", "visage", "regard",
    ],
    "product_interaction": [
        "holding", "applying", "spraying", "opening", "pouring",
        "touching", "wearing", "trying", "using", "unboxing",
        "interaction", "hands on", "manipulating",
    ],
    "environment_establishing": [
        "establishing", "wide shot", "location", "setting",
        "landscape", "cityscape", "skyline", "panoramic",
        "environment", "exterior", "overview",
    ],
    "macro_detail": [
        "macro", "detail", "texture", "close detail", "extreme close",
        "surface", "grain", "pattern", "micro", "fine detail",
    ],
    "motion_action": [
        "action", "running", "jumping", "movement", "motion",
        "dynamic", "sport", "athletic", "energy", "speed",
    ],
    "unboxing_reveal": [
        "unbox", "reveal", "unwrap", "discover", "open box",
        "first look", "packaging", "presentation",
    ],
    "silhouette_artistic": [
        "silhouette", "shadow", "outline", "backlit figure",
        "contre-jour", "artistic shadow",
    ],
    "pov_first_person": [
        "pov", "point of view", "first person", "subjective",
        "through eyes", "viewer perspective",
    ],
    "hands_only": [
        "hands", "fingers", "hand holding", "hand close",
        "manicure", "gesture", "grip",
    ],
    "ingredient_component": [
        "ingredient", "component", "raw material", "element",
        "formula", "extract", "essence",
    ],
    "before_after_transform": [
        "before after", "before and after", "transformation",
        "transform", "compare", "evolution", "metamorphosis",
    ],
    "slow_motion_moment": [
        "slow motion", "slow-motion", "slow mo", "ralenti",
        "time frozen", "suspended", "droplet",
    ],
    "reflection_mirror": [
        "reflection", "mirror", "reflected", "reflective",
        "water reflection", "glass reflection",
    ],
    "aerial_drone": [
        "aerial", "drone", "bird's eye", "overhead", "from above",
        "top down", "satellite view",
    ],
    "packshot_endframe": [
        "packshot", "pack shot", "end frame", "endframe",
        "final shot", "product with logo", "closing shot",
    ],
    "call_to_action": [
        "call to action", "cta", "buy now", "shop now",
        "discover more", "learn more", "visit", "available",
    ],
}


class KnowledgeEngine:
    """Main knowledge orchestrator for professional prompt enrichment."""

    def __init__(self) -> None:
        self.detector = IndustryDetector()
        self._patterns_cache: dict[str, dict[str, Any]] = {}

    # ── Industry detection ──────────────────────────────────────────

    def detect_industry(self, scenario: str) -> IndustryMatch:
        """Auto-detect the industry from scenario text."""
        return self.detector.detect(scenario)

    def get_industry_patterns(self, industry: str) -> dict[str, Any]:
        """Load and cache patterns for an industry."""
        if industry in self._patterns_cache:
            return self._patterns_cache[industry]

        try:
            from knowledge.ad_patterns import ALL_PATTERNS
            patterns = ALL_PATTERNS.get(industry, ALL_PATTERNS.get("luxury", {}))
            self._patterns_cache[industry] = patterns
            return patterns
        except ImportError:
            logger.warning("Could not import ad_patterns, using defaults")
            return {}

    # ── Archetype detection ─────────────────────────────────────────

    def detect_archetype(self, scene_description: str) -> str:
        """Detect the scene archetype from a scene description.

        Returns the archetype key (e.g. 'product_hero_shot') or
        'lifestyle_context' as default.
        """
        text = scene_description.lower()
        best_archetype = "lifestyle_context"
        best_score = 0

        for archetype, signals in _ARCHETYPE_SIGNALS.items():
            score = sum(1 for sig in signals if sig in text)
            if score > best_score:
                best_score = score
                best_archetype = archetype

        return best_archetype

    # ── Image prompt enrichment ─────────────────────────────────────

    def enrich_image_prompt(
        self,
        original_prompt: str,
        industry: str,
        scene_context: "SceneContext | None" = None,
        scene_description: str = "",
    ) -> str:
        """Build enriched image prompt.

        Client's words are ALWAYS first. Technical enrichment appended.

        Args:
            original_prompt: The client's original scene description (sacred).
            industry: Detected industry key.
            scene_context: Optional SceneContext from intelligence module.
            scene_description: Raw scene text for archetype detection.

        Returns:
            Enriched prompt string.
        """
        parts: list[str] = [original_prompt]

        patterns = self.get_industry_patterns(industry)
        archetype = self.detect_archetype(scene_description or original_prompt)

        # 1. Industry prompt modifiers (pick 3-5)
        prompt_mods = patterns.get("prompt_modifiers", [])
        if prompt_mods:
            selected = random.sample(prompt_mods, min(4, len(prompt_mods)))
            parts.extend(selected)

        # 2. Lens selection
        lens_prefs = patterns.get("lens_preferences", [])
        if lens_prefs:
            lens = self._select_lens_for_context(lens_prefs, scene_context, archetype)
            if lens:
                parts.append(lens)

        # 3. Lighting selection
        lighting_prefs = patterns.get("lighting_preferences", [])
        if lighting_prefs:
            light = self._select_lighting_for_context(lighting_prefs, scene_context, archetype)
            if light:
                parts.append(light)

        # 4. Visual signature
        visual = patterns.get("visual_signature", {})
        if visual:
            if visual.get("grain"):
                parts.append(visual["grain"])
            if visual.get("depth_of_field"):
                parts.append(f"depth of field: {visual['depth_of_field']}")
            if visual.get("color_grade"):
                parts.append(visual["color_grade"])

        # 5. Scene archetype modifiers
        try:
            from knowledge.scene_structures.scene_archetypes import SCENE_ARCHETYPES
            arch_data = SCENE_ARCHETYPES.get(archetype, {})
            if arch_data.get("image_modifiers"):
                parts.extend(arch_data["image_modifiers"][:2])
        except ImportError:
            pass

        # 6. Context-aware additions (if SceneContext available)
        if scene_context is not None:
            ctx_enrichment = self._get_context_enrichment(scene_context)
            if ctx_enrichment:
                parts.append(ctx_enrichment)

        # 7. Base quality
        parts.append("8K resolution, photorealistic, professional advertising photograph")

        return ", ".join(parts)

    # ── Video prompt enrichment ─────────────────────────────────────

    def enrich_video_prompt(
        self,
        original_prompt: str,
        industry: str,
        scene_context: "SceneContext | None" = None,
    ) -> str:
        """Build enriched video/animation prompt for Kling.

        Client's words first, then Kling-specific technical additions.
        """
        parts: list[str] = [original_prompt]

        patterns = self.get_industry_patterns(industry)

        # Video modifiers from industry
        video_mods = patterns.get("video_modifiers", [])
        if video_mods:
            selected = random.sample(video_mods, min(3, len(video_mods)))
            parts.extend(selected)

        # Movement style
        movement = patterns.get("movement_style", {})
        if movement.get("camera"):
            parts.append(movement["camera"])
        if movement.get("pacing"):
            parts.append(movement["pacing"])

        # Context-aware speed
        if scene_context is not None:
            if scene_context.implied_speed == "slow":
                parts.append("slow deliberate movement, elegant pacing")
            elif scene_context.implied_speed == "fast":
                parts.append("dynamic energetic movement, rapid pacing")

            if scene_context.implied_subject_motion:
                parts.append(scene_context.implied_subject_motion)

        return ", ".join(parts)

    # ── Backward-compatible aliases ─────────────────────────────────

    def get_image_enrichment(
        self,
        industry: str,
        scene_context: "SceneContext",
        scene_type: str = "lifestyle",
    ) -> str:
        """Legacy method — delegates to enrich_image_prompt."""
        return self.enrich_image_prompt(
            original_prompt="",
            industry=industry,
            scene_context=scene_context,
            scene_description=scene_type,
        ).lstrip(", ")

    def get_video_enrichment(
        self,
        industry: str,
        scene_context: "SceneContext",
    ) -> str:
        """Legacy method — delegates to enrich_video_prompt."""
        return self.enrich_video_prompt(
            original_prompt="",
            industry=industry,
            scene_context=scene_context,
        ).lstrip(", ")

    # ── Private helpers ─────────────────────────────────────────────

    def _select_lens_for_context(
        self,
        lens_keys: list[str],
        context: "SceneContext | None",
        archetype: str,
    ) -> str | None:
        """Select a lens description string from available lens keys."""
        try:
            from knowledge.prompt_templates.lighting_setups import LIGHTING_SETUPS
            from knowledge.prompt_templates.lens_library import LENS_LIBRARY
        except ImportError:
            return None

        # Archetype-based focal preference
        archetype_focal = {
            "macro_detail": ["macro_100mm", "macro_105mm"],
            "model_portrait_closeup": ["portrait_85mm_f14", "telephoto_135mm", "noctilux_58mm"],
            "product_hero_shot": ["standard_50mm_f14", "macro_100mm", "zoom_24_70mm"],
            "environment_establishing": ["wide_24mm", "ultra_wide_14mm", "wide_16mm"],
            "aerial_drone": ["wide_24mm", "ultra_wide_14mm"],
            "lifestyle_context": ["classic_35mm", "standard_50mm_f14", "zoom_24_70mm"],
            "motion_action": ["zoom_70_200mm", "telephoto_200mm", "wide_24mm"],
        }

        preferred = archetype_focal.get(archetype, [])

        # Try archetype preference first, filtered by what the industry allows
        for key in preferred:
            if key in lens_keys:
                lens_data = LENS_LIBRARY.get(key, {}) if isinstance(LENS_LIBRARY, dict) else {}
                if lens_data:
                    return f"{lens_data.get('focal_length', key)} lens, {lens_data.get('aperture', '')}, {lens_data.get('depth_of_field_effect', '')}"
                return key

        # Framing from context
        if context is not None:
            framing = context.implied_framing
            framing_map = {
                "close_up": ["portrait_85mm_f14", "telephoto_135mm", "macro_100mm"],
                "medium": ["standard_50mm_f14", "classic_35mm", "zoom_24_70mm"],
                "wide": ["wide_24mm", "ultra_wide_14mm", "classic_35mm"],
            }
            for key in framing_map.get(framing, []):
                if key in lens_keys:
                    return key

        # Fallback: pick first available
        return lens_keys[0] if lens_keys else None

    def _select_lighting_for_context(
        self,
        lighting_keys: list[str],
        context: "SceneContext | None",
        archetype: str,
    ) -> str | None:
        """Select a lighting description from available keys."""
        try:
            from knowledge.prompt_templates.lighting_setups import LIGHTING_SETUPS
        except ImportError:
            return None

        # Archetype-based lighting preference
        archetype_lighting = {
            "product_hero_shot": ["product_dark_field", "product_backlit_glow", "tabletop_product"],
            "model_portrait_closeup": ["butterfly", "beauty_dish", "clamshell", "rembrandt"],
            "macro_detail": ["raking_texture", "tabletop_product", "product_light_field"],
            "silhouette_artistic": ["silhouette", "backlit"],
            "environment_establishing": ["golden_hour", "blue_hour", "overcast_diffused"],
            "motion_action": ["rim_light", "strobe_flash", "harsh_noon"],
        }

        preferred = archetype_lighting.get(archetype, [])
        for key in preferred:
            if key in lighting_keys:
                setup = LIGHTING_SETUPS.get(key)
                if setup:
                    return setup["prompt"]

        # Context-aware selection
        if context is not None:
            for key in lighting_keys:
                setup = LIGHTING_SETUPS.get(key)
                if not setup:
                    continue
                best_for = setup.get("best_for", [])
                if context.time_of_day == "golden_hour" and "golden" in key:
                    return setup["prompt"]
                if context.environment_type == "studio" and "studio" in key:
                    return setup["prompt"]
                if context.implied_lighting_direction == "backlit" and "back" in key:
                    return setup["prompt"]

        # Fallback: pick random from available
        if lighting_keys:
            key = random.choice(lighting_keys)
            setup = LIGHTING_SETUPS.get(key)
            if setup:
                return setup["prompt"]

        return None

    def _get_context_enrichment(self, context: "SceneContext") -> str:
        """Build enrichment string from SceneContext analysis."""
        additions: list[str] = []

        # Framing
        framing_map = {
            "close_up": "extreme detail, every texture visible, shallow depth of field",
            "wide": "expansive composition, environmental context, leading lines",
            "medium": "balanced composition, subject and environment harmony",
        }
        fr = framing_map.get(context.implied_framing, "")
        if fr:
            additions.append(fr)

        # Time of day
        time_map = {
            "golden_hour": "golden hour warm light, long shadows, 5500K",
            "night": "dramatic night lighting, selective illumination, deep shadows",
            "overcast": "soft diffused daylight, even illumination",
            "morning": "fresh morning light, cool undertones, gentle directional sun",
            "noon": "bright midday sun, hard shadows, high contrast",
            "blue_hour": "blue hour cool ambient, transitional twilight",
        }
        tod = time_map.get(context.time_of_day, "")
        if tod:
            additions.append(tod)

        # Environment
        env_map = {
            "studio": "controlled studio environment",
            "outdoor": "natural outdoor setting, environmental atmosphere",
            "interior": "interior scene, architectural context",
        }
        env = env_map.get(context.environment_type, "")
        if env:
            additions.append(env)

        return ", ".join(additions)

    def _get_default_enrichment(self, context: "SceneContext") -> str:
        """Fallback enrichment when no industry patterns are loaded."""
        return (
            "professional advertising photography, 85mm f/1.8 lens, "
            "natural lighting, photorealistic, 8K detail, "
            "cinematic color grading, shallow depth of field"
        )
