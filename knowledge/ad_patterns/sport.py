"""Sport industry advertising patterns.

Defines the canonical visual language for athletic and sportswear advertising.
Think Nike, Adidas, Under Armour, Gatorade -- high energy, dramatic lighting,
sweat and motion, raw empowerment.
"""

SPORT_PATTERN = {
    "industry": "sport",

    # ------------------------------------------------------------------
    # Scene flow -- typical 30-second athletic spot
    # ------------------------------------------------------------------
    "scene_flow": [
        {
            "archetype": "establishing",
            "duration": 2.0,
            "description": "Pre-dawn stadium, empty track, or gritty gym -- anticipation before effort",
        },
        {
            "archetype": "portrait",
            "duration": 2.5,
            "description": "Athlete lacing up, chalking hands, eyes locked forward in fierce concentration",
        },
        {
            "archetype": "action_burst",
            "duration": 3.5,
            "description": "Explosive first movement -- sprint start, box jump, first punch",
        },
        {
            "archetype": "detail",
            "duration": 2.0,
            "description": "Macro on shoe tread gripping, sweat droplets flying, muscle fiber tension",
        },
        {
            "archetype": "peak_performance",
            "duration": 4.0,
            "description": "Full-speed athletic peak -- crossing the line, slam dunk, match point",
        },
        {
            "archetype": "product_hero",
            "duration": 3.0,
            "description": "Product in context -- shoe mid-stride, jersey drenched in sweat, gear in hand",
        },
        {
            "archetype": "triumph",
            "duration": 3.5,
            "description": "Victory moment -- fist pump, team embrace, raw primal scream of achievement",
        },
        {
            "archetype": "endframe",
            "duration": 2.5,
            "description": "Brand mark lands with motivational tagline over black or minimal background",
        },
    ],

    # ------------------------------------------------------------------
    # Visual signature
    # ------------------------------------------------------------------
    "visual_signature": {
        "color_temperature": "cool neutral 5000K base with selective warm accent highlights",
        "contrast": "high and punchy, deep blacks crushed for drama",
        "saturation": "bold but controlled, selective color pops on brand hues",
        "grain": "minimal clean digital with natural motion texture from speed",
        "depth_of_field": "medium f/2.8-f/5.6 to keep athletic context visible",
        "color_grade": "teal-shadow / amber-highlight split, desaturated midtones",
    },

    # ------------------------------------------------------------------
    # Lighting -- keys from lighting_setups.py
    # ------------------------------------------------------------------
    "lighting_preferences": [
        "split",
        "rim_light",
        "backlit",
        "silhouette",
        "harsh_noon",
        "golden_hour",
        "low_key",
        "chiaroscuro",
        "cinematic_teal_orange",
        "fog_haze",
    ],

    # ------------------------------------------------------------------
    # Lenses -- keys from lens_library.py
    # ------------------------------------------------------------------
    "lens_preferences": [
        "zoom_24_70mm",
        "zoom_70_200mm",
        "wide_16mm",
        "portrait_85mm_f14",
        "telephoto_400mm",
        "wide_24mm",
        "standard_50mm_f14",
    ],

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------
    "movement_style": {
        "camera": "dynamic tracking, handheld energy, low-angle crane sweeps, whip pans",
        "subject": "explosive sprints, jumps, strikes, falls, sweat spray in air",
        "pacing": "building intensity through cuts, climactic peak then sudden stillness",
    },

    # ------------------------------------------------------------------
    # Transitions (ordered by preference)
    # ------------------------------------------------------------------
    "transition_preferences": [
        "hard cut on impact",
        "whip pan",
        "match cut on movement arc",
        "speed ramp freeze-to-motion",
        "flash frame white",
        "smash cut to black",
    ],

    # ------------------------------------------------------------------
    # Audio direction
    # ------------------------------------------------------------------
    "music_style": "driving electronic beats layered with orchestral swells, bass-heavy drops, hip-hop energy, heartbeat sub-bass",

    # ------------------------------------------------------------------
    # Banned elements
    # ------------------------------------------------------------------
    "banned_elements": [
        "slow lifeless pacing with no momentum",
        "flat even lighting that kills muscle definition",
        "overly retouched skin losing sweat and texture",
        "weak passive compositions with centered subjects",
        "excessive unmotivated slow motion",
        "cluttered busy backgrounds that distract from athlete",
        "stock-photo smiling athletes with no grit",
        "cool blue color casts that look clinical",
        "dutch angles used as a gimmick",
        "text-heavy frames that break immersion",
    ],

    # ------------------------------------------------------------------
    # Prompt modifiers for image generation
    # ------------------------------------------------------------------
    "prompt_modifiers": [
        "high-performance sports photography",
        "Nike campaign aesthetic",
        "dramatic athletic hero shot",
        "sweat droplets visible on skin catching rim light",
        "explosive motion capture frozen at 1/2000s",
        "stadium atmosphere with volumetric light shafts",
        "muscular definition sculpted by directional hard light",
        "determination etched in athlete's expression",
        "motion blur conveying raw speed and power",
        "gritty authentic training environment",
        "dramatic low angle hero composition looking up",
        "Under Armour campaign intensity and rawness",
        "selective desaturated color grade with single brand color pop",
        "dirt chalk or water spray frozen mid-air",
        "backlit silhouette in heroic power pose",
        "gym environment with dramatic pools of overhead light",
        "competitive fire burning in athlete's eyes",
        "raw unfiltered athletic moment no posing",
        "finish line triumph arms raised composition",
        "pre-game ritual intimate close-up hands and gear",
        "Adidas Impossible Is Nothing visual language",
        "track spikes digging into rubber surface macro",
        "breath visible in cold morning air backlit",
        "stadium floodlights creating star burst flares",
        "boxing ring ropes and canvas texture foreground",
    ],

    # ------------------------------------------------------------------
    # Video / Kling animation modifiers
    # ------------------------------------------------------------------
    "video_modifiers": [
        "explosive start burst of speed from stillness",
        "slow-motion impact moment muscles rippling on contact",
        "sweat flying off skin in dramatic backlit slow-mo",
        "dynamic camera tracking alongside sprinting athlete",
        "quick cuts between three angles of the same movement",
        "slam dunk or goal celebration raw emotion",
        "shoe sole hitting ground with dust cloud erupting",
        "chest heaving with heavy breathing after max effort",
        "fist pump victory moment freeze at apex",
        "equipment slamming down barbell crash with chalk cloud",
        "athlete emerging from tunnel into stadium light",
        "rope slam waves rippling outward from impact",
    ],

    # ------------------------------------------------------------------
    # Reference brands
    # ------------------------------------------------------------------
    "reference_brands": [
        "Nike",
        "Adidas",
        "Under Armour",
        "Gatorade",
        "Puma",
        "New Balance",
        "Reebok",
        "Jordan Brand",
        "Beats by Dre",
        "Red Bull",
        "Oakley",
        "The North Face",
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
