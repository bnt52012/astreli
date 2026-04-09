"""
Photography styles reference module.

Contains 100+ professional photography styles, each with structured metadata
including prompt keywords optimized for Gemini and SDXL image generation,
industry mappings, and mood descriptors.

Exports:
    PHOTOGRAPHY_STYLES: list of style dictionaries
    STYLE_BY_KEY: dict mapping snake_case keys to style dicts
"""

PHOTOGRAPHY_STYLES = [
    # -------------------------------------------------------------------------
    # Editorial & Fashion
    # -------------------------------------------------------------------------
    {
        "key": "editorial_fashion",
        "name": "Editorial Fashion",
        "description": (
            "High fashion editorial photography in the tradition of Vogue and "
            "Harper's Bazaar. Strong visual narrative with intentional styling "
            "and dramatic compositions."
        ),
        "prompt_keywords": [
            "high fashion editorial",
            "Vogue quality",
            "dramatic lighting",
            "intentional styling",
            "visual narrative",
            "couture",
            "fashion spread",
            "editorial composition",
        ],
        "best_industries": ["fashion", "luxury", "beauty"],
        "mood": "dramatic and aspirational",
    },
    {
        "key": "high_fashion_editorial",
        "name": "High Fashion Editorial",
        "description": (
            "Ultra-premium haute couture editorial with avant-garde styling. "
            "Pushes creative boundaries with bold color, unconventional poses, "
            "and striking backdrops."
        ),
        "prompt_keywords": [
            "haute couture",
            "avant-garde styling",
            "bold composition",
            "high contrast",
            "fashion editorial",
            "designer clothing",
            "striking pose",
            "artistic direction",
        ],
        "best_industries": ["fashion", "luxury", "beauty"],
        "mood": "bold and boundary-pushing",
    },
    {
        "key": "street_fashion",
        "name": "Street Fashion",
        "description": (
            "Candid street-style photography capturing fashion in urban "
            "environments. Authentic energy with documentary sensibility and "
            "real-world context."
        ),
        "prompt_keywords": [
            "street style",
            "urban environment",
            "candid moment",
            "natural light",
            "city backdrop",
            "authentic fashion",
            "documentary style",
            "pavement texture",
        ],
        "best_industries": ["fashion", "lifestyle", "sport"],
        "mood": "energetic and authentic",
    },
    {
        "key": "lookbook",
        "name": "Lookbook",
        "description": (
            "Clean, consistent lookbook photography for seasonal collections. "
            "Focus on garment detail, fit, and versatile styling across "
            "multiple looks."
        ),
        "prompt_keywords": [
            "lookbook photography",
            "clean background",
            "full body",
            "garment detail",
            "consistent lighting",
            "seasonal collection",
            "neutral backdrop",
            "fashion catalog",
        ],
        "best_industries": ["fashion", "luxury"],
        "mood": "clean and consistent",
    },
    {
        "key": "red_carpet",
        "name": "Red Carpet",
        "description": (
            "Glamorous red carpet photography with polished lighting and "
            "celebrity-grade presentation. Captures arrivals, gowns, and "
            "the spectacle of premiere events."
        ),
        "prompt_keywords": [
            "red carpet",
            "glamour lighting",
            "celebrity style",
            "evening gown",
            "paparazzi flash",
            "premiere event",
            "black tie",
            "polished presentation",
        ],
        "best_industries": ["fashion", "luxury", "beauty", "jewelry_watches"],
        "mood": "glamorous and polished",
    },
    {
        "key": "catalog_ecommerce",
        "name": "Catalog E-commerce",
        "description": (
            "Clean, standardized e-commerce product photography on white or "
            "neutral backgrounds. Optimized for online retail with even "
            "lighting and accurate color reproduction."
        ),
        "prompt_keywords": [
            "e-commerce photography",
            "white background",
            "product packshot",
            "even lighting",
            "accurate color",
            "catalog quality",
            "clean composition",
            "retail ready",
        ],
        "best_industries": ["fashion", "tech", "beauty"],
        "mood": "clean and commercial",
    },
    {
        "key": "campaign_heroshot",
        "name": "Campaign Heroshot",
        "description": (
            "High-impact hero imagery for advertising campaigns. Designed for "
            "billboards, banners, and key visuals with maximum stopping power "
            "and brand storytelling."
        ),
        "prompt_keywords": [
            "hero shot",
            "campaign photography",
            "advertising quality",
            "dramatic presentation",
            "key visual",
            "billboard ready",
            "brand storytelling",
            "high impact",
        ],
        "best_industries": [
            "luxury", "fashion", "automotive", "tech", "fragrance",
        ],
        "mood": "powerful and commanding",
    },
    {
        "key": "behind_the_scenes",
        "name": "Behind the Scenes",
        "description": (
            "Intimate behind-the-scenes photography from sets, studios, and "
            "production environments. Captures the creative process and "
            "authentic moments between takes."
        ),
        "prompt_keywords": [
            "behind the scenes",
            "BTS photography",
            "candid production",
            "on-set moment",
            "creative process",
            "intimate access",
            "unscripted",
            "natural light",
        ],
        "best_industries": ["fashion", "beauty", "luxury"],
        "mood": "intimate and authentic",
    },

    # -------------------------------------------------------------------------
    # Portrait
    # -------------------------------------------------------------------------
    {
        "key": "fine_art_portrait",
        "name": "Fine Art Portrait",
        "description": (
            "Museum-quality portrait photography with painterly light and "
            "rich tonal range. Inspired by classical masters with "
            "contemporary sensibility."
        ),
        "prompt_keywords": [
            "fine art portrait",
            "painterly light",
            "rich tonal range",
            "Rembrandt lighting",
            "gallery quality",
            "classical composition",
            "artistic expression",
            "museum worthy",
        ],
        "best_industries": ["luxury", "beauty", "fashion"],
        "mood": "timeless and refined",
    },
    {
        "key": "celebrity_portrait",
        "name": "Celebrity Portrait",
        "description": (
            "Polished celebrity portrait photography with controlled studio "
            "lighting and retouching. Conveys charisma, status, and "
            "personality."
        ),
        "prompt_keywords": [
            "celebrity portrait",
            "studio lighting",
            "polished retouching",
            "charismatic expression",
            "magazine cover",
            "star quality",
            "professional makeup",
            "confident pose",
        ],
        "best_industries": ["luxury", "fashion", "beauty", "fragrance"],
        "mood": "charismatic and polished",
    },
    {
        "key": "environmental_portrait",
        "name": "Environmental Portrait",
        "description": (
            "Portraits that place subjects within meaningful environments. "
            "The setting tells part of the story, adding context, narrative, "
            "and depth to the subject."
        ),
        "prompt_keywords": [
            "environmental portrait",
            "contextual setting",
            "subject in environment",
            "storytelling",
            "natural light",
            "location portrait",
            "narrative depth",
            "wide composition",
        ],
        "best_industries": ["travel", "luxury", "real_estate"],
        "mood": "narrative and grounded",
    },
    {
        "key": "golden_hour_portrait",
        "name": "Golden Hour Portrait",
        "description": (
            "Warm, sun-kissed portraits shot during the golden hour. Soft "
            "directional light creates flattering skin tones and a romantic, "
            "nostalgic atmosphere."
        ),
        "prompt_keywords": [
            "golden hour",
            "warm sunlight",
            "sun-kissed skin",
            "backlit portrait",
            "lens flare",
            "soft shadows",
            "romantic glow",
            "magic hour",
        ],
        "best_industries": ["beauty", "fashion", "travel", "fragrance"],
        "mood": "warm and romantic",
    },
    {
        "key": "sport_dramatic_portrait",
        "name": "Sport Dramatic Portrait",
        "description": (
            "Intense athletic portraits with dramatic studio lighting. "
            "Emphasizes physicality, determination, and raw human power "
            "through hard light and deep contrast."
        ),
        "prompt_keywords": [
            "athlete portrait",
            "dramatic lighting",
            "high contrast",
            "sweat detail",
            "powerful stance",
            "hard light",
            "intense expression",
            "sports editorial",
        ],
        "best_industries": ["sport", "fashion"],
        "mood": "intense and powerful",
    },

    # -------------------------------------------------------------------------
    # Beauty
    # -------------------------------------------------------------------------
    {
        "key": "beauty_closeup",
        "name": "Beauty Closeup",
        "description": (
            "Extreme closeup beauty photography highlighting skin texture, "
            "makeup artistry, and product application. Precision lighting "
            "reveals luminous skin and fine detail."
        ),
        "prompt_keywords": [
            "beauty closeup",
            "luminous skin",
            "macro detail",
            "butterfly lighting",
            "makeup artistry",
            "skin texture",
            "dewy finish",
            "beauty editorial",
        ],
        "best_industries": ["beauty", "fashion", "fragrance"],
        "mood": "polished and luminous",
    },

    # -------------------------------------------------------------------------
    # Lifestyle
    # -------------------------------------------------------------------------
    {
        "key": "lifestyle_candid",
        "name": "Lifestyle Candid",
        "description": (
            "Natural, unposed lifestyle photography capturing authentic "
            "moments. Feels spontaneous and relatable while maintaining "
            "aspirational quality."
        ),
        "prompt_keywords": [
            "lifestyle photography",
            "candid moment",
            "natural light",
            "authentic emotion",
            "unposed",
            "relatable scene",
            "warm tones",
            "aspirational living",
        ],
        "best_industries": [
            "fashion", "beauty", "food_beverage", "travel", "real_estate",
        ],
        "mood": "warm and authentic",
    },

    # -------------------------------------------------------------------------
    # Product & Commercial
    # -------------------------------------------------------------------------
    {
        "key": "commercial_product",
        "name": "Commercial Product",
        "description": (
            "Premium commercial product photography with controlled studio "
            "lighting and meticulous styling. Designed for advertising and "
            "brand campaigns."
        ),
        "prompt_keywords": [
            "commercial product photography",
            "studio lighting",
            "premium surface",
            "advertising quality",
            "controlled environment",
            "brand campaign",
            "product hero",
            "professional styling",
        ],
        "best_industries": ["tech", "luxury", "beauty", "fragrance"],
        "mood": "premium and polished",
    },
    {
        "key": "flat_lay_styled",
        "name": "Flat Lay Styled",
        "description": (
            "Curated overhead flat lay arrangements with editorial styling. "
            "Objects are thoughtfully composed in a grid or organic layout "
            "for maximum visual impact."
        ),
        "prompt_keywords": [
            "flat lay",
            "overhead perspective",
            "curated arrangement",
            "editorial styling",
            "organized composition",
            "top-down view",
            "styled objects",
            "visual storytelling",
        ],
        "best_industries": ["beauty", "fashion", "food_beverage", "tech"],
        "mood": "curated and organized",
    },
    {
        "key": "tech_product_launch",
        "name": "Tech Product Launch",
        "description": (
            "Sleek technology product photography for launches and reveals. "
            "Clean lines, gradient backgrounds, and dramatic rim lighting "
            "showcase innovation and precision engineering."
        ),
        "prompt_keywords": [
            "tech product",
            "product launch",
            "gradient background",
            "rim lighting",
            "sleek design",
            "innovation",
            "precision engineering",
            "clean lines",
        ],
        "best_industries": ["tech", "automotive"],
        "mood": "sleek and innovative",
    },

    # -------------------------------------------------------------------------
    # Architecture & Interior
    # -------------------------------------------------------------------------
    {
        "key": "architectural_interior",
        "name": "Architectural Interior",
        "description": (
            "Professional interior architecture photography with corrected "
            "verticals and balanced exposures. Showcases spatial design, "
            "materials, and natural light flow."
        ),
        "prompt_keywords": [
            "interior photography",
            "architectural detail",
            "corrected verticals",
            "natural light",
            "spatial design",
            "material texture",
            "wide angle",
            "balanced exposure",
        ],
        "best_industries": ["real_estate", "luxury", "travel"],
        "mood": "spacious and refined",
    },
    {
        "key": "real_estate_luxury",
        "name": "Real Estate Luxury",
        "description": (
            "High-end real estate photography showcasing luxury properties. "
            "Twilight exteriors, perfectly staged interiors, and lifestyle "
            "vignettes that sell a dream."
        ),
        "prompt_keywords": [
            "luxury real estate",
            "twilight exterior",
            "staged interior",
            "premium property",
            "architectural elegance",
            "natural light",
            "lifestyle vignette",
            "aspirational living",
        ],
        "best_industries": ["real_estate", "luxury"],
        "mood": "aspirational and elegant",
    },
    {
        "key": "real_estate_aerial",
        "name": "Real Estate Aerial",
        "description": (
            "Aerial drone photography for property and estate marketing. "
            "Bird's eye perspective reveals property scale, landscaping, "
            "and surrounding context."
        ),
        "prompt_keywords": [
            "aerial drone",
            "property overview",
            "bird's eye view",
            "landscape context",
            "estate grounds",
            "overhead perspective",
            "geographic context",
            "real estate marketing",
        ],
        "best_industries": ["real_estate", "travel", "luxury"],
        "mood": "expansive and impressive",
    },

    # -------------------------------------------------------------------------
    # Food & Beverage
    # -------------------------------------------------------------------------
    {
        "key": "food_editorial",
        "name": "Food Editorial",
        "description": (
            "Magazine-quality food photography with artful styling and "
            "narrative context. Goes beyond appetite appeal to tell the "
            "story of cuisine, culture, and craft."
        ),
        "prompt_keywords": [
            "food editorial",
            "magazine quality",
            "artful styling",
            "warm tones",
            "shallow depth of field",
            "appetite appeal",
            "culinary storytelling",
            "professional food styling",
        ],
        "best_industries": ["food_beverage", "travel", "luxury"],
        "mood": "appetizing and narrative",
    },
    {
        "key": "food_overhead_flat_lay",
        "name": "Food Overhead Flat Lay",
        "description": (
            "Top-down food photography with carefully arranged ingredients "
            "and dishes. Shows the full spread, textures, and color palette "
            "of a meal or recipe."
        ),
        "prompt_keywords": [
            "overhead food",
            "flat lay",
            "top-down perspective",
            "ingredient arrangement",
            "table setting",
            "color palette",
            "recipe layout",
            "food styling",
        ],
        "best_industries": ["food_beverage"],
        "mood": "organized and appetizing",
    },

    # -------------------------------------------------------------------------
    # Automotive
    # -------------------------------------------------------------------------
    {
        "key": "automotive_studio",
        "name": "Automotive Studio",
        "description": (
            "Controlled studio automotive photography with dramatic lighting "
            "and reflective surfaces. Showcases vehicle design, paint finish, "
            "and engineering craftsmanship."
        ),
        "prompt_keywords": [
            "automotive studio",
            "dramatic lighting",
            "reflective paint",
            "car photography",
            "controlled environment",
            "design lines",
            "premium finish",
            "studio backdrop",
        ],
        "best_industries": ["automotive", "luxury"],
        "mood": "dramatic and premium",
    },
    {
        "key": "automotive_rig_shot",
        "name": "Automotive Rig Shot",
        "description": (
            "Dynamic rig shot photography capturing vehicles in motion. "
            "The car stays sharp while the background blurs at speed, "
            "conveying power and performance."
        ),
        "prompt_keywords": [
            "rig shot",
            "motion blur background",
            "sharp vehicle",
            "speed effect",
            "dynamic movement",
            "automotive action",
            "performance photography",
            "long exposure motion",
        ],
        "best_industries": ["automotive", "sport"],
        "mood": "dynamic and powerful",
    },

    # -------------------------------------------------------------------------
    # Jewelry & Watches
    # -------------------------------------------------------------------------
    {
        "key": "jewelry_macro",
        "name": "Jewelry Macro",
        "description": (
            "Extreme macro jewelry photography revealing gemstone fire, metal "
            "finish, and intricate craftsmanship. Precision lighting controls "
            "reflections and sparkle."
        ),
        "prompt_keywords": [
            "jewelry macro",
            "gemstone detail",
            "diamond fire",
            "metal reflection",
            "precision lighting",
            "craftsmanship detail",
            "luxury closeup",
            "focus stacking",
        ],
        "best_industries": ["jewelry_watches", "luxury"],
        "mood": "luxurious and precise",
    },

    # -------------------------------------------------------------------------
    # Fragrance & Still Life
    # -------------------------------------------------------------------------
    {
        "key": "fragrance_still_life",
        "name": "Fragrance Still Life",
        "description": (
            "Evocative fragrance bottle photography with atmospheric props "
            "and lighting. Translates scent into visual language through "
            "mood, texture, and ingredient storytelling."
        ),
        "prompt_keywords": [
            "fragrance photography",
            "perfume bottle",
            "atmospheric lighting",
            "glass refraction",
            "ingredient props",
            "scent visualization",
            "luxury still life",
            "editorial fragrance",
        ],
        "best_industries": ["fragrance", "luxury", "beauty"],
        "mood": "evocative and sensual",
    },
    {
        "key": "still_life_classical",
        "name": "Still Life Classical",
        "description": (
            "Classical still life photography inspired by Dutch Golden Age "
            "masters. Rich chiaroscuro, draped fabrics, and arranged objects "
            "create timeless compositions."
        ),
        "prompt_keywords": [
            "classical still life",
            "chiaroscuro lighting",
            "Dutch masters",
            "draped fabric",
            "oil painting quality",
            "dark background",
            "arranged objects",
            "rich tones",
        ],
        "best_industries": ["luxury", "food_beverage", "jewelry_watches"],
        "mood": "timeless and painterly",
    },
    {
        "key": "still_life_modern",
        "name": "Still Life Modern",
        "description": (
            "Contemporary still life with graphic compositions and bold color "
            "choices. Clean lines, geometric arrangements, and modern surfaces "
            "create a fresh aesthetic."
        ),
        "prompt_keywords": [
            "modern still life",
            "graphic composition",
            "bold color",
            "geometric arrangement",
            "clean surface",
            "contemporary styling",
            "minimalist props",
            "studio lighting",
        ],
        "best_industries": ["beauty", "tech", "luxury", "food_beverage"],
        "mood": "fresh and graphic",
    },

    # -------------------------------------------------------------------------
    # Sport & Action
    # -------------------------------------------------------------------------
    {
        "key": "sport_action",
        "name": "Sport Action",
        "description": (
            "High-speed sports action photography freezing peak moments. "
            "Fast shutter speeds capture athletes mid-motion with tack-sharp "
            "detail and explosive energy."
        ),
        "prompt_keywords": [
            "sports action",
            "high-speed capture",
            "peak moment",
            "fast shutter",
            "athletic motion",
            "explosive energy",
            "tack sharp",
            "dynamic composition",
        ],
        "best_industries": ["sport", "fashion"],
        "mood": "explosive and energetic",
    },

    # -------------------------------------------------------------------------
    # Travel
    # -------------------------------------------------------------------------
    {
        "key": "travel_documentary",
        "name": "Travel Documentary",
        "description": (
            "Authentic travel documentary photography capturing culture, "
            "people, and places. Rich in storytelling with photojournalistic "
            "sensibility and vivid natural color."
        ),
        "prompt_keywords": [
            "travel documentary",
            "cultural authenticity",
            "natural light",
            "storytelling",
            "vivid color",
            "photojournalistic",
            "location portrait",
            "local culture",
        ],
        "best_industries": ["travel", "luxury"],
        "mood": "authentic and immersive",
    },
    {
        "key": "travel_luxury",
        "name": "Travel Luxury",
        "description": (
            "Premium luxury travel photography showcasing exclusive "
            "destinations, resorts, and experiences. Polished and aspirational "
            "with warm, inviting tones."
        ),
        "prompt_keywords": [
            "luxury travel",
            "exclusive destination",
            "resort photography",
            "premium experience",
            "aspirational lifestyle",
            "warm tones",
            "paradise setting",
            "five-star quality",
        ],
        "best_industries": ["travel", "luxury", "real_estate"],
        "mood": "aspirational and inviting",
    },

    # -------------------------------------------------------------------------
    # Cinematic & Film
    # -------------------------------------------------------------------------
    {
        "key": "cinematic_film_still",
        "name": "Cinematic Film Still",
        "description": (
            "Photography styled as a frame from a feature film. Widescreen "
            "composition, cinematic color grading, and atmospheric depth "
            "create narrative tension."
        ),
        "prompt_keywords": [
            "cinematic still",
            "film frame",
            "widescreen composition",
            "color grading",
            "atmospheric depth",
            "anamorphic bokeh",
            "narrative tension",
            "movie quality",
        ],
        "best_industries": ["fashion", "luxury", "automotive", "fragrance"],
        "mood": "cinematic and atmospheric",
    },
    {
        "key": "film_noir",
        "name": "Film Noir",
        "description": (
            "Classic film noir aesthetic with high-contrast black and white, "
            "hard shadows, and venetian blind light patterns. Evokes mystery, "
            "intrigue, and urban drama."
        ),
        "prompt_keywords": [
            "film noir",
            "high contrast",
            "black and white",
            "hard shadows",
            "venetian blind light",
            "mystery atmosphere",
            "urban night",
            "dramatic chiaroscuro",
        ],
        "best_industries": ["fashion", "luxury", "fragrance"],
        "mood": "mysterious and dramatic",
    },

    # -------------------------------------------------------------------------
    # Vintage & Film Stock
    # -------------------------------------------------------------------------
    {
        "key": "vintage_kodak_portra",
        "name": "Vintage Kodak Portra",
        "description": (
            "Emulates the warm, natural skin tones and fine grain of Kodak "
            "Portra film stock. Soft contrast with beautiful highlight "
            "rolloff and muted pastels."
        ),
        "prompt_keywords": [
            "Kodak Portra",
            "film grain",
            "warm skin tones",
            "soft contrast",
            "analog photography",
            "highlight rolloff",
            "muted pastels",
            "35mm film",
        ],
        "best_industries": ["fashion", "beauty", "travel"],
        "mood": "warm and nostalgic",
    },
    {
        "key": "vintage_fuji_pro",
        "name": "Vintage Fuji Pro",
        "description": (
            "Emulates the cool greens, vivid blues, and punchy saturation "
            "of Fujifilm Pro 400H. Clean highlights and distinctive color "
            "rendering beloved by wedding and portrait photographers."
        ),
        "prompt_keywords": [
            "Fujifilm Pro 400H",
            "cool green tones",
            "vivid blues",
            "film emulation",
            "clean highlights",
            "punchy saturation",
            "fine grain",
            "analog color",
        ],
        "best_industries": ["fashion", "beauty", "travel"],
        "mood": "cool and vivid",
    },
    {
        "key": "vintage_kodachrome",
        "name": "Vintage Kodachrome",
        "description": (
            "Emulates the legendary saturated reds, deep blues, and warm "
            "yellows of Kodachrome slide film. High contrast with rich, "
            "punchy color and archival quality."
        ),
        "prompt_keywords": [
            "Kodachrome",
            "saturated reds",
            "deep blues",
            "slide film",
            "high contrast",
            "warm yellows",
            "punchy color",
            "vintage saturation",
        ],
        "best_industries": ["travel", "fashion", "automotive"],
        "mood": "vivid and nostalgic",
    },
    {
        "key": "polaroid",
        "name": "Polaroid",
        "description": (
            "Instant Polaroid photography aesthetic with soft faded colors, "
            "distinctive white border, and slightly overexposed quality. "
            "Evokes spontaneity and personal memory."
        ),
        "prompt_keywords": [
            "Polaroid instant",
            "faded colors",
            "white border",
            "soft overexposure",
            "nostalgic snapshot",
            "instant film",
            "vintage texture",
            "personal memory",
        ],
        "best_industries": ["fashion", "beauty", "travel"],
        "mood": "nostalgic and spontaneous",
    },

    # -------------------------------------------------------------------------
    # Art Movements & Aesthetics
    # -------------------------------------------------------------------------
    {
        "key": "art_deco",
        "name": "Art Deco",
        "description": (
            "Photography inspired by Art Deco design with geometric patterns, "
            "metallic gold and black palette, and symmetrical compositions. "
            "Evokes 1920s glamour and opulence."
        ),
        "prompt_keywords": [
            "Art Deco",
            "geometric patterns",
            "gold and black",
            "symmetrical composition",
            "1920s glamour",
            "metallic accents",
            "ornate detail",
            "luxury opulence",
        ],
        "best_industries": [
            "luxury", "jewelry_watches", "fashion", "fragrance",
        ],
        "mood": "glamorous and geometric",
    },
    {
        "key": "minimalist_scandinavian",
        "name": "Minimalist Scandinavian",
        "description": (
            "Clean Scandinavian minimalism with neutral palette, natural "
            "materials, and abundant negative space. Celebrates simplicity, "
            "functionality, and quiet beauty."
        ),
        "prompt_keywords": [
            "Scandinavian minimalism",
            "neutral palette",
            "negative space",
            "natural materials",
            "clean lines",
            "functional beauty",
            "white space",
            "simple composition",
        ],
        "best_industries": ["real_estate", "tech", "beauty"],
        "mood": "calm and minimal",
    },
    {
        "key": "japanese_wabi_sabi",
        "name": "Japanese Wabi-Sabi",
        "description": (
            "Photography embracing the Japanese aesthetic of wabi-sabi: "
            "beauty in imperfection, transience, and incompleteness. Muted "
            "tones, natural textures, and quiet contemplation."
        ),
        "prompt_keywords": [
            "wabi-sabi",
            "imperfect beauty",
            "natural texture",
            "muted earth tones",
            "asymmetric composition",
            "organic forms",
            "quiet contemplation",
            "rustic patina",
        ],
        "best_industries": ["luxury", "food_beverage", "beauty"],
        "mood": "contemplative and organic",
    },
    {
        "key": "brutalist",
        "name": "Brutalist",
        "description": (
            "Raw, bold photography inspired by Brutalist architecture. "
            "Exposed concrete, hard geometric forms, and uncompromising "
            "compositions convey strength and honesty."
        ),
        "prompt_keywords": [
            "brutalist architecture",
            "raw concrete",
            "geometric forms",
            "hard edges",
            "monumental scale",
            "stark composition",
            "industrial texture",
            "uncompromising",
        ],
        "best_industries": ["fashion", "tech", "automotive"],
        "mood": "raw and monumental",
    },
    {
        "key": "baroque_opulence",
        "name": "Baroque Opulence",
        "description": (
            "Richly layered photography inspired by Baroque painting. "
            "Deep dramatic light, ornate detail, velvet textures, and "
            "sumptuous color create overwhelming sensory richness."
        ),
        "prompt_keywords": [
            "Baroque style",
            "dramatic chiaroscuro",
            "ornate detail",
            "velvet texture",
            "rich color",
            "opulent composition",
            "gilded elements",
            "classical grandeur",
        ],
        "best_industries": [
            "luxury", "fashion", "jewelry_watches", "fragrance",
        ],
        "mood": "opulent and dramatic",
    },
    {
        "key": "surrealist",
        "name": "Surrealist",
        "description": (
            "Dreamlike surrealist photography with impossible compositions "
            "and unexpected juxtapositions. Inspired by Dali and Magritte, "
            "blending reality with the subconscious."
        ),
        "prompt_keywords": [
            "surrealist",
            "dreamlike composition",
            "impossible scene",
            "unexpected juxtaposition",
            "subconscious imagery",
            "visual paradox",
            "floating objects",
            "distorted perspective",
        ],
        "best_industries": ["fashion", "luxury", "fragrance", "beauty"],
        "mood": "dreamlike and provocative",
    },
    {
        "key": "pop_art",
        "name": "Pop Art",
        "description": (
            "Bold, graphic photography inspired by Pop Art movement. "
            "Saturated primary colors, Ben-Day dots, bold outlines, and "
            "commercial iconography create playful, energetic images."
        ),
        "prompt_keywords": [
            "Pop Art",
            "bold primary colors",
            "graphic composition",
            "Ben-Day dots",
            "bold outlines",
            "commercial iconography",
            "high saturation",
            "playful energy",
        ],
        "best_industries": ["fashion", "beauty", "food_beverage"],
        "mood": "playful and bold",
    },

    # -------------------------------------------------------------------------
    # Conceptual & Fine Art
    # -------------------------------------------------------------------------
    {
        "key": "conceptual_art",
        "name": "Conceptual Art",
        "description": (
            "Idea-driven conceptual photography where the concept takes "
            "precedence over aesthetics. Symbolic imagery, metaphor, and "
            "visual puzzles communicate deeper meanings."
        ),
        "prompt_keywords": [
            "conceptual photography",
            "symbolic imagery",
            "visual metaphor",
            "idea-driven",
            "artistic concept",
            "gallery quality",
            "thought-provoking",
            "abstract narrative",
        ],
        "best_industries": ["luxury", "fashion", "beauty"],
        "mood": "intellectual and provocative",
    },

    # -------------------------------------------------------------------------
    # Specialty Techniques
    # -------------------------------------------------------------------------
    {
        "key": "underwater",
        "name": "Underwater",
        "description": (
            "Submerged underwater photography with flowing fabrics, refracted "
            "light, and weightless movement. Creates ethereal, otherworldly "
            "compositions impossible on land."
        ),
        "prompt_keywords": [
            "underwater photography",
            "submerged",
            "flowing fabric",
            "refracted light",
            "weightless movement",
            "aquatic atmosphere",
            "blue-green tones",
            "ethereal quality",
        ],
        "best_industries": ["fashion", "beauty", "sport", "travel"],
        "mood": "ethereal and otherworldly",
    },
    {
        "key": "aerial_drone",
        "name": "Aerial Drone",
        "description": (
            "Aerial drone photography capturing landscapes, architecture, "
            "and patterns from above. Reveals hidden geometries and sweeping "
            "perspectives impossible from ground level."
        ),
        "prompt_keywords": [
            "aerial drone",
            "bird's eye view",
            "sweeping landscape",
            "geometric patterns",
            "dramatic scale",
            "overhead perspective",
            "wide vista",
            "geographic context",
        ],
        "best_industries": ["travel", "real_estate", "automotive"],
        "mood": "expansive and dramatic",
    },
    {
        "key": "night_photography",
        "name": "Night Photography",
        "description": (
            "After-dark photography utilizing city lights, neon, and long "
            "exposures. Transforms ordinary scenes into luminous nocturnal "
            "compositions with extended tonal range."
        ),
        "prompt_keywords": [
            "night photography",
            "city lights",
            "neon glow",
            "long exposure",
            "nocturnal scene",
            "light trails",
            "urban night",
            "dark atmosphere",
        ],
        "best_industries": ["automotive", "travel", "fashion", "tech"],
        "mood": "atmospheric and luminous",
    },
    {
        "key": "motion_blur_artistic",
        "name": "Motion Blur Artistic",
        "description": (
            "Intentional motion blur used as a creative tool. Slow shutter "
            "speeds transform movement into painterly streaks and ghostly "
            "traces of energy."
        ),
        "prompt_keywords": [
            "motion blur",
            "slow shutter",
            "painterly movement",
            "artistic blur",
            "dynamic energy",
            "intentional motion",
            "ghostly traces",
            "kinetic composition",
        ],
        "best_industries": ["fashion", "sport", "automotive"],
        "mood": "dynamic and artistic",
    },
    {
        "key": "double_exposure",
        "name": "Double Exposure",
        "description": (
            "Overlaid double exposure photography blending two images into "
            "one. Creates dreamlike, poetic compositions where landscapes "
            "merge with portraits or textures."
        ),
        "prompt_keywords": [
            "double exposure",
            "overlaid images",
            "blended composition",
            "dreamlike overlay",
            "merged portrait",
            "transparent layers",
            "artistic blend",
            "poetic imagery",
        ],
        "best_industries": ["fashion", "beauty", "travel"],
        "mood": "dreamlike and poetic",
    },
    {
        "key": "reflection_photography",
        "name": "Reflection Photography",
        "description": (
            "Photography utilizing reflections in water, glass, mirrors, or "
            "polished surfaces. Creates symmetrical compositions and visual "
            "depth through mirrored imagery."
        ),
        "prompt_keywords": [
            "reflection",
            "mirror image",
            "water reflection",
            "symmetrical composition",
            "glass surface",
            "visual depth",
            "polished surface",
            "mirrored symmetry",
        ],
        "best_industries": ["luxury", "real_estate", "automotive", "travel"],
        "mood": "contemplative and symmetrical",
    },
    {
        "key": "smoke_fog_atmospheric",
        "name": "Smoke Fog Atmospheric",
        "description": (
            "Atmospheric photography using smoke, fog, or haze to create "
            "depth and mystery. Volumetric light cuts through the atmosphere, "
            "revealing dramatic shafts and soft diffusion."
        ),
        "prompt_keywords": [
            "smoke atmosphere",
            "fog haze",
            "volumetric light",
            "atmospheric depth",
            "light shafts",
            "mysterious mood",
            "soft diffusion",
            "dramatic atmosphere",
        ],
        "best_industries": ["fashion", "fragrance", "luxury", "automotive"],
        "mood": "mysterious and atmospheric",
    },
    {
        "key": "crystal_prism",
        "name": "Crystal Prism",
        "description": (
            "Photography using crystal prisms, glass elements, and refractive "
            "materials to create rainbow light leaks, kaleidoscopic effects, "
            "and prismatic distortions."
        ),
        "prompt_keywords": [
            "crystal prism",
            "rainbow refraction",
            "light leak",
            "kaleidoscopic effect",
            "prismatic distortion",
            "glass element",
            "spectral color",
            "optical effect",
        ],
        "best_industries": ["beauty", "fashion", "jewelry_watches"],
        "mood": "magical and prismatic",
    },
    {
        "key": "tilt_shift_miniature",
        "name": "Tilt Shift Miniature",
        "description": (
            "Tilt-shift photography creating a miniature model effect. "
            "Selective focus plane makes real scenes appear as tiny dioramas, "
            "or corrects architectural perspective."
        ),
        "prompt_keywords": [
            "tilt-shift",
            "miniature effect",
            "selective focus",
            "diorama appearance",
            "lens blur",
            "toy-like scene",
            "perspective control",
            "narrow focus plane",
        ],
        "best_industries": ["real_estate", "travel", "automotive"],
        "mood": "whimsical and curious",
    },
    {
        "key": "infrared",
        "name": "Infrared",
        "description": (
            "Infrared photography rendering foliage as white or pink and "
            "skies as deep black. Creates a surreal, alien landscape with "
            "dreamlike color inversion."
        ),
        "prompt_keywords": [
            "infrared photography",
            "white foliage",
            "surreal landscape",
            "color inversion",
            "deep black sky",
            "otherworldly",
            "dreamlike colors",
            "false color",
        ],
        "best_industries": ["travel", "fashion"],
        "mood": "surreal and otherworldly",
    },

    # -------------------------------------------------------------------------
    # Studio Lighting
    # -------------------------------------------------------------------------
    {
        "key": "studio_high_key",
        "name": "Studio High Key",
        "description": (
            "Bright, airy high-key studio photography with minimal shadows. "
            "White backgrounds and soft diffused lighting create a clean, "
            "optimistic, and approachable feel."
        ),
        "prompt_keywords": [
            "high-key lighting",
            "bright white",
            "minimal shadows",
            "soft diffused light",
            "clean background",
            "airy atmosphere",
            "optimistic mood",
            "even illumination",
        ],
        "best_industries": ["beauty", "tech", "fashion"],
        "mood": "bright and optimistic",
    },
    {
        "key": "studio_low_key",
        "name": "Studio Low Key",
        "description": (
            "Dark, moody low-key studio photography with selective "
            "highlights. Deep shadows and minimal fill create dramatic, "
            "cinematic atmosphere with strong focal contrast."
        ),
        "prompt_keywords": [
            "low-key lighting",
            "deep shadows",
            "selective highlights",
            "dramatic contrast",
            "dark background",
            "moody atmosphere",
            "minimal fill",
            "chiaroscuro",
        ],
        "best_industries": [
            "luxury", "fragrance", "automotive", "jewelry_watches",
        ],
        "mood": "dramatic and moody",
    },
    {
        "key": "color_gel",
        "name": "Color Gel",
        "description": (
            "Photography using colored gel lighting to create vivid, "
            "dramatic color casts. Complementary or contrasting gels produce "
            "bold, editorial compositions."
        ),
        "prompt_keywords": [
            "color gel lighting",
            "vivid color cast",
            "complementary colors",
            "dramatic gel",
            "editorial lighting",
            "bold color",
            "studio gel",
            "colored light",
        ],
        "best_industries": ["fashion", "beauty", "sport", "tech"],
        "mood": "vivid and dramatic",
    },

    # -------------------------------------------------------------------------
    # Mood-Based
    # -------------------------------------------------------------------------
    {
        "key": "moody_dark_editorial",
        "name": "Moody Dark Editorial",
        "description": (
            "Dark, atmospheric editorial photography with desaturated tones "
            "and deep shadow detail. Conveys intensity, sophistication, and "
            "emotional weight."
        ),
        "prompt_keywords": [
            "dark editorial",
            "moody atmosphere",
            "desaturated tones",
            "deep shadows",
            "intense mood",
            "cinematic darkness",
            "emotional weight",
            "rich blacks",
        ],
        "best_industries": ["fashion", "luxury", "fragrance"],
        "mood": "dark and intense",
    },
    {
        "key": "bright_and_airy",
        "name": "Bright and Airy",
        "description": (
            "Light, bright photography with soft shadows, pastel tones, and "
            "open highlights. Creates a fresh, optimistic, and welcoming "
            "atmosphere."
        ),
        "prompt_keywords": [
            "bright and airy",
            "soft shadows",
            "pastel tones",
            "open highlights",
            "fresh atmosphere",
            "natural light",
            "warm whites",
            "optimistic mood",
        ],
        "best_industries": ["beauty", "real_estate", "food_beverage", "travel"],
        "mood": "fresh and optimistic",
    },
    {
        "key": "clean_minimalist",
        "name": "Clean Minimalist",
        "description": (
            "Ultra-clean minimalist photography with maximum negative space "
            "and stripped-back composition. Every element is essential; "
            "nothing is superfluous."
        ),
        "prompt_keywords": [
            "clean minimalist",
            "negative space",
            "essential composition",
            "stripped back",
            "single subject",
            "precise placement",
            "geometric simplicity",
            "white space",
        ],
        "best_industries": ["tech", "beauty", "luxury"],
        "mood": "calm and precise",
    },
    {
        "key": "gritty_urban",
        "name": "Gritty Urban",
        "description": (
            "Raw, textured urban photography with high contrast and grain. "
            "Captures the energy and edge of city life with an unflinching, "
            "documentary feel."
        ),
        "prompt_keywords": [
            "gritty urban",
            "high contrast",
            "film grain",
            "raw texture",
            "city edge",
            "street photography",
            "industrial backdrop",
            "unflinching realism",
        ],
        "best_industries": ["fashion", "sport", "automotive"],
        "mood": "raw and edgy",
    },
    {
        "key": "soft_romantic",
        "name": "Soft Romantic",
        "description": (
            "Delicate, romantic photography with soft focus, warm pastels, "
            "and gentle backlight. Dreamy quality evokes tenderness, beauty, "
            "and quiet intimacy."
        ),
        "prompt_keywords": [
            "soft romantic",
            "gentle backlight",
            "warm pastels",
            "dreamy focus",
            "tender mood",
            "intimate composition",
            "delicate tones",
            "romantic atmosphere",
        ],
        "best_industries": ["beauty", "fashion", "fragrance", "jewelry_watches"],
        "mood": "tender and dreamy",
    },
    {
        "key": "bold_graphic",
        "name": "Bold Graphic",
        "description": (
            "High-impact graphic photography with strong shapes, saturated "
            "color blocks, and striking contrast. Designed for maximum "
            "visual stopping power."
        ),
        "prompt_keywords": [
            "bold graphic",
            "strong shapes",
            "saturated color blocks",
            "high contrast",
            "striking composition",
            "visual impact",
            "geometric elements",
            "stopping power",
        ],
        "best_industries": ["fashion", "tech", "sport"],
        "mood": "bold and impactful",
    },
    {
        "key": "blue_hour_urban",
        "name": "Blue Hour Urban",
        "description": (
            "Urban photography during blue hour when city lights glow against "
            "deep cobalt skies. Creates a moody, cinematic atmosphere with "
            "cool-warm color interplay."
        ),
        "prompt_keywords": [
            "blue hour",
            "cobalt sky",
            "city lights",
            "twilight urban",
            "cool-warm contrast",
            "cinematic atmosphere",
            "dusk photography",
            "neon reflections",
        ],
        "best_industries": ["automotive", "travel", "real_estate", "tech"],
        "mood": "moody and cinematic",
    },

    # -------------------------------------------------------------------------
    # Retro & Decade Aesthetics
    # -------------------------------------------------------------------------
    {
        "key": "retro_70s",
        "name": "Retro 70s",
        "description": (
            "1970s-inspired photography with warm amber tones, soft focus, "
            "and desaturated earth colors. Captures the free-spirited "
            "bohemian energy of the era."
        ),
        "prompt_keywords": [
            "1970s aesthetic",
            "warm amber tones",
            "soft focus",
            "earth colors",
            "bohemian style",
            "retro warmth",
            "vintage grain",
            "free-spirited energy",
        ],
        "best_industries": ["fashion", "beauty", "travel"],
        "mood": "warm and free-spirited",
    },
    {
        "key": "retro_80s",
        "name": "Retro 80s",
        "description": (
            "1980s-inspired photography with neon colors, synthwave palette, "
            "and bold geometric compositions. High energy, flashy, and "
            "unapologetically excessive."
        ),
        "prompt_keywords": [
            "1980s aesthetic",
            "neon colors",
            "synthwave palette",
            "bold geometric",
            "high energy",
            "flashy composition",
            "retro futurism",
            "excessive glamour",
        ],
        "best_industries": ["fashion", "sport", "tech"],
        "mood": "flashy and energetic",
    },
    {
        "key": "retro_90s",
        "name": "Retro 90s",
        "description": (
            "1990s-inspired photography with grunge textures, desaturated "
            "color, and raw flash aesthetic. Captures the anti-glamour "
            "attitude of the decade."
        ),
        "prompt_keywords": [
            "1990s aesthetic",
            "grunge texture",
            "desaturated color",
            "raw flash",
            "anti-glamour",
            "casual attitude",
            "lo-fi quality",
            "authentic rawness",
        ],
        "best_industries": ["fashion", "beauty"],
        "mood": "raw and rebellious",
    },
    {
        "key": "y2k_aesthetic",
        "name": "Y2K Aesthetic",
        "description": (
            "Early 2000s Y2K aesthetic with metallic finishes, cyber motifs, "
            "and futuristic optimism. Glossy surfaces, chrome reflections, "
            "and digital-age playfulness."
        ),
        "prompt_keywords": [
            "Y2K aesthetic",
            "metallic finish",
            "cyber motifs",
            "glossy surface",
            "chrome reflection",
            "futuristic optimism",
            "digital age",
            "millennium style",
        ],
        "best_industries": ["fashion", "beauty", "tech"],
        "mood": "futuristic and playful",
    },

    # -------------------------------------------------------------------------
    # Digital Culture Aesthetics
    # -------------------------------------------------------------------------
    {
        "key": "cyberpunk",
        "name": "Cyberpunk",
        "description": (
            "Cyberpunk photography with neon-drenched cityscapes, rain-slick "
            "streets, and dystopian atmosphere. Vivid magenta, cyan, and "
            "electric blue dominate the palette."
        ),
        "prompt_keywords": [
            "cyberpunk",
            "neon lights",
            "rain-slick streets",
            "dystopian atmosphere",
            "magenta and cyan",
            "electric blue",
            "futuristic city",
            "tech noir",
        ],
        "best_industries": ["tech", "fashion", "automotive"],
        "mood": "dystopian and electric",
    },
    {
        "key": "vaporwave",
        "name": "Vaporwave",
        "description": (
            "Vaporwave aesthetic with pastel pink and purple gradients, "
            "retro computing imagery, and nostalgic digital artifacts. "
            "Surreal, ironic, and dreamily artificial."
        ),
        "prompt_keywords": [
            "vaporwave",
            "pastel gradient",
            "pink and purple",
            "retro computing",
            "digital artifact",
            "nostalgic surrealism",
            "glitch aesthetic",
            "dreamy artificial",
        ],
        "best_industries": ["tech", "fashion", "beauty"],
        "mood": "dreamy and ironic",
    },
    {
        "key": "cottagecore",
        "name": "Cottagecore",
        "description": (
            "Idyllic cottagecore aesthetic celebrating rural life, wildflowers, "
            "and handmade simplicity. Warm, soft light with earthy tones and "
            "pastoral romance."
        ),
        "prompt_keywords": [
            "cottagecore",
            "rural idyll",
            "wildflowers",
            "handmade simplicity",
            "soft warm light",
            "earthy tones",
            "pastoral romance",
            "natural linen",
        ],
        "best_industries": ["fashion", "food_beverage", "beauty"],
        "mood": "idyllic and gentle",
    },
    {
        "key": "dark_academia",
        "name": "Dark Academia",
        "description": (
            "Dark academia aesthetic with scholarly interiors, leather-bound "
            "books, and autumn palettes. Moody, intellectual atmosphere "
            "inspired by classic literature and Gothic architecture."
        ),
        "prompt_keywords": [
            "dark academia",
            "scholarly interior",
            "leather-bound books",
            "autumn palette",
            "Gothic architecture",
            "moody intellectual",
            "rich brown tones",
            "classical study",
        ],
        "best_industries": ["fashion", "luxury", "fragrance"],
        "mood": "intellectual and moody",
    },
    {
        "key": "old_money_aesthetic",
        "name": "Old Money Aesthetic",
        "description": (
            "Understated old money aesthetic with muted luxury, heritage "
            "materials, and quiet elegance. Whispers wealth through quality "
            "rather than logos or flash."
        ),
        "prompt_keywords": [
            "old money",
            "understated luxury",
            "heritage materials",
            "quiet elegance",
            "muted tones",
            "classic quality",
            "refined taste",
            "subtle wealth",
        ],
        "best_industries": [
            "luxury", "fashion", "jewelry_watches", "real_estate",
        ],
        "mood": "understated and refined",
    },
    {
        "key": "new_luxury",
        "name": "New Luxury",
        "description": (
            "Contemporary new luxury aesthetic blending modern minimalism "
            "with premium materials. Clean, architectural spaces and "
            "cutting-edge design communicate forward-thinking wealth."
        ),
        "prompt_keywords": [
            "new luxury",
            "modern minimalism",
            "premium materials",
            "contemporary design",
            "architectural space",
            "cutting-edge",
            "forward-thinking",
            "refined modernity",
        ],
        "best_industries": ["luxury", "tech", "automotive", "real_estate"],
        "mood": "modern and premium",
    },
    {
        "key": "eco_sustainable",
        "name": "Eco Sustainable",
        "description": (
            "Earth-conscious sustainable photography with natural textures, "
            "organic materials, and green-toned palettes. Communicates "
            "environmental responsibility and authentic connection to nature."
        ),
        "prompt_keywords": [
            "eco sustainable",
            "natural texture",
            "organic materials",
            "green palette",
            "earth-conscious",
            "environmental",
            "raw natural",
            "sustainable living",
        ],
        "best_industries": ["beauty", "fashion", "food_beverage", "travel"],
        "mood": "natural and responsible",
    },

    # -------------------------------------------------------------------------
    # Weather & Environment
    # -------------------------------------------------------------------------
    {
        "key": "wet_rain_aesthetic",
        "name": "Wet Rain Aesthetic",
        "description": (
            "Rain-soaked photography with glistening surfaces, water "
            "droplets, and reflective wet pavement. Creates moody, romantic "
            "atmosphere with rich saturated color."
        ),
        "prompt_keywords": [
            "rain aesthetic",
            "wet surfaces",
            "water droplets",
            "reflective pavement",
            "glistening",
            "moody atmosphere",
            "rain-soaked",
            "saturated color",
        ],
        "best_industries": ["fashion", "automotive", "fragrance"],
        "mood": "moody and romantic",
    },
    {
        "key": "snow_winter",
        "name": "Snow Winter",
        "description": (
            "Winter snow photography with crisp white landscapes, cool blue "
            "shadows, and cozy warm contrasts. Captures the quiet beauty "
            "and drama of cold-weather scenes."
        ),
        "prompt_keywords": [
            "snow winter",
            "crisp white",
            "cool blue shadows",
            "frost detail",
            "cozy warmth",
            "winter landscape",
            "cold atmosphere",
            "seasonal drama",
        ],
        "best_industries": ["fashion", "travel", "luxury", "sport"],
        "mood": "crisp and serene",
    },

    # -------------------------------------------------------------------------
    # Location-Based
    # -------------------------------------------------------------------------
    {
        "key": "tropical_paradise",
        "name": "Tropical Paradise",
        "description": (
            "Vivid tropical photography with lush greenery, turquoise water, "
            "and warm golden sunlight. Captures the escapist allure of "
            "paradise destinations."
        ),
        "prompt_keywords": [
            "tropical paradise",
            "lush greenery",
            "turquoise water",
            "golden sunlight",
            "palm trees",
            "exotic location",
            "paradise beach",
            "vivid saturation",
        ],
        "best_industries": ["travel", "luxury", "fashion", "fragrance"],
        "mood": "exotic and vibrant",
    },
    {
        "key": "desert_arid",
        "name": "Desert Arid",
        "description": (
            "Desert landscape photography with vast sandy expanses, dramatic "
            "shadows, and warm earth tones. Captures the austere beauty and "
            "infinite scale of arid environments."
        ),
        "prompt_keywords": [
            "desert landscape",
            "arid terrain",
            "sand dunes",
            "warm earth tones",
            "dramatic shadows",
            "vast expanse",
            "harsh sunlight",
            "austere beauty",
        ],
        "best_industries": ["travel", "fashion", "automotive"],
        "mood": "vast and austere",
    },
    {
        "key": "forest_woodland",
        "name": "Forest Woodland",
        "description": (
            "Enchanting forest photography with dappled light, moss-covered "
            "trees, and deep green canopy. Creates an atmosphere of mystery, "
            "calm, and natural wonder."
        ),
        "prompt_keywords": [
            "forest woodland",
            "dappled light",
            "moss-covered trees",
            "deep green canopy",
            "natural wonder",
            "forest floor",
            "filtered sunlight",
            "enchanted atmosphere",
        ],
        "best_industries": ["travel", "fashion", "fragrance"],
        "mood": "enchanting and calm",
    },
    {
        "key": "mountain_alpine",
        "name": "Mountain Alpine",
        "description": (
            "Alpine mountain photography with dramatic peaks, sweeping "
            "valleys, and atmospheric clouds. Conveys grandeur, adventure, "
            "and the sublime power of high altitude."
        ),
        "prompt_keywords": [
            "alpine mountain",
            "dramatic peaks",
            "sweeping valley",
            "atmospheric clouds",
            "high altitude",
            "mountain grandeur",
            "adventure landscape",
            "crisp mountain air",
        ],
        "best_industries": ["travel", "sport", "luxury", "automotive"],
        "mood": "grand and adventurous",
    },
    {
        "key": "coastal_beach",
        "name": "Coastal Beach",
        "description": (
            "Coastal photography with crashing waves, sandy shores, and "
            "ocean horizons. Golden light, sea spray, and weathered textures "
            "create a timeless seaside atmosphere."
        ),
        "prompt_keywords": [
            "coastal beach",
            "crashing waves",
            "sandy shore",
            "ocean horizon",
            "golden light",
            "sea spray",
            "weathered texture",
            "seaside atmosphere",
        ],
        "best_industries": ["travel", "fashion", "luxury", "real_estate"],
        "mood": "refreshing and timeless",
    },

    # -------------------------------------------------------------------------
    # Cultural & Regional
    # -------------------------------------------------------------------------
    {
        "key": "mediterranean",
        "name": "Mediterranean",
        "description": (
            "Sun-drenched Mediterranean photography with terracotta, azure "
            "blue, and whitewashed architecture. Captures the warmth, "
            "leisure, and beauty of coastal European life."
        ),
        "prompt_keywords": [
            "Mediterranean",
            "terracotta tones",
            "azure blue",
            "whitewashed architecture",
            "sun-drenched",
            "coastal European",
            "olive groves",
            "warm leisure",
        ],
        "best_industries": ["travel", "luxury", "food_beverage", "real_estate"],
        "mood": "warm and leisurely",
    },
    {
        "key": "moroccan_north_african",
        "name": "Moroccan North African",
        "description": (
            "Rich Moroccan and North African photography with intricate "
            "tilework, vibrant spice markets, and warm earth-tone palettes. "
            "Ornate pattern and saturated color."
        ),
        "prompt_keywords": [
            "Moroccan style",
            "intricate tilework",
            "spice market",
            "warm earth tones",
            "ornate pattern",
            "vibrant textiles",
            "North African",
            "rich saturation",
        ],
        "best_industries": ["travel", "luxury", "fashion", "food_beverage"],
        "mood": "vibrant and ornate",
    },
    {
        "key": "indian_bollywood",
        "name": "Indian Bollywood",
        "description": (
            "Vibrant Indian and Bollywood-inspired photography with rich "
            "jewel tones, ornate gold detail, and celebratory energy. "
            "Captures the color and spectacle of South Asian culture."
        ),
        "prompt_keywords": [
            "Bollywood style",
            "jewel tones",
            "ornate gold detail",
            "vibrant celebration",
            "rich embroidery",
            "South Asian culture",
            "festive energy",
            "dramatic color",
        ],
        "best_industries": [
            "fashion", "jewelry_watches", "luxury", "beauty",
        ],
        "mood": "vibrant and celebratory",
    },
    {
        "key": "chinese_luxury",
        "name": "Chinese Luxury",
        "description": (
            "Refined Chinese luxury photography blending traditional motifs "
            "with contemporary sophistication. Red and gold palettes, silk "
            "textures, and calligraphic elegance."
        ),
        "prompt_keywords": [
            "Chinese luxury",
            "red and gold palette",
            "silk texture",
            "traditional motif",
            "contemporary refinement",
            "calligraphic elegance",
            "jade accent",
            "Eastern sophistication",
        ],
        "best_industries": [
            "luxury", "jewelry_watches", "fashion", "beauty",
        ],
        "mood": "refined and cultural",
    },
    {
        "key": "middle_eastern_opulence",
        "name": "Middle Eastern Opulence",
        "description": (
            "Luxurious Middle Eastern photography with gold, marble, and "
            "intricate geometric patterns. Reflects the grandeur of Gulf "
            "luxury and Islamic art traditions."
        ),
        "prompt_keywords": [
            "Middle Eastern luxury",
            "gold and marble",
            "geometric pattern",
            "Islamic art",
            "Gulf opulence",
            "ornate architecture",
            "rich embellishment",
            "desert luxury",
        ],
        "best_industries": [
            "luxury", "jewelry_watches", "real_estate", "fragrance",
        ],
        "mood": "opulent and grand",
    },
    {
        "key": "scandinavian_hygge",
        "name": "Scandinavian Hygge",
        "description": (
            "Cozy Scandinavian hygge photography with warm candlelight, "
            "knit textures, and intimate domestic scenes. Celebrates comfort, "
            "togetherness, and quiet contentment."
        ),
        "prompt_keywords": [
            "hygge atmosphere",
            "warm candlelight",
            "knit textures",
            "cozy interior",
            "intimate scene",
            "Scandinavian comfort",
            "soft warmth",
            "quiet contentment",
        ],
        "best_industries": ["real_estate", "food_beverage", "luxury"],
        "mood": "cozy and intimate",
    },
    {
        "key": "italian_dolce_vita",
        "name": "Italian Dolce Vita",
        "description": (
            "La Dolce Vita-inspired photography capturing Italian elegance, "
            "effortless style, and la bella vita. Warm Mediterranean light, "
            "Vespa culture, and timeless sophistication."
        ),
        "prompt_keywords": [
            "Dolce Vita",
            "Italian elegance",
            "effortless style",
            "Mediterranean light",
            "la bella vita",
            "Vespa culture",
            "timeless sophistication",
            "Roman holiday",
        ],
        "best_industries": [
            "fashion", "luxury", "travel", "food_beverage", "automotive",
        ],
        "mood": "elegant and carefree",
    },
    {
        "key": "french_parisian",
        "name": "French Parisian",
        "description": (
            "Quintessentially Parisian photography with Haussmann "
            "architecture, cafe culture, and effortless French chic. Soft "
            "light, muted tones, and romantic urban backdrops."
        ),
        "prompt_keywords": [
            "Parisian style",
            "Haussmann architecture",
            "French chic",
            "cafe culture",
            "soft muted tones",
            "romantic backdrop",
            "effortless elegance",
            "Left Bank atmosphere",
        ],
        "best_industries": ["fashion", "luxury", "beauty", "fragrance"],
        "mood": "chic and romantic",
    },
    {
        "key": "japanese_minimalist",
        "name": "Japanese Minimalist",
        "description": (
            "Japanese minimalist photography with clean composition, "
            "deliberate negative space, and reverence for form. Influenced "
            "by Zen aesthetics and the beauty of restraint."
        ),
        "prompt_keywords": [
            "Japanese minimalist",
            "Zen aesthetic",
            "deliberate negative space",
            "clean composition",
            "form reverence",
            "restraint",
            "natural material",
            "quiet elegance",
        ],
        "best_industries": ["luxury", "beauty", "tech", "food_beverage"],
        "mood": "serene and deliberate",
    },

    # -------------------------------------------------------------------------
    # Processing & Style
    # -------------------------------------------------------------------------
    {
        "key": "raw_unfiltered",
        "name": "Raw Unfiltered",
        "description": (
            "Unprocessed, straight-from-camera photography with no filters "
            "or heavy retouching. Emphasizes authenticity, truth, and the "
            "beauty of imperfection."
        ),
        "prompt_keywords": [
            "raw unfiltered",
            "no retouching",
            "authentic capture",
            "straight from camera",
            "natural imperfection",
            "honest photography",
            "unprocessed",
            "real moment",
        ],
        "best_industries": ["fashion", "sport", "travel"],
        "mood": "authentic and honest",
    },
    {
        "key": "hyper_polished",
        "name": "Hyper Polished",
        "description": (
            "Ultra-retouched, hyper-polished photography with flawless "
            "surfaces and perfected detail. Every pixel is refined for "
            "maximum commercial impact and aspirational appeal."
        ),
        "prompt_keywords": [
            "hyper polished",
            "ultra retouched",
            "flawless surface",
            "perfected detail",
            "commercial polish",
            "aspirational quality",
            "pixel perfect",
            "premium finish",
        ],
        "best_industries": ["beauty", "luxury", "fashion", "jewelry_watches"],
        "mood": "flawless and aspirational",
    },
    {
        "key": "documentary_realism",
        "name": "Documentary Realism",
        "description": (
            "Truthful documentary photography with photojournalistic "
            "integrity. Natural light, unmanipulated compositions, and "
            "decisive moments capture reality as it unfolds."
        ),
        "prompt_keywords": [
            "documentary realism",
            "photojournalistic",
            "natural light",
            "decisive moment",
            "unmanipulated",
            "truthful representation",
            "real world",
            "authentic capture",
        ],
        "best_industries": ["travel", "sport", "fashion"],
        "mood": "honest and compelling",
    },
    {
        "key": "fantasy_ethereal",
        "name": "Fantasy Ethereal",
        "description": (
            "Ethereal fantasy photography with soft glowing light, flowing "
            "fabrics, and otherworldly settings. Creates a fairy-tale "
            "atmosphere of magic and wonder."
        ),
        "prompt_keywords": [
            "ethereal fantasy",
            "soft glowing light",
            "flowing fabric",
            "otherworldly setting",
            "fairy-tale atmosphere",
            "magical quality",
            "dreamy softness",
            "enchanted scene",
        ],
        "best_industries": ["fashion", "beauty", "fragrance", "jewelry_watches"],
        "mood": "magical and ethereal",
    },
    {
        "key": "gothic_dark",
        "name": "Gothic Dark",
        "description": (
            "Dark Gothic photography with dramatic shadow play, Victorian "
            "elements, and brooding atmosphere. Deep blacks, rich burgundy, "
            "and ornate decay create haunting beauty."
        ),
        "prompt_keywords": [
            "Gothic dark",
            "dramatic shadows",
            "Victorian elements",
            "brooding atmosphere",
            "deep blacks",
            "rich burgundy",
            "ornate decay",
            "haunting beauty",
        ],
        "best_industries": ["fashion", "luxury", "fragrance"],
        "mood": "haunting and dramatic",
    },

    # -------------------------------------------------------------------------
    # Color Treatment
    # -------------------------------------------------------------------------
    {
        "key": "pastel_dream",
        "name": "Pastel Dream",
        "description": (
            "Soft pastel photography with desaturated candy colors and "
            "gentle gradients. Creates a dreamy, youthful atmosphere of "
            "lightness and visual sweetness."
        ),
        "prompt_keywords": [
            "pastel colors",
            "soft desaturated",
            "candy tones",
            "gentle gradient",
            "dreamy atmosphere",
            "youthful energy",
            "light and sweet",
            "millennial pink",
        ],
        "best_industries": ["beauty", "fashion", "food_beverage"],
        "mood": "dreamy and youthful",
    },
    {
        "key": "monochrome_classic",
        "name": "Monochrome Classic",
        "description": (
            "Classic black and white photography with full tonal range from "
            "deep blacks to pure whites. Strips away color to reveal form, "
            "light, and emotional essence."
        ),
        "prompt_keywords": [
            "monochrome",
            "black and white",
            "full tonal range",
            "deep blacks",
            "pure whites",
            "classic photography",
            "form and light",
            "emotional essence",
        ],
        "best_industries": [
            "fashion", "luxury", "beauty", "automotive", "sport",
        ],
        "mood": "timeless and essential",
    },
    {
        "key": "duotone",
        "name": "Duotone",
        "description": (
            "Duotone photography using two contrasting colors to create "
            "bold, graphic imagery. Strips the image to a striking two-color "
            "palette for maximum visual impact."
        ),
        "prompt_keywords": [
            "duotone",
            "two-color palette",
            "bold contrast",
            "graphic imagery",
            "color reduction",
            "striking simplicity",
            "halftone effect",
            "visual impact",
        ],
        "best_industries": ["tech", "fashion", "sport"],
        "mood": "bold and graphic",
    },
    {
        "key": "split_tone",
        "name": "Split Tone",
        "description": (
            "Split-toned photography with different color casts in highlights "
            "and shadows. Creates sophisticated color harmony, often pairing "
            "warm highlights with cool shadows."
        ),
        "prompt_keywords": [
            "split tone",
            "warm highlights",
            "cool shadows",
            "color harmony",
            "toned photography",
            "complementary cast",
            "sophisticated grade",
            "dual tone",
        ],
        "best_industries": ["fashion", "travel", "beauty"],
        "mood": "sophisticated and harmonious",
    },

    # -------------------------------------------------------------------------
    # Experimental & Digital Art
    # -------------------------------------------------------------------------
    {
        "key": "glitch_art",
        "name": "Glitch Art",
        "description": (
            "Digital glitch art photography with corrupted data, pixel "
            "distortion, and chromatic aberration. Embraces digital errors "
            "as an expressive aesthetic medium."
        ),
        "prompt_keywords": [
            "glitch art",
            "pixel distortion",
            "data corruption",
            "chromatic aberration",
            "digital error",
            "RGB shift",
            "scan line",
            "broken digital",
        ],
        "best_industries": ["tech", "fashion", "beauty"],
        "mood": "disruptive and digital",
    },
    {
        "key": "holographic",
        "name": "Holographic",
        "description": (
            "Holographic photography with iridescent rainbow reflections, "
            "chrome surfaces, and spectral light play. Futuristic and "
            "eye-catching with shifting prismatic color."
        ),
        "prompt_keywords": [
            "holographic",
            "iridescent rainbow",
            "chrome surface",
            "spectral light",
            "prismatic color",
            "futuristic shimmer",
            "metallic sheen",
            "shifting spectrum",
        ],
        "best_industries": ["beauty", "fashion", "tech", "jewelry_watches"],
        "mood": "futuristic and iridescent",
    },
]


# ---------------------------------------------------------------------------
# Lookup dictionary: key -> style dict
# ---------------------------------------------------------------------------
STYLE_BY_KEY = {s["key"]: s for s in PHOTOGRAPHY_STYLES}
