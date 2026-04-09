"""
Transition Grammar — Which transitions work between which scene types.

Defines the default transition choices based on scene-pair combinations.
The client can always override these defaults in their scenario.
"""

from __future__ import annotations

# Default transition when scene pair not found
DEFAULT_TRANSITION = "dissolve"

# Scene type → scene type → recommended transition
# Keys are SceneType values or SceneArchetype values
TRANSITION_RULES: dict[str, dict[str, str]] = {
    # ── From personnage scenes ────────────────────────────────
    "personnage": {
        "personnage": "dissolve",       # Smooth personality continuity
        "produit": "dissolve",          # Elegant shift from person to product
        "transition": "fade",           # Clean exit to title/text
        "endframe": "dissolve",         # Graceful close
    },
    # ── From produit scenes ───────────────────────────────────
    "produit": {
        "personnage": "dissolve",       # Re-introduce the human element
        "produit": "cut",               # Dynamic product montage
        "transition": "fade",           # Clean transition to text
        "endframe": "dissolve",         # Product → brand logo
    },
    # ── From transition/title scenes ──────────────────────────
    "transition": {
        "personnage": "fade",           # Emerge from title into action
        "produit": "fade",              # Title → product reveal
        "transition": "cut",            # Between titles: clean cut
        "endframe": "dissolve",         # Title → final brand
    },

    # ── Archetype-specific rules (higher priority) ────────────

    # Establishing shots
    "establishing": {
        "portrait": "dissolve",         # Wide → close = dissolve
        "lifestyle": "dissolve",
        "product_hero": "dissolve",
        "interaction": "dissolve",
        "_default": "dissolve",
    },
    # Portrait close-ups
    "portrait": {
        "interaction": "dissolve",      # Face → using product
        "product_hero": "dissolve",     # Face → product focus
        "macro_detail": "cut",          # Face → extreme detail = punch cut
        "lifestyle": "dissolve",
        "_default": "dissolve",
    },
    # Product hero shots
    "product_hero": {
        "endframe": "dissolve",         # Product → brand = always dissolve
        "lifestyle": "dissolve",
        "portrait": "dissolve",
        "macro_detail": "cut",          # Hero → detail = punch cut
        "packshot": "dissolve",
        "_default": "dissolve",
    },
    # Macro detail shots
    "macro_detail": {
        "product_hero": "cut",          # Detail → hero = punch
        "portrait": "dissolve",
        "lifestyle": "dissolve",
        "_default": "cut",              # Details usually cut
    },
    # Action shots
    "action": {
        "action": "cut",                # Action → action = fast cuts
        "portrait": "cut",              # Action → face = impact cut
        "product_hero": "dissolve",     # Action → product = reveal dissolve
        "endframe": "dissolve",
        "_default": "cut",
    },
    # Montage
    "montage": {
        "montage": "cut",               # Montage = always cuts
        "_default": "cut",
    },
    # Reveal
    "reveal": {
        "product_hero": "dissolve",     # Reveal → product = continue the reveal
        "portrait": "dissolve",
        "_default": "dissolve",
    },
    # Endframe
    "endframe": {
        "_default": "fade",             # Endframe → anything = fade (rare)
    },
    # Ambient
    "ambient": {
        "_default": "dissolve",         # Ambient = always soft transitions
    },
}


# ── Transition timing rules ──────────────────────────────────

TRANSITION_DURATIONS: dict[str, float] = {
    "fade": 0.8,
    "dissolve": 0.6,
    "wipeleft": 0.4,
    "wiperight": 0.4,
    "wipeup": 0.4,
    "wipedown": 0.4,
    "slideleft": 0.5,
    "slideright": 0.5,
    "circlecrop": 0.5,
    "radial": 0.5,
    "smoothleft": 0.6,
    "smoothright": 0.6,
    "smoothup": 0.6,
    "smoothdown": 0.6,
    "cut": 0.0,
}

# ── Industry-specific transition preferences ──────────────────

INDUSTRY_TRANSITION_STYLE: dict[str, dict] = {
    "luxury": {
        "preferred": ["dissolve", "fade"],
        "avoided": ["wipeleft", "wiperight", "cut"],
        "default_duration_multiplier": 1.3,  # Slower transitions
        "notes": "Luxury demands smooth, unhurried transitions. Never jarring cuts.",
    },
    "beauty": {
        "preferred": ["dissolve", "fade"],
        "avoided": ["wipeleft", "slideleft"],
        "default_duration_multiplier": 1.2,
        "notes": "Soft, feminine transitions. Dissolves feel like skin cream blending.",
    },
    "fashion": {
        "preferred": ["cut", "dissolve"],
        "avoided": [],
        "default_duration_multiplier": 0.9,  # Slightly faster
        "notes": "Fashion allows bold cuts for energy. Mix cuts and dissolves.",
    },
    "sport": {
        "preferred": ["cut", "wipeleft", "wiperight"],
        "avoided": ["fade"],
        "default_duration_multiplier": 0.7,  # Fast transitions
        "notes": "Energy and impact. Hard cuts for action, wipes for dynamic movement.",
    },
    "food_beverage": {
        "preferred": ["dissolve", "fade"],
        "avoided": ["cut"],
        "default_duration_multiplier": 1.1,
        "notes": "Appetite appeal needs smooth transitions. Let the eye savor.",
    },
    "automotive": {
        "preferred": ["dissolve", "smoothleft", "smoothright"],
        "avoided": [],
        "default_duration_multiplier": 1.0,
        "notes": "Smooth like the driving experience. Smooth transitions preferred.",
    },
    "tech": {
        "preferred": ["cut", "dissolve", "slideleft"],
        "avoided": ["fade"],
        "default_duration_multiplier": 0.8,
        "notes": "Modern, clean, precise. Cuts for snappiness, slides for progression.",
    },
    "travel": {
        "preferred": ["dissolve", "fade", "smoothleft"],
        "avoided": ["cut"],
        "default_duration_multiplier": 1.2,
        "notes": "Dreamy, flowing. Dissolves that transport the viewer.",
    },
    "fragrance": {
        "preferred": ["dissolve", "fade"],
        "avoided": ["cut", "wipeleft"],
        "default_duration_multiplier": 1.4,  # Very slow, sensual
        "notes": "Most ethereal transitions. Everything should feel like mist.",
    },
    "jewelry_watches": {
        "preferred": ["dissolve", "fade"],
        "avoided": ["wipeleft", "slideleft"],
        "default_duration_multiplier": 1.3,
        "notes": "Precious, deliberate. Each transition should feel like revealing a treasure.",
    },
    "real_estate": {
        "preferred": ["dissolve", "smoothleft", "smoothright"],
        "avoided": ["cut"],
        "default_duration_multiplier": 1.1,
        "notes": "Smooth walk-through feel. Transitions should feel like moving through spaces.",
    },
}


def get_recommended_transition(
    from_type: str,
    to_type: str,
    industry: str | None = None,
) -> str:
    """Get the recommended transition between two scene types.

    Args:
        from_type: Scene type or archetype of the outgoing scene.
        to_type: Scene type or archetype of the incoming scene.
        industry: Optional industry for style-specific preferences.

    Returns:
        FFmpeg xfade transition name.
    """
    # Check archetype-specific rules first
    rules = TRANSITION_RULES.get(from_type.lower(), {})
    transition = rules.get(to_type.lower()) or rules.get("_default")

    if not transition:
        # Fall back to scene-type level rules
        for scene_type in ("personnage", "produit", "transition"):
            if from_type.lower().startswith(scene_type):
                rules = TRANSITION_RULES.get(scene_type, {})
                transition = rules.get(to_type.lower()) or rules.get("_default")
                break

    if not transition:
        transition = DEFAULT_TRANSITION

    # Apply industry preferences if available
    if industry and industry.lower() in INDUSTRY_TRANSITION_STYLE:
        style = INDUSTRY_TRANSITION_STYLE[industry.lower()]
        if transition in style.get("avoided", []):
            # Use first preferred transition instead
            preferred = style.get("preferred", [DEFAULT_TRANSITION])
            transition = preferred[0]

    return transition


def get_transition_duration(transition: str, industry: str | None = None) -> float:
    """Get the duration for a specific transition type.

    Args:
        transition: FFmpeg xfade transition name.
        industry: Optional industry for duration scaling.

    Returns:
        Duration in seconds.
    """
    base = TRANSITION_DURATIONS.get(transition.lower(), 0.5)

    if industry and industry.lower() in INDUSTRY_TRANSITION_STYLE:
        multiplier = INDUSTRY_TRANSITION_STYLE[industry.lower()].get(
            "default_duration_multiplier", 1.0,
        )
        base *= multiplier

    return round(base, 2)
