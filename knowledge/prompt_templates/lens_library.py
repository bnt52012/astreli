"""
Lens Library — comprehensive catalog of photographic lens types for AI image generation.

Each entry contains optical characteristics, descriptive metadata, and exact prompt
keywords tuned to make Gemini / SDXL faithfully replicate the visual signature of
the lens.  Pure Python data — no imports, no side-effects.
"""

LENS_LIBRARY = [
    # ─────────────────────────────────────────────────────────────────────
    # FISHEYE
    # ─────────────────────────────────────────────────────────────────────
    {
        "key": "fisheye_8mm",
        "focal_length": "8mm",
        "aperture": "f/3.5",
        "name": "8mm Fisheye",
        "description": (
            "Extreme barrel distortion with a 180-degree field of view. "
            "Bends straight lines into curves, creating a surreal, immersive globe effect."
        ),
        "prompt_keywords": [
            "8mm fisheye lens",
            "extreme barrel distortion",
            "180-degree field of view",
            "spherical perspective warp",
            "curved horizon line",
            "ultra-wide immersive",
            "rectilinear distortion",
            "deep depth of field",
        ],
        "best_for": ["action sports", "skateboarding", "creative portraits", "real estate interior"],
        "typical_use": "Skateboard videos, extreme-sport POV, creative editorial work",
        "depth_of_field_effect": "Nearly everything in focus due to extreme wide angle; background and foreground both sharp.",
    },

    # ─────────────────────────────────────────────────────────────────────
    # ULTRA-WIDE PRIMES
    # ─────────────────────────────────────────────────────────────────────
    {
        "key": "ultra_wide_14mm",
        "focal_length": "14mm",
        "aperture": "f/2.8",
        "name": "14mm Ultra-Wide",
        "description": (
            "Dramatic perspective distortion that exaggerates foreground elements and "
            "makes architecture soar. Ideal for sweeping landscapes and astrophotography."
        ),
        "prompt_keywords": [
            "14mm ultra-wide angle lens",
            "dramatic perspective distortion",
            "expansive field of view",
            "architectural grandeur",
            "converging vertical lines",
            "deep depth of field",
            "foreground emphasis",
            "starscape wide-field",
        ],
        "best_for": ["architecture", "landscape", "astrophotography", "interior design"],
        "typical_use": "Real-estate interiors, Milky Way photography, dramatic environmental shots",
        "depth_of_field_effect": "Extremely deep — virtually everything from inches to infinity is in focus.",
    },
    {
        "key": "ultra_wide_16mm",
        "focal_length": "16mm",
        "aperture": "f/2.8",
        "name": "16mm Ultra-Wide",
        "description": (
            "Slightly tighter than 14mm but still dramatically wide. Strong foreground-to-"
            "background depth and pronounced leading lines."
        ),
        "prompt_keywords": [
            "16mm ultra-wide lens",
            "dramatic perspective",
            "foreground emphasis",
            "immersive viewpoint",
            "strong leading lines",
            "expansive composition",
            "deep focus throughout",
        ],
        "best_for": ["landscape", "documentary", "sport action", "interior"],
        "typical_use": "Environmental storytelling, sports arena establishing shots, vast landscapes",
        "depth_of_field_effect": "Very deep depth of field; minor vignetting at wide apertures.",
    },

    # ─────────────────────────────────────────────────────────────────────
    # WIDE-ANGLE PRIMES
    # ─────────────────────────────────────────────────────────────────────
    {
        "key": "wide_20mm",
        "focal_length": "20mm",
        "aperture": "f/1.8",
        "name": "20mm Wide-Angle",
        "description": (
            "Wide enough for environmental context while keeping distortion manageable. "
            "Great for photojournalism and environmental portraits."
        ),
        "prompt_keywords": [
            "20mm wide angle lens",
            "environmental context",
            "leading lines",
            "wide perspective",
            "moderate wide-angle distortion",
            "contextual framing",
            "deep focus",
        ],
        "best_for": ["landscape", "street photography", "environmental portrait", "photojournalism"],
        "typical_use": "Environmental storytelling with moderate spatial exaggeration",
        "depth_of_field_effect": "Deep focus at most apertures; noticeable but controlled bokeh wide open.",
    },
    {
        "key": "wide_24mm",
        "focal_length": "24mm",
        "aperture": "f/1.4",
        "name": "24mm Wide",
        "description": (
            "A versatile wide angle that balances context with subject emphasis. "
            "Opens up at f/1.4 for environmental bokeh rarely seen at this focal length."
        ),
        "prompt_keywords": [
            "24mm wide angle lens",
            "f/1.4 shallow depth of field",
            "environmental bokeh",
            "wide perspective",
            "moderate barrel distortion",
            "storytelling composition",
            "contextual background blur",
        ],
        "best_for": ["documentary", "fashion editorial", "lifestyle", "wedding"],
        "typical_use": "Wedding venue establishing shots, fashion location work, documentary features",
        "depth_of_field_effect": "Stopped down: deep focus. Wide open at f/1.4: surprising background separation with wide context.",
    },
    {
        "key": "wide_28mm",
        "focal_length": "28mm",
        "aperture": "f/2.0",
        "name": "28mm Classic Reportage",
        "description": (
            "The classic street and reportage focal length. Natural enough for candid work "
            "yet wide enough to capture scenes in tight spaces."
        ),
        "prompt_keywords": [
            "28mm wide angle lens",
            "classic reportage perspective",
            "environmental storytelling",
            "street photography composition",
            "natural spatial relationship",
            "photojournalistic framing",
            "moderate depth of field",
        ],
        "best_for": ["street photography", "documentary", "lifestyle", "travel"],
        "typical_use": "Candid street photography, travel documentation, reportage",
        "depth_of_field_effect": "Moderate depth of field; at f/2 some background softening but strong contextual detail.",
    },

    # ─────────────────────────────────────────────────────────────────────
    # STANDARD / NORMAL PRIMES
    # ─────────────────────────────────────────────────────────────────────
    {
        "key": "standard_35mm",
        "focal_length": "35mm",
        "aperture": "f/1.4",
        "name": "35mm Classic",
        "description": (
            "The quintessential documentary lens. Matches the natural field of view of the "
            "human eye and produces images that feel immediate and authentic."
        ),
        "prompt_keywords": [
            "35mm lens",
            "natural perspective",
            "classic documentary style",
            "beautiful bokeh at f/1.4",
            "human-eye field of view",
            "photojournalistic look",
            "organic rendering",
            "street photography",
        ],
        "best_for": ["street photography", "documentary", "fashion", "lifestyle", "portrait"],
        "typical_use": "Walk-around prime, editorial features, candid moments",
        "depth_of_field_effect": "Wide open: gentle background blur that retains context. Stopped down: sharp corner-to-corner.",
    },
    {
        "key": "pancake_40mm",
        "focal_length": "40mm",
        "aperture": "f/2.0",
        "name": "40mm Pancake",
        "description": (
            "The closest focal length to how the human eye perceives a scene. Compact and "
            "unobtrusive, producing honest, undistorted images."
        ),
        "prompt_keywords": [
            "40mm lens",
            "human eye perspective",
            "natural undistorted view",
            "honest rendering",
            "minimal distortion",
            "compact pancake lens look",
            "neutral perspective",
        ],
        "best_for": ["documentary", "lifestyle", "casual portrait", "everyday carry"],
        "typical_use": "Discreet daily shooting, vlogging, quick candid captures",
        "depth_of_field_effect": "Moderate separation at f/2; neither dramatically shallow nor fully deep.",
    },
    {
        "key": "nifty_fifty_f14",
        "focal_length": "50mm",
        "aperture": "f/1.4",
        "name": "50mm f/1.4 Nifty Fifty",
        "description": (
            "The workhorse standard lens beloved for its natural rendering and beautiful "
            "bokeh. Produces a classic, timeless photographic look."
        ),
        "prompt_keywords": [
            "50mm lens f/1.4",
            "nifty fifty",
            "natural perspective",
            "beautiful circular bokeh",
            "classic photography look",
            "shallow depth of field",
            "subject isolation",
            "creamy out-of-focus areas",
        ],
        "best_for": ["portrait", "street photography", "lifestyle", "product", "low-light"],
        "typical_use": "Versatile everyday lens for portraits, street, and general photography",
        "depth_of_field_effect": "At f/1.4: pleasing subject separation with smooth, round bokeh. Stopped down: sharp and deep.",
    },
    {
        "key": "nifty_fifty_f18",
        "focal_length": "50mm",
        "aperture": "f/1.8",
        "name": "50mm f/1.8 Budget Fifty",
        "description": (
            "The affordable standard lens. Slightly less bokeh than its f/1.4 sibling but "
            "still delivers the classic 50mm rendering with pleasing background softness."
        ),
        "prompt_keywords": [
            "50mm lens f/1.8",
            "standard lens",
            "natural perspective",
            "moderate shallow depth of field",
            "clean bokeh",
            "classic film-era look",
            "versatile prime",
        ],
        "best_for": ["portrait", "lifestyle", "product photography", "beginner"],
        "typical_use": "First prime lens, budget portrait and lifestyle work",
        "depth_of_field_effect": "Moderate background blur at f/1.8; slightly busier bokeh than f/1.4 lenses.",
    },
    {
        "key": "noctilux_58mm",
        "focal_length": "58mm",
        "aperture": "f/0.95",
        "name": "58mm Noctilux / Noct-Nikkor",
        "description": (
            "Ultra-fast exotic lens with a dreamy, glowing rendering wide open. Razor-thin "
            "focus plane produces an unmistakable ethereal, painterly quality."
        ),
        "prompt_keywords": [
            "58mm Noctilux f/0.95",
            "ultra-shallow depth of field",
            "dreamy glow wide open",
            "razor-thin focus plane",
            "ethereal light rendering",
            "painterly bokeh",
            "luminous highlight roll-off",
            "vintage character",
        ],
        "best_for": ["fine-art portrait", "night photography", "editorial", "fashion"],
        "typical_use": "Night-time street portraits, editorial beauty, fine-art fashion",
        "depth_of_field_effect": "Paper-thin plane of focus; extreme bokeh with a distinctive warm glow and soft vignette.",
    },

    # ─────────────────────────────────────────────────────────────────────
    # SHORT TELEPHOTO / PORTRAIT PRIMES
    # ─────────────────────────────────────────────────────────────────────
    {
        "key": "portrait_85mm_f14",
        "focal_length": "85mm",
        "aperture": "f/1.4",
        "name": "85mm f/1.4 Portrait King",
        "description": (
            "The gold-standard portrait lens. Flattering facial compression, creamy bokeh, "
            "and tack-sharp eyes make this the go-to for headshots and beauty work."
        ),
        "prompt_keywords": [
            "85mm portrait lens f/1.4",
            "flattering facial compression",
            "creamy buttery bokeh",
            "tack-sharp subject with blurred background",
            "professional portrait lighting",
            "beautiful skin rendering",
            "smooth out-of-focus highlights",
            "subject isolation",
        ],
        "best_for": ["portrait", "beauty", "fashion", "wedding", "headshot"],
        "typical_use": "Studio and natural-light headshots, beauty campaigns, bridal portraits",
        "depth_of_field_effect": "Wonderfully shallow; background melts into smooth, creamy blur while subject stays razor-sharp.",
    },
    {
        "key": "portrait_85mm_f18",
        "focal_length": "85mm",
        "aperture": "f/1.8",
        "name": "85mm f/1.8 Portrait",
        "description": (
            "A lighter, more affordable portrait prime. Slightly deeper depth of field than "
            "the f/1.4 but still delivers beautiful subject separation."
        ),
        "prompt_keywords": [
            "85mm portrait lens f/1.8",
            "flattering perspective",
            "smooth background separation",
            "portrait compression",
            "gentle bokeh",
            "sharp subject rendering",
            "natural skin tones",
        ],
        "best_for": ["portrait", "fashion", "editorial", "event"],
        "typical_use": "Event portraits, editorial headshots, outdoor fashion",
        "depth_of_field_effect": "Pleasantly shallow with smooth transitions; slightly more in-focus background detail than f/1.4.",
    },

    # ─────────────────────────────────────────────────────────────────────
    # MACRO LENSES
    # ─────────────────────────────────────────────────────────────────────
    {
        "key": "macro_100mm",
        "focal_length": "100mm",
        "aperture": "f/2.8",
        "name": "100mm Macro",
        "description": (
            "True 1:1 life-size magnification reveals textures invisible to the naked eye. "
            "Doubles as a sharp short-telephoto portrait lens."
        ),
        "prompt_keywords": [
            "100mm macro lens",
            "1:1 life-size magnification",
            "extreme close-up detail",
            "texture rendering",
            "every surface detail visible",
            "precise focus stacking",
            "clinical sharpness",
            "product detail shot",
        ],
        "best_for": ["jewelry", "beauty close-up", "food detail", "product", "watch", "nature"],
        "typical_use": "Jewelry and watch advertising, beauty skin detail, insect photography",
        "depth_of_field_effect": "At macro distances: paper-thin focus plane, requiring focus stacking for full sharpness.",
    },
    {
        "key": "macro_105mm",
        "focal_length": "105mm",
        "aperture": "f/2.8",
        "name": "105mm Micro-Nikkor Macro",
        "description": (
            "Slightly longer working distance than 100mm macro, giving more room for lighting. "
            "Legendary sharpness and neutral color rendition."
        ),
        "prompt_keywords": [
            "105mm macro lens",
            "micro-nikkor rendering",
            "1:1 magnification",
            "professional macro detail",
            "precise working distance",
            "sharp edge-to-edge",
            "neutral color rendition",
        ],
        "best_for": ["nature macro", "product detail", "beauty", "scientific imaging"],
        "typical_use": "Nature close-ups, product detail photography, scientific documentation",
        "depth_of_field_effect": "Extremely shallow at close focus; at portrait distances, pleasing moderate bokeh.",
    },

    # ─────────────────────────────────────────────────────────────────────
    # MEDIUM & LONG TELEPHOTO PRIMES
    # ─────────────────────────────────────────────────────────────────────
    {
        "key": "telephoto_135mm",
        "focal_length": "135mm",
        "aperture": "f/1.8",
        "name": "135mm Telephoto Portrait",
        "description": (
            "Strong background compression transforms busy scenes into clean compositions. "
            "Produces a distinctive, flattened perspective with melting bokeh."
        ),
        "prompt_keywords": [
            "135mm telephoto portrait lens",
            "strong background compression",
            "melting creamy bokeh",
            "telephoto subject isolation",
            "compressed perspective",
            "smooth highlight rendering",
            "distant background blur",
            "editorial fashion look",
        ],
        "best_for": ["portrait", "fashion runway", "editorial", "sport"],
        "typical_use": "Fashion editorial, runway photography, tight headshots with clean backgrounds",
        "depth_of_field_effect": "Very shallow; backgrounds dissolve into painterly wash of color and light.",
    },
    {
        "key": "telephoto_200mm",
        "focal_length": "200mm",
        "aperture": "f/2.0",
        "name": "200mm f/2.0 Telephoto",
        "description": (
            "Extreme compression and massive subject isolation. The lens of choice for "
            "professional sports and wildlife photographers who need speed and reach."
        ),
        "prompt_keywords": [
            "200mm telephoto lens f/2.0",
            "extreme background compression",
            "massive subject isolation",
            "professional sports photography",
            "stacked background planes",
            "telephoto bokeh",
            "fast action freezing",
            "shallow depth of field at distance",
        ],
        "best_for": ["sport", "wildlife", "fashion runway", "automotive"],
        "typical_use": "Professional sports sideline, wildlife safari, fashion runway",
        "depth_of_field_effect": "Dramatically shallow even at distance; backgrounds become abstract color fields.",
    },
    {
        "key": "telephoto_300mm",
        "focal_length": "300mm",
        "aperture": "f/2.8",
        "name": "300mm Super-Telephoto",
        "description": (
            "Long-reach lens that pulls distant subjects close while compressing spatial "
            "relationships into flat, graphic compositions."
        ),
        "prompt_keywords": [
            "300mm super telephoto lens",
            "extreme reach",
            "compressed spatial planes",
            "wildlife isolation",
            "sports action close-up",
            "flat graphic perspective",
            "background color wash",
        ],
        "best_for": ["wildlife", "sport", "bird photography", "air show"],
        "typical_use": "Bird photography, professional football/baseball, motorsport",
        "depth_of_field_effect": "Very shallow relative to distance; backgrounds reduced to soft, uniform tone.",
    },
    {
        "key": "telephoto_400mm",
        "focal_length": "400mm",
        "aperture": "f/4.0",
        "name": "400mm Super-Telephoto",
        "description": (
            "Maximum reach for wildlife and distant sport. Extreme compression turns "
            "backgrounds into smooth, abstract canvases."
        ),
        "prompt_keywords": [
            "400mm super telephoto lens",
            "extreme telephoto reach",
            "maximum compression",
            "wildlife detail at distance",
            "abstract background rendering",
            "heat haze shimmer",
            "atmospheric perspective",
        ],
        "best_for": ["wildlife", "sport", "aviation", "safari"],
        "typical_use": "Safari wildlife, stadium sports, bird-in-flight photography",
        "depth_of_field_effect": "Background is a pure blur of color; foreground and background planes stack and compress.",
    },

    # ─────────────────────────────────────────────────────────────────────
    # ZOOM LENSES
    # ─────────────────────────────────────────────────────────────────────
    {
        "key": "zoom_24_70mm",
        "focal_length": "24-70mm",
        "aperture": "f/2.8",
        "name": "24-70mm Standard Zoom",
        "description": (
            "The professional workhorse zoom covering wide to short telephoto. Reliable, "
            "sharp, and versatile — the desert-island lens for working photographers."
        ),
        "prompt_keywords": [
            "24-70mm zoom lens f/2.8",
            "professional workhorse",
            "versatile focal range",
            "sharp throughout zoom range",
            "consistent f/2.8 aperture",
            "editorial versatility",
            "event photography",
        ],
        "best_for": ["editorial", "event", "wedding", "commercial", "travel"],
        "typical_use": "Wedding day coverage, press conferences, corporate events",
        "depth_of_field_effect": "Moderate at f/2.8; subject separation depends on focal length chosen within zoom range.",
    },
    {
        "key": "zoom_70_200mm",
        "focal_length": "70-200mm",
        "aperture": "f/2.8",
        "name": "70-200mm Telephoto Zoom",
        "description": (
            "The other half of the pro zoom duo. Covers portraiture through sports with "
            "consistent fast aperture and beautiful compression."
        ),
        "prompt_keywords": [
            "70-200mm telephoto zoom lens f/2.8",
            "professional telephoto compression",
            "versatile portrait-to-action range",
            "constant f/2.8 aperture",
            "fashion runway lens",
            "smooth zoom bokeh",
            "subject isolation across range",
        ],
        "best_for": ["fashion", "sport", "portrait", "automotive", "wedding ceremony"],
        "typical_use": "Fashion runway, sports sideline, wedding ceremony from a distance",
        "depth_of_field_effect": "At 200mm f/2.8: strong background blur. At 70mm f/2.8: moderate, pleasing separation.",
    },

    # ─────────────────────────────────────────────────────────────────────
    # TILT-SHIFT LENSES
    # ─────────────────────────────────────────────────────────────────────
    {
        "key": "tilt_shift_17mm",
        "focal_length": "17mm",
        "aperture": "f/4.0",
        "name": "17mm Tilt-Shift",
        "description": (
            "Ultra-wide tilt-shift for correcting converging verticals on tall buildings. "
            "Also produces surreal miniature-model effects when the tilt plane is angled."
        ),
        "prompt_keywords": [
            "17mm tilt-shift lens",
            "corrected vertical lines",
            "architectural precision",
            "miniature model effect",
            "selective focus plane",
            "rectilinear correction",
            "parallel building edges",
        ],
        "best_for": ["architecture", "real estate", "cityscape", "creative miniature"],
        "typical_use": "Skyscraper exterior shots, urban cityscapes, architectural magazine work",
        "depth_of_field_effect": "Controllable: shift corrects perspective; tilt moves the focus plane for selective sharpness.",
    },
    {
        "key": "tilt_shift_24mm",
        "focal_length": "24mm",
        "aperture": "f/3.5",
        "name": "24mm Tilt-Shift",
        "description": (
            "The most popular tilt-shift focal length. Corrects perspective for architecture "
            "and enables dramatic selective-focus effects for creative work."
        ),
        "prompt_keywords": [
            "24mm tilt-shift lens",
            "corrected verticals",
            "selective focus plane",
            "architectural precision",
            "miniature diorama effect",
            "controlled perspective",
            "product flat-lay precision",
        ],
        "best_for": ["architecture", "real estate", "product flat-lay", "interior design"],
        "typical_use": "Interior architecture, product flat-lays, cityscape miniature effects",
        "depth_of_field_effect": "Full user control over the plane of sharp focus; can slice focus diagonally across a scene.",
    },
    {
        "key": "tilt_shift_45mm",
        "focal_length": "45mm",
        "aperture": "f/2.8",
        "name": "45mm Tilt-Shift",
        "description": (
            "A normal-perspective tilt-shift ideal for product and food photography. "
            "The tilt creates a smooth gradient of focus across tabletop scenes."
        ),
        "prompt_keywords": [
            "45mm tilt-shift lens",
            "product photography precision",
            "graduated focus plane",
            "tabletop selective focus",
            "controlled depth of field",
            "food photography tilt",
            "diagonal focus gradient",
        ],
        "best_for": ["product", "food", "tabletop", "still life", "catalog"],
        "typical_use": "Food editorial, product catalog, tabletop still-life compositions",
        "depth_of_field_effect": "Tilt creates a wedge-shaped zone of sharpness; beautiful gradual blur on either side.",
    },

    # ─────────────────────────────────────────────────────────────────────
    # ANAMORPHIC LENSES
    # ─────────────────────────────────────────────────────────────────────
    {
        "key": "anamorphic_50mm",
        "focal_length": "50mm",
        "aperture": "f/2.0",
        "name": "50mm Anamorphic",
        "description": (
            "Cinematic anamorphic look with signature oval bokeh, horizontal lens flares, "
            "and a widescreen aspect ratio. Gives images an unmistakably filmic quality."
        ),
        "prompt_keywords": [
            "50mm anamorphic lens",
            "oval bokeh highlights",
            "horizontal blue lens flare",
            "cinematic widescreen 2.39:1",
            "anamorphic squeeze distortion",
            "filmic halation",
            "cinematic color rendering",
            "shallow depth of field",
        ],
        "best_for": ["cinematic", "fashion film", "music video", "commercial"],
        "typical_use": "Narrative film, fashion commercials, cinematic brand campaigns",
        "depth_of_field_effect": "Shallow with distinctive oval-shaped out-of-focus highlights and edge stretch.",
    },
    {
        "key": "anamorphic_75mm",
        "focal_length": "75mm",
        "aperture": "f/2.0",
        "name": "75mm Anamorphic",
        "description": (
            "Tighter anamorphic framing for close-ups and medium shots. Exaggerated oval "
            "bokeh and prominent horizontal flares for a dramatic cinematic feel."
        ),
        "prompt_keywords": [
            "75mm anamorphic lens",
            "tight cinematic framing",
            "exaggerated oval bokeh",
            "prominent horizontal flare streaks",
            "widescreen aspect ratio",
            "anamorphic breathing",
            "cinematic depth rendering",
        ],
        "best_for": ["cinematic close-up", "fashion film", "dialogue scene", "music video"],
        "typical_use": "Close-up dialogue scenes, beauty cinematography, intimate fashion film",
        "depth_of_field_effect": "Noticeably shallow with elongated, elliptical highlights and a cinematic falloff.",
    },

    # ─────────────────────────────────────────────────────────────────────
    # ART / SPECIALTY / VINTAGE LENSES
    # ─────────────────────────────────────────────────────────────────────
    {
        "key": "lensbaby_freelensing",
        "focal_length": "50mm",
        "aperture": "f/2.5",
        "name": "Lensbaby / Freelensing",
        "description": (
            "Selective-focus optic with a sharp sweet spot surrounded by progressive blur. "
            "Mimics the tilt effect of freelensing for a dreamy, lo-fi aesthetic."
        ),
        "prompt_keywords": [
            "Lensbaby selective focus",
            "sweet spot sharp center",
            "surrounding progressive blur",
            "dreamy lo-fi aesthetic",
            "freelensing tilt effect",
            "creative edge blur",
            "light leak artifact",
            "ethereal soft glow",
        ],
        "best_for": ["creative portrait", "wedding detail", "fine art", "floral"],
        "typical_use": "Dreamy wedding portraits, creative fine-art photography, floral still life",
        "depth_of_field_effect": "Only a small circular area is sharp; everything else swirls into progressive blur.",
    },
    {
        "key": "petzval_art_lens",
        "focal_length": "85mm",
        "aperture": "f/2.2",
        "name": "Petzval 85mm Art Lens",
        "description": (
            "Recreates the 19th-century Petzval optical formula with sharp center focus "
            "and signature swirly bokeh that spirals around the subject."
        ),
        "prompt_keywords": [
            "Petzval art lens",
            "swirly bokeh pattern",
            "sharp center soft edges",
            "19th-century optical character",
            "brass-era rendering",
            "vignette with swirling blur",
            "vintage portrait look",
            "Lomography Petzval",
        ],
        "best_for": ["fine-art portrait", "vintage editorial", "creative bokeh", "wedding"],
        "typical_use": "Vintage-styled portrait sessions, fine-art editorial, creative fashion",
        "depth_of_field_effect": "Center is sharp; bokeh spirals outward in concentric swirls with pronounced field curvature.",
    },
    {
        "key": "helios_44_2",
        "focal_length": "58mm",
        "aperture": "f/2.0",
        "name": "Vintage Helios 44-2 (Swirly Bokeh)",
        "description": (
            "Soviet-era M42-mount legend famous for its swirly, rotating bokeh pattern. "
            "Slightly soft wide open with warm color cast and charming optical imperfections."
        ),
        "prompt_keywords": [
            "Helios 44-2 vintage lens",
            "swirly rotating bokeh",
            "Soviet-era lens character",
            "warm color cast",
            "soft wide-open rendering",
            "circular bokeh swirl pattern",
            "vintage optical imperfections",
            "M42 mount classic look",
        ],
        "best_for": ["portrait", "creative bokeh", "vintage aesthetic", "nature"],
        "typical_use": "Budget vintage portrait sessions, creative nature photography, retro-styled content",
        "depth_of_field_effect": "Background bokeh rotates in a distinctive swirl; slightly soft center at f/2 with glow.",
    },

    # ─────────────────────────────────────────────────────────────────────
    # BONUS ENTRIES (to exceed 30)
    # ─────────────────────────────────────────────────────────────────────
    {
        "key": "wide_zoom_16_35mm",
        "focal_length": "16-35mm",
        "aperture": "f/2.8",
        "name": "16-35mm Wide Zoom",
        "description": (
            "Professional wide-angle zoom covering ultra-wide to moderate wide. "
            "Versatile for landscapes, architecture, and environmental reportage."
        ),
        "prompt_keywords": [
            "16-35mm wide zoom lens f/2.8",
            "versatile wide angle range",
            "professional landscape lens",
            "interior photography zoom",
            "constant aperture wide zoom",
            "dramatic perspective control",
            "deep depth of field",
        ],
        "best_for": ["landscape", "architecture", "interior", "event"],
        "typical_use": "Landscape photography, real-estate interiors, press and event coverage",
        "depth_of_field_effect": "Deep focus throughout; at 35mm f/2.8 slight background softening is possible.",
    },
    {
        "key": "portrait_105mm_f14",
        "focal_length": "105mm",
        "aperture": "f/1.4",
        "name": "105mm f/1.4 Bokeh Master",
        "description": (
            "Massive, heavy portrait lens that produces the most extreme bokeh of any "
            "autofocus optic. Backgrounds become pure abstract color."
        ),
        "prompt_keywords": [
            "105mm f/1.4 bokeh master",
            "extreme background blur",
            "ultimate portrait isolation",
            "abstract color background",
            "telephoto bokeh king",
            "compressed perspective",
            "dreamy out-of-focus rendering",
        ],
        "best_for": ["portrait", "editorial", "fashion", "fine art"],
        "typical_use": "High-end portrait sessions, editorial beauty, gallery-quality prints",
        "depth_of_field_effect": "Absurdly shallow; at close focus the in-focus zone is mere millimeters thick.",
    },
    {
        "key": "cine_prime_25mm",
        "focal_length": "25mm",
        "aperture": "T1.5",
        "name": "25mm Cinema Prime",
        "description": (
            "Cine-rated wide prime with smooth focus throw and minimal breathing. "
            "Round iris blades produce perfectly circular bokeh for motion-picture work."
        ),
        "prompt_keywords": [
            "25mm cinema prime lens",
            "T1.5 cine aperture",
            "perfectly circular bokeh",
            "minimal focus breathing",
            "cinematic wide angle",
            "motion picture rendering",
            "smooth focus transition",
        ],
        "best_for": ["narrative film", "commercial video", "cinematic content", "music video"],
        "typical_use": "Wide establishing shots in narrative film, commercial cinematography",
        "depth_of_field_effect": "Wide open: gentle separation with round highlights. Stopped down: sharp and clean.",
    },
    {
        "key": "soft_focus_portrait",
        "focal_length": "135mm",
        "aperture": "f/2.8",
        "name": "135mm Soft-Focus Portrait",
        "description": (
            "Dedicated soft-focus lens with adjustable spherical aberration. Creates a "
            "glowing halo around highlights while retaining underlying sharpness."
        ),
        "prompt_keywords": [
            "soft focus portrait lens",
            "glowing highlight halo",
            "adjustable spherical aberration",
            "dreamy portrait glow",
            "diffused skin rendering",
            "romantic soft-focus effect",
            "ethereal light bloom",
        ],
        "best_for": ["bridal portrait", "boudoir", "fine-art portrait", "glamour"],
        "typical_use": "Bridal beauty shots, glamour portraits, romantic fine-art work",
        "depth_of_field_effect": "Sharp core detail wrapped in a luminous soft halo; adjustable from subtle to heavy diffusion.",
    },
]


# ─────────────────────────────────────────────────────────────────────────────
# Quick-lookup dictionary keyed by each lens's unique snake_case identifier.
# ─────────────────────────────────────────────────────────────────────────────
LENS_BY_KEY = {lens["key"]: lens for lens in LENS_LIBRARY}
