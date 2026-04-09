"""
55+ professional lighting configurations for AI advertising prompt enrichment.

Each setup maps a unique key to a dict with:
  - name: human-readable name
  - prompt: exact prompt text that produces this lighting in Gemini / SDXL
  - mood: emotional quality
  - color_temperature: approximate Kelvin or descriptor
  - best_for: list of industries / scene types where this excels

Keys are referenced by ad_patterns/*.py lighting_preferences lists.
"""

LIGHTING_SETUPS = {
    # ──────────────────────────────────────────────────────────────────
    # Classic Portrait Lighting (6)
    # ──────────────────────────────────────────────────────────────────
    "rembrandt": {
        "name": "Rembrandt Lighting",
        "prompt": "Rembrandt lighting, triangular highlight on shadow cheek, 45-degree key light, dramatic chiaroscuro portrait, painterly quality",
        "mood": "dramatic, classic, painterly",
        "color_temperature": "5600K neutral to warm",
        "best_for": ["portrait", "editorial", "luxury", "fragrance"],
    },
    "butterfly": {
        "name": "Butterfly / Paramount Lighting",
        "prompt": "butterfly lighting, key light directly above and in front of subject, symmetrical shadow under nose, glamorous Hollywood portrait",
        "mood": "glamorous, symmetrical, beauty",
        "color_temperature": "5600K neutral",
        "best_for": ["beauty", "portrait", "fashion", "fragrance"],
    },
    "split": {
        "name": "Split Lighting",
        "prompt": "split lighting, exactly half of face illuminated, half in deep shadow, dramatic 90-degree side light",
        "mood": "dramatic, mysterious, edgy",
        "color_temperature": "5600K neutral",
        "best_for": ["editorial", "fragrance", "fashion", "sport"],
    },
    "loop": {
        "name": "Loop Lighting",
        "prompt": "loop lighting, key light 30-45 degrees to side and slightly above, small nose shadow angled downward, flattering portrait light",
        "mood": "flattering, versatile, natural",
        "color_temperature": "5600K neutral",
        "best_for": ["portrait", "lifestyle", "commercial", "beauty"],
    },
    "broad": {
        "name": "Broad Lighting",
        "prompt": "broad lighting, lit side of face turned toward camera, open inviting feel, wider facial appearance",
        "mood": "approachable, flattering, warm",
        "color_temperature": "5600K neutral",
        "best_for": ["beauty", "lifestyle", "portrait", "commercial"],
    },
    "short": {
        "name": "Short Lighting",
        "prompt": "short lighting, shadow side of face toward camera, sculpted slimming effect, dramatic editorial portrait",
        "mood": "dramatic, sculpting, editorial",
        "color_temperature": "5600K neutral",
        "best_for": ["editorial", "portrait", "luxury", "fashion"],
    },

    # ──────────────────────────────────────────────────────────────────
    # Accent & Separation Lights (3)
    # ──────────────────────────────────────────────────────────────────
    "rim_light": {
        "name": "Rim / Edge Light",
        "prompt": "rim light separating subject from background, bright edge highlight, dramatic halo outline, backlit edge definition",
        "mood": "dramatic, defining, premium",
        "color_temperature": "5600K or gelled",
        "best_for": ["automotive", "product", "sport", "fashion", "fragrance"],
    },
    "hair_light": {
        "name": "Hair Light",
        "prompt": "dedicated hair light from above-behind, luminous hair highlight, separation from background, editorial polish",
        "mood": "polished, editorial, dimensional",
        "color_temperature": "5600K neutral",
        "best_for": ["beauty", "fashion", "portrait", "luxury"],
    },
    "kicker": {
        "name": "Kicker Light",
        "prompt": "kicker accent light from behind at 45 degrees, subtle rim on one side, dimensional separation, cinematic depth",
        "mood": "cinematic, dimensional, subtle drama",
        "color_temperature": "5600K or warm",
        "best_for": ["portrait", "editorial", "fashion", "luxury"],
    },

    # ──────────────────────────────────────────────────────────────────
    # Studio Beauty & Product Setups (7)
    # ──────────────────────────────────────────────────────────────────
    "beauty_dish": {
        "name": "Beauty Dish",
        "prompt": "beauty dish lighting, focused yet soft circular light, slight shadow falloff, contrasty beauty editorial, crisp skin texture",
        "mood": "editorial beauty, controlled, precise",
        "color_temperature": "5600K neutral",
        "best_for": ["beauty", "fashion", "portrait", "cosmetics"],
    },
    "ring_light": {
        "name": "Ring Light",
        "prompt": "ring light illumination, perfectly even flat lighting, distinctive ring-shaped catchlights in eyes, social media beauty aesthetic",
        "mood": "modern, even, social media",
        "color_temperature": "5500K daylight",
        "best_for": ["beauty", "fashion", "social", "cosmetics"],
    },
    "clamshell": {
        "name": "Clamshell Lighting",
        "prompt": "clamshell lighting, key light above and fill reflector below chin, minimal shadows, luminous beauty lighting, even skin illumination",
        "mood": "clean, beauty, luminous",
        "color_temperature": "5600K neutral",
        "best_for": ["beauty", "cosmetics", "portrait", "jewelry"],
    },
    "three_point": {
        "name": "Three-Point Lighting",
        "prompt": "classic three-point lighting setup, key light, fill light, backlight separation, broadcast quality, professional studio",
        "mood": "professional, balanced, broadcast",
        "color_temperature": "5600K neutral",
        "best_for": ["commercial", "portrait", "product", "interview"],
    },
    "high_key": {
        "name": "High Key",
        "prompt": "high key lighting, bright white background, minimal shadows, even illumination, clean airy feel, overexposed background",
        "mood": "bright, clean, optimistic, commercial",
        "color_temperature": "5600K-6500K daylight",
        "best_for": ["beauty", "tech", "commercial", "e-commerce", "fashion"],
    },
    "low_key": {
        "name": "Low Key",
        "prompt": "low key dramatic lighting, predominantly dark frame, selective illumination on subject, deep shadows, noir atmosphere",
        "mood": "dramatic, moody, cinematic, mysterious",
        "color_temperature": "variable",
        "best_for": ["luxury", "fragrance", "automotive", "jewelry", "editorial"],
    },
    "strobe_flash": {
        "name": "Strobe / Flash Freeze",
        "prompt": "strobe flash freeze, sharp frozen motion, crisp highlight, studio flash pop, high-speed sync, action frozen in time",
        "mood": "energetic, sharp, dynamic",
        "color_temperature": "5500K daylight",
        "best_for": ["sport", "fashion", "beauty", "action"],
    },

    # ──────────────────────────────────────────────────────────────────
    # Natural Light (8)
    # ──────────────────────────────────────────────────────────────────
    "golden_hour": {
        "name": "Golden Hour",
        "prompt": "golden hour sunlight, warm directional 3200-4500K amber glow, long dramatic shadows, magic hour, cinematic warmth",
        "mood": "warm, romantic, cinematic",
        "color_temperature": "3200-4500K warm",
        "best_for": ["fashion", "travel", "lifestyle", "fragrance", "real_estate"],
    },
    "blue_hour": {
        "name": "Blue Hour",
        "prompt": "blue hour twilight, cool ambient 7000-10000K, transitional sky gradient, city lights emerging, atmospheric depth",
        "mood": "cool, urban, sophisticated, melancholic",
        "color_temperature": "7000-10000K cool blue",
        "best_for": ["automotive", "real_estate", "luxury", "tech", "travel"],
    },
    "overcast_diffused": {
        "name": "Overcast Diffused Daylight",
        "prompt": "overcast sky diffused natural light, soft even illumination, no harsh shadows, neutral white balance, flattering portrait light",
        "mood": "soft, neutral, flattering, gentle",
        "color_temperature": "6500K daylight neutral",
        "best_for": ["fashion", "portrait", "beauty", "lifestyle", "food_beverage"],
    },
    "harsh_noon": {
        "name": "Harsh Noon Sun",
        "prompt": "direct overhead midday sun, hard shadows, high contrast, bright specular highlights, strong directional light",
        "mood": "bold, authentic, energetic, raw",
        "color_temperature": "5500K neutral daylight",
        "best_for": ["sport", "travel", "streetwear", "fashion"],
    },
    "window_light_soft": {
        "name": "Window Light (Soft)",
        "prompt": "soft diffused window light, gentle directional illumination, gradient shadow falloff, interior warmth, Vermeer quality",
        "mood": "intimate, natural, warm, peaceful",
        "color_temperature": "5000-5500K natural",
        "best_for": ["portrait", "food_beverage", "lifestyle", "real_estate", "beauty"],
    },
    "window_light_dramatic": {
        "name": "Window Light (Dramatic)",
        "prompt": "dramatic single window light, strong directional beam, deep shadows opposite side, high contrast interior, cinematic window shaft",
        "mood": "dramatic, moody, cinematic, contemplative",
        "color_temperature": "5500K natural",
        "best_for": ["editorial", "luxury", "portrait", "fashion", "fragrance"],
    },
    "backlit": {
        "name": "Backlit / Contre-jour",
        "prompt": "backlit contre-jour, light source behind subject, glowing edges, lens flare, ethereal halo, translucent highlights",
        "mood": "ethereal, romantic, dreamy, transcendent",
        "color_temperature": "varies with source",
        "best_for": ["fashion", "beauty", "fragrance", "travel", "lifestyle"],
    },
    "dappled_light": {
        "name": "Dappled Light",
        "prompt": "dappled sunlight filtered through foliage, organic light-shadow pattern, natural bokeh, garden atmosphere",
        "mood": "natural, whimsical, organic, gentle",
        "color_temperature": "5000-5500K green-filtered",
        "best_for": ["fashion", "beauty", "travel", "lifestyle"],
    },

    # ──────────────────────────────────────────────────────────────────
    # Dramatic & Artistic (5)
    # ──────────────────────────────────────────────────────────────────
    "chiaroscuro": {
        "name": "Chiaroscuro",
        "prompt": "chiaroscuro dramatic lighting, extreme contrast between light and shadow, Caravaggio-inspired, painterly dramatic illumination",
        "mood": "dramatic, artistic, powerful, masterful",
        "color_temperature": "warm 4000-5000K",
        "best_for": ["luxury", "fragrance", "editorial", "jewelry", "fashion"],
    },
    "silhouette": {
        "name": "Silhouette",
        "prompt": "pure silhouette backlighting, subject as solid dark shape against bright background, dramatic outline, no facial detail",
        "mood": "dramatic, mysterious, powerful, graphic",
        "color_temperature": "varies with background",
        "best_for": ["sport", "fashion", "fragrance", "automotive", "travel"],
    },
    "neon_gel": {
        "name": "Neon / Color Gel Lighting",
        "prompt": "neon colored gel lighting, vivid pink and cyan split, urban night aesthetic, cyberpunk atmosphere, RGB LED color wash",
        "mood": "modern, urban, edgy, futuristic",
        "color_temperature": "mixed / colored",
        "best_for": ["fashion", "tech", "nightlife", "beauty", "sport"],
    },
    "cinematic_teal_orange": {
        "name": "Cinematic Teal & Orange",
        "prompt": "cinematic teal and orange color grading, complementary color contrast, Hollywood blockbuster look, warm skin cool shadows",
        "mood": "cinematic, dramatic, filmic, polished",
        "color_temperature": "mixed warm highlights / cool shadows",
        "best_for": ["automotive", "fashion", "travel", "sport", "luxury"],
    },
    "anamorphic_flare": {
        "name": "Anamorphic Lens Flare",
        "prompt": "anamorphic horizontal lens flare, blue streak across frame, cinematic bokeh ovals, widescreen atmosphere, J.J. Abrams style",
        "mood": "cinematic, epic, atmospheric, dreamlike",
        "color_temperature": "varies",
        "best_for": ["automotive", "luxury", "fashion", "travel", "fragrance"],
    },

    # ──────────────────────────────────────────────────────────────────
    # Product-Specific (6)
    # ──────────────────────────────────────────────────────────────────
    "product_dark_field": {
        "name": "Dark Field Product",
        "prompt": "dark field illumination, light from sides only on black background, gemstone fire and brilliance, edge-lit product, dramatic isolation",
        "mood": "precious, brilliant, luxurious, dramatic",
        "color_temperature": "5600K neutral",
        "best_for": ["jewelry", "watches", "glass", "fragrance", "luxury"],
    },
    "product_light_field": {
        "name": "Light Field / Gradient Product",
        "prompt": "smooth gradient background lighting, seamless tonal transition, clean modern product photography, floating product feel",
        "mood": "clean, modern, premium, commercial",
        "color_temperature": "5600K neutral white",
        "best_for": ["tech", "product", "beauty", "cosmetics", "e-commerce"],
    },
    "product_backlit_glow": {
        "name": "Product Backlit Glow",
        "prompt": "product backlit with luminous glow, translucent edges, halo of light behind product, dramatic product hero shot",
        "mood": "premium, ethereal, hero, aspirational",
        "color_temperature": "variable",
        "best_for": ["tech", "fragrance", "beauty", "luxury", "automotive"],
    },
    "tabletop_product": {
        "name": "Tabletop Product Setup",
        "prompt": "tabletop studio product lighting, controlled diffused overhead, fill cards, precise highlight placement, commercial product shot",
        "mood": "controlled, commercial, precise, clean",
        "color_temperature": "5600K daylight",
        "best_for": ["food_beverage", "product", "cosmetics", "jewelry", "tech"],
    },
    "reflective_surface": {
        "name": "Reflective Surface",
        "prompt": "product on reflective black surface, mirror reflection below, dramatic studio lighting, premium floating effect",
        "mood": "premium, sleek, high-end, sophisticated",
        "color_temperature": "5600K neutral",
        "best_for": ["tech", "automotive", "luxury", "jewelry", "fragrance"],
    },
    "raking_texture": {
        "name": "Raking / Texture Light",
        "prompt": "raking texture light at extreme angle, surface detail revealed, deep shadow in grooves, tactile quality visible, texture emphasis",
        "mood": "tactile, detailed, raw, honest",
        "color_temperature": "5600K neutral",
        "best_for": ["food_beverage", "luxury", "fashion", "jewelry", "real_estate"],
    },

    # ──────────────────────────────────────────────────────────────────
    # Atmospheric & Environmental (6)
    # ──────────────────────────────────────────────────────────────────
    "fog_haze": {
        "name": "Fog / Haze Atmosphere",
        "prompt": "atmospheric fog and haze, volumetric light beams, mysterious depth, layered atmosphere, god rays through mist",
        "mood": "mysterious, ethereal, moody, cinematic",
        "color_temperature": "varies",
        "best_for": ["fragrance", "fashion", "travel", "luxury", "automotive"],
    },
    "candle_firelight": {
        "name": "Candlelight / Firelight",
        "prompt": "warm candlelight illumination, flickering amber glow, intimate atmosphere, 2200-2700K, dancing shadows",
        "mood": "intimate, romantic, warm, cozy",
        "color_temperature": "2200-2700K very warm",
        "best_for": ["luxury", "fragrance", "food_beverage", "jewelry", "real_estate"],
    },
    "tungsten_warm": {
        "name": "Tungsten Warm Interior",
        "prompt": "tungsten warm interior lighting, 3200K amber-orange cast, incandescent warmth, cozy indoor atmosphere",
        "mood": "warm, cozy, nostalgic, homey",
        "color_temperature": "3200K tungsten",
        "best_for": ["real_estate", "food_beverage", "lifestyle", "luxury"],
    },
    "moonlight_cool": {
        "name": "Moonlight / Cool Blue Night",
        "prompt": "moonlight cool blue illumination, soft nocturnal glow, 8000-10000K blue cast, nighttime atmosphere, silvery quality",
        "mood": "mysterious, nocturnal, romantic, serene",
        "color_temperature": "8000-10000K cool blue",
        "best_for": ["fragrance", "luxury", "travel", "fashion", "automotive"],
    },
    "dust_particles": {
        "name": "Dust Particles in Light",
        "prompt": "visible dust particles floating in directional light beam, atmospheric depth, vintage atmosphere, textured air",
        "mood": "nostalgic, atmospheric, warm, vintage",
        "color_temperature": "warm 4000-5000K",
        "best_for": ["luxury", "fragrance", "heritage", "fashion"],
    },
    "underwater_caustics": {
        "name": "Underwater Caustics",
        "prompt": "underwater caustic light patterns, refracted rippling sunlight through water, aquatic dancing highlights, submerged atmosphere",
        "mood": "fresh, aquatic, surreal, otherworldly",
        "color_temperature": "blue-green tinted",
        "best_for": ["beauty", "fragrance", "travel", "fashion"],
    },

    # ──────────────────────────────────────────────────────────────────
    # Automotive & Specialized (3)
    # ──────────────────────────────────────────────────────────────────
    "automotive_studio": {
        "name": "Automotive Studio",
        "prompt": "automotive studio lighting, multiple strip lights defining body lines, gradient ceiling reflection, precision engineered illumination",
        "mood": "precision, engineering, premium, powerful",
        "color_temperature": "5600K neutral",
        "best_for": ["automotive"],
    },
    "spotlight_theatrical": {
        "name": "Theatrical Spotlight",
        "prompt": "focused theatrical spotlight, isolated pool of light on dark stage, dramatic subject isolation, performance lighting",
        "mood": "dramatic, focused, theatrical, isolated",
        "color_temperature": "3200-5600K variable",
        "best_for": ["fashion", "jewelry", "luxury", "fragrance", "sport"],
    },
    "practical_lights": {
        "name": "Practical In-Scene Lights",
        "prompt": "practical in-scene light sources visible, table lamps, neon signs, screen glow, motivated lighting, diegetic illumination",
        "mood": "authentic, cinematic, immersive, narrative",
        "color_temperature": "mixed multiple sources",
        "best_for": ["lifestyle", "real_estate", "fashion", "travel"],
    },

    # ──────────────────────────────────────────────────────────────────
    # Seasonal & Time (4)
    # ──────────────────────────────────────────────────────────────────
    "winter_cool": {
        "name": "Winter Cool Light",
        "prompt": "cool winter daylight, blue-white tone, crisp clear atmosphere, frost sparkle, clean northern light",
        "mood": "fresh, crisp, pristine, clean",
        "color_temperature": "7000-8000K cool",
        "best_for": ["fashion", "sport", "beauty", "luxury"],
    },
    "tropical_warm": {
        "name": "Tropical Warm",
        "prompt": "tropical warm saturated sunlight, vivid green foliage, turquoise reflections, paradise atmosphere, intense color",
        "mood": "warm, exotic, paradise, vibrant",
        "color_temperature": "5000-5500K warm neutral",
        "best_for": ["travel", "fashion", "beauty", "food_beverage"],
    },
    "autumn_warm": {
        "name": "Autumn Warm",
        "prompt": "warm autumn light, golden amber tones filtered through colored leaves, low-angle sun, cozy harvest atmosphere",
        "mood": "warm, nostalgic, cozy, rich",
        "color_temperature": "3500-4500K warm",
        "best_for": ["fashion", "food_beverage", "lifestyle", "luxury"],
    },
    "sunset_dramatic": {
        "name": "Dramatic Sunset",
        "prompt": "dramatic sunset backlighting, vivid orange pink and purple sky, deep warm tones, silhouette foreground, epic cinematic sky",
        "mood": "dramatic, romantic, epic, inspiring",
        "color_temperature": "2500-4000K warm to very warm",
        "best_for": ["travel", "fashion", "automotive", "sport", "fragrance"],
    },

    # ──────────────────────────────────────────────────────────────────
    # Modern & Technical (4)
    # ──────────────────────────────────────────────────────────────────
    "led_panel": {
        "name": "LED Panel Array",
        "prompt": "modern LED panel lighting, precise color control, clean even illumination, digital color accuracy",
        "mood": "modern, precise, controlled, clean",
        "color_temperature": "variable / tunable",
        "best_for": ["tech", "beauty", "product", "commercial"],
    },
    "mixed_color_temp": {
        "name": "Mixed Color Temperature",
        "prompt": "mixed color temperature lighting, warm and cool sources competing, visual tension, cinematic color contrast",
        "mood": "cinematic, tension, dynamic, complex",
        "color_temperature": "mixed warm + cool",
        "best_for": ["fashion", "editorial", "automotive", "fragrance"],
    },
    "softbox_key": {
        "name": "Large Softbox Key",
        "prompt": "large softbox key light, soft wraparound illumination, gentle shadow gradients, professional studio quality",
        "mood": "clean, professional, controlled",
        "color_temperature": "5600K daylight",
        "best_for": ["product", "portrait", "commercial", "beauty"],
    },
    "strip_lights": {
        "name": "Strip Lights",
        "prompt": "strip light rim lighting, narrow vertical highlights defining edges, dramatic product edge definition, specular accents",
        "mood": "dramatic, defining, premium, technical",
        "color_temperature": "5600K neutral",
        "best_for": ["product", "automotive", "tech", "luxury"],
    },

    # ──────────────────────────────────────────────────────────────────
    # Additional Specialized (5)
    # ──────────────────────────────────────────────────────────────────
    "cathedral_light": {
        "name": "Cathedral / Grand Window",
        "prompt": "cathedral window light, dramatic directional beams through tall windows, sacred grand atmosphere, dust motes in shafts",
        "mood": "grand, reverent, timeless, awe-inspiring",
        "color_temperature": "5000-5500K neutral warm",
        "best_for": ["luxury", "jewelry", "fragrance", "real_estate"],
    },
    "noir_venetian": {
        "name": "Film Noir / Venetian Blind",
        "prompt": "film noir lighting, venetian blind shadow stripes across face, high contrast hard light, detective mystery atmosphere",
        "mood": "mysterious, cinematic, dangerous, dramatic",
        "color_temperature": "neutral to cool",
        "best_for": ["fragrance", "fashion", "editorial", "luxury"],
    },
    "dawn_first_light": {
        "name": "Dawn First Light",
        "prompt": "first light of dawn, pink and lavender horizon glow, soft diffused pre-sunrise, quiet stillness, awakening atmosphere",
        "mood": "hopeful, fresh, quiet, new beginning",
        "color_temperature": "4000-5500K pink-neutral",
        "best_for": ["travel", "beauty", "lifestyle", "sport", "fragrance"],
    },
    "museum_gallery": {
        "name": "Museum / Gallery Track",
        "prompt": "precise museum gallery track lighting, controlled focused spots, curated illumination, art exhibition atmosphere",
        "mood": "precise, refined, curated, intellectual",
        "color_temperature": "4000K warm white",
        "best_for": ["luxury", "jewelry", "art", "fashion"],
    },
    "industrial_loft": {
        "name": "Industrial Loft",
        "prompt": "industrial loft natural light, large factory windows, raw concrete surfaces, warm afternoon sun, exposed brick",
        "mood": "urban, authentic, creative, raw",
        "color_temperature": "5000-5500K natural warm",
        "best_for": ["fashion", "lifestyle", "real_estate", "food_beverage"],
    },
}

# Convenience lookup — same dict, just documenting the pattern
LIGHTING_BY_NAME = LIGHTING_SETUPS
