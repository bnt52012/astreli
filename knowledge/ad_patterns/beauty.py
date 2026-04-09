"""
Beauty industry advertising patterns.

Defines the visual language, pacing, and production style for beauty and
skincare advertisements. Inspired by L'Oréal, Dior Beauty, Charlotte Tilbury,
MAC, Glossier, and Fenty Beauty. Emphasises luminous skin close-ups, dewy
textures, soft flattering light, and pink/nude/pearl tonal palettes.
"""

BEAUTY_PATTERN = {

    # ------------------------------------------------------------------
    # Scene flow — typical ad structure (8 scenes)
    # ------------------------------------------------------------------
    "scene_flow": [
        {
            "archetype": "hero_face",
            "duration": 3.0,
            "description": (
                "Tight close-up of model's face — dewy skin catching light, "
                "eyes opening or a slow blink. Establishes the luminous, "
                "radiant tone of the piece."
            ),
        },
        {
            "archetype": "product_reveal",
            "duration": 3.5,
            "description": (
                "Product on a clean surface — glass, wet stone, or petal-strewn "
                "marble. Soft directional light catches the packaging and any "
                "visible texture of the formula."
            ),
        },
        {
            "archetype": "application_ritual",
            "duration": 4.0,
            "description": (
                "Close-up of the product being applied — fingertip spreading "
                "serum across a cheekbone, brush sweeping powder, or lips being "
                "painted. Texture is the star."
            ),
        },
        {
            "archetype": "transformation_result",
            "duration": 3.0,
            "description": (
                "The payoff — radiant skin glow, bold lip colour, or defined "
                "lashes. Shot tighter than the opening to show the visible "
                "difference the product creates."
            ),
        },
        {
            "archetype": "ingredient_macro",
            "duration": 2.5,
            "description": (
                "Macro of hero ingredient or texture — a serum droplet hanging "
                "from a dropper, cream swirl, crushed pigment powder, or fresh "
                "botanical extract."
            ),
        },
        {
            "archetype": "lifestyle_confidence",
            "duration": 4.0,
            "description": (
                "Model in motion — stepping into sunlight, laughing with a "
                "friend, catching her reflection. Connects the product to "
                "everyday confidence."
            ),
        },
        {
            "archetype": "product_beauty_shot",
            "duration": 3.0,
            "description": (
                "Final hero product angle — different from earlier reveal, "
                "perhaps with the cap off or surrounded by water droplets. "
                "Reinforce brand and SKU."
            ),
        },
        {
            "archetype": "endframe",
            "duration": 2.5,
            "description": (
                "Logo and tagline on soft gradient background — blush pink to "
                "champagne, or clean white. Minimal, elegant, and feminine."
            ),
        },
    ],

    # ------------------------------------------------------------------
    # Visual signature
    # ------------------------------------------------------------------
    "visual_signature": {
        "color_temperature": "neutral to slightly warm, 5000-5600K, flattering to all skin tones",
        "contrast": "low to medium — soft luminous gradients, no harsh tonal jumps",
        "saturation": "clean and vibrant but never oversaturated, skin-flattering colour science",
        "grain": "minimal to none — clean digital with occasional soft film emulsion look",
        "depth_of_field": "shallow f/1.8-f/2.8 for face close-ups, medium f/4 for products",
        "color_grade": "lifted shadows with pink/peach shift, highlights pushed warm, skin-tone-aware grading",
    },

    # ------------------------------------------------------------------
    # Lighting preferences — keys from lighting_setups.py
    # ------------------------------------------------------------------
    "lighting_preferences": [
        "butterfly",
        "ring_light",
        "beauty_dish",
        "clamshell",
        "window_light_soft",
        "hair_light",
        "high_key",
        "backlit",
        "overcast_diffused",
        "rim_light",
    ],

    # ------------------------------------------------------------------
    # Lens preferences — keys from lens_library.py
    # ------------------------------------------------------------------
    "lens_preferences": [
        "macro_100mm",
        "portrait_85mm_f18",
        "zoom_70_200mm",
        "standard_50mm_f14",
        "macro_105mm",
        "telephoto_135mm",
        "noctilux_58mm",
    ],

    # ------------------------------------------------------------------
    # Movement style
    # ------------------------------------------------------------------
    "movement_style": {
        "camera": (
            "Slow, smooth gliding — gentle arcs around the face, imperceptible "
            "push-ins toward the skin, and fluid lateral slides across product "
            "arrangements. Stabilisation must be flawless."
        ),
        "subject": (
            "Gentle, deliberate — a slow head turn revealing a jawline, "
            "fingertips gliding across a cheekbone, eyelids closing and "
            "opening. Hands are always graceful."
        ),
        "pacing": (
            "Serene and flowing. Transitions feel like breathing — smooth in, "
            "smooth out. No sudden movements. Rhythm mirrors the ritual of "
            "applying skincare."
        ),
    },

    # ------------------------------------------------------------------
    # Transition preferences (ordered by preference)
    # ------------------------------------------------------------------
    "transition_preferences": [
        "soft_dissolve",
        "luminous_cross_fade",
        "gentle_wipe",
        "light_bloom_transition",
        "fade_to_white",
        "match_dissolve_on_texture",
    ],

    # ------------------------------------------------------------------
    # Music style
    # ------------------------------------------------------------------
    "music_style": (
        "Light, airy, and modern — soft electronic pads with breathy female "
        "vocals, gentle piano melodies, or ambient textures with subtle "
        "rhythmic pulse. Think Lana Del Rey instrumentals, Sigur Rós-lite "
        "ambience, or lo-fi R&B without lyrics. Never aggressive, never heavy."
    ),

    # ------------------------------------------------------------------
    # Banned elements — things to NEVER do
    # ------------------------------------------------------------------
    "banned_elements": [
        "harsh direct on-camera flash or paparazzi-style lighting",
        "shaky handheld camera or unstabilised footage",
        "extreme high-contrast lighting that creates deep facial shadows",
        "cold blue or green colour casts on skin tones",
        "unflattering macro of skin pores under harsh side light",
        "fast aggressive jump cuts or MTV-style editing",
        "dark moody lighting that obscures skin quality",
        "industrial, gritty, or urban-decay backgrounds",
        "oversaturated or neon skin-tone rendering",
        "visible digital noise or compression artefacts on skin",
    ],

    # ------------------------------------------------------------------
    # Prompt modifiers — phrases appended to image generation prompts
    # ------------------------------------------------------------------
    "prompt_modifiers": [
        "beauty editorial photography, luminous dewy skin",
        "soft butterfly lighting pattern with gentle fill",
        "clean white or soft gradient background",
        "product droplets and cream textures visible in sharp detail",
        "skin-flattering warm colour temperature",
        "high-end beauty retouching preserving natural skin texture",
        "macro detail of serum droplet or cream swirl",
        "soft bokeh background with sharp subject focus",
        "Glossier and Fenty Beauty campaign aesthetic",
        "fresh radiant complexion catching the light",
        "editorial beauty close-up shot on medium format",
        "clean minimalist product styling on glass surface",
        "water droplets or splash conveying freshness",
        "botanical ingredients and natural elements as props",
        "pearl-like luminosity reflecting from skin highlights",
        "professional beauty dish lighting with soft falloff",
        "glass-skin effect with multiple specular highlights",
        "pink and champagne tones in highlights and reflections",
        "fingertip application showing product texture",
        "ring-lit catch lights in the eyes",
        "dewy mist on skin surface for freshness",
        "backlit hair glow creating angelic rim light",
    ],

    # ------------------------------------------------------------------
    # Video modifiers — phrases for Kling animation prompts
    # ------------------------------------------------------------------
    "video_modifiers": [
        "slow-motion product application on skin, cream spreading smoothly",
        "water or micellar splash in cinematic slow motion",
        "gentle head turn revealing luminous skin from shadow to light",
        "product rotating slowly on glass pedestal with refractions",
        "serum droplet falling from dropper into liquid surface, ripple",
        "fine powder particles floating weightlessly in soft light",
        "soft light shifting gradually across the face",
        "gentle breeze through hair with backlit rim glow",
        "cream texture being swirled by fingertip in extreme close-up",
        "eyelashes fluttering open in slow motion",
        "mist spray dispersing in slow motion against backlight",
    ],

    # ------------------------------------------------------------------
    # Reference brands
    # ------------------------------------------------------------------
    "reference_brands": [
        "L'Oréal Paris",
        "Dior Beauty",
        "Charlotte Tilbury",
        "MAC Cosmetics",
        "Glossier",
        "Fenty Beauty",
        "NARS",
        "Estée Lauder",
        "La Mer",
        "Chanel Beauté",
        "Pat McGrath Labs",
        "Rare Beauty",
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
