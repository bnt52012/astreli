"""Advertising patterns for the fragrance industry.

Defines the FRAGRANCE_PATTERN dictionary capturing the visual language,
pacing, lighting, and cinematic conventions used by luxury fragrance houses
such as Chanel, Dior, Tom Ford, and Yves Saint Laurent.  Emphasis on
abstract emotional storytelling, liquid and glass textures, mysterious
atmosphere, and sensual visual metaphor for invisible scent.
"""

FRAGRANCE_PATTERN = {
    "industry": "fragrance",

    # ------------------------------------------------------------------
    # Scene flow
    # ------------------------------------------------------------------
    "scene_flow": [
        {
            "archetype": "atmospheric_opening",
            "duration": 4.5,
            "description": "Evocative environment establishing the emotional world of the scent — desert dusk, rain-slicked street, candlelit boudoir",
        },
        {
            "archetype": "sensual_encounter",
            "duration": 4.0,
            "description": "Model in a charged sensorial moment: eyes closed, skin glistening, fabric grazing shoulder",
        },
        {
            "archetype": "bottle_reveal",
            "duration": 3.5,
            "description": "Fragrance bottle beauty shot backlit through amber or coloured liquid, caustic light patterns on surface",
        },
        {
            "archetype": "ritual_application",
            "duration": 3.0,
            "description": "Spritz on pulse point in slow motion, mist cloud expanding and catching backlight",
        },
        {
            "archetype": "abstract_synesthesia",
            "duration": 4.0,
            "description": "Visual metaphor translating scent notes — swirling petals, liquid gold pour, smoke tendrils, crushed spices",
        },
        {
            "archetype": "transformation",
            "duration": 4.0,
            "description": "Model transformed by the fragrance — heightened confidence, magnetic presence, cinematic slow walk",
        },
        {
            "archetype": "bottle_hero_final",
            "duration": 3.5,
            "description": "Bottle in atmospheric isolation, condensation or dew visible, warm light glowing through glass",
        },
        {
            "archetype": "endframe_brand",
            "duration": 3.0,
            "description": "Brand wordmark with fragrance name on dark or gradient field, lingering dissolve from bottle",
        },
    ],

    # ------------------------------------------------------------------
    # Visual signature
    # ------------------------------------------------------------------
    "visual_signature": {
        "color_temperature": "mood-dependent — warm amber 3200 K for oriental scents, cool blue 7000 K for aquatic, golden 4500 K for floral",
        "contrast": "high cinematic contrast with rich shadow detail and luminous highlights",
        "saturation": "either deeply saturated jewel tones or ethereally desaturated pastels, never middle-ground",
        "grain": "cinematic film grain at 200-500 ISO equivalent, adding tactile texture without noise",
        "depth_of_field": "extremely shallow f/1.4 producing dreamlike bokeh that dissolves background into colour wash",
        "color_grade": "teal-and-orange split tone for drama, or monochromatic amber warmth for intimacy",
    },

    # ------------------------------------------------------------------
    # Lighting preferences — references to lighting setup keys
    # ------------------------------------------------------------------
    "lighting_preferences": [
        "chiaroscuro",
        "golden_hour",
        "candle_firelight",
        "backlit",
        "moonlight_cool",
        "fog_haze",
        "neon_gel",
        "window_light_dramatic",
        "product_backlit_glow",
        "cinematic_teal_orange",
    ],

    # ------------------------------------------------------------------
    # Lens preferences — references to lens keys
    # ------------------------------------------------------------------
    "lens_preferences": [
        "portrait_85mm_f14",
        "standard_50mm_f14",
        "macro_100mm",
        "telephoto_135mm",
        "anamorphic_50mm",
        "helios_44_2",
        "petzval",
    ],

    # ------------------------------------------------------------------
    # Movement style
    # ------------------------------------------------------------------
    "movement_style": {
        "camera": "slow floating dolly and crane, dreamlike drift, occasional imperceptible push-in",
        "subject": "languid deliberate gestures — trailing fingertips, turning toward light, closing eyes",
        "pacing": "hypnotic and unhurried, every movement stretching time, breaths between beats",
    },

    # ------------------------------------------------------------------
    # Transition preferences (ordered)
    # ------------------------------------------------------------------
    "transition_preferences": [
        "long cross-dissolve layering two images into double exposure",
        "slow fade through warm amber glow",
        "match dissolve on circular bottle cap to full moon or eye",
        "liquid morph from pouring perfume to flowing landscape",
        "soft focus pull transition between foreground and background planes",
        "smoke or mist wipe obscuring and revealing next scene",
    ],

    # ------------------------------------------------------------------
    # Music style
    # ------------------------------------------------------------------
    "music_style": "sensual ambient pads, breathy whispered vocals, sparse trip-hop beat, minimal piano with long reverb tail, orchestral swells at climax",

    # ------------------------------------------------------------------
    # Banned elements
    # ------------------------------------------------------------------
    "banned_elements": [
        "fast cuts or staccato editing breaking the spell",
        "clinical or sterile product photography without atmosphere",
        "bright flat even lighting destroying mood",
        "everyday mundane domestic settings",
        "excessive on-screen text or price callouts",
        "comedic or slapstick tone",
        "stock-footage lifestyle filler with no emotional charge",
        "visible brand competitors in frame",
        "shaky handheld footage",
        "literal depictions of scent ingredients without abstraction",
    ],

    # ------------------------------------------------------------------
    # Prompt modifiers (20+)
    # ------------------------------------------------------------------
    "prompt_modifiers": [
        "luxury fragrance campaign photography, editorial beauty lighting",
        "bottle backlit with amber glow transmitting through golden liquid",
        "sensual dreamlike atmosphere with shallow depth of field",
        "visual olfactory synesthesia translating scent into image",
        "glass bottle refraction and light caustics on dark surface",
        "perfume mist cloud suspended in backlit air",
        "flower petals floating weightlessly in slow-motion breeze",
        "golden liquid visible inside sculptural flacon",
        "Chanel No.5 campaign level of restraint and elegance",
        "Dior Sauvage raw masculine landscape energy",
        "velvet-smooth skin illuminated by single warm directional source",
        "mysterious shadowed portrait revealing only contour and cheekbone",
        "raw ingredients visualized — Damask rose, oud wood, amber resin, bergamot",
        "desert sand dune at golden hour with long shadows",
        "steam rising in a dimly lit bathroom, warm diffusion",
        "Venetian palazzo candlelit evening, reflections on terrazzo",
        "silk charmeuse fabric flowing over skin in slow motion",
        "bare shoulder caught in warm directional sidelight",
        "spritz mist cloud backlit and sparkling with micro-droplets",
        "bottle resting on raw marble slab surrounded by scattered rose petals",
        "Tom Ford noir aesthetic, obsidian black and molten gold",
        "YSL Libre campaign energy, confident stride",
        "crushed violet and tonka bean macro texture",
        "rain on skin catching city neon reflections",
    ],

    # ------------------------------------------------------------------
    # Video modifiers (10+)
    # ------------------------------------------------------------------
    "video_modifiers": [
        "perfume mist spraying in extreme slow motion with backlight catching every droplet",
        "model slowly closing eyes and inhaling with visible pleasure",
        "liquid swirling inside bottle as it is gently rotated",
        "silk fabric falling from shoulder in slow-motion cascade",
        "flower petals drifting through air in controlled studio breeze",
        "model walking through lavender field at golden hour, camera tracking",
        "bottle placed on reflective surface with controlled gentle landing and ripple",
        "camera orbiting bottle at constant radius with shifting specular highlights",
        "steam rising and curling around model silhouette in warm bathroom light",
        "fingertip trailing slowly across collarbone leaving glistening trace",
        "liquid gold pouring in macro, viscous and luminous",
        "double-exposure blend of model face and blooming rose",
    ],

    # ------------------------------------------------------------------
    # Reference brands
    # ------------------------------------------------------------------
    "reference_brands": [
        "Chanel",
        "Dior",
        "Tom Ford",
        "Yves Saint Laurent",
        "Guerlain",
        "Hermès",
        "Givenchy",
        "Maison Francis Kurkdjian",
        "Byredo",
        "Le Labo",
        "Creed",
        "Jo Malone",
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
