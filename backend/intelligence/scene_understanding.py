"""
Deep Scene Understanding Module.

Parses natural language scene descriptions to extract implied technical
requirements for optimal pipeline routing and prompt construction.

This module does NOT make creative decisions. It deeply UNDERSTANDS
what the client wrote to route it perfectly through the pipeline.

Examples of understanding:
- "she walks toward camera" -> tracking shot + forward motion in Kling
- "close-up on her wrist" -> macro framing in Gemini prompt
- "same location but at sunset" -> reference scene N's decor + modify lighting
- "she holds the bottle" -> mannequin + product in same frame -> Nano Banana Pro
- "the bottle rotates slowly" -> product-only -> Kling-V3 orbit mode

The client never sees any of this analysis. They just see a perfect result.
"""

from __future__ import annotations

import logging
import re

from backend.models.enums import (
    CameraMovement,
    EmotionalTone,
    SceneType,
)
from backend.models.scene import SceneAnalysis, SceneContext

logger = logging.getLogger(__name__)


# ── Natural Language Pattern Matchers ─────────────────────────

# Camera work detection patterns (description text -> CameraMovement)
CAMERA_PATTERNS: list[tuple[re.Pattern, CameraMovement]] = [
    (re.compile(r"walk[s]?\s+(toward|towards|to)\s+(the\s+)?camera", re.I), CameraMovement.DOLLY_IN),
    (re.compile(r"approach(es)?\s+(the\s+)?camera", re.I), CameraMovement.DOLLY_IN),
    (re.compile(r"camera\s+pull[s]?\s+back", re.I), CameraMovement.DOLLY_OUT),
    (re.compile(r"walk[s]?\s+away", re.I), CameraMovement.DOLLY_OUT),
    (re.compile(r"reveal\s+shot", re.I), CameraMovement.DOLLY_OUT),
    (re.compile(r"orbit|circle[s]?\s+around|rotating?\s+around", re.I), CameraMovement.ORBIT),
    (re.compile(r"360|turntable|spin(s|ning)?", re.I), CameraMovement.ORBIT),
    (re.compile(r"track(s|ing)?\s+(left|right|alongside|follow)", re.I), CameraMovement.TRACKING),
    (re.compile(r"follow(s|ing)?\s+\w+\s+(as|while)", re.I), CameraMovement.TRACKING),
    (re.compile(r"crane\s+up|rise[s]?\s+up|ascend", re.I), CameraMovement.CRANE_UP),
    (re.compile(r"aerial\s+rise|drone\s+up", re.I), CameraMovement.CRANE_UP),
    (re.compile(r"crane\s+down|descend|lower", re.I), CameraMovement.CRANE_DOWN),
    (re.compile(r"pan[s]?\s+left", re.I), CameraMovement.PAN_LEFT),
    (re.compile(r"pan[s]?\s+right", re.I), CameraMovement.PAN_RIGHT),
    (re.compile(r"zoom[s]?\s+in|push\s+in", re.I), CameraMovement.ZOOM_IN),
    (re.compile(r"zoom[s]?\s+out|pull\s+out", re.I), CameraMovement.ZOOM_OUT),
    (re.compile(r"handheld|shaky|documentary", re.I), CameraMovement.HANDHELD),
    (re.compile(r"steadicam|smooth\s+follow|glide", re.I), CameraMovement.STEADICAM),
    (re.compile(r"tilt[s]?\s+up|look[s]?\s+up", re.I), CameraMovement.TILT_UP),
    (re.compile(r"tilt[s]?\s+down|look[s]?\s+down", re.I), CameraMovement.TILT_DOWN),
    (re.compile(r"static|still|fixed|locked", re.I), CameraMovement.STATIC),
]

# Emotional tone detection patterns
TONE_PATTERNS: list[tuple[re.Pattern, EmotionalTone]] = [
    (re.compile(r"luxur(y|ious)|opulen|prestig|premium|exclusive|haute", re.I), EmotionalTone.LUXURY),
    (re.compile(r"energy|energetic|dynamic|explosive|power|fast|adrenaline|sport", re.I), EmotionalTone.ENERGETIC),
    (re.compile(r"intimate|close|personal|tender|gentle|soft\s+touch|caress", re.I), EmotionalTone.INTIMATE),
    (re.compile(r"dramat(ic)?|epic|intense|powerful|bold|striking|cinematic", re.I), EmotionalTone.DRAMATIC),
    (re.compile(r"playful|fun|cheerful|bright|colorful|joyful|whimsical", re.I), EmotionalTone.PLAYFUL),
    (re.compile(r"minimal(ist)?|clean|pure|simple|white\s+space|zen|austere", re.I), EmotionalTone.MINIMALIST),
    (re.compile(r"nostalg(ic|ia)|vintage|retro|classic|timeless|heritage|memory", re.I), EmotionalTone.NOSTALGIC),
    (re.compile(r"powerful|strong|fierce|confident|empower|warrior|champion", re.I), EmotionalTone.POWERFUL),
    (re.compile(r"serene|calm|peaceful|tranquil|zen|meditat|breath", re.I), EmotionalTone.SERENE),
    (re.compile(r"myster(y|ious)|enigma|shadow|dark|noir|secret|intrigue", re.I), EmotionalTone.MYSTERIOUS),
    (re.compile(r"joy(ful|ous)?|happy|celebrat|laugh|smile|delight|euphori", re.I), EmotionalTone.JOYFUL),
    (re.compile(r"elegan(t|ce)|grace(ful)?|refine|sophisticat|poised|chic", re.I), EmotionalTone.ELEGANT),
]

# Scene cross-reference patterns
REFERENCE_PATTERNS: list[re.Pattern] = [
    re.compile(r"same\s+(location|place|setting|room|environment)\s+as\s+scene\s+(\d+)", re.I),
    re.compile(r"same\s+as\s+scene\s+(\d+)\s+but", re.I),
    re.compile(r"return(s|ing)?\s+to\s+scene\s+(\d+)", re.I),
    re.compile(r"back\s+(in|at|to)\s+the\s+same", re.I),
    re.compile(r"continuation\s+of\s+scene\s+(\d+)", re.I),
]

# Product interaction patterns (mannequin + product in same frame)
PRODUCT_INTERACTION_PATTERNS: list[re.Pattern] = [
    re.compile(r"hold(s|ing)?\s+the\s+(bottle|product|box|package|item|perfume|cream|lipstick)", re.I),
    re.compile(r"appl(y|ies|ying)\s+the\s+(product|cream|perfume|lipstick|serum|fragrance)", re.I),
    re.compile(r"touch(es|ing)?\s+the\s+(bottle|product|cap|lid|surface)", re.I),
    re.compile(r"spray(s|ing)?\s+(the\s+)?(perfume|fragrance|product|mist)", re.I),
    re.compile(r"pour(s|ing)?\s+(the\s+)?(liquid|cream|product|oil|serum)", re.I),
    re.compile(r"open(s|ing)?\s+(the\s+)?(box|package|bottle|cap|jar)", re.I),
    re.compile(r"wear(s|ing)?\s+(the\s+)?(watch|jewelry|necklace|bracelet|ring|earring)", re.I),
    re.compile(r"(model|mannequin|person|she|he)\s+with\s+(the\s+)?product", re.I),
    re.compile(r"product\s+(in|on)\s+(her|his)\s+hand", re.I),
    re.compile(r"display(s|ing)?\s+the\s+product", re.I),
]

# Wardrobe change detection
WARDROBE_PATTERNS: list[re.Pattern] = [
    re.compile(r"(now\s+)?wear(s|ing)?\s+(a\s+)?(different|new|another)\s+(outfit|dress|suit|clothing)", re.I),
    re.compile(r"change[ds]?\s+(into|to)\s+(a\s+)?(new|different|another)", re.I),
    re.compile(r"(different|new|another)\s+(outfit|dress|look|costume|attire)", re.I),
    re.compile(r"wardrobe\s+change", re.I),
]

# Text overlay detection
TEXT_OVERLAY_PATTERNS: list[re.Pattern] = [
    re.compile(r"(brand\s+name|logo|title|slogan|tagline|text|CTA|call\s+to\s+action)\s+(appear|display|show|overlay|fade)", re.I),
    re.compile(r"(display|show|overlay|reveal)[s]?\s+(the\s+)?(brand|logo|title|text|slogan)", re.I),
    re.compile(r"title\s+(card|screen|slide)", re.I),
    re.compile(r"end\s+(card|screen|slate)", re.I),
    re.compile(r"\"[^\"]+\".*\b(appear|display|show|text)\b", re.I),
]

# Framing/composition detection
FRAMING_PATTERNS: dict[str, re.Pattern] = {
    "extreme_closeup": re.compile(r"extreme\s+close[\s-]?up|ECU|macro\s+shot|detail\s+shot", re.I),
    "closeup": re.compile(r"close[\s-]?up|tight\s+shot|CU\b", re.I),
    "medium_closeup": re.compile(r"medium\s+close[\s-]?up|MCU|bust\s+shot", re.I),
    "medium": re.compile(r"medium\s+shot|waist\s+shot|MS\b|mid[\s-]?shot", re.I),
    "wide": re.compile(r"wide\s+shot|full\s+shot|WS\b|establishing", re.I),
    "extreme_wide": re.compile(r"extreme\s+wide|EWS|aerial|panoram|landscape", re.I),
}

# Multi-character detection
CHARACTER_PATTERNS: list[re.Pattern] = [
    re.compile(r"(character|person|model|mannequin)\s+[AB]\b", re.I),
    re.compile(r"(first|second|other)\s+(model|character|person|mannequin)", re.I),
    re.compile(r"(two|both|couple|pair|duo)\s+(model|character|person|mannequin)", re.I),
]


class SceneUnderstanding:
    """Deeply understands scene descriptions to route them optimally.

    Extracts implied technical requirements from natural language
    without changing the client's creative intent. All understanding
    is used for pipeline routing and prompt enrichment only.
    """

    def analyze_scene(
        self,
        scene: SceneAnalysis,
        all_scenes: list[SceneAnalysis] | None = None,
    ) -> SceneContext:
        """Analyze a single scene and extract its technical context.

        Args:
            scene: The GPT-4o scene analysis to understand deeply.
            all_scenes: All scenes in the scenario (for cross-references).

        Returns:
            SceneContext with extracted technical understanding.
        """
        text = f"{scene.description} {scene.image_prompt} {scene.video_prompt}"
        ctx = SceneContext()

        # Detect emotional tone
        ctx.emotional_tone = self._detect_tone(text)

        # Detect implied camera work
        ctx.detected_camera_work = self._detect_camera_work(text, scene.camera_movement)

        # Detect product interaction (mannequin holding/using product)
        ctx.requires_product_in_frame = self._detect_product_interaction(text)

        # If scene has mannequin AND product interaction -> must use Pro model
        if scene.needs_mannequin or scene.type == SceneType.PERSONNAGE:
            ctx.requires_face_consistency = True

        # Detect wardrobe changes
        ctx.has_wardrobe_change = self._detect_wardrobe_change(text)

        # Detect cross-scene references
        if all_scenes:
            ctx.linked_scene_ids = self._detect_scene_references(text)

        # Detect multi-character scenarios
        ctx.character_id = self._detect_character_id(text)

        # Build enrichment keywords from analysis
        ctx.enrichment_keywords = self._extract_enrichment_keywords(scene, ctx)

        # Suggest technical parameters based on understanding
        ctx.lighting_suggestion = self._suggest_lighting(ctx.emotional_tone, text)
        ctx.lens_suggestion = self._suggest_lens(text)
        ctx.composition_suggestion = self._suggest_composition(text)

        logger.info(
            "[UNDERSTANDING] Scene %d: tone=%s, camera=%s, face_consistency=%s, "
            "product_in_frame=%s, wardrobe_change=%s",
            scene.id,
            ctx.emotional_tone.value,
            ctx.detected_camera_work.value,
            ctx.requires_face_consistency,
            ctx.requires_product_in_frame,
            ctx.has_wardrobe_change,
        )

        return ctx

    def analyze_all_scenes(
        self,
        scenes: list[SceneAnalysis],
    ) -> list[SceneContext]:
        """Analyze all scenes with cross-reference awareness.

        Args:
            scenes: All scenes from the scenario analysis.

        Returns:
            List of SceneContext, one per scene.
        """
        contexts = []
        for scene in scenes:
            ctx = self.analyze_scene(scene, all_scenes=scenes)
            contexts.append(ctx)

        # Post-processing: propagate linked scene context
        self._propagate_cross_references(scenes, contexts)

        return contexts

    def should_route_to_pro(self, scene: SceneAnalysis, context: SceneContext) -> bool:
        """Determine if a scene should use Gemini Pro (chat session) instead of Flash.

        The rule: if there's ANY possibility the mannequin's face needs to appear
        consistently, route to Pro. When in doubt, choose the higher-quality path.

        Args:
            scene: The scene analysis.
            context: The extracted scene context.

        Returns:
            True if the scene should use Gemini Pro chat session.
        """
        # Explicit personnage scene
        if scene.type == SceneType.PERSONNAGE:
            return True

        # Mannequin is needed (GPT-4o flagged it)
        if scene.needs_mannequin:
            return True

        # Product interaction detected (mannequin holding/using product)
        if context.requires_product_in_frame and context.requires_face_consistency:
            return True

        return False

    # ── Private Detection Methods ─────────────────────────────

    def _detect_tone(self, text: str) -> EmotionalTone:
        """Detect the emotional tone from scene text."""
        scores: dict[EmotionalTone, int] = {}
        for pattern, tone in TONE_PATTERNS:
            matches = pattern.findall(text)
            if matches:
                scores[tone] = scores.get(tone, 0) + len(matches)

        if scores:
            return max(scores, key=scores.get)
        return EmotionalTone.ELEGANT  # Default for advertising

    def _detect_camera_work(self, text: str, explicit_camera: str) -> CameraMovement:
        """Detect camera movement from text, preferring explicit value."""
        # If GPT-4o already set a specific camera movement, respect it
        try:
            explicit = CameraMovement(explicit_camera.lower().replace(" ", "_"))
            if explicit != CameraMovement.STATIC:
                return explicit
        except ValueError:
            pass

        # Detect from natural language
        for pattern, movement in CAMERA_PATTERNS:
            if pattern.search(text):
                return movement

        return CameraMovement.STATIC

    def _detect_product_interaction(self, text: str) -> bool:
        """Detect if the mannequin interacts with the product in this scene."""
        return any(p.search(text) for p in PRODUCT_INTERACTION_PATTERNS)

    def _detect_wardrobe_change(self, text: str) -> bool:
        """Detect if this scene involves a wardrobe/outfit change."""
        return any(p.search(text) for p in WARDROBE_PATTERNS)

    def _detect_scene_references(self, text: str) -> list[int]:
        """Detect references to other scenes by number."""
        referenced: list[int] = []
        for pattern in REFERENCE_PATTERNS:
            for match in pattern.finditer(text):
                for group in match.groups():
                    if group and group.isdigit():
                        referenced.append(int(group))
        return sorted(set(referenced))

    def _detect_character_id(self, text: str) -> str | None:
        """Detect if a specific character (A, B, etc.) is referenced."""
        for pattern in CHARACTER_PATTERNS:
            match = pattern.search(text)
            if match:
                # Try to extract character identifier
                full = match.group(0).upper()
                if " A" in full or "FIRST" in full:
                    return "A"
                if " B" in full or "SECOND" in full:
                    return "B"
        return None

    def _extract_enrichment_keywords(
        self,
        scene: SceneAnalysis,
        context: SceneContext,
    ) -> list[str]:
        """Extract keywords that can silently improve prompt quality."""
        keywords: list[str] = []

        # Framing keywords
        for frame_type, pattern in FRAMING_PATTERNS.items():
            if pattern.search(scene.description) or pattern.search(scene.image_prompt):
                keywords.append(frame_type.replace("_", " "))

        # Text overlay detection
        for pattern in TEXT_OVERLAY_PATTERNS:
            if pattern.search(scene.description):
                keywords.append("text_overlay")
                break

        # Seasonal/temporal context
        seasonal_patterns = {
            "christmas": re.compile(r"christmas|xmas|holiday|festiv|winter\s+magic", re.I),
            "summer": re.compile(r"summer|beach|tropical|sun(ny|lit|shine)|pool", re.I),
            "autumn": re.compile(r"autumn|fall|harvest|golden\s+leaves|october", re.I),
            "spring": re.compile(r"spring|bloom|blossom|fresh|renewal|garden", re.I),
            "night": re.compile(r"night|evening|moonl|star(s|lit|ry)|neon|city\s+lights", re.I),
            "golden_hour": re.compile(r"golden\s+hour|sunset|sunrise|dawn|dusk|magic\s+hour", re.I),
        }
        for season, pattern in seasonal_patterns.items():
            if pattern.search(f"{scene.description} {scene.image_prompt}"):
                keywords.append(season)

        return keywords

    def _suggest_lighting(self, tone: EmotionalTone, text: str) -> str:
        """Suggest lighting setup based on emotional tone."""
        lighting_map: dict[EmotionalTone, str] = {
            EmotionalTone.LUXURY: "soft golden key light, subtle rim light, warm color temperature 3200K",
            EmotionalTone.ENERGETIC: "high contrast lighting, strong directional key, vibrant fill",
            EmotionalTone.INTIMATE: "warm low-key lighting, soft wraparound, candlelight warmth",
            EmotionalTone.DRAMATIC: "chiaroscuro lighting, strong shadows, single hard key light",
            EmotionalTone.PLAYFUL: "bright even lighting, colorful accents, high key",
            EmotionalTone.MINIMALIST: "clean studio lighting, large softbox, even diffusion",
            EmotionalTone.NOSTALGIC: "warm tungsten tones, soft diffusion, slightly desaturated",
            EmotionalTone.POWERFUL: "heroic lighting from below, rim light separation, high contrast",
            EmotionalTone.SERENE: "soft natural light, overcast diffusion, cool neutral tones",
            EmotionalTone.MYSTERIOUS: "low-key noir lighting, deep shadows, isolated pools of light",
            EmotionalTone.JOYFUL: "bright natural sunlight, fill flash, high key cheerful",
            EmotionalTone.ELEGANT: "Rembrandt lighting, subtle fill, neutral-warm color temperature",
        }
        return lighting_map.get(tone, "")

    def _suggest_lens(self, text: str) -> str:
        """Suggest lens choice based on scene content."""
        text_lower = text.lower()

        if any(w in text_lower for w in ("macro", "detail", "texture", "close-up on product", "extreme close")):
            return "100mm macro f/2.8"
        if any(w in text_lower for w in ("portrait", "face", "beauty", "close-up on her", "close-up on his")):
            return "85mm f/1.4"
        if any(w in text_lower for w in ("wide", "landscape", "establishing", "panoram", "environ")):
            return "24mm f/2.8"
        if any(w in text_lower for w in ("product shot", "still life", "packshot", "bottle")):
            return "90mm f/2.8 macro"
        if any(w in text_lower for w in ("full body", "fashion", "editorial")):
            return "50mm f/1.4"

        return "50mm f/1.4"  # Versatile default

    def _suggest_composition(self, text: str) -> str:
        """Suggest composition approach based on scene content."""
        text_lower = text.lower()

        if any(w in text_lower for w in ("text", "slogan", "title", "CTA", "overlay")):
            return "rule of thirds with negative space for text placement"
        if any(w in text_lower for w in ("product center", "hero shot", "packshot")):
            return "centered composition, symmetrical framing"
        if any(w in text_lower for w in ("walk", "path", "road", "corridor", "approach")):
            return "leading lines drawing the eye to the subject"
        if any(w in text_lower for w in ("landscape", "wide", "establishing")):
            return "rule of thirds, foreground interest, layered depth"

        return "rule of thirds"

    def _propagate_cross_references(
        self,
        scenes: list[SceneAnalysis],
        contexts: list[SceneContext],
    ) -> None:
        """When a scene references another, propagate relevant context."""
        for i, ctx in enumerate(contexts):
            for ref_id in ctx.linked_scene_ids:
                ref_idx = ref_id - 1  # Scene IDs are 1-based
                if 0 <= ref_idx < len(contexts):
                    ref_ctx = contexts[ref_idx]
                    # If referencing a personnage scene, this one might need consistency too
                    if ref_ctx.requires_face_consistency:
                        ctx.requires_face_consistency = True
                    # Propagate character ID if referencing same character
                    if ref_ctx.character_id and not ctx.character_id:
                        ctx.character_id = ref_ctx.character_id
