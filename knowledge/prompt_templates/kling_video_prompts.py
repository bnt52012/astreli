"""
Kling AI / Fal.ai video prompt optimization library.

Kling responds best to concrete, physical descriptions of WHAT MOVES and HOW it
moves. Generic "cinematic" language produces ambient, directionless output. The
tables below encode what years of ad-agency trial-and-error on Kling v1.6 →
v2.5-turbo-pro have taught us about the language the model actually follows.

Used by:
  - intelligence/prompt_enricher.py  (builds the final video prompt per scene)
  - main.py _run_real_pipeline        (wraps each scene before Fal.ai submission)
"""
from __future__ import annotations

from typing import Iterable


# ─────────────────────────────────────────────────────────────────────────────
# CAMERA MOVEMENTS
# Kling interprets camera direction from explicit verbs + tracking vocabulary.
# Each entry ships a short "prefix" (the directive), a "details" block (what
# the movement looks like), and a "speed_modifier" (how fast it should feel).
# ─────────────────────────────────────────────────────────────────────────────

CAMERA_MOVEMENTS_KLING: dict[str, dict] = {
    "dolly_in": {
        "prompt_prefix": "Cinematic slow dolly push-in toward the subject.",
        "prompt_details": (
            "Camera glides forward smoothly on a track, gradually revealing "
            "finer details. Background slightly shifts in parallax."
        ),
        "speed_modifier": "Ultra-slow, taking the full duration of the clip.",
        "best_for": ["product_hero", "macro_detail", "reveal"],
    },
    "dolly_out": {
        "prompt_prefix": "Smooth dolly pull-back revealing the full scene.",
        "prompt_details": (
            "Camera retreats steadily, expanding the frame to show environment "
            "context. Subject remains centered."
        ),
        "speed_modifier": "Slow and deliberate reveal.",
        "best_for": ["establishing", "endframe"],
    },
    "orbit_left": {
        "prompt_prefix": "Camera orbits smoothly around the subject from right to left.",
        "prompt_details": (
            "Circular tracking shot at consistent distance, rotating 45-90 "
            "degrees. Subject stays perfectly centered. Lighting shifts "
            "naturally as angle changes."
        ),
        "speed_modifier": "Slow 360-degree rotation feel, majestic pace.",
        "best_for": ["product_hero", "jewelry", "watch", "bottle"],
    },
    "orbit_right": {
        "prompt_prefix": "Camera orbits smoothly around the subject from left to right.",
        "prompt_details": (
            "Circular tracking shot, subject centered, catching different "
            "light angles as camera moves."
        ),
        "speed_modifier": "Slow, elegant rotation.",
        "best_for": ["product_hero", "automotive", "sculpture"],
    },
    # Alias: plain "orbit" → orbit_right by convention
    "orbit": {
        "prompt_prefix": "Camera orbits smoothly around the subject.",
        "prompt_details": (
            "Circular tracking shot at consistent distance, rotating roughly "
            "60 degrees. Subject stays centered. Lighting shifts naturally as "
            "the angle changes."
        ),
        "speed_modifier": "Slow, elegant rotation.",
        "best_for": ["product_hero", "jewelry", "watch", "bottle"],
    },
    "zoom_in": {
        "prompt_prefix": "Gradual optical zoom tightening the frame on the subject.",
        "prompt_details": (
            "Focal length increases smoothly, isolating the subject from its "
            "environment. Depth of field narrows progressively."
        ),
        "speed_modifier": "Very gradual, almost imperceptible zoom.",
        "best_for": ["macro_detail", "portrait", "product_interaction"],
    },
    "zoom_out": {
        "prompt_prefix": "Gradual optical zoom out widening the frame.",
        "prompt_details": (
            "Focal length shortens smoothly, progressively revealing the "
            "environment around the subject."
        ),
        "speed_modifier": "Very gradual reveal.",
        "best_for": ["establishing", "endframe", "context_reveal"],
    },
    "pan_left": {
        "prompt_prefix": "Smooth horizontal pan from right to left.",
        "prompt_details": (
            "Camera rotates on its axis, scanning the scene horizontally. "
            "Reveals new elements as it moves."
        ),
        "speed_modifier": "Slow, cinematic pan.",
        "best_for": ["establishing", "lifestyle", "environment"],
    },
    "pan_right": {
        "prompt_prefix": "Smooth horizontal pan from left to right.",
        "prompt_details": (
            "Camera rotates on its axis, revealing the scene progressively "
            "from left to right."
        ),
        "speed_modifier": "Gentle, revealing pace.",
        "best_for": ["establishing", "lifestyle", "reveal"],
    },
    "crane_up": {
        "prompt_prefix": "Camera rises vertically, revealing the scene from above.",
        "prompt_details": (
            "Smooth vertical ascent, transitioning from close detail to wider "
            "environmental context. Creates sense of grandeur."
        ),
        "speed_modifier": "Majestic, slow rise.",
        "best_for": ["establishing", "luxury", "architecture"],
    },
    "crane_down": {
        "prompt_prefix": "Camera descends smoothly from high angle to eye level.",
        "prompt_details": (
            "Vertical descent revealing the subject progressively. Creates "
            "intimate arrival at the subject."
        ),
        "speed_modifier": "Graceful descent.",
        "best_for": ["product_reveal", "fashion", "food"],
    },
    "static": {
        "prompt_prefix": "Camera is completely locked and static.",
        "prompt_details": (
            "No camera movement at all. Only the subject and environment have "
            "subtle natural motion — liquid movement, fabric sway, light "
            "shifts, steam rising."
        ),
        "speed_modifier": "Static camera, subtle subject animation only.",
        "best_for": ["macro_detail", "portrait", "product_still"],
    },
    "tracking": {
        "prompt_prefix": "Camera tracks alongside the subject's movement.",
        "prompt_details": (
            "Camera moves in parallel with the subject, maintaining consistent "
            "framing. Smooth steadicam feel."
        ),
        "speed_modifier": "Matching subject speed.",
        "best_for": ["motion_action", "lifestyle", "fashion_walk"],
    },
    "handheld": {
        "prompt_prefix": "Subtle handheld camera movement for organic feel.",
        "prompt_details": (
            "Very slight natural camera sway, breathing motion. Creates "
            "documentary authenticity without shakiness."
        ),
        "speed_modifier": "Natural, organic micro-movements.",
        "best_for": ["lifestyle", "behind_scenes", "street_fashion"],
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# SUBJECT ANIMATIONS
# Concrete physics-aware descriptions of how specific elements move. Kling
# follows these verbatim much more reliably than abstract "it moves nicely".
# ─────────────────────────────────────────────────────────────────────────────

SUBJECT_ANIMATIONS_KLING: dict[str, str] = {
    "liquid_pour": (
        "Liquid pours smoothly in a continuous stream, catching light with "
        "dynamic refractions and reflections. Surface tension creates natural "
        "meniscus."
    ),
    "liquid_swirl": (
        "Liquid swirls gently inside the glass, creating dynamic light "
        "patterns and reflections. Natural fluid dynamics."
    ),
    "steam_rise": (
        "Delicate wisps of steam or mist rise slowly and naturally, curling "
        "and dissipating in the air. Volumetric, realistic vapor."
    ),
    "fabric_flow": (
        "Fabric moves with natural wind dynamics — gentle billowing, soft "
        "rippling. Physically accurate cloth simulation."
    ),
    "hair_movement": (
        "Hair sways naturally with subtle wind or head movement. Individual "
        "strands catch light dynamically."
    ),
    "light_shift": (
        "Lighting shifts subtly across the subject surface, as if clouds "
        "passing or time progressing. Natural caustics on reflective surfaces."
    ),
    "rotation_product": (
        "Product rotates slowly on its axis, revealing different facets and "
        "catching light from multiple angles. Smooth, mechanical precision."
    ),
    "sparkle_glint": (
        "Light catches facets of gemstone or metal surface, creating dynamic "
        "sparkle points that shift with perspective."
    ),
    "condensation_drip": (
        "Water condensation droplets form and slowly slide down a cold glass "
        "surface. Realistic water physics."
    ),
    "smoke_wisp": (
        "Thin wisps of smoke drift lazily through the scene, creating "
        "atmospheric depth. Volumetric and translucent."
    ),
    "candle_flicker": (
        "Warm candlelight flickers subtly, creating gentle dancing shadows "
        "and warm light shifts on nearby surfaces."
    ),
    "reflection_ripple": (
        "Reflections on water or polished surfaces ripple gently, distorting "
        "and reforming the reflected image."
    ),
    "page_turn": (
        "Pages turn slowly with natural paper physics, catching light on "
        "each page surface."
    ),
    "door_reveal": (
        "Door or lid opens slowly, revealing contents with dramatic lighting "
        "from within."
    ),
    "unboxing": (
        "Packaging opens elegantly, tissue paper parts to reveal product "
        "beneath. Luxurious unveiling."
    ),
}


# ─────────────────────────────────────────────────────────────────────────────
# MOOD MODIFIERS
# Pace + intention cues that land at the end of the prompt.
# ─────────────────────────────────────────────────────────────────────────────

MOOD_MODIFIERS_KLING: dict[str, str] = {
    "luxury": (
        "Ultra-slow, deliberate, every frame breathes elegance. No rushed "
        "movements. Cinematic 24fps with slight motion blur."
    ),
    "energetic": (
        "Dynamic, purposeful movement. Slightly faster pace with sharp focus. "
        "Active energy without chaos."
    ),
    "serene": (
        "Peaceful, meditative pace. Movements are barely perceptible, "
        "creating a sense of calm contemplation."
    ),
    "dramatic": (
        "Bold contrasts in movement speed. Slow build to key moments. "
        "Theatrical lighting shifts."
    ),
    "playful": (
        "Light, bouncy energy. Subtle acceleration and deceleration. "
        "Youthful dynamism."
    ),
    "mysterious": (
        "Slow reveals, shadows in motion. Fog or haze adding depth. "
        "Enigmatic atmosphere."
    ),
    "romantic": (
        "Soft, dreamy motion. Shallow depth of field shifts. Warm, gentle "
        "light movements."
    ),
    "powerful": (
        "Strong, confident movement. Low angle perspectives. Commanding "
        "presence."
    ),
}


# Industry → default mood map. Used when a scene enricher doesn't get an
# explicit mood from the caller.
INDUSTRY_MOOD_DEFAULTS: dict[str, str] = {
    "luxury": "luxury",
    "jewelry_watches": "luxury",
    "fragrance": "romantic",
    "beauty": "serene",
    "fashion": "luxury",
    "automotive": "powerful",
    "food_beverage": "luxury",
    "sport": "energetic",
    "tech": "dramatic",
    "real_estate": "serene",
    "hospitality": "serene",
}


# ─────────────────────────────────────────────────────────────────────────────
# Auto-detection helpers
# ─────────────────────────────────────────────────────────────────────────────

# Keyword → [animation keys]. Order matters: the first match wins per family.
_KEYWORD_TO_ANIMATIONS: list[tuple[tuple[str, ...], list[str]]] = [
    (("whiskey", "bourbon", "rum", "tequila", "cognac", "spirit", "liqueur"),
        ["liquid_swirl", "light_shift"]),
    (("wine", "champagne", "cocktail", "beverage", "drink", "liquid"),
        ["liquid_swirl", "light_shift"]),
    (("pour", "pouring", "stream"),
        ["liquid_pour"]),
    (("steam", "mist", "fog", "vapor"),
        ["steam_rise"]),
    (("smoke",),
        ["smoke_wisp"]),
    (("silk", "dress", "gown", "fabric", "cloth", "drape", "scarf"),
        ["fabric_flow"]),
    (("hair", "mane", "strands"),
        ["hair_movement"]),
    (("candle", "flame", "fire"),
        ["candle_flicker"]),
    (("diamond", "crystal", "gem", "sparkle", "facet", "gemstone"),
        ["sparkle_glint", "light_shift"]),
    (("condensation", "chilled", "ice-cold", "frozen", "frosted"),
        ["condensation_drip"]),
    (("water", "pond", "lake", "pool", "reflection", "puddle"),
        ["reflection_ripple"]),
    (("page", "book", "magazine"),
        ["page_turn"]),
    (("unbox", "packaging", "reveal", "box opens", "lid"),
        ["unboxing", "door_reveal"]),
    (("bottle", "flask", "decanter", "jar", "vial"),
        ["rotation_product", "light_shift"]),
    (("watch", "timepiece", "dial", "bezel"),
        ["rotation_product", "sparkle_glint"]),
    (("perfume", "fragrance", "eau de"),
        ["rotation_product", "light_shift"]),
    (("car", "automobile", "vehicle", "sports car"),
        ["rotation_product", "light_shift"]),
    (("product", "object", "item"),
        ["rotation_product", "light_shift"]),
]


def detect_subject_animations(text: str, *, max_animations: int = 3) -> list[str]:
    """Heuristic keyword → animation list.

    Scans the scene description and returns up to ``max_animations`` keys from
    ``SUBJECT_ANIMATIONS_KLING`` that best describe what should move in the
    shot. Preserves first-match ordering for deterministic output.
    """
    if not text:
        return []
    lowered = text.lower()
    out: list[str] = []
    for keywords, anims in _KEYWORD_TO_ANIMATIONS:
        if any(k in lowered for k in keywords):
            for a in anims:
                if a not in out:
                    out.append(a)
                    if len(out) >= max_animations:
                        return out
    return out


def mood_for_industry(industry: str | None, default: str = "luxury") -> str:
    """Map an industry key to a Kling mood modifier key."""
    if not industry:
        return default
    return INDUSTRY_MOOD_DEFAULTS.get(industry.lower(), default)


# ─────────────────────────────────────────────────────────────────────────────
# PROMPT BUILDER
# ─────────────────────────────────────────────────────────────────────────────

def build_kling_video_prompt(
    scene_description: str,
    camera_movement: str,
    subject_animations: Iterable[str] | None = None,
    mood: str = "luxury",
    duration_seconds: float = 5.0,
) -> str:
    """Build an optimized Kling/Fal.ai video prompt.

    Combines: scene content → camera movement → subject animations → mood →
    technical tail. The ordering matters: Kling anchors on the first ~200
    tokens for subject, then reads camera language, then atmospheric cues.

    Args:
        scene_description: What is in the frame (from GPT-4o prompt_video).
        camera_movement: Key in CAMERA_MOVEMENTS_KLING (static/dolly_in/...).
        subject_animations: Keys in SUBJECT_ANIMATIONS_KLING. If None, returns
            no animation lines — caller should run ``detect_subject_animations``
            first.
        mood: Key in MOOD_MODIFIERS_KLING. Defaults to "luxury".
        duration_seconds: Target clip length (seconds).

    Returns:
        A single-line prompt string ready to pass to fal_client.subscribe.
    """
    parts: list[str] = []

    # 1. Scene content (WHAT is in the frame — leads the prompt)
    if scene_description and scene_description.strip():
        parts.append(scene_description.strip().rstrip("."))

    # 2. Camera movement directive + detail
    cam = CAMERA_MOVEMENTS_KLING.get(camera_movement) or CAMERA_MOVEMENTS_KLING["static"]
    parts.append(cam["prompt_prefix"].rstrip("."))
    parts.append(cam["prompt_details"].rstrip("."))

    # 3. Subject animations (physics-specific motion)
    if subject_animations:
        for anim_key in subject_animations:
            text = SUBJECT_ANIMATIONS_KLING.get(anim_key)
            if text:
                parts.append(text.rstrip("."))

    # 4. Mood modifier
    mood_text = MOOD_MODIFIERS_KLING.get(mood) or MOOD_MODIFIERS_KLING["luxury"]
    parts.append(mood_text.rstrip("."))

    # 5. Technical tail
    parts.append(
        f"Duration: {duration_seconds:.1f} seconds. Photorealistic, 8K "
        f"quality, cinematic depth of field"
    )

    return ". ".join(p for p in parts if p) + "."


__all__ = [
    "CAMERA_MOVEMENTS_KLING",
    "SUBJECT_ANIMATIONS_KLING",
    "MOOD_MODIFIERS_KLING",
    "INDUSTRY_MOOD_DEFAULTS",
    "detect_subject_animations",
    "mood_for_industry",
    "build_kling_video_prompt",
]
