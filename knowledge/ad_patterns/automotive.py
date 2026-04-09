"""Automotive industry advertising patterns.

Defines the canonical visual language for luxury and performance car advertising.
Think Mercedes-Benz, BMW, Porsche, Tesla -- metallic reflections, sweeping
landscapes, raw power, precision engineering.
"""

AUTOMOTIVE_PATTERN = {
    "industry": "automotive",

    # ------------------------------------------------------------------
    # Scene flow -- typical 30-45 second automotive spot
    # ------------------------------------------------------------------
    "scene_flow": [
        {
            "archetype": "landscape_reveal",
            "duration": 3.5,
            "description": "Sweeping aerial of dramatic road -- mountain pass, coastal highway, or rain-slicked city",
        },
        {
            "archetype": "car_reveal",
            "duration": 4.0,
            "description": "First full car shot -- low angle three-quarter view, paint catching light",
        },
        {
            "archetype": "design_detail",
            "duration": 2.5,
            "description": "Sculpted body line, LED signature headlight, badge macro, brake caliper",
        },
        {
            "archetype": "driving_sequence",
            "duration": 5.0,
            "description": "Car devouring the road -- tracking shot alongside at speed, landscape blurring",
        },
        {
            "archetype": "interior",
            "duration": 3.0,
            "description": "Cockpit luxury -- leather stitching, ambient lighting, driver's hands on wheel",
        },
        {
            "archetype": "engineering_detail",
            "duration": 2.5,
            "description": "Wheel rotation, carbon fiber weave, exhaust tip, suspension at work",
        },
        {
            "archetype": "performance_climax",
            "duration": 4.0,
            "description": "Apex cornering, launch control acceleration, or controlled drift with tire smoke",
        },
        {
            "archetype": "endframe",
            "duration": 3.0,
            "description": "Car in heroic pose -- three-quarter front, brand mark and model name",
        },
    ],

    # ------------------------------------------------------------------
    # Visual signature
    # ------------------------------------------------------------------
    "visual_signature": {
        "color_temperature": "cool neutral 5200K exterior with warm 3500K interior accents",
        "contrast": "high cinematic with deep crushed blacks and clean specular whites",
        "saturation": "controlled and precise, selective pop on car body color only",
        "grain": "near zero to preserve metallic flake and paint clarity",
        "depth_of_field": "medium f/4-f/5.6 keeping full car sharp with soft environment",
        "color_grade": "cool steel blue shadows, warm amber interior tones, teal-orange split",
    },

    # ------------------------------------------------------------------
    # Lighting -- keys from lighting_setups.py
    # ------------------------------------------------------------------
    "lighting_preferences": [
        "golden_hour",
        "blue_hour",
        "rim_light",
        "backlit",
        "silhouette",
        "neon_gel",
        "reflective_surface",
        "cinematic_teal_orange",
        "moonlight_cool",
        "fog_haze",
    ],

    # ------------------------------------------------------------------
    # Lenses -- keys from lens_library.py
    # ------------------------------------------------------------------
    "lens_preferences": [
        "wide_24mm",
        "zoom_70_200mm",
        "standard_50mm_f14",
        "ultra_wide_14mm",
        "macro_100mm",
        "classic_35mm",
        "anamorphic_75mm",
    ],

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------
    "movement_style": {
        "camera": "sweeping crane arcs, low-angle tracking alongside, smooth gimbal orbits, helicopter aerials",
        "subject": "car in controlled powerful motion, wheels spinning, body rolling through corners",
        "pacing": "measured build-up to dramatic reveal, alternating between detail stillness and driving energy",
    },

    # ------------------------------------------------------------------
    # Transitions (ordered by preference)
    # ------------------------------------------------------------------
    "transition_preferences": [
        "dramatic hard cut on engine note",
        "slow dissolve between landscape and detail",
        "speed ramp from real-time to slow motion",
        "match cut on body line to road curve",
        "fade through deep black",
        "light flare wipe from headlight sweep",
    ],

    # ------------------------------------------------------------------
    # Audio direction
    # ------------------------------------------------------------------
    "music_style": "orchestral epic swells, deep electronic pulse, engine sound design woven into score, bass resonance on acceleration",

    # ------------------------------------------------------------------
    # Banned elements
    # ------------------------------------------------------------------
    "banned_elements": [
        "cheap static tripod angles that look like dealership footage",
        "flat even lighting with no sculpting on body panels",
        "dirty damaged or dusty vehicles breaking premium feel",
        "cluttered parking lot or suburban backgrounds",
        "unflattering reflections of crew or equipment in paint",
        "amateur dashcam or GoPro interior aesthetic",
        "visible license plates or dealer markings",
        "overhead noon sun creating ugly roof hot spots",
        "cartoonish color grading that undermines sophistication",
        "text overlays covering the car body",
    ],

    # ------------------------------------------------------------------
    # Prompt modifiers for image generation
    # ------------------------------------------------------------------
    "prompt_modifiers": [
        "professional automotive photography studio quality",
        "dramatic low-angle three-quarter car portrait",
        "reflective paint surface with environment mapped in clearcoat",
        "chrome and glass specular highlights precisely controlled",
        "open road stretching to vanishing point on horizon",
        "rain-slicked asphalt reflecting tail lights in streaks",
        "LED headlight signature detail shot at dusk",
        "carbon fiber weave texture visible at macro distance",
        "quilted leather interior with contrast stitching detail",
        "forged alloy wheels and ceramic brake calipers close-up",
        "tunnel lighting rhythm painting moving light bars on body",
        "dawn silhouette car in power stance against orange sky",
        "aerodynamic sculpture lines highlighted by raking sidelight",
        "BMW M campaign intensity and precision aesthetic",
        "Porsche campaign engineering perfection visual language",
        "motorsport heritage livery and pit lane atmosphere",
        "engine bay mechanical precision surgical cleanliness",
        "night driving with city lights streaking past windows",
        "dust cloud trailing behind on dry desert road",
        "aerial tracking shot looking down at car on winding mountain road",
        "Mercedes-Benz elegance and restrained luxury",
        "exhaust tip detail with heat shimmer visible",
        "car emerging from darkness into single shaft of light",
        "reflection of driver in side mirror cinematic framing",
        "tire tread pattern macro with road debris texture",
    ],

    # ------------------------------------------------------------------
    # Video / Kling animation modifiers
    # ------------------------------------------------------------------
    "video_modifiers": [
        "car launching forward from standstill with raw acceleration",
        "slow orbit around parked car revealing every angle and line",
        "rear wheel spin with tire smoke billowing on launch",
        "headlights sweeping on sequentially illuminating darkness",
        "car cornering hard with controlled rear drift and tire squeal",
        "rain water spraying off rear wheel arches at speed",
        "camera tracking alongside at highway speed matching pace",
        "interior ambient lighting pulsing on as door opens",
        "panoramic sunroof opening to reveal sky above driver",
        "gullwing or scissor doors opening in dramatic synchronized reveal",
        "exhaust burble and flame on downshift in tunnel",
        "car cresting hill and briefly going airborne with suspension compression",
    ],

    # ------------------------------------------------------------------
    # Reference brands
    # ------------------------------------------------------------------
    "reference_brands": [
        "Mercedes-Benz",
        "BMW",
        "Porsche",
        "Tesla",
        "Audi",
        "Lexus",
        "Lamborghini",
        "Ferrari",
        "Land Rover",
        "Volvo",
        "McLaren",
        "Bentley",
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
