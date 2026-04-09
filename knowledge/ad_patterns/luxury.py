"""
Luxury industry advertising patterns.

Defines the visual language, pacing, and production style for luxury brand
advertisements. Inspired by houses like Chanel, Louis Vuitton, Hermès,
Rolls-Royce, Cartier, and Bottega Veneta. Emphasises slow deliberation,
deep blacks, gold accents, extreme material quality, and timeless elegance.
"""

LUXURY_PATTERN = {

    # ------------------------------------------------------------------
    # Scene flow — typical ad structure (8 scenes)
    # ------------------------------------------------------------------
    "scene_flow": [
        {
            "archetype": "grand_establishing",
            "duration": 5.0,
            "description": (
                "Sweeping wide shot of a heritage location — marble palazzo "
                "interior, atelier façade at dusk, or misty château grounds. "
                "Sets the world the brand inhabits."
            ),
        },
        {
            "archetype": "craftsmanship_detail",
            "duration": 3.5,
            "description": (
                "Extreme macro of artisan hands at work — stitching leather, "
                "setting a gemstone, or polishing lacquer. Celebrates the "
                "human craft behind the product."
            ),
        },
        {
            "archetype": "lifestyle_portrait",
            "duration": 4.0,
            "description": (
                "Model in an aspirational setting — candlelit dining room, "
                "private library, or vintage car interior. Conveys the life "
                "the product belongs to."
            ),
        },
        {
            "archetype": "product_hero",
            "duration": 4.5,
            "description": (
                "Hero product shot on dark velvet or marble with dramatic "
                "side light. Gold reflections and precise specular highlights "
                "reveal material quality."
            ),
        },
        {
            "archetype": "interaction",
            "duration": 3.5,
            "description": (
                "Model interacting with the product — fastening a watch clasp, "
                "opening a handbag, or draping a scarf. Every gesture is "
                "unhurried and deliberate."
            ),
        },
        {
            "archetype": "second_detail",
            "duration": 3.0,
            "description": (
                "Alternate macro angle — texture of exotic leather grain, "
                "engraved logo, or hand-painted edge. Reinforces obsessive "
                "attention to detail."
            ),
        },
        {
            "archetype": "aspirational_moment",
            "duration": 4.0,
            "description": (
                "Cinematic lifestyle beat — stepping onto a yacht deck at "
                "golden hour, walking through a gallery, or ascending a grand "
                "staircase. Pure aspiration."
            ),
        },
        {
            "archetype": "endframe",
            "duration": 3.0,
            "description": (
                "Logo in restrained gold typography on deep black or dark "
                "marble background. No tagline, no CTA — the name alone "
                "carries the weight."
            ),
        },
    ],

    # ------------------------------------------------------------------
    # Visual signature
    # ------------------------------------------------------------------
    "visual_signature": {
        "color_temperature": "warm neutral, 4500-5500K, leaning amber in highlights",
        "contrast": "medium-high with rich, detailed blacks and controlled highlights",
        "saturation": "restrained and desaturated overall with selective rich golds and deep jewel tones",
        "grain": "fine analogue film grain adding subtle organic texture",
        "depth_of_field": "very shallow f/1.4-f/2.0 for portraits, f/2.8 for product, dreamy bokeh circles",
        "color_grade": "matte shadows with warm mid-tones, teal-shifted blacks, lifted black point",
    },

    # ------------------------------------------------------------------
    # Lighting preferences — keys from lighting_setups.py
    # ------------------------------------------------------------------
    "lighting_preferences": [
        "rembrandt",
        "chiaroscuro",
        "candle_firelight",
        "golden_hour",
        "window_light_dramatic",
        "product_dark_field",
        "rim_light",
        "low_key",
        "tungsten_warm",
        "backlit",
    ],

    # ------------------------------------------------------------------
    # Lens preferences — keys from lens_library.py
    # ------------------------------------------------------------------
    "lens_preferences": [
        "portrait_85mm_f14",
        "standard_50mm_f14",
        "macro_100mm",
        "telephoto_135mm",
        "classic_35mm",
        "tilt_shift_24mm",
        "petzval",
    ],

    # ------------------------------------------------------------------
    # Movement style
    # ------------------------------------------------------------------
    "movement_style": {
        "camera": (
            "Extremely slow and fluid — imperceptible dolly pushes, gentle "
            "crane descents, and glacial orbits. Every move should feel like "
            "the camera is floating on silk."
        ),
        "subject": (
            "Minimal and controlled. Graceful hand gestures, a slow head turn, "
            "fabric settling after a step. Never hurried, never casual."
        ),
        "pacing": (
            "Each frame is composed like a painting. Hold shots longer than "
            "feels natural — let the viewer absorb texture and light. Cuts are "
            "rare; dissolves preferred."
        ),
    },

    # ------------------------------------------------------------------
    # Transition preferences (ordered by preference)
    # ------------------------------------------------------------------
    "transition_preferences": [
        "long_dissolve",
        "slow_fade_to_black",
        "soft_cross_fade",
        "light_leak_dissolve",
        "match_cut_on_shape",
        "dip_to_black",
    ],

    # ------------------------------------------------------------------
    # Music style
    # ------------------------------------------------------------------
    "music_style": (
        "Solo piano or sparse orchestral strings — Satie, Debussy, or Ólafur "
        "Arnalds in spirit. Minimal ambient drones with warm analogue "
        "textures. No percussion, no vocals. Silence is acceptable between "
        "phrases. The score should feel like an overheard recital in an empty "
        "palazzo."
    ),

    # ------------------------------------------------------------------
    # Banned elements — things to NEVER do
    # ------------------------------------------------------------------
    "banned_elements": [
        "fast cuts or rapid-fire editing of any kind",
        "shaky handheld camera or unstabilised movement",
        "bright neon colours or saturated primaries",
        "busy, cluttered, or visually noisy compositions",
        "direct on-camera flash or paparazzi lighting",
        "casual or rounded sans-serif typography",
        "oversaturated skin tones or plastic retouching",
        "dutch angles or extreme tilted framing",
        "fish-eye or ultra-wide barrel distortion on people",
        "stock-photo-style forced smiles or thumbs-up gestures",
    ],

    # ------------------------------------------------------------------
    # Prompt modifiers — phrases appended to image generation prompts
    # ------------------------------------------------------------------
    "prompt_modifiers": [
        "luxury editorial photography, Hasselblad medium format quality",
        "rich tonal range with deep detailed shadows",
        "selective focus with creamy circular bokeh",
        "marble and gold accents in the environment",
        "timeless elegance and heritage atmosphere",
        "soft directional natural light through tall windows",
        "fine art photography museum-print quality",
        "muted desaturated palette with selective warm gold tones",
        "meticulous composition with generous negative space",
        "cashmere and silk texture rendering, tactile quality",
        "high-end retouching preserving natural skin texture",
        "Rembrandt triangle lighting on the face",
        "old money aesthetic, understated wealth",
        "architectural symmetry and classical proportions in background",
        "hand-crafted artisanal details visible at macro scale",
        "subtle fine film grain adding analogue warmth",
        "haute couture editorial campaign style",
        "deep black backgrounds with single dramatic light source",
        "Vogue Italia and Tom Ford campaign aesthetic",
        "reflections in polished dark wood or lacquered surfaces",
        "golden ratio composition, Renaissance painting balance",
        "anamorphic oval bokeh in background highlights",
        "subdued colour harmony inspired by Old Master paintings",
    ],

    # ------------------------------------------------------------------
    # Video modifiers — phrases for Kling animation prompts
    # ------------------------------------------------------------------
    "video_modifiers": [
        "ultra-slow motion at 0.3x-0.5x speed, every frame pristine",
        "imperceptible camera drift, almost static but alive",
        "gentle dolly push-in revealing product detail",
        "slow reveal through gradual focus pull foreground to background",
        "silk or cashmere fabric floating weightlessly in slow motion",
        "candlelight flicker casting dancing warm shadows",
        "subtle particle dust motes drifting through light beams",
        "slow 180-degree orbit around product on dark surface",
        "gentle hair and fabric movement from invisible breeze",
        "atmospheric golden haze drifting through the frame",
        "liquid gold pouring in extreme slow motion",
        "reflections rippling on a polished marble floor",
    ],

    # ------------------------------------------------------------------
    # Reference brands
    # ------------------------------------------------------------------
    "reference_brands": [
        "Chanel",
        "Louis Vuitton",
        "Hermès",
        "Rolls-Royce",
        "Cartier",
        "Bottega Veneta",
        "Tom Ford",
        "Brunello Cucinelli",
        "Loro Piana",
        "Patek Philippe",
        "Van Cleef & Arpels",
        "Berluti",
    ],

    # ------------------------------------------------------------------
    # Typical durations
    # ------------------------------------------------------------------
    "typical_durations": {
        "15s": 15,
        "30s": 30,
        "45s": 45,
        "60s": 60,
    },
}
