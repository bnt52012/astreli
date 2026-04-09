"""
Food and beverage advertising patterns.

Covers restaurants, packaged food, beverages (alcoholic and non-alcoholic),
meal kits, snacks, coffee/tea, health foods, and culinary brands.
Reference campaigns: Coca-Cola, Nespresso, Blue Apron, Heineken,
Oatly, Whole Foods, McDonald's premium, craft brewery.
"""

PATTERNS: dict = {
    "scene_flow": [
        {
            "scene_type": "ingredient_origin",
            "typical_duration": "2-4s",
            "purpose": "Show where it comes from — sun-ripened tomatoes on the vine, coffee cherries on a hillside, wheat fields at golden hour. Establishes freshness, quality, and provenance.",
        },
        {
            "scene_type": "preparation_craft",
            "typical_duration": "3-6s",
            "purpose": "The making — hands kneading dough, a chef plating, a bartender shaking, milk frothing. The craft and care behind the product.",
        },
        {
            "scene_type": "hero_pour_or_plate",
            "typical_duration": "3-5s",
            "purpose": "The money shot — a perfect pour with condensation, a plate set down with steam rising, a fork breaking into a golden crust. The single most appetizing frame.",
        },
        {
            "scene_type": "texture_detail",
            "typical_duration": "2-3s",
            "purpose": "Extreme close-up of food texture — bubbling cheese, cracking chocolate shell, fizzing carbonation, dripping honey. Triggers sensory response.",
        },
        {
            "scene_type": "social_enjoyment",
            "typical_duration": "3-5s",
            "purpose": "People sharing and enjoying — friends around a table, a couple cooking together, a family meal. Food as connection and experience.",
        },
        {
            "scene_type": "product_packaging",
            "typical_duration": "2-3s",
            "purpose": "The retail product in its best light — bottle on a bar, package on a kitchen counter, can in hand. Drives recognition at point of purchase.",
        },
        {
            "scene_type": "brand_appetite_close",
            "typical_duration": "2-3s",
            "purpose": "Logo and tagline, often paired with a final appetizing image or the sound of a sip, crunch, or pop. Leave them hungry.",
        },
    ],
    "visual_signature": {
        "color_temperature": "Warm (4500-5500K). Food almost always looks better warm — it suggests freshness, home cooking, and appetite. Cool tones only for premium spirits or clinical health-food contexts.",
        "contrast": "Medium. Enough to give food dimension and make textures pop, but not so much that shadows go black and details are lost. Highlights should be controlled — no blown-out whites on plates.",
        "saturation": "Elevated but natural. Colors should look more vivid than reality but never artificial. Reds, oranges, and greens are typically boosted 10-15%. Yellows and browns are warmed.",
        "grain": "Minimal for commercial food photography. Ultra-clean and sharp. Artisanal and craft brands may embrace slight grain for a 'homemade' or 'documentary' feel.",
        "depth_of_field": "Shallow for hero shots (f/1.8-f/2.8) to isolate the dish and blur the background. Medium for table scenes (f/4-f/5.6) to keep multiple elements in focus. Deep for environment shots.",
    },
    "lighting_preferences": [
        {
            "name": "Backlight with bounce",
            "description": "Main light behind and above the food, with a white card bouncing fill from the front. Creates luminous edges, steam visibility, and highlights liquid transparency. The gold standard of food photography.",
        },
        {
            "name": "Side window light",
            "description": "Soft, directional light from one side simulating a window. Creates gentle shadows that give food dimension and texture. Natural and inviting.",
        },
        {
            "name": "Overhead flat lay",
            "description": "Even, diffused light from directly above for top-down shots. Eliminates harsh shadows across multiple dishes. The Instagram flat-lay standard.",
        },
        {
            "name": "Warm practical glow",
            "description": "Candles, pendant lamps, and warm overhead fixtures as the primary light source. Creates the atmosphere of a restaurant or dinner party.",
        },
        {
            "name": "Dramatic chiaroscuro",
            "description": "Single hard light source creating deep shadows and bright highlights. Moody and artistic — used for dark-background 'hero on black' food styling.",
        },
        {
            "name": "Fire and flame light",
            "description": "Light from an open flame — grill, oven, wood fire. Warm, flickering, dynamic. Suggests cooking over fire and artisanal preparation.",
        },
        {
            "name": "Bright and airy",
            "description": "High-key lighting with minimal shadows, white or light-colored surfaces. Fresh, healthy, modern. The clean-eating, wellness-brand look.",
        },
        {
            "name": "Golden hour natural",
            "description": "Late-afternoon outdoor light for al fresco dining, picnic, or farm scenes. Warm, romantic, and appetizing.",
        },
    ],
    "lens_preferences": [
        {
            "focal_length": "100mm macro",
            "aperture": "f/2.8",
            "use_case": "Texture close-ups — cheese pull, chocolate snap, sauce drizzle, bubble detail. Reveals the sensory details that trigger appetite.",
        },
        {
            "focal_length": "50mm",
            "aperture": "f/1.4",
            "use_case": "Hero dish shots and table scenes. Natural perspective, beautiful bokeh for isolating the main subject from surrounding elements.",
        },
        {
            "focal_length": "85mm",
            "aperture": "f/1.8",
            "use_case": "Beverage hero shots and single-dish portraits. Slight compression flatters bottles and glassware. Beautiful background blur.",
        },
        {
            "focal_length": "35mm",
            "aperture": "f/2.0",
            "use_case": "Table-scene storytelling and environmental context. Shows the setting — kitchen, restaurant, outdoor table — with the food in context.",
        },
        {
            "focal_length": "24mm tilt-shift",
            "aperture": "f/3.5",
            "use_case": "Overhead flat-lay shots with controlled focus plane. Keeps multiple dishes sharp while maintaining shallow depth on edges.",
        },
    ],
    "movement_style": {
        "camera_movement": "Controlled and appetizing. Slow push-ins toward the hero dish, gentle overhead tracking across a spread, smooth slider reveals. Movement should feel like leaning in to smell or taste. No jerky or fast motion that would make food look unappealing.",
        "subject_movement": "Pouring, drizzling, sprinkling, slicing, breaking, pulling, dipping. The active verbs of food preparation and consumption. Every movement should trigger a sensory response — the stretch of cheese, the crunch of a chip, the fizz of a pour.",
        "pacing": "Medium. Fast enough to maintain appetite interest, slow enough to let the viewer savor each shot. Hero moments should hold 30% longer than feels natural to let the craving build.",
    },
    "transition_preferences": [
        "Match cut from ingredient to finished dish — a tomato on the vine cuts to tomato sauce on pasta.",
        "Overhead wipe following a drizzle, pour, or sprinkle across the frame.",
        "Steam or smoke dissolve — rising steam blurs the frame and clears to the next scene.",
        "Snap zoom into a texture detail, then cut to a new scene.",
        "Hands entering frame as a natural wipe — a plate being set down reveals the next shot.",
        "Liquid pour transition — beer, coffee, or sauce flowing fills the frame and resolves into the next scene.",
    ],
    "music_style": {
        "tempo": "80-120 BPM. Light, rhythmic, warm. Should feel like a dinner playlist — not too fast, not too slow.",
        "instruments": "Acoustic guitar, light percussion (shakers, cajons), piano, whistling, ukulele, gentle brass. Organic and warm. Premium brands may use jazz (upright bass, brushed drums, muted trumpet).",
        "mood": "Warm, inviting, joyful, communal. The feeling of gathering around a table with people you love. Can range from playful and bright (snacks, fast-casual) to sophisticated and intimate (fine dining, premium spirits).",
        "avoid": "Heavy electronic music, aggressive beats, dark or moody atmospheres (unless specifically a bar/nightlife context). Also avoid anything that feels rushed or stressful.",
    },
    "banned_elements": [
        "Unappetizing food presentation — wilted greens, overcooked proteins, sloppy plating.",
        "Cool, blue-toned lighting on food — it kills appetite appeal instantly.",
        "Messy or dirty surfaces that look unsanitary rather than rustic.",
        "Artificial-looking food colors that scream food dye or heavy processing.",
        "People talking with their mouths full or unflattering eating close-ups.",
        "Harsh overhead fluorescent lighting that flattens food and creates green casts.",
        "Stock-photo 'fake food' with shellac and inedible props — modern food advertising demands authenticity.",
        "Overly cluttered frames where you cannot identify the hero dish.",
        "Steam or smoke that obscures rather than enhances the food.",
        "Fingerprints or smudges on glassware and plates.",
        "Slow, boring pans across a table with nothing happening.",
        "Generic restaurant interiors with no character or atmosphere.",
    ],
    "prompt_modifiers": [
        "professional food photography, appetizing and mouth-watering",
        "backlit food hero shot, luminous edges and visible steam",
        "extreme macro of food texture, bubbling cheese detail",
        "warm side-window lighting, natural and inviting atmosphere",
        "dark moody food photography, single dish on black background",
        "overhead flat lay of curated table spread, styled props",
        "pour shot with liquid dynamics, splash and fizz frozen",
        "rustic wooden table surface, artisanal and handcrafted feel",
        "golden hour outdoor dining, warm natural sunlight",
        "close-up of hands preparing food, chef craftsmanship",
        "condensation droplets on cold beverage glass, refreshing",
        "sauce drizzle in slow motion, glossy and viscous",
        "bright and airy kitchen setting, clean modern aesthetic",
        "ingredient spread around hero dish, farm-to-table story",
        "fire-grilled texture, charred edges and smoke wisps",
        "cocktail photography with ice, garnish, and colored light",
        "breakfast scene with morning light streaming through window",
        "chocolate or dessert photography with rich dark tones",
        "crisp salad with water droplets, fresh and vibrant greens",
        "coffee art and steam macro, warm tones and creamy texture",
    ],
    "video_modifiers": [
        "slow motion pour into glass with fizz and foam dynamics",
        "overhead tracking shot across a styled dinner table spread",
        "tabletop slider push-in to hero dish with steam rising",
        "120fps chocolate breaking or cheese pulling in slow motion",
        "hands-in-frame cooking montage, rhythmic ingredient preparation",
        "rotating product shot with condensation catching backlight",
        "match-cut sequence from raw ingredient to finished plate",
        "smoke and steam rising through backlight beam, atmospheric",
        "social dining scene with passing plates and pouring drinks",
        "snap zoom from wide table to extreme close-up of texture",
    ],
}
