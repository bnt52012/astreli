"""Real estate and luxury property advertising patterns.

Defines the canonical visual language for high-end residential and commercial
property marketing.  Inspired by Sotheby's International Realty, Christie's,
and Architectural Digest: wide-angle interiors flooded with natural light,
warm-toned finishes, twilight exteriors, and an aspirational lifestyle
narrative woven through every room.
"""

REAL_ESTATE_PATTERN = {
    "industry": "real_estate",

    # ------------------------------------------------------------------
    # Scene flow
    # ------------------------------------------------------------------
    "scene_flow": [
        {
            "archetype": "exterior_hero",
            "duration": 4.5,
            "description": "Twilight or golden-hour facade shot — architecture fully "
                           "lit from within, landscaping manicured, sky dramatic",
        },
        {
            "archetype": "entry_reveal",
            "duration": 3.5,
            "description": "Front door opens or camera glides through foyer, "
                           "revealing double-height ceiling and natural light flood",
        },
        {
            "archetype": "living_space",
            "duration": 4.0,
            "description": "Great room or primary living area — wide symmetrical "
                           "composition, fireplace or statement art as anchor",
        },
        {
            "archetype": "material_detail",
            "duration": 2.5,
            "description": "Close-up of signature finish — veined marble island, "
                           "white-oak herringbone floor, bronze hardware",
        },
        {
            "archetype": "kitchen_bath",
            "duration": 3.5,
            "description": "Chef's kitchen or spa bathroom — clean lines, "
                           "natural stone, pendant lighting warm glow",
        },
        {
            "archetype": "lifestyle_moment",
            "duration": 4.0,
            "description": "Life being lived — morning coffee on the terrace, "
                           "children on the lawn, dinner party in the garden",
        },
        {
            "archetype": "view_amenity",
            "duration": 3.5,
            "description": "Hero view from property — ocean panorama, city skyline, "
                           "vineyard hillside, or infinity-edge pool at sunset",
        },
        {
            "archetype": "endframe",
            "duration": 2.5,
            "description": "Aerial pull-back or twilight wide, address and brokerage "
                           "logo fade in, contact information",
        },
    ],

    # ------------------------------------------------------------------
    # Visual signature
    # ------------------------------------------------------------------
    "visual_signature": {
        "color_temperature": "warm neutral 4800-5200K, inviting and livable",
        "contrast": "medium, controlled — no crushed shadows, window views retained",
        "saturation": "natural warm palette, muted earth tones, selective green foliage pop",
        "grain": "none, clean and sharp edge-to-edge",
        "depth_of_field": "deep f/8-f/11 interiors for wall-to-wall sharpness, "
                         "shallow f/2.8 for lifestyle vignettes",
        "color_grade": "warm midtones, neutral highlights, slightly lifted shadows "
                       "to keep dark corners inviting",
    },

    # ------------------------------------------------------------------
    # Lighting — keys from the canonical lighting_setups registry
    # ------------------------------------------------------------------
    "lighting_preferences": [
        "window_light_soft",
        "window_light_dramatic",
        "golden_hour",
        "blue_hour",
        "three_point",
        "overcast_diffused",
        "candle_firelight",
        "high_key",
        "backlit",
        "tungsten_warm",
    ],

    # ------------------------------------------------------------------
    # Lens — keys from the canonical lens registry
    # ------------------------------------------------------------------
    "lens_preferences": [
        "ultra_wide_14mm",
        "tilt_shift_24mm",
        "tilt_shift_17mm",
        "classic_35mm",
        "standard_50mm_f18",
        "wide_24mm",
        "portrait_85mm_f14",
    ],

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------
    "movement_style": {
        "camera": "smooth motorized gimbal walkthrough, slow reveal around corners, "
                  "drone orbit for exteriors, locked-off tripod for hero compositions",
        "subject": "doors opening, curtains drawing, water filling a freestanding tub, "
                   "family arriving home",
        "pacing": "leisurely and elegant — each room allowed to breathe before "
                  "transitioning to the next",
    },

    # ------------------------------------------------------------------
    # Transitions (ordered by preference)
    # ------------------------------------------------------------------
    "transition_preferences": [
        "gentle cross-dissolve",
        "doorway / archway natural wipe",
        "slow fade to white",
        "match-cut room to room",
        "camera-pass-through-wall morph",
        "light bloom transition",
    ],

    # ------------------------------------------------------------------
    # Audio
    # ------------------------------------------------------------------
    "music_style": (
        "elegant solo piano with soft sustain, ambient string quartet, "
        "sophisticated downtempo lounge — understated enough to let room "
        "tone and lifestyle foley (footsteps on marble, clinking glass, "
        "birdsong from the garden) carry emotional weight"
    ),

    # ------------------------------------------------------------------
    # Banned elements
    # ------------------------------------------------------------------
    "banned_elements": [
        "fisheye barrel distortion on interiors",
        "dark or unflattering room exposures",
        "visible clutter, laundry, or personal items",
        "blown-out overexposed window views",
        "on-camera flash harshness or hot spots",
        "converging vertical lines on architecture",
        "HDR tone-mapping artifacts or halos",
        "visible power cables, extension cords, or outlets",
        "shaky handheld footage in walkthroughs",
        "wide-angle perspective stretching on faces",
    ],

    # ------------------------------------------------------------------
    # Prompt modifiers (20+)
    # ------------------------------------------------------------------
    "prompt_modifiers": [
        "Architectural Digest cover quality, editorial precision",
        "twilight exterior real estate photography, sky gradient",
        "natural light flooding through floor-to-ceiling windows",
        "vertical lines perfectly corrected, tilt-shift precision",
        "double-height ceiling with clerestory window drama",
        "Calacatta marble island, waterfall edge, warm pendants",
        "panoramic ocean view through minimal steel-frame glazing",
        "white-oak herringbone flooring, warm afternoon light",
        "infinity-edge pool reflecting sunset sky gradient",
        "Bulthaup kitchen, handleless cabinetry, clean composition",
        "freestanding soaking tub, spa bathroom, river-view window",
        "walk-in dressing room, backlit shelving, luxury organization",
        "landscaped courtyard with mature olive trees, gravel path",
        "penthouse terrace with skyline view, lounge furniture styled",
        "Sotheby's listing quality, aspirational lifestyle framing",
        "natural stone accent wall, raking texture light",
        "wine cellar vaulted brick ceiling, warm spot lighting",
        "home cinema, acoustic panels, recessed LED ambient",
        "breakfast nook, banquette seating, morning light streaming",
        "garage with polished concrete floor, curated car collection",
        "outdoor kitchen and pergola, evening entertaining setup",
        "master suite with reading nook, linen curtains, soft glow",
    ],

    # ------------------------------------------------------------------
    # Video modifiers (10+)
    # ------------------------------------------------------------------
    "video_modifiers": [
        "smooth gimbal walkthrough, eye-level, steady two-mph pace",
        "front door swinging open to reveal sun-filled great room",
        "sheer curtains drawing back to unveil panoramic view",
        "camera craning upward to emphasize ceiling height and volume",
        "garden fountain trickling, shallow-focus foreground bokeh",
        "fireplace flames flickering, warm light dancing on walls",
        "motorized blinds opening to flood bedroom with daylight",
        "pool surface gently rippling, underwater light caustics",
        "twilight time-lapse, sky transitioning from gold to blue",
        "elevator doors parting to reveal penthouse foyer",
        "drone orbiting property at dusk, interior glow visible",
        "chef plating a dish in the kitchen, lifestyle vignette",
    ],

    # ------------------------------------------------------------------
    # Reference brands
    # ------------------------------------------------------------------
    "reference_brands": [
        "Sotheby's International Realty",
        "Christie's Real Estate",
        "Compass",
        "Douglas Elliman",
        "The Agency",
        "Engel & Völkers",
        "Knight Frank",
        "Savills",
        "Architectural Digest",
        "Dwell",
        "Luxury Portfolio International",
        "Coldwell Banker Global Luxury",
    ],

    # ------------------------------------------------------------------
    # Typical durations (seconds)
    # ------------------------------------------------------------------
    "typical_durations": {
        "15s": 15,
        "30s": 30,
        "45s": 45,
        "60s": 60,
    },
}
