"""
Transition Grammar — rules governing how scenes connect in advertising sequences.

This module provides three data structures:

    TRANSITION_RULES
        Dict mapping (archetype_from, archetype_to) tuples to a dict with
        ``transition`` (the recommended transition type) and ``reasoning``
        (a brief rationale). Covers 40+ major archetype-pair combinations.

    DEFAULT_TRANSITIONS
        Dict mapping a single archetype key to its preferred default exit
        transition when no specific pair rule applies.

    INDUSTRY_TRANSITION_OVERRIDES
        Dict mapping an industry name to a list of preferred transition types,
        ordered from most to least preferred for that vertical.

Transition type vocabulary:
    cut, dissolve, fade_to_black, fade_from_black, wipe, whip_pan,
    smash_cut, light_wipe, speed_ramp, match_cut, j_cut, l_cut,
    iris, morph, split_reveal, zoom_transition, hold
"""

# ─────────────────────────────────────────────────────────────────────────────
# TRANSITION RULES — (archetype_from, archetype_to) -> recommendation
# ─────────────────────────────────────────────────────────────────────────────

TRANSITION_RULES = {

    # ── From: environment_establishing ───────────────────────────────────
    ("environment_establishing", "model_portrait_closeup"): {
        "transition": "dissolve",
        "reasoning": "Wide-to-close dissolve eases the viewer from context to character.",
    },
    ("environment_establishing", "lifestyle_context"): {
        "transition": "dissolve",
        "reasoning": "Both scenes share environmental focus; dissolve blends spatial continuity.",
    },
    ("environment_establishing", "product_hero_shot"): {
        "transition": "dissolve",
        "reasoning": "Dissolve builds anticipation from setting to product reveal.",
    },
    ("environment_establishing", "motion_action"): {
        "transition": "cut",
        "reasoning": "Hard cut injects energy when shifting from calm establishing to action.",
    },
    ("environment_establishing", "aerial_drone"): {
        "transition": "dissolve",
        "reasoning": "Both share wide perspectives; dissolve maintains spatial scale.",
    },
    ("environment_establishing", "social_group"): {
        "transition": "dissolve",
        "reasoning": "Dissolve transitions from place to people within that place.",
    },

    # ── From: model_portrait_closeup ─────────────────────────────────────
    ("model_portrait_closeup", "macro_detail"): {
        "transition": "dissolve",
        "reasoning": "Dissolve suggests the camera is pushing deeper into the subject's world.",
    },
    ("model_portrait_closeup", "product_interaction"): {
        "transition": "cut",
        "reasoning": "Cut connects the person to their action without delay.",
    },
    ("model_portrait_closeup", "lifestyle_context"): {
        "transition": "dissolve",
        "reasoning": "Dissolve pulls back from intimate portrait to wider lifestyle context.",
    },
    ("model_portrait_closeup", "product_hero_shot"): {
        "transition": "dissolve",
        "reasoning": "Dissolve links person and product emotionally.",
    },
    ("model_portrait_closeup", "packshot_endframe"): {
        "transition": "fade_to_black",
        "reasoning": "Fade to black gives the portrait a final, contemplative close before endframe.",
    },
    ("model_portrait_closeup", "silhouette_artistic"): {
        "transition": "dissolve",
        "reasoning": "Dissolve transitions from detail to abstraction gracefully.",
    },
    ("model_portrait_closeup", "reflection_mirror"): {
        "transition": "match_cut",
        "reasoning": "Match cut on the face connects real portrait to reflected portrait.",
    },

    # ── From: macro_detail ───────────────────────────────────────────────
    ("macro_detail", "lifestyle_context"): {
        "transition": "dissolve",
        "reasoning": "Dissolve expands from micro to macro context smoothly.",
    },
    ("macro_detail", "model_portrait_closeup"): {
        "transition": "dissolve",
        "reasoning": "Dissolve connects texture detail to the person it belongs to.",
    },
    ("macro_detail", "product_hero_shot"): {
        "transition": "cut",
        "reasoning": "Cut reveals the full product after teasing a detail.",
    },
    ("macro_detail", "macro_detail"): {
        "transition": "cut",
        "reasoning": "Back-to-back details use cuts for rhythm and pacing.",
    },
    ("macro_detail", "packshot_endframe"): {
        "transition": "dissolve",
        "reasoning": "Dissolve from detail to final packshot resolves the visual journey.",
    },
    ("macro_detail", "ingredient_component"): {
        "transition": "cut",
        "reasoning": "Cut between related close-ups maintains micro-scale rhythm.",
    },

    # ── From: lifestyle_context ──────────────────────────────────────────
    ("lifestyle_context", "model_portrait_closeup"): {
        "transition": "dissolve",
        "reasoning": "Dissolve narrows focus from environment to person naturally.",
    },
    ("lifestyle_context", "macro_detail"): {
        "transition": "cut",
        "reasoning": "Cut jumps scales decisively for visual surprise.",
    },
    ("lifestyle_context", "product_hero_shot"): {
        "transition": "dissolve",
        "reasoning": "Dissolve elevates the product from context to hero status.",
    },
    ("lifestyle_context", "packshot_endframe"): {
        "transition": "dissolve",
        "reasoning": "Dissolve wraps the lifestyle story into the brand endframe.",
    },
    ("lifestyle_context", "lifestyle_context"): {
        "transition": "cut",
        "reasoning": "Cuts between lifestyle scenes maintain editorial pacing.",
    },
    ("lifestyle_context", "social_group"): {
        "transition": "cut",
        "reasoning": "Cut shifts from individual lifestyle to group scene with energy.",
    },
    ("lifestyle_context", "call_to_action"): {
        "transition": "dissolve",
        "reasoning": "Dissolve bridges storytelling to conversion frame.",
    },

    # ── From: product_hero_shot ──────────────────────────────────────────
    ("product_hero_shot", "lifestyle_context"): {
        "transition": "dissolve",
        "reasoning": "Dissolve places the hero product into real-world context.",
    },
    ("product_hero_shot", "macro_detail"): {
        "transition": "dissolve",
        "reasoning": "Dissolve zooms viewer into product detail.",
    },
    ("product_hero_shot", "model_portrait_closeup"): {
        "transition": "dissolve",
        "reasoning": "Dissolve introduces the person who uses the product.",
    },
    ("product_hero_shot", "packshot_endframe"): {
        "transition": "fade_to_black",
        "reasoning": "Fade separates hero drama from clean endframe.",
    },
    ("product_hero_shot", "product_interaction"): {
        "transition": "cut",
        "reasoning": "Cut transitions from display to demonstration directly.",
    },
    ("product_hero_shot", "scale_comparison"): {
        "transition": "cut",
        "reasoning": "Cut introduces reference object for immediate size context.",
    },

    # ── From: product_interaction ────────────────────────────────────────
    ("product_interaction", "macro_detail"): {
        "transition": "cut",
        "reasoning": "Cut jumps from use to detail for rhythm.",
    },
    ("product_interaction", "product_hero_shot"): {
        "transition": "dissolve",
        "reasoning": "Dissolve returns to hero product after demonstration.",
    },
    ("product_interaction", "lifestyle_context"): {
        "transition": "dissolve",
        "reasoning": "Dissolve expands from interaction to environmental context.",
    },
    ("product_interaction", "packshot_endframe"): {
        "transition": "fade_to_black",
        "reasoning": "Fade provides clean exit from interaction to branded endframe.",
    },
    ("product_interaction", "hands_only"): {
        "transition": "cut",
        "reasoning": "Cut tightens from full interaction to hands-only detail.",
    },
    ("product_interaction", "before_after_transform"): {
        "transition": "dissolve",
        "reasoning": "Dissolve connects product use to its visible result.",
    },

    # ── From: motion_action ──────────────────────────────────────────────
    ("motion_action", "motion_action"): {
        "transition": "cut",
        "reasoning": "Back-to-back action cuts drive adrenaline rhythm.",
    },
    ("motion_action", "macro_detail"): {
        "transition": "cut",
        "reasoning": "Cut from action to detail creates impactful scale shift.",
    },
    ("motion_action", "model_portrait_closeup"): {
        "transition": "dissolve",
        "reasoning": "Dissolve calms energy from action to reflective portrait.",
    },
    ("motion_action", "packshot_endframe"): {
        "transition": "dissolve",
        "reasoning": "Dissolve resolves action energy into brand endframe.",
    },
    ("motion_action", "slow_motion_moment"): {
        "transition": "speed_ramp",
        "reasoning": "Speed ramp connects real-time action to slow-motion replay.",
    },
    ("motion_action", "product_hero_shot"): {
        "transition": "dissolve",
        "reasoning": "Dissolve connects athletic energy to the product driving it.",
    },

    # ── From: unboxing_reveal ────────────────────────────────────────────
    ("unboxing_reveal", "product_hero_shot"): {
        "transition": "dissolve",
        "reasoning": "Dissolve completes the reveal by elevating product to hero status.",
    },
    ("unboxing_reveal", "macro_detail"): {
        "transition": "cut",
        "reasoning": "Cut dives straight into product detail after unboxing.",
    },
    ("unboxing_reveal", "product_interaction"): {
        "transition": "cut",
        "reasoning": "Cut transitions from reveal to first use seamlessly.",
    },
    ("unboxing_reveal", "hands_only"): {
        "transition": "cut",
        "reasoning": "Cut continues the tactile, hands-focused narrative.",
    },

    # ── From: silhouette_artistic ────────────────────────────────────────
    ("silhouette_artistic", "product_hero_shot"): {
        "transition": "dissolve",
        "reasoning": "Dissolve transitions from abstract mood to concrete product reveal.",
    },
    ("silhouette_artistic", "model_portrait_closeup"): {
        "transition": "dissolve",
        "reasoning": "Dissolve moves from mystery silhouette to revealed identity.",
    },
    ("silhouette_artistic", "environment_establishing"): {
        "transition": "dissolve",
        "reasoning": "Dissolve connects artistic mood to environmental context.",
    },

    # ── From: pov_first_person ───────────────────────────────────────────
    ("pov_first_person", "product_interaction"): {
        "transition": "cut",
        "reasoning": "Cut shifts from viewer's eyes to third-person interaction.",
    },
    ("pov_first_person", "product_hero_shot"): {
        "transition": "dissolve",
        "reasoning": "Dissolve lifts from personal POV to product showcase.",
    },
    ("pov_first_person", "hands_only"): {
        "transition": "cut",
        "reasoning": "Cut maintains first-person feel by staying on hands.",
    },

    # ── From: hands_only ─────────────────────────────────────────────────
    ("hands_only", "product_hero_shot"): {
        "transition": "dissolve",
        "reasoning": "Dissolve transitions from tactile interaction to product showcase.",
    },
    ("hands_only", "macro_detail"): {
        "transition": "cut",
        "reasoning": "Cut pushes deeper into detail from hands close-up.",
    },
    ("hands_only", "model_portrait_closeup"): {
        "transition": "dissolve",
        "reasoning": "Dissolve reveals the person behind the hands.",
    },

    # ── From: ingredient_component ───────────────────────────────────────
    ("ingredient_component", "product_hero_shot"): {
        "transition": "dissolve",
        "reasoning": "Dissolve assembles components into the finished product.",
    },
    ("ingredient_component", "macro_detail"): {
        "transition": "cut",
        "reasoning": "Cut between ingredient and texture detail maintains micro rhythm.",
    },
    ("ingredient_component", "before_after_transform"): {
        "transition": "dissolve",
        "reasoning": "Dissolve connects raw ingredients to their transformative result.",
    },

    # ── From: before_after_transform ─────────────────────────────────────
    ("before_after_transform", "product_hero_shot"): {
        "transition": "dissolve",
        "reasoning": "Dissolve connects proven result to the product responsible.",
    },
    ("before_after_transform", "call_to_action"): {
        "transition": "dissolve",
        "reasoning": "Dissolve carries proof of efficacy directly to conversion frame.",
    },
    ("before_after_transform", "packshot_endframe"): {
        "transition": "dissolve",
        "reasoning": "Dissolve wraps the transformation story with brand close.",
    },

    # ── From: slow_motion_moment ─────────────────────────────────────────
    ("slow_motion_moment", "product_hero_shot"): {
        "transition": "speed_ramp",
        "reasoning": "Speed ramp returns from slow motion to reveal the product.",
    },
    ("slow_motion_moment", "motion_action"): {
        "transition": "speed_ramp",
        "reasoning": "Speed ramp snaps back to real-time action energy.",
    },
    ("slow_motion_moment", "packshot_endframe"): {
        "transition": "dissolve",
        "reasoning": "Dissolve settles the dramatic moment into brand endframe.",
    },

    # ── From: time_lapse ─────────────────────────────────────────────────
    ("time_lapse", "product_hero_shot"): {
        "transition": "dissolve",
        "reasoning": "Dissolve anchors compressed time back to a single product moment.",
    },
    ("time_lapse", "lifestyle_context"): {
        "transition": "dissolve",
        "reasoning": "Dissolve transitions from time abstraction to present lifestyle.",
    },
    ("time_lapse", "packshot_endframe"): {
        "transition": "fade_to_black",
        "reasoning": "Fade from time passage to endframe signals narrative conclusion.",
    },

    # ── From: reflection_mirror ──────────────────────────────────────────
    ("reflection_mirror", "product_hero_shot"): {
        "transition": "dissolve",
        "reasoning": "Dissolve moves from reflective abstraction to product clarity.",
    },
    ("reflection_mirror", "model_portrait_closeup"): {
        "transition": "match_cut",
        "reasoning": "Match cut on face links reflected and direct portrait.",
    },

    # ── From: aerial_drone ───────────────────────────────────────────────
    ("aerial_drone", "environment_establishing"): {
        "transition": "dissolve",
        "reasoning": "Dissolve lands the aerial perspective into ground-level establishing.",
    },
    ("aerial_drone", "lifestyle_context"): {
        "transition": "dissolve",
        "reasoning": "Dissolve descends from aerial context to human-scale lifestyle.",
    },
    ("aerial_drone", "motion_action"): {
        "transition": "cut",
        "reasoning": "Cut drops from sky to ground action with dynamic impact.",
    },

    # ── From: social_group ───────────────────────────────────────────────
    ("social_group", "product_hero_shot"): {
        "transition": "dissolve",
        "reasoning": "Dissolve shifts from group energy to the product they share.",
    },
    ("social_group", "lifestyle_context"): {
        "transition": "cut",
        "reasoning": "Cut moves between group and individual lifestyle vignettes.",
    },
    ("social_group", "packshot_endframe"): {
        "transition": "dissolve",
        "reasoning": "Dissolve wraps the social narrative into branded endframe.",
    },

    # ── From: behind_the_scenes ──────────────────────────────────────────
    ("behind_the_scenes", "product_hero_shot"): {
        "transition": "dissolve",
        "reasoning": "Dissolve elevates craft process into finished product glory.",
    },
    ("behind_the_scenes", "ingredient_component"): {
        "transition": "cut",
        "reasoning": "Cut links workshop to raw materials for narrative continuity.",
    },
    ("behind_the_scenes", "macro_detail"): {
        "transition": "cut",
        "reasoning": "Cut jumps from workshop to detail of the crafted result.",
    },

    # ── From: text_overlay_title ─────────────────────────────────────────
    ("text_overlay_title", "product_hero_shot"): {
        "transition": "dissolve",
        "reasoning": "Dissolve transitions from brand message to product visual.",
    },
    ("text_overlay_title", "lifestyle_context"): {
        "transition": "dissolve",
        "reasoning": "Dissolve carries the headline into the story.",
    },
    ("text_overlay_title", "environment_establishing"): {
        "transition": "dissolve",
        "reasoning": "Dissolve introduces the world the title card described.",
    },

    # ── From: scale_comparison ───────────────────────────────────────────
    ("scale_comparison", "product_hero_shot"): {
        "transition": "cut",
        "reasoning": "Cut returns to hero shot after size has been communicated.",
    },
    ("scale_comparison", "macro_detail"): {
        "transition": "cut",
        "reasoning": "Cut dives into detail now that scale is established.",
    },

    # ── From: seasonal_holiday ───────────────────────────────────────────
    ("seasonal_holiday", "product_hero_shot"): {
        "transition": "dissolve",
        "reasoning": "Dissolve connects seasonal mood to product focus.",
    },
    ("seasonal_holiday", "call_to_action"): {
        "transition": "dissolve",
        "reasoning": "Dissolve carries seasonal urgency to conversion frame.",
    },
    ("seasonal_holiday", "packshot_endframe"): {
        "transition": "dissolve",
        "reasoning": "Dissolve closes the seasonal narrative with brand endframe.",
    },

    # ── From: call_to_action ─────────────────────────────────────────────
    ("call_to_action", "packshot_endframe"): {
        "transition": "dissolve",
        "reasoning": "Dissolve transitions from action prompt to brand close.",
    },

    # ── From: packshot_endframe (rarely transitions out, but for loops) ──
    ("packshot_endframe", "environment_establishing"): {
        "transition": "fade_from_black",
        "reasoning": "Fade from black restarts the narrative from the endframe.",
    },

    # ── From: split_screen ───────────────────────────────────────────────
    ("split_screen", "product_hero_shot"): {
        "transition": "wipe",
        "reasoning": "Wipe collapses the split into a single hero product view.",
    },
    ("split_screen", "before_after_transform"): {
        "transition": "wipe",
        "reasoning": "Wipe naturally connects dual-panel to comparison format.",
    },
    ("split_screen", "call_to_action"): {
        "transition": "dissolve",
        "reasoning": "Dissolve consolidates comparison into a single CTA frame.",
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# DEFAULT TRANSITIONS — fallback exit transition per archetype
# ─────────────────────────────────────────────────────────────────────────────

DEFAULT_TRANSITIONS = {
    "product_hero_shot":        "dissolve",
    "lifestyle_context":        "dissolve",
    "model_portrait_closeup":   "dissolve",
    "product_interaction":      "cut",
    "environment_establishing": "dissolve",
    "macro_detail":             "cut",
    "motion_action":            "cut",
    "unboxing_reveal":          "dissolve",
    "silhouette_artistic":      "dissolve",
    "pov_first_person":         "cut",
    "hands_only":               "cut",
    "ingredient_component":     "cut",
    "before_after_transform":   "dissolve",
    "split_screen":             "wipe",
    "slow_motion_moment":       "speed_ramp",
    "time_lapse":               "dissolve",
    "reflection_mirror":        "dissolve",
    "aerial_drone":             "dissolve",
    "social_group":             "cut",
    "behind_the_scenes":        "cut",
    "text_overlay_title":       "dissolve",
    "packshot_endframe":        "fade_to_black",
    "scale_comparison":         "cut",
    "seasonal_holiday":         "dissolve",
    "call_to_action":           "dissolve",
}


# ─────────────────────────────────────────────────────────────────────────────
# INDUSTRY TRANSITION OVERRIDES — preferred transitions per vertical
# ─────────────────────────────────────────────────────────────────────────────

INDUSTRY_TRANSITION_OVERRIDES = {
    "luxury": [
        "dissolve", "fade_to_black", "fade_from_black", "light_wipe",
    ],
    "beauty": [
        "dissolve", "fade_to_black", "morph", "light_wipe",
    ],
    "fashion": [
        "cut", "whip_pan", "smash_cut", "dissolve",
    ],
    "sport": [
        "cut", "smash_cut", "whip_pan", "speed_ramp",
    ],
    "food_beverage": [
        "dissolve", "cut", "morph", "wipe",
    ],
    "automotive": [
        "cut", "dissolve", "speed_ramp", "whip_pan",
    ],
    "tech": [
        "cut", "dissolve", "wipe", "zoom_transition",
    ],
    "travel": [
        "dissolve", "fade_to_black", "fade_from_black", "wipe",
    ],
    "real_estate": [
        "dissolve", "fade_to_black", "wipe", "fade_from_black",
    ],
    "jewelry_watches": [
        "dissolve", "fade_to_black", "light_wipe", "fade_from_black",
    ],
    "fragrance": [
        "dissolve", "fade_to_black", "morph", "fade_from_black",
    ],
}


# ─────────────────────────────────────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────────────────────────────────────

def get_transition(from_archetype: str, to_archetype: str) -> str:
    """Return the recommended transition between two archetypes.

    Checks TRANSITION_RULES first; falls back to the from-archetype's
    DEFAULT_TRANSITIONS entry; ultimate fallback is ``"dissolve"``.
    """
    rule = TRANSITION_RULES.get((from_archetype, to_archetype))
    if rule:
        return rule["transition"]
    return DEFAULT_TRANSITIONS.get(from_archetype, "dissolve")


def get_transition_with_reasoning(
    from_archetype: str, to_archetype: str
) -> dict:
    """Return transition and reasoning dict, with defaults if no rule exists."""
    rule = TRANSITION_RULES.get((from_archetype, to_archetype))
    if rule:
        return rule
    return {
        "transition": DEFAULT_TRANSITIONS.get(from_archetype, "dissolve"),
        "reasoning": "No specific rule; using default exit transition for this archetype.",
    }


def get_industry_transitions(industry: str) -> list[str]:
    """Return ordered list of preferred transitions for an industry."""
    return INDUSTRY_TRANSITION_OVERRIDES.get(industry, ["dissolve", "cut"])
