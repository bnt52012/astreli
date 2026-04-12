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

import json
import logging
import random
from pathlib import Path
from typing import Any, TYPE_CHECKING

if TYPE_CHECKING:
    from intelligence.scene_understanding import SceneContext

from knowledge.industry_detector import IndustryDetector, IndustryMatch

logger = logging.getLogger(__name__)


# ── Real-ads dataset location ───────────────────────────────────────────
# Populated by generate_real_ad_analyses.py — 1000 shot-by-shot breakdowns
# of real iconic campaigns. Each JSON file has a `plans` array where every
# plan carries a gold-standard `kling_prompt` and `gemini_prompt` field.

REAL_ADS_DIR = Path("dataset/real_ads")


# Map archetype → preferred shot_size buckets (from generate_real_ad_analyses.py
# schema). Lets us find training examples whose framing matches the scene we
# are currently enriching.
_ARCHETYPE_TO_SHOT_SIZE: dict[str, list[str]] = {
    "product_hero_shot": ["close_up", "medium_close"],
    "macro_detail": ["extreme_close_up", "close_up"],
    "model_portrait_closeup": ["close_up", "medium_close"],
    "hands_only": ["close_up", "medium_close"],
    "product_interaction": ["close_up", "medium_close", "medium"],
    "packshot_endframe": ["medium_close", "close_up"],
    "ingredient_component": ["extreme_close_up", "close_up"],
    "unboxing_reveal": ["close_up", "medium"],
    "lifestyle_context": ["medium", "medium_close", "wide"],
    "slow_motion_moment": ["close_up", "medium_close"],
    "motion_action": ["medium", "wide"],
    "environment_establishing": ["wide", "extreme_wide"],
    "aerial_drone": ["extreme_wide", "wide"],
    "pov_first_person": ["medium", "medium_close"],
    "silhouette_artistic": ["medium", "wide"],
    "reflection_mirror": ["close_up", "medium_close"],
    "before_after_transform": ["medium_close", "medium"],
    "call_to_action": ["medium_close", "medium"],
}


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
        # Real-ads cache: industry_key → list of ad dicts (each with `plans`)
        self._real_ads_cache: dict[str, list[dict[str, Any]]] | None = None
        self._real_ads_loaded = False

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

    # ── Real-ad analyses (gold-standard training examples) ─────────

    def load_real_ads(self, force: bool = False) -> int:
        """Lazy-load 1000 real-ad breakdowns into an in-memory index.

        Walks ``dataset/real_ads/<industry>/*.json`` and groups records by
        industry key. Safe to call multiple times — returns immediately on
        subsequent calls unless ``force=True``.

        Returns:
            Number of ads loaded (0 if the directory is missing or empty).
        """
        if self._real_ads_loaded and not force:
            return sum(len(v) for v in (self._real_ads_cache or {}).values())

        cache: dict[str, list[dict[str, Any]]] = {}
        if not REAL_ADS_DIR.exists():
            self._real_ads_cache = cache
            self._real_ads_loaded = True
            logger.info("Real-ads directory %s not found — skipping", REAL_ADS_DIR)
            return 0

        total = 0
        for path in REAL_ADS_DIR.rglob("*.json"):
            if path.name.startswith("_"):
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as e:
                logger.debug("Skip real-ad %s: %s", path, e)
                continue
            plans = data.get("plans") or []
            if not plans:
                continue
            industry_key = (
                data.get("_industry_key")
                or data.get("industry")
                or "unknown"
            ).lower()
            cache.setdefault(industry_key, []).append(data)
            total += 1

        self._real_ads_cache = cache
        self._real_ads_loaded = True
        logger.info(
            "Real-ads loaded: %d ads across %d industries",
            total, len(cache),
        )
        return total

    def find_similar_real_ads(
        self,
        industry: str,
        archetype: str = "",
        shot_size: str = "",
        camera_movement: str = "",
        n: int = 3,
    ) -> list[dict[str, Any]]:
        """Return up to ``n`` matching (ad, plan) pairs for a target scene.

        Matches first by industry, then filters plans by shot_size derived
        from the archetype, then (optionally) by camera movement. Each
        returned dict is flat: {brand, agency, campaign_name, plan}.

        Args:
            industry: Industry key (luxury_fashion, beauty_cosmetics, …).
            archetype: Scene archetype key; maps to preferred shot_size list.
            shot_size: Explicit shot_size override (takes precedence over
                the archetype mapping).
            camera_movement: Optional secondary filter.
            n: Maximum number of examples to return.

        Returns:
            List of dicts with keys: brand, agency, campaign_name, plan.
        """
        self.load_real_ads()
        cache = self._real_ads_cache or {}
        if not cache:
            return []

        industry_key = (industry or "").lower()
        pool: list[dict[str, Any]] = cache.get(industry_key, [])
        if not pool:
            # Loose fallback: any ad whose industry string starts with ours
            for k, v in cache.items():
                if k.startswith(industry_key) or industry_key.startswith(k):
                    pool.extend(v)
            if not pool:
                return []

        preferred_sizes = [shot_size] if shot_size else _ARCHETYPE_TO_SHOT_SIZE.get(
            archetype, []
        )

        # Score every (ad, plan) combination.
        scored: list[tuple[int, dict[str, Any], dict[str, Any]]] = []
        for ad in pool:
            for plan in ad.get("plans", []) or []:
                score = 0
                p_size = (plan.get("shot_size") or "").lower()
                if preferred_sizes and p_size in preferred_sizes:
                    score += 3 if p_size == (preferred_sizes[0] if preferred_sizes else "") else 2
                if camera_movement and (plan.get("camera_movement") or "").lower() == camera_movement.lower():
                    score += 2
                if plan.get("kling_prompt") and plan.get("gemini_prompt"):
                    score += 1  # complete plans preferred
                if score > 0:
                    scored.append((score, ad, plan))

        if not scored:
            # Fallback: take random plans from this industry pool
            fallback: list[dict[str, Any]] = []
            random.shuffle(pool)
            for ad in pool:
                for plan in ad.get("plans", []) or []:
                    if plan.get("kling_prompt") and plan.get("gemini_prompt"):
                        fallback.append({
                            "brand": ad.get("brand", ""),
                            "agency": ad.get("agency", ""),
                            "campaign_name": ad.get("campaign_name", ""),
                            "plan": plan,
                        })
                        break
                if len(fallback) >= n:
                    break
            return fallback[:n]

        scored.sort(key=lambda t: t[0], reverse=True)
        results: list[dict[str, Any]] = []
        seen_ads: set[int] = set()
        for score, ad, plan in scored:
            ad_id = id(ad)
            if ad_id in seen_ads:
                continue  # avoid picking two plans from the same campaign
            seen_ads.add(ad_id)
            results.append({
                "brand": ad.get("brand", ""),
                "agency": ad.get("agency", ""),
                "campaign_name": ad.get("campaign_name", ""),
                "plan": plan,
            })
            if len(results) >= n:
                break
        return results

    def build_real_ad_reference(
        self,
        examples: list[dict[str, Any]],
        field: str,
    ) -> str:
        """Format matched real-ad examples as a single reference line.

        Args:
            examples: Output of ``find_similar_real_ads``.
            field: Either ``kling_prompt`` or ``gemini_prompt``.

        Returns:
            A human-readable reference string (empty if no usable examples).
        """
        if not examples:
            return ""
        lines: list[str] = []
        for ex in examples:
            plan = ex.get("plan") or {}
            text = (plan.get(field) or "").strip()
            if not text:
                continue
            brand = ex.get("brand") or "an award-winning brand"
            lines.append(f'Reference style from "{brand}" campaign: {text}')
        return " ".join(lines)

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

        # 7. Real-ad reference (gold-standard gemini_prompt from similar shots)
        try:
            examples = self.find_similar_real_ads(
                industry=industry,
                archetype=archetype,
                n=2,
            )
            ref = self.build_real_ad_reference(examples, "gemini_prompt")
            if ref:
                parts.append(ref)
        except Exception as e:
            logger.debug("real-ad image enrichment skipped: %s", e)

        # 8. Base quality
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

        # Real-ad reference (gold-standard kling_prompt from similar shots)
        try:
            archetype_hint = self.detect_archetype(original_prompt or "")
            cam_hint = (
                scene_context.implied_camera_movement
                if scene_context is not None
                else ""
            )
            examples = self.find_similar_real_ads(
                industry=industry,
                archetype=archetype_hint,
                camera_movement=cam_hint or "",
                n=2,
            )
            ref = self.build_real_ad_reference(examples, "kling_prompt")
            if ref:
                parts.append(ref)
        except Exception as e:
            logger.debug("real-ad video enrichment skipped: %s", e)

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
