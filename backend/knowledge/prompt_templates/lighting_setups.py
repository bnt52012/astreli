"""
Lighting Setups Knowledge Base
===============================
Comprehensive mapping of professional photography and cinematography lighting setups
to prompt-enrichment data. Each entry provides description, prompt keywords, mood, and best use cases.
"""

LIGHTING_SETUPS: dict[str, dict] = {
    # ──────────────────────────────────────────────
    # CLASSIC PORTRAIT LIGHTING PATTERNS
    # ──────────────────────────────────────────────
    "rembrandt": {
        "description": "Named after the Dutch painter. Key light at 45 degrees above and to the side creates a triangle of light on the shadow-side cheek. Dramatic yet flattering for most face shapes.",
        "prompt_keywords": ["Rembrandt lighting", "triangle cheek highlight", "45-degree key light", "classic portrait lighting", "chiaroscuro face"],
        "mood": "dramatic, painterly, classic",
        "best_for": ["portraits", "editorial", "fine art", "dramatic headshots"],
    },
    "butterfly_paramount": {
        "description": "Key light centered directly above and in front of the subject creates a butterfly-shaped shadow under the nose. Glamorous lighting popularized by Hollywood's golden age.",
        "prompt_keywords": ["butterfly lighting", "paramount lighting", "centered overhead key", "butterfly shadow under nose", "Hollywood glamour lighting"],
        "mood": "glamorous, classic Hollywood, flattering",
        "best_for": ["beauty", "glamour portraits", "fashion", "cosmetics advertising"],
    },
    "split": {
        "description": "Key light at 90 degrees to the subject, illuminating exactly half the face while the other half falls into shadow. Maximum drama and mystery.",
        "prompt_keywords": ["split lighting", "half-face illumination", "90-degree side light", "dramatic half shadow", "stark face division"],
        "mood": "dramatic, mysterious, bold",
        "best_for": ["dramatic portraits", "music industry", "film noir style", "character studies"],
    },
    "loop": {
        "description": "Key light slightly above and 30-45 degrees to the side creates a small loop-shaped shadow from the nose on the opposite cheek. Versatile and universally flattering.",
        "prompt_keywords": ["loop lighting", "small nose shadow loop", "30-degree key light", "versatile portrait light", "flattering face lighting"],
        "mood": "natural, flattering, approachable",
        "best_for": ["corporate portraits", "general portraiture", "headshots", "school photos"],
    },
    "broad": {
        "description": "The side of the face closest to camera is lit (broad side). Makes faces appear wider. Subject turned slightly away from light.",
        "prompt_keywords": ["broad lighting", "lit near side", "face-widening light", "broad side illumination"],
        "mood": "open, approachable, traditional",
        "best_for": ["thin faces needing fullness", "traditional portraits", "group shots"],
    },
    "short": {
        "description": "The side of the face away from camera is lit (short side), shadowing the side closest to camera. Slimming and sculpting effect.",
        "prompt_keywords": ["short lighting", "shadow near side", "sculpting face light", "slimming portrait lighting", "far-side illumination"],
        "mood": "sculpted, dramatic, slimming",
        "best_for": ["round faces needing definition", "dramatic portraits", "moody headshots"],
    },
    "clamshell": {
        "description": "Two lights stacked vertically - key light above and fill reflector/light below chin. Wraps face in even, flattering light with catchlights in eyes.",
        "prompt_keywords": ["clamshell lighting", "dual vertical lights", "above-below face wrap", "beauty clamshell", "even face illumination", "double catchlight"],
        "mood": "flattering, beauty, even",
        "best_for": ["beauty photography", "cosmetics", "headshots", "fashion close-ups"],
    },

    # ──────────────────────────────────────────────
    # ACCENT & RIM LIGHTING
    # ──────────────────────────────────────────────
    "rim_edge": {
        "description": "Light from behind the subject creating a bright outline or rim around the edge of the body/hair, separating subject from background.",
        "prompt_keywords": ["rim lighting", "edge light", "backlit rim", "luminous outline", "hair light separation", "glowing edge"],
        "mood": "ethereal, separated, defined",
        "best_for": ["portraits with dark backgrounds", "product photography", "fashion", "dramatic editorial"],
    },
    "backlight": {
        "description": "Primary light source behind the subject creating silhouettes or translucent glow effects. Often combined with fill from front.",
        "prompt_keywords": ["backlight", "backlighting", "behind-subject light", "translucent glow", "contre-jour", "backlit subject"],
        "mood": "ethereal, dramatic, atmospheric",
        "best_for": ["fashion", "lifestyle", "nature", "romantic portraits", "golden hour simulation"],
    },
    "kicker": {
        "description": "Accent light placed behind and to the side of the subject, adding a bright accent along the jaw, cheek, or shoulder for depth.",
        "prompt_keywords": ["kicker light", "accent side light", "jaw accent", "shoulder highlight", "depth separation light"],
        "mood": "dimensional, dramatic, refined",
        "best_for": ["cinematic portraits", "product highlights", "editorial", "corporate headshots"],
    },
    "hair_light": {
        "description": "Dedicated overhead or behind light illuminating the hair to create separation from background and show texture and shine.",
        "prompt_keywords": ["hair light", "overhead hair illumination", "hair shine highlight", "hair texture light", "top separation light"],
        "mood": "polished, dimensional, glamorous",
        "best_for": ["beauty", "hair product advertising", "fashion", "portrait"],
    },

    # ──────────────────────────────────────────────
    # NATURAL LIGHT
    # ──────────────────────────────────────────────
    "golden_hour": {
        "description": "Natural sunlight during the hour after sunrise or before sunset. Warm, directional, low-angle light with long shadows and golden tones.",
        "prompt_keywords": ["golden hour light", "warm sunset glow", "low-angle sun", "golden warm tones", "magic hour", "long warm shadows"],
        "mood": "warm, romantic, magical",
        "best_for": ["lifestyle", "portraits", "wedding", "landscape", "fashion on-location"],
    },
    "blue_hour": {
        "description": "Natural light during civil twilight (20-30 min after sunset). Cool blue ambient light with residual warm horizon glow.",
        "prompt_keywords": ["blue hour light", "civil twilight", "cool blue ambient", "twilight glow", "pre-dawn blue", "post-sunset blue"],
        "mood": "serene, contemplative, cool",
        "best_for": ["architecture", "cityscape", "moody portraits", "luxury real estate"],
    },
    "overcast_soft": {
        "description": "Diffused natural light through cloud cover acting as giant softbox. Even, wrap-around illumination with soft shadows.",
        "prompt_keywords": ["overcast natural light", "diffused cloud light", "soft even illumination", "cloud softbox", "wrap-around daylight"],
        "mood": "soft, even, gentle",
        "best_for": ["portraits", "product outdoors", "fashion", "garden photography"],
    },
    "hard_noon_sun": {
        "description": "Direct overhead midday sunlight creating harsh shadows, high contrast, and intense highlights. Challenging but creates bold graphic looks.",
        "prompt_keywords": ["harsh noon sun", "hard overhead sunlight", "sharp shadows", "high contrast midday", "direct sun"],
        "mood": "bold, harsh, graphic",
        "best_for": ["fashion editorial", "street photography", "graphic bold looks", "swimwear"],
    },
    "open_shade": {
        "description": "Subject in shade while background may be sunlit. Creates even, cool-toned light from reflected sky without direct sun.",
        "prompt_keywords": ["open shade lighting", "shaded even light", "reflected sky light", "no direct sun", "cool shade"],
        "mood": "even, cool, natural",
        "best_for": ["portraits", "weddings", "outdoor events", "casual lifestyle"],
    },
    "dappled_light": {
        "description": "Sunlight filtered through leaves or perforated surfaces creating patterns of light and shadow on the subject.",
        "prompt_keywords": ["dappled light", "filtered sunlight through leaves", "light pattern on face", "tree shadow pattern", "broken light"],
        "mood": "natural, artistic, organic",
        "best_for": ["nature portraits", "bohemian fashion", "fine art", "romantic editorial"],
    },
    "window_light": {
        "description": "Natural light through a window creating soft directional illumination with gentle falloff. The most accessible beautiful light source.",
        "prompt_keywords": ["window light", "natural window illumination", "soft directional daylight", "gentle light falloff", "side window glow"],
        "mood": "intimate, natural, soft",
        "best_for": ["portraits", "still life", "interior", "food photography", "boudoir"],
    },
    "window_light_sheer": {
        "description": "Window light further diffused through sheer curtains for ultra-soft, ethereal illumination with minimal shadows.",
        "prompt_keywords": ["sheer curtain window light", "ultra-soft diffused daylight", "ethereal window glow", "curtain-filtered light"],
        "mood": "ethereal, dreamy, ultra-soft",
        "best_for": ["boudoir", "newborn", "fine art portrait", "beauty"],
    },

    # ──────────────────────────────────────────────
    # STUDIO LIGHTING MODIFIERS
    # ──────────────────────────────────────────────
    "beauty_dish": {
        "description": "Parabolic dish reflector creating focused yet slightly soft light with characteristic hot center and rapid falloff. The beauty photographer's workhorse.",
        "prompt_keywords": ["beauty dish lighting", "focused parabolic light", "hot center soft edge", "beauty dish catchlight", "rapid light falloff"],
        "mood": "focused beauty, punchy, glamorous",
        "best_for": ["beauty", "fashion", "headshots", "cosmetics"],
    },
    "ring_light": {
        "description": "Circular light surrounding the lens creating even, shadowless face illumination with distinctive circular catchlights in eyes.",
        "prompt_keywords": ["ring light", "circular catchlight", "shadowless face light", "even ring illumination", "circular eye reflection"],
        "mood": "even, modern, social media",
        "best_for": ["beauty", "social media content", "makeup tutorials", "fashion close-ups"],
    },
    "softbox_large": {
        "description": "Large softbox (4x6 ft or larger) creating broad, soft, wrap-around illumination mimicking a large window. Forgiving and versatile.",
        "prompt_keywords": ["large softbox lighting", "broad soft illumination", "wrap-around studio light", "window-like studio light", "soft even studio"],
        "mood": "soft, professional, versatile",
        "best_for": ["portraits", "product", "fashion", "corporate", "food"],
    },
    "softbox_small": {
        "description": "Small softbox creating more directional, slightly harder light with quicker falloff. More contrast than large softbox.",
        "prompt_keywords": ["small softbox lighting", "directional soft light", "controlled soft illumination", "focused softbox"],
        "mood": "directional, controlled, moderate contrast",
        "best_for": ["product details", "headshots", "controlled accent"],
    },
    "strip_light": {
        "description": "Narrow rectangular softbox creating thin, elongated highlights ideal for rim lighting, product reflections, and body contouring.",
        "prompt_keywords": ["strip light", "narrow highlight", "elongated reflection", "thin light strip", "body contour light", "product reflection strip"],
        "mood": "sleek, contoured, refined",
        "best_for": ["product photography", "automotive", "body/fitness", "beverages", "fashion"],
    },
    "octabox": {
        "description": "Octagonal softbox creating round, natural-looking catchlights and soft even light. Popular for portraits and beauty.",
        "prompt_keywords": ["octabox lighting", "octagonal soft light", "round catchlight", "natural portrait light", "octagonal softbox"],
        "mood": "natural, soft, portrait-friendly",
        "best_for": ["portraits", "beauty", "headshots", "fashion"],
    },
    "fresnel_spot": {
        "description": "Hard, focused beam of light with adjustable spread. Cinematic look with defined edges and theatrical quality.",
        "prompt_keywords": ["Fresnel spot light", "focused beam", "theatrical lighting", "hard focused spot", "cinematic spot", "defined light edge"],
        "mood": "theatrical, cinematic, focused",
        "best_for": ["cinematic portraits", "theater", "product hero shots", "dramatic editorial"],
    },
    "umbrella_shoot_through": {
        "description": "Light fired through translucent umbrella for broad, soft, slightly wraparound illumination. Quick and affordable soft light.",
        "prompt_keywords": ["shoot-through umbrella light", "broad soft umbrella", "translucent umbrella diffusion", "wrap-around umbrella light"],
        "mood": "soft, broad, natural",
        "best_for": ["group portraits", "events", "on-location work", "family photos"],
    },
    "umbrella_reflective": {
        "description": "Light bounced into silver or white reflective umbrella for broad, efficient illumination with more punch than shoot-through.",
        "prompt_keywords": ["reflective umbrella light", "bounced umbrella", "silver umbrella highlight", "punchy umbrella light"],
        "mood": "bright, efficient, punchy",
        "best_for": ["events", "group shots", "corporate", "on-location portraits"],
    },
    "grid_spot": {
        "description": "Honeycomb grid attached to light modifier restricting spill for precise, controlled light placement without affecting surroundings.",
        "prompt_keywords": ["grid spot lighting", "honeycomb grid", "controlled light spill", "precise light placement", "no-spill spotlight"],
        "mood": "controlled, precise, dramatic",
        "best_for": ["product photography", "hair light", "accent lighting", "dramatic portraits"],
    },
    "snoot": {
        "description": "Tube-shaped modifier creating very tight, focused beam of light for precise highlighting of small areas.",
        "prompt_keywords": ["snoot lighting", "tight focused beam", "precise spot light", "narrow tube light", "surgical light placement"],
        "mood": "precise, focused, dramatic",
        "best_for": ["jewelry", "product details", "hair highlights", "artistic accents"],
    },
    "barn_doors": {
        "description": "Hinged metal flaps on light source to shape and control light spread, blocking spill in specific directions.",
        "prompt_keywords": ["barn door lighting", "shaped light control", "directional light flags", "controlled light spread"],
        "mood": "controlled, theatrical, shaped",
        "best_for": ["studio product", "theatrical portraits", "controlled background lighting"],
    },

    # ──────────────────────────────────────────────
    # DRAMATIC & CREATIVE LIGHTING
    # ──────────────────────────────────────────────
    "chiaroscuro": {
        "description": "Strong contrast between light and dark inspired by Renaissance painting. Deep shadows with selective illumination creating volumetric drama.",
        "prompt_keywords": ["chiaroscuro lighting", "strong light-dark contrast", "Renaissance lighting", "deep shadow drama", "volumetric light and shadow"],
        "mood": "dramatic, painterly, classical",
        "best_for": ["fine art portraits", "still life", "luxury products", "editorial"],
    },
    "low_key": {
        "description": "Predominantly dark image with selective, dramatic lighting on key elements. Shadow-dominant with strategic highlights.",
        "prompt_keywords": ["low key lighting", "dark dominant", "selective dramatic highlights", "shadow-rich image", "moody darkness"],
        "mood": "moody, mysterious, dramatic",
        "best_for": ["luxury products", "spirits advertising", "dramatic portraits", "fine dining", "fragrance"],
    },
    "high_key": {
        "description": "Bright, even illumination minimizing shadows. Light-dominant with white or bright backgrounds and minimal contrast.",
        "prompt_keywords": ["high key lighting", "bright even illumination", "minimal shadows", "white background bright", "clean bright studio"],
        "mood": "bright, clean, optimistic",
        "best_for": ["beauty", "e-commerce", "baby photography", "healthcare", "skincare"],
    },
    "flat_even": {
        "description": "Completely even illumination from all angles eliminating all shadows. Used for documentation or deliberate stylistic choice.",
        "prompt_keywords": ["flat even lighting", "shadowless illumination", "all-angle even light", "no shadow flat light"],
        "mood": "clean, neutral, documentary",
        "best_for": ["e-commerce white background", "documentation", "forensic photography", "before-after"],
    },
    "cross_lighting": {
        "description": "Two lights at opposing angles (often 90/270 degrees) creating complex shadows and highlights with dimensional texture revelation.",
        "prompt_keywords": ["cross lighting", "opposing angle lights", "dual directional", "texture-revealing cross light", "dimensional cross illumination"],
        "mood": "textured, dimensional, complex",
        "best_for": ["texture photography", "product detail", "architectural detail", "male portraits"],
    },
    "under_lighting": {
        "description": "Light from below the subject creating unnatural, eerie shadows. Used sparingly for horror or dramatic effect.",
        "prompt_keywords": ["under lighting", "below face light", "upward shadow cast", "eerie bottom light", "horror lighting"],
        "mood": "eerie, unnatural, dramatic",
        "best_for": ["horror", "dramatic effect", "Halloween", "conceptual art"],
    },
    "silhouette_backlight": {
        "description": "Strong backlight with no fill, reducing subject to pure black outline against bright background for graphic impact.",
        "prompt_keywords": ["silhouette lighting", "pure backlight", "black outline", "graphic silhouette", "no fill backlit"],
        "mood": "graphic, mysterious, bold",
        "best_for": ["fitness", "dance", "fashion", "fine art", "editorial"],
    },
    "contre_jour": {
        "description": "Shooting into the light source with subject between camera and light, creating translucent edges and dreamy halos.",
        "prompt_keywords": ["contre-jour lighting", "shooting into light", "translucent edges", "dreamy light halo", "into-the-sun"],
        "mood": "dreamy, ethereal, romantic",
        "best_for": ["romantic portraits", "fashion", "nature", "wedding"],
    },

    # ──────────────────────────────────────────────
    # COLORED & CREATIVE LIGHTING
    # ──────────────────────────────────────────────
    "colored_gels": {
        "description": "Colored gel filters on lights creating vivid colored illumination for creative, fashion, and music industry applications.",
        "prompt_keywords": ["colored gel lighting", "vivid color light", "gel filter illumination", "creative colored light", "fashion color wash"],
        "mood": "creative, vibrant, editorial",
        "best_for": ["fashion editorial", "music industry", "creative portraits", "nightlife"],
    },
    "complementary_gels": {
        "description": "Two colored gels using complementary colors (e.g., orange/teal, magenta/green) on opposing lights for cinematic color contrast.",
        "prompt_keywords": ["complementary color gel lighting", "orange teal split", "dual color opposition", "cinematic color contrast", "split color lighting"],
        "mood": "cinematic, vivid, high-impact",
        "best_for": ["music videos", "fashion campaigns", "creative portraits", "poster imagery"],
    },
    "neon": {
        "description": "Neon tube or LED neon lighting casting vibrant colored ambient glow, popular for urban and nightlife aesthetics.",
        "prompt_keywords": ["neon lighting", "neon tube glow", "vibrant neon ambient", "neon sign light", "urban neon cast"],
        "mood": "urban, vibrant, nocturnal",
        "best_for": ["urban portraits", "nightlife", "streetwear", "music", "nightclub"],
    },
    "practical_lights": {
        "description": "Visible real-world light sources in frame (lamps, candles, string lights, neon signs) providing both illumination and visual interest.",
        "prompt_keywords": ["practical lighting", "visible light source in frame", "real-world lamp", "candle light in scene", "string lights"],
        "mood": "intimate, realistic, atmospheric",
        "best_for": ["interior scenes", "restaurant photography", "lifestyle", "film stills"],
    },
    "candlelight": {
        "description": "Warm, flickering candlelight creating intimate amber illumination with soft dancing shadows and romantic warmth.",
        "prompt_keywords": ["candlelight", "warm amber glow", "flickering light", "intimate candle illumination", "dancing shadow", "romantic warm light"],
        "mood": "intimate, romantic, warm",
        "best_for": ["romantic dining", "spa", "luxury lifestyle", "intimate portraits"],
    },
    "fire_light": {
        "description": "Illumination from fireplace or campfire with warm orange glow, dancing shadows, and primal atmospheric quality.",
        "prompt_keywords": ["firelight", "warm fire glow", "campfire illumination", "dancing fire shadow", "orange fire ambient"],
        "mood": "primal, warm, adventurous",
        "best_for": ["camping lifestyle", "winter scenes", "rustic settings", "intimate gatherings"],
    },

    # ──────────────────────────────────────────────
    # ATMOSPHERIC & VOLUMETRIC
    # ──────────────────────────────────────────────
    "volumetric_fog": {
        "description": "Light beams made visible through haze, fog, or smoke creating dramatic shafts of light and atmospheric depth.",
        "prompt_keywords": ["volumetric fog lighting", "visible light beams", "haze atmosphere", "god rays", "light shaft through fog", "atmospheric depth"],
        "mood": "atmospheric, dramatic, ethereal",
        "best_for": ["cinematic scenes", "concerts", "dramatic portraits", "forest scenes", "church interiors"],
    },
    "smoke_haze": {
        "description": "Theatrical haze or smoke softening and diffusing light throughout the scene, creating mood and visual depth between planes.",
        "prompt_keywords": ["smoke haze lighting", "theatrical haze", "diffused atmospheric light", "smoky ambiance", "depth haze"],
        "mood": "mysterious, moody, layered",
        "best_for": ["music performance", "fashion", "dramatic portrait", "product atmosphere"],
    },
    "dust_particles": {
        "description": "Backlit dust or particles floating in air creating magical, textured atmosphere with visible motes of light.",
        "prompt_keywords": ["backlit dust particles", "floating dust motes", "particle-filled light beam", "magical dust atmosphere", "sunlit particles"],
        "mood": "magical, textured, nostalgic",
        "best_for": ["fine art", "vintage scenes", "nostalgic imagery", "dance photography"],
    },

    # ──────────────────────────────────────────────
    # PRODUCT-SPECIFIC LIGHTING
    # ──────────────────────────────────────────────
    "light_tent": {
        "description": "Product surrounded by diffusion material creating completely soft, even illumination from all sides. Ideal for reflective objects.",
        "prompt_keywords": ["light tent product", "all-around diffusion", "even product illumination", "reflective object lighting", "product tent"],
        "mood": "clean, even, controlled",
        "best_for": ["jewelry", "watches", "chrome products", "glass products"],
    },
    "product_gradient": {
        "description": "Graduated background lighting creating smooth tonal gradient behind product, adding depth without distraction.",
        "prompt_keywords": ["gradient background lighting", "graduated product backdrop", "smooth tonal background", "product depth gradient"],
        "mood": "professional, depth, premium",
        "best_for": ["product photography", "catalog", "e-commerce premium", "tech products"],
    },
    "product_reflection": {
        "description": "Product placed on reflective surface (glass, acrylic) creating mirror reflection below for premium, luxurious presentation.",
        "prompt_keywords": ["product reflection surface", "mirror reflection below", "reflective surface product", "glass table reflection", "luxury product mirror"],
        "mood": "premium, luxurious, refined",
        "best_for": ["luxury products", "tech gadgets", "perfume", "jewelry", "automotive"],
    },
    "light_painting": {
        "description": "Long exposure with hand-held lights selectively painting illumination onto the subject, creating unique, sculptural lighting.",
        "prompt_keywords": ["light painting photography", "hand-painted light", "selective long exposure illumination", "sculptural light painting"],
        "mood": "artistic, unique, sculptural",
        "best_for": ["creative product", "automotive", "fine art", "experimental"],
    },

    # ──────────────────────────────────────────────
    # CINEMATIC LIGHTING STYLES
    # ──────────────────────────────────────────────
    "three_point": {
        "description": "Classic three-point lighting: key light (main), fill light (shadow reduction), and back light (separation). The foundation of professional lighting.",
        "prompt_keywords": ["three-point lighting", "key fill back light", "classic studio setup", "professional three-light", "balanced lighting setup"],
        "mood": "professional, balanced, dimensional",
        "best_for": ["interviews", "corporate video", "product", "standard portraits"],
    },
    "motivated_lighting": {
        "description": "Lighting that appears to come from a logical source within the scene (window, lamp, TV glow) for narrative believability.",
        "prompt_keywords": ["motivated lighting", "source-justified light", "narrative lighting", "realistic scene illumination", "story-driven light"],
        "mood": "realistic, narrative, natural",
        "best_for": ["cinematic scenes", "interior lifestyle", "narrative photography", "film production stills"],
    },
    "available_light": {
        "description": "Using only existing ambient light in a scene without adding artificial sources. Authentic and documentary in character.",
        "prompt_keywords": ["available light only", "natural ambient", "no artificial light", "existing light source", "documentary lighting"],
        "mood": "authentic, documentary, natural",
        "best_for": ["documentary", "street photography", "photojournalism", "candid"],
    },
    "bounce_light": {
        "description": "Light bounced off reflective surfaces (walls, ceilings, reflectors) for soft, indirect illumination without harsh direct light.",
        "prompt_keywords": ["bounced light", "reflected illumination", "ceiling bounce", "indirect soft light", "wall bounce light"],
        "mood": "soft, natural, indirect",
        "best_for": ["events", "interiors", "casual portraits", "real estate"],
    },
    "butterfly_with_reflector": {
        "description": "Butterfly/paramount lighting from above with V-flat or reflector below to fill neck shadows and add lower catchlight.",
        "prompt_keywords": ["butterfly plus reflector", "paramount with fill", "above-below beauty light", "glamour fill lighting"],
        "mood": "glamorous, polished, beauty-focused",
        "best_for": ["beauty close-ups", "cosmetics", "skincare advertising", "magazine covers"],
    },
    "cove_lighting": {
        "description": "Indirect lighting built into architectural elements (ceiling coves, floor channels) creating soft ambient glow for interior photography.",
        "prompt_keywords": ["cove lighting", "architectural indirect light", "ceiling cove glow", "ambient architectural illumination"],
        "mood": "ambient, architectural, modern",
        "best_for": ["interior architecture", "luxury real estate", "hospitality", "retail spaces"],
    },
    "gobo_pattern": {
        "description": "Patterned mask (gobo) placed before light creating shaped shadows - window frames, foliage, geometric patterns - on subject or background.",
        "prompt_keywords": ["gobo pattern lighting", "shadow pattern projection", "window shadow gobo", "patterned light projection", "leaf shadow gobo"],
        "mood": "artistic, atmospheric, patterned",
        "best_for": ["fashion editorial", "creative portraits", "cinematic scenes", "atmospheric sets"],
    },
    "top_light_overhead": {
        "description": "Single overhead light creating dramatic shadows under brow, nose, and chin. Used in cinema for intensity and vulnerability.",
        "prompt_keywords": ["overhead top light", "dramatic brow shadow", "overhead single source", "top-down illumination", "cinema overhead light"],
        "mood": "intense, vulnerable, dramatic",
        "best_for": ["cinematic portraits", "dramatic scenes", "interrogation-style", "artistic"],
    },
    "bi_color_warm_cool": {
        "description": "Two lights at different color temperatures - warm (tungsten) and cool (daylight) - creating natural-looking mixed color temperature scenes.",
        "prompt_keywords": ["bi-color lighting", "warm cool split", "mixed color temperature", "tungsten daylight mix", "warm cool contrast"],
        "mood": "natural, complex, cinematic",
        "best_for": ["interior scenes", "cinematic photography", "night scenes", "restaurant"],
    },
    "LED_panel": {
        "description": "Modern LED panel providing adjustable color temperature and intensity in a thin, portable form factor for versatile on-location work.",
        "prompt_keywords": ["LED panel lighting", "adjustable color temperature", "portable studio light", "modern LED illumination"],
        "mood": "versatile, modern, adjustable",
        "best_for": ["on-location", "video interviews", "product photography", "behind-the-scenes"],
    },
    "projected_pattern": {
        "description": "Light projected through patterned materials (lace, mesh, blinds) creating textured light and shadow on the subject.",
        "prompt_keywords": ["projected pattern light", "lace shadow projection", "mesh light pattern", "textured shadow overlay", "venetian blind light"],
        "mood": "artistic, textured, mysterious",
        "best_for": ["fashion editorial", "fine art", "boudoir", "creative portraits"],
    },
}
