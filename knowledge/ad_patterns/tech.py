"""Technology industry advertising patterns.

Defines the canonical visual language for consumer electronics and tech product
advertising.  Inspired by Apple, Samsung, Google, and Sony launch campaigns:
clean minimalism, floating product hero shots, dark gradient backgrounds,
precision-machined materials, and confident mechanical camera motion.
"""

TECH_PATTERN = {
    "industry": "tech",

    # ------------------------------------------------------------------
    # Scene flow
    # ------------------------------------------------------------------
    "scene_flow": [
        {
            "archetype": "establishing",
            "duration": 3.0,
            "description": "Abstract gradient void or ultra-modern space fades up; "
                           "sets a futuristic, distraction-free tone",
        },
        {
            "archetype": "product_hero",
            "duration": 4.0,
            "description": "Device materializes on a seamless dark surface, "
                           "rim light tracing machined edges",
        },
        {
            "archetype": "detail_macro",
            "duration": 3.0,
            "description": "Extreme close-up of signature feature — camera array, "
                           "hinge mechanism, or chip die shot",
        },
        {
            "archetype": "interaction",
            "duration": 3.5,
            "description": "Person picks up and uses the device in a clean, "
                           "modern environment; screen content visible",
        },
        {
            "archetype": "product_hero_alt",
            "duration": 3.0,
            "description": "Second hero angle emphasizing material finish — "
                           "brushed aluminum, ceramic, or matte glass",
        },
        {
            "archetype": "lifestyle",
            "duration": 4.0,
            "description": "Device integrated into everyday life: coffee shop, "
                           "commuter train, creative studio",
        },
        {
            "archetype": "feature_burst",
            "duration": 2.5,
            "description": "Rapid montage of specs — water resistance, "
                           "fast charging, AI processing — with kinetic typography",
        },
        {
            "archetype": "endframe",
            "duration": 2.5,
            "description": "Full product family lineup on black, logo resolve, "
                           "tagline and availability date",
        },
    ],

    # ------------------------------------------------------------------
    # Visual signature
    # ------------------------------------------------------------------
    "visual_signature": {
        "color_temperature": "neutral-to-cool 5600-6500K, blue-tinged highlights",
        "contrast": "high controlled contrast, deep blacks, clean whites",
        "saturation": "desaturated base with selective UI accent color pops",
        "grain": "zero grain, pixel-perfect clean digital acquisition",
        "depth_of_field": "shallow f/2.0-f/2.8 on hero, deep f/8 on lifestyle",
        "color_grade": "tech-neutral with subtle teal shadows, warm skin pass",
    },

    # ------------------------------------------------------------------
    # Lighting — keys from the canonical lighting_setups registry
    # ------------------------------------------------------------------
    "lighting_preferences": [
        "product_dark_field",
        "rim_light",
        "beauty_dish",
        "high_key",
        "low_key",
        "product_backlit_glow",
        "three_point",
        "window_light_soft",
        "neon_gel",
        "tungsten_warm",
    ],

    # ------------------------------------------------------------------
    # Lens — keys from the canonical lens registry
    # ------------------------------------------------------------------
    "lens_preferences": [
        "portrait_85mm_f14",
        "macro_100mm",
        "classic_35mm",
        "standard_50mm_f18",
        "tilt_shift_24mm",
        "anamorphic_50mm",
        "telephoto_135mm",
    ],

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------
    "movement_style": {
        "camera": "precise robotic motion, controlled orbit, smooth linear dolly, "
                  "macro slider for detail passes",
        "subject": "device reveal via mechanical arm, screen wake animation, "
                   "lid-open gesture, magnetic snap",
        "pacing": "confident and deliberate — every frame earns its place",
    },

    # ------------------------------------------------------------------
    # Transitions (ordered by preference)
    # ------------------------------------------------------------------
    "transition_preferences": [
        "hard cut on action",
        "match-shape wipe",
        "whip pan to black",
        "light flash transition",
        "morph cut",
        "screen-content zoom through",
    ],

    # ------------------------------------------------------------------
    # Audio
    # ------------------------------------------------------------------
    "music_style": (
        "minimal electronic pulse, spatial synth pads, precision sound design "
        "with tactile foley — click, snap, glass tap — building to a confident "
        "resolve"
    ),

    # ------------------------------------------------------------------
    # Banned elements
    # ------------------------------------------------------------------
    "banned_elements": [
        "cluttered or messy backgrounds",
        "visible fingerprints or smudges on glass",
        "cheap-looking plastic materials",
        "warm vintage or sepia color grading",
        "busy over-stimulating compositions",
        "outdated UI or placeholder screens",
        "stock-photo-style forced smiles",
        "lens flare that obscures the product",
        "shaky handheld camera movement",
        "Comic Sans or novelty typefaces",
    ],

    # ------------------------------------------------------------------
    # Prompt modifiers (20+)
    # ------------------------------------------------------------------
    "prompt_modifiers": [
        "Apple product photography aesthetic, seamless infinity cove",
        "machined aluminum bead-blasted texture, specular edge catch",
        "device floating on dark gradient, contact shadow only",
        "edge-to-edge OLED screen with vivid interface render",
        "Samsung Galaxy campaign quality, confident color blocking",
        "Google Pixel signature behind-the-glass depth",
        "Sony industrial design language, sharp chamfered edges",
        "circuit board macro, gold traces and BGA array visible",
        "glass and titanium material study, refraction highlights",
        "modern workspace hero shot, concrete desk, single plant",
        "futuristic abstract environment, volumetric light beams",
        "wireless earbuds levitating in product isolation",
        "holographic prismatic light effect on dark field",
        "thin profile edge-on silhouette, millimeter-precision",
        "camera module engineering detail, sapphire lens element",
        "device in hand, natural grip, shallow depth of field",
        "dramatic product reveal, light sweeping across surface",
        "ecosystem lineup, phone tablet laptop watch, unified design",
        "chip wafer close-up, nanometer process node detail",
        "MagSafe alignment animation, magnetic field lines implied",
        "dark mode UI glow as primary scene illumination",
        "precision CNC milling path texture on enclosure",
    ],

    # ------------------------------------------------------------------
    # Video modifiers (10+)
    # ------------------------------------------------------------------
    "video_modifiers": [
        "device rotating slowly on turntable, 360-degree reveal",
        "screen lighting up with boot animation, glow spreading",
        "camera module lenses retracting with mechanical precision",
        "device placed on charging pad, alignment haptic pulse",
        "laptop lid opening in single fluid motion, screen blooming",
        "finger tap on display triggering ripple UI response",
        "wireless earbuds rising from case, pairing animation",
        "notification cascade arriving on lock screen",
        "water droplets beading and rolling off IP68 surface",
        "chip inserting into logic board, microscopic solder reflow",
        "slow-motion drop test onto hard surface, no damage",
        "split-screen before-and-after computational photography",
    ],

    # ------------------------------------------------------------------
    # Reference brands
    # ------------------------------------------------------------------
    "reference_brands": [
        "Apple",
        "Samsung",
        "Google",
        "Sony",
        "Microsoft Surface",
        "Nothing",
        "OnePlus",
        "Bang & Olufsen",
        "Dyson",
        "Bose",
        "Tesla",
        "DJI",
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
