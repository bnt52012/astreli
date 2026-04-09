"""Food and beverage industry advertising patterns.

Defines the canonical visual language for food, drink, and culinary advertising.
Think Coca-Cola, McDonald's, Haagen-Dazs, Nespresso -- warm appetizing colors,
rising steam, extreme texture close-ups, pure indulgence.
"""

FOOD_BEVERAGE_PATTERN = {
    "industry": "food_beverage",

    # ------------------------------------------------------------------
    # Scene flow -- typical 30-second food/beverage spot
    # ------------------------------------------------------------------
    "scene_flow": [
        {
            "archetype": "establishing",
            "duration": 3.0,
            "description": "Warm kitchen, rustic farm table, or intimate restaurant setting the mood",
        },
        {
            "archetype": "ingredient_showcase",
            "duration": 2.5,
            "description": "Hero ingredients in extreme close-up -- dewy tomatoes, cracked pepper, cocoa nibs",
        },
        {
            "archetype": "process",
            "duration": 4.0,
            "description": "Preparation ritual -- pouring, sizzling, whisking, flame kissing the surface",
        },
        {
            "archetype": "product_hero",
            "duration": 4.0,
            "description": "Final dish or drink in its most appetizing moment -- steam, glisten, drip",
        },
        {
            "archetype": "interaction",
            "duration": 3.5,
            "description": "First bite, first sip -- eyes closing, genuine pleasure on face",
        },
        {
            "archetype": "detail_reprise",
            "duration": 2.5,
            "description": "Cross-section reveal, slow pour, or perfect splash frozen in time",
        },
        {
            "archetype": "lifestyle",
            "duration": 3.0,
            "description": "Shared table, friends clinking glasses, family passing the dish",
        },
        {
            "archetype": "endframe",
            "duration": 2.5,
            "description": "Product pack shot with brand mark on warm textured surface",
        },
    ],

    # ------------------------------------------------------------------
    # Visual signature
    # ------------------------------------------------------------------
    "visual_signature": {
        "color_temperature": "warm 3800-5000K, appetite-enhancing golden tones",
        "contrast": "medium with rich tonal range, luminous highlights",
        "saturation": "rich natural colors boosted selectively on reds oranges and greens",
        "grain": "minimal and clean to preserve fine texture detail",
        "depth_of_field": "very shallow f/1.4-f/2.8 isolating hero subject with creamy bokeh",
        "color_grade": "warm amber lift in shadows, clean whites, saturated midtones",
    },

    # ------------------------------------------------------------------
    # Lighting -- keys from lighting_setups.py
    # ------------------------------------------------------------------
    "lighting_preferences": [
        "window_light_soft",
        "window_light_dramatic",
        "backlit",
        "tungsten_warm",
        "candle_firelight",
        "product_dark_field",
        "product_light_field",
        "product_backlit_glow",
        "tabletop_product",
        "rim_light",
    ],

    # ------------------------------------------------------------------
    # Lenses -- keys from lens_library.py
    # ------------------------------------------------------------------
    "lens_preferences": [
        "macro_100mm",
        "portrait_85mm_f14",
        "standard_50mm_f18",
        "tilt_shift_24mm",
        "classic_35mm",
        "macro_105mm",
        "pancake_40mm",
    ],

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------
    "movement_style": {
        "camera": "slow deliberate dollies, gentle top-down descents, smooth arcs around hero dish",
        "subject": "pouring liquids, rising steam, dripping sauce, bubbles ascending, ice cracking",
        "pacing": "sensuous and unhurried, lingering on texture and detail before moving on",
    },

    # ------------------------------------------------------------------
    # Transitions (ordered by preference)
    # ------------------------------------------------------------------
    "transition_preferences": [
        "soft dissolve",
        "clean cut on action",
        "fade through warm black",
        "match cut on shape or color",
        "rack focus transition",
        "wipe with steam or liquid",
    ],

    # ------------------------------------------------------------------
    # Audio direction
    # ------------------------------------------------------------------
    "music_style": "warm jazz, gentle acoustic guitar, ambient kitchen sounds layered with soft strings, occasional playful pizzicato",

    # ------------------------------------------------------------------
    # Banned elements
    # ------------------------------------------------------------------
    "banned_elements": [
        "blue or green color casts on food making it look unappetizing",
        "harsh direct flash killing all texture and depth",
        "fast frantic editing that prevents savoring the food",
        "clinical sterile backgrounds that feel like a lab",
        "messy unintentional spills that look like mistakes not style",
        "overhead fluorescent lighting with greenish cast",
        "plastic or artificial looking food that breaks trust",
        "dutch angles on plated food that look chaotic",
        "over-sharpened images that create halos on edges",
        "visible crew reflections in glassware or cutlery",
    ],

    # ------------------------------------------------------------------
    # Prompt modifiers for image generation
    # ------------------------------------------------------------------
    "prompt_modifiers": [
        "professional food photography editorial quality",
        "appetizing warm color grading with golden tones",
        "visible steam rising from hot surface catching backlight",
        "macro texture of ingredient surface in sharp detail",
        "condensation droplets beading on chilled glass",
        "sauce dripping with perfect viscosity slow and thick",
        "rustic reclaimed wood surface with natural grain texture",
        "fresh herb garnish vibrant green against warm tones",
        "cream pouring into dark coffee creating marble spiral",
        "caramelized golden crust detail shot at macro distance",
        "ice crystals forming on frosted glass surface",
        "Bon Appetit magazine cover quality plating",
        "ingredient scatter in artful asymmetric arrangement",
        "cross-section revealing layers of filling and texture",
        "hand reaching for food creating authentic candid moment",
        "farm-to-table rustic elegance with linen napkins",
        "champagne bubbles rising in elegant flute backlit",
        "chocolate drizzle captured mid-flow catching sidelight",
        "perfectly plated fine dining with negative space",
        "backlit beverage glowing warm amber through glass",
        "Nespresso campaign sophistication and richness",
        "morning light raking across fresh pastry surface",
        "olive oil pooling on bread with herb flecks visible",
        "citrus zest spray frozen mid-squeeze catching light",
        "copper cookware reflecting warm kitchen environment",
    ],

    # ------------------------------------------------------------------
    # Video / Kling animation modifiers
    # ------------------------------------------------------------------
    "video_modifiers": [
        "slow-motion pour with visible liquid dynamics and viscosity",
        "steam rising lazily from freshly plated dish catching backlight",
        "cheese pull stretching slowly between two halves",
        "champagne cork popping with foam cascading down bottle",
        "sauce drizzle in slow motion pooling on surface",
        "ice cube tumbling into glass with liquid splashing upward",
        "flames leaping from cooking pan in controlled burst",
        "bread being torn apart with steam escaping from center",
        "knife slicing cleanly through revealing perfect interior",
        "coffee cream swirl viewed from directly above",
        "butter melting and sliding across hot pancake surface",
        "sprinkle of sea salt falling in slow motion onto chocolate",
    ],

    # ------------------------------------------------------------------
    # Reference brands
    # ------------------------------------------------------------------
    "reference_brands": [
        "Coca-Cola",
        "McDonald's",
        "Haagen-Dazs",
        "Nespresso",
        "Starbucks",
        "Heineken",
        "Magnum Ice Cream",
        "Godiva",
        "Ferrero Rocher",
        "Guinness",
        "Perrier",
        "Lindt",
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
