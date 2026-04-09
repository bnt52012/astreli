"""
Photography Styles Knowledge Base
==================================
Comprehensive mapping of photography and advertising visual styles to prompt-enrichment data.
Each entry provides description, prompt keywords for AI generation, typical industries, and mood.
"""

PHOTOGRAPHY_STYLES: dict[str, dict] = {
    # ──────────────────────────────────────────────
    # EDITORIAL & FASHION
    # ──────────────────────────────────────────────
    "editorial_fashion": {
        "description": "High-fashion editorial spreads as seen in Vogue, Harper's Bazaar. Dramatic poses, bold styling, narrative-driven imagery with artistic direction.",
        "prompt_keywords": ["editorial fashion photography", "high fashion", "dramatic pose", "avant-garde styling", "fashion magazine spread", "artistic fashion direction"],
        "typical_industries": ["luxury fashion", "haute couture", "fashion magazines", "designer brands"],
        "mood": "dramatic, aspirational, bold",
    },
    "editorial_beauty": {
        "description": "Close-up beauty editorial focusing on skin, makeup, and hair with flawless retouching and controlled studio lighting.",
        "prompt_keywords": ["beauty editorial", "close-up beauty shot", "flawless skin", "beauty retouching", "glossy magazine beauty", "luminous complexion"],
        "typical_industries": ["cosmetics", "skincare", "beauty magazines", "hair care"],
        "mood": "polished, luminous, pristine",
    },
    "editorial_lifestyle": {
        "description": "Styled lifestyle imagery for magazine features blending real-life scenarios with editorial polish.",
        "prompt_keywords": ["editorial lifestyle", "styled living", "curated lifestyle", "magazine feature photography", "aspirational daily life"],
        "typical_industries": ["lifestyle magazines", "home decor", "wellness", "travel"],
        "mood": "aspirational, curated, warm",
    },
    "haute_couture": {
        "description": "Ultra-high-end fashion photography showcasing one-of-a-kind garments with theatrical staging and artistic vision.",
        "prompt_keywords": ["haute couture photography", "theatrical fashion", "couture gown", "dramatic staging", "fashion art", "opulent setting"],
        "typical_industries": ["haute couture houses", "luxury fashion", "art exhibitions"],
        "mood": "theatrical, opulent, artistic",
    },
    "ready_to_wear": {
        "description": "Commercial fashion photography for ready-to-wear collections, balancing style with wearability and accessibility.",
        "prompt_keywords": ["ready to wear fashion", "commercial fashion", "accessible style", "seasonal collection", "fashion lookbook"],
        "typical_industries": ["fashion retail", "department stores", "fast fashion", "mid-range fashion"],
        "mood": "stylish, accessible, contemporary",
    },
    "streetwear": {
        "description": "Urban streetwear photography with gritty textures, bold graphics, and authentic street culture aesthetic.",
        "prompt_keywords": ["streetwear photography", "urban fashion", "street culture", "gritty texture", "bold graphic", "city backdrop"],
        "typical_industries": ["streetwear brands", "sneaker culture", "urban fashion", "youth fashion"],
        "mood": "edgy, authentic, urban",
    },
    "sportswear": {
        "description": "Athletic and sportswear photography emphasizing movement, performance, and dynamic energy.",
        "prompt_keywords": ["sportswear photography", "athletic wear", "dynamic movement", "performance apparel", "action shot", "sweat detail"],
        "typical_industries": ["athletic brands", "sportswear", "fitness", "activewear"],
        "mood": "energetic, powerful, dynamic",
    },
    "athleisure": {
        "description": "Hybrid athletic-leisure photography bridging workout and casual wear in aspirational lifestyle settings.",
        "prompt_keywords": ["athleisure photography", "casual athletic", "lifestyle fitness", "relaxed sporty", "workout to brunch aesthetic"],
        "typical_industries": ["athleisure brands", "wellness lifestyle", "yoga brands", "casual fitness"],
        "mood": "relaxed, healthy, aspirational",
    },
    "swimwear": {
        "description": "Swimwear and resort photography shot on location with natural light, beach or poolside settings, sun-kissed skin tones.",
        "prompt_keywords": ["swimwear photography", "resort wear", "beach setting", "sun-kissed skin", "tropical backdrop", "pool photography"],
        "typical_industries": ["swimwear", "resort fashion", "beachwear", "travel fashion"],
        "mood": "sun-drenched, carefree, sensual",
    },
    "lingerie": {
        "description": "Intimate apparel photography balancing sensuality with sophistication, soft lighting, and elegant poses.",
        "prompt_keywords": ["lingerie photography", "intimate apparel", "soft sensual lighting", "elegant pose", "silk and lace detail"],
        "typical_industries": ["lingerie brands", "intimate apparel", "luxury undergarments"],
        "mood": "sensual, sophisticated, intimate",
    },
    "boudoir": {
        "description": "Intimate personal photography in bedroom or private settings with romantic lighting and empowering poses.",
        "prompt_keywords": ["boudoir photography", "intimate portrait", "romantic lighting", "bedroom setting", "soft shadows", "empowering sensual"],
        "typical_industries": ["personal branding", "gift photography", "intimate portraiture"],
        "mood": "intimate, romantic, empowering",
    },

    # ──────────────────────────────────────────────
    # COMMERCIAL & ADVERTISING
    # ──────────────────────────────────────────────
    "commercial_advertising": {
        "description": "Polished commercial imagery designed for ad campaigns with clear brand messaging, hero product placement, and aspirational appeal.",
        "prompt_keywords": ["commercial advertising photography", "ad campaign", "hero shot", "brand imagery", "aspirational commercial", "polished advertisement"],
        "typical_industries": ["all consumer brands", "advertising agencies", "marketing"],
        "mood": "polished, aspirational, brand-driven",
    },
    "catalog": {
        "description": "Clean, consistent product-on-model photography for catalogs and e-commerce with neutral backgrounds and even lighting.",
        "prompt_keywords": ["catalog photography", "clean product shot", "neutral background", "consistent lighting", "e-commerce model photography"],
        "typical_industries": ["retail", "e-commerce", "department stores", "fashion retail"],
        "mood": "clean, consistent, informative",
    },
    "lookbook": {
        "description": "Fashion lookbook photography showing full outfits in styled but approachable settings, telling a seasonal story.",
        "prompt_keywords": ["lookbook photography", "styled outfit", "seasonal story", "fashion collection", "full-length outfit shot"],
        "typical_industries": ["fashion brands", "boutiques", "seasonal collections"],
        "mood": "styled, cohesive, narrative",
    },
    "campaign": {
        "description": "Big-budget brand campaign imagery with cinematic quality, strong art direction, and memorable visual storytelling.",
        "prompt_keywords": ["brand campaign photography", "cinematic brand imagery", "art directed", "campaign key visual", "hero campaign shot"],
        "typical_industries": ["luxury brands", "automotive", "tech", "major consumer brands"],
        "mood": "cinematic, memorable, prestigious",
    },
    "direct_response": {
        "description": "Performance-marketing imagery optimized for click-through, with clear product visibility, benefit messaging space, and attention-grabbing composition.",
        "prompt_keywords": ["direct response ad", "performance marketing image", "clear product visibility", "attention grabbing", "CTA-optimized composition"],
        "typical_industries": ["e-commerce", "DTC brands", "digital marketing", "social media ads"],
        "mood": "compelling, clear, action-oriented",
    },
    "social_media_native": {
        "description": "Platform-native content designed to blend with organic social feeds while maintaining brand quality.",
        "prompt_keywords": ["social media native content", "Instagram-worthy", "authentic social post", "UGC-inspired", "feed-native aesthetic"],
        "typical_industries": ["all consumer brands", "influencer marketing", "social media marketing"],
        "mood": "authentic, relatable, scroll-stopping",
    },
    "user_generated_content_style": {
        "description": "Professionally shot content that mimics the authentic, unpolished look of real user content for trust and relatability.",
        "prompt_keywords": ["UGC style photography", "authentic look", "unpolished aesthetic", "real person feel", "phone camera quality", "genuine moment"],
        "typical_industries": ["DTC brands", "beauty", "food", "lifestyle brands"],
        "mood": "authentic, trustworthy, relatable",
    },

    # ──────────────────────────────────────────────
    # PORTRAIT STYLES
    # ──────────────────────────────────────────────
    "portrait_classic": {
        "description": "Traditional portraiture with careful attention to lighting, pose, and expression. Timeless and dignified.",
        "prompt_keywords": ["classic portrait photography", "traditional portrait", "dignified pose", "careful lighting", "timeless portrait"],
        "typical_industries": ["personal portraiture", "fine art", "family photography"],
        "mood": "timeless, dignified, refined",
    },
    "portrait_environmental": {
        "description": "Subject photographed in their natural environment (workspace, home, outdoors) telling their story through setting.",
        "prompt_keywords": ["environmental portrait", "subject in natural setting", "contextual portrait", "workplace portrait", "storytelling through environment"],
        "typical_industries": ["editorial", "corporate", "documentary", "personal branding"],
        "mood": "authentic, contextual, narrative",
    },
    "portrait_corporate": {
        "description": "Professional headshots and corporate portraits with clean backgrounds, even lighting, and approachable expressions.",
        "prompt_keywords": ["corporate portrait", "professional headshot", "business portrait", "clean background headshot", "executive portrait"],
        "typical_industries": ["corporate", "professional services", "LinkedIn", "annual reports"],
        "mood": "professional, approachable, trustworthy",
    },
    "portrait_beauty": {
        "description": "Close-up beauty portraits emphasizing skin texture, makeup, and facial features with meticulous lighting and retouching.",
        "prompt_keywords": ["beauty portrait", "close-up face", "flawless skin detail", "beauty lighting", "makeup photography", "skin glow"],
        "typical_industries": ["cosmetics", "skincare", "beauty editorial"],
        "mood": "flawless, luminous, detailed",
    },
    "portrait_fashion": {
        "description": "Fashion-forward portraits where clothing and styling are as important as the subject, with editorial flair.",
        "prompt_keywords": ["fashion portrait", "styled portrait", "editorial face", "fashion-forward", "designer styling"],
        "typical_industries": ["fashion", "luxury brands", "magazines"],
        "mood": "stylish, editorial, striking",
    },
    "portrait_cinematic": {
        "description": "Film-inspired portraits with dramatic lighting, shallow depth of field, and color grading reminiscent of cinema.",
        "prompt_keywords": ["cinematic portrait", "film-inspired portrait", "dramatic lighting portrait", "shallow depth of field face", "movie-still portrait", "cinematic color grading"],
        "typical_industries": ["entertainment", "personal branding", "artistic portraiture"],
        "mood": "dramatic, cinematic, moody",
    },
    "portrait_candid": {
        "description": "Unposed, natural moment portraits capturing genuine expressions and authentic interactions.",
        "prompt_keywords": ["candid portrait", "natural expression", "unposed moment", "genuine emotion", "spontaneous portrait"],
        "typical_industries": ["wedding", "event", "documentary", "family"],
        "mood": "genuine, spontaneous, warm",
    },
    "portrait_conceptual": {
        "description": "Artistic portraits built around a concept or theme, using props, costumes, and creative techniques.",
        "prompt_keywords": ["conceptual portrait", "artistic portrait", "themed portrait", "creative concept", "surreal portrait"],
        "typical_industries": ["fine art", "advertising", "gallery exhibitions"],
        "mood": "imaginative, thought-provoking, artistic",
    },
    "portrait_fitness": {
        "description": "Athletic physique portraits highlighting musculature, definition, and physical achievement with dramatic lighting.",
        "prompt_keywords": ["fitness portrait", "athletic physique", "muscle definition", "dramatic body lighting", "sweat and strength"],
        "typical_industries": ["fitness brands", "sports nutrition", "gym marketing", "athletic apparel"],
        "mood": "powerful, defined, motivational",
    },

    # ──────────────────────────────────────────────
    # PRODUCT PHOTOGRAPHY
    # ──────────────────────────────────────────────
    "product_hero": {
        "description": "Single hero product shot with dramatic lighting, precise focus, and premium feel. The money shot for campaigns.",
        "prompt_keywords": ["hero product shot", "dramatic product lighting", "premium product photography", "single product focus", "campaign product image"],
        "typical_industries": ["all consumer products", "luxury goods", "tech", "beauty"],
        "mood": "premium, dramatic, focused",
    },
    "product_flat_lay": {
        "description": "Top-down arrangement of products and props on a styled surface, popular for social media and e-commerce.",
        "prompt_keywords": ["flat lay photography", "top-down product arrangement", "styled flat lay", "overhead product shot", "curated arrangement"],
        "typical_industries": ["beauty", "fashion accessories", "stationery", "food", "lifestyle"],
        "mood": "curated, organized, social-media-ready",
    },
    "product_ghost_mannequin": {
        "description": "Clothing photographed on invisible mannequin to show garment shape and fit without a visible form.",
        "prompt_keywords": ["ghost mannequin photography", "invisible mannequin", "hollow man effect", "garment shape display", "floating clothing"],
        "typical_industries": ["fashion e-commerce", "clothing retail", "uniform companies"],
        "mood": "clean, shape-focused, professional",
    },
    "product_on_white": {
        "description": "Pure white background product photography standard for Amazon, e-commerce, and clean catalog presentation.",
        "prompt_keywords": ["product on white background", "pure white seamless", "clean product shot", "e-commerce product photo", "isolated product"],
        "typical_industries": ["e-commerce", "Amazon listings", "product catalogs"],
        "mood": "clean, professional, standardized",
    },
    "product_lifestyle": {
        "description": "Product shown in real-life context and use scenarios, connecting the item to aspirational lifestyle moments.",
        "prompt_keywords": ["product lifestyle shot", "product in context", "lifestyle product photography", "product in use", "aspirational product setting"],
        "typical_industries": ["home goods", "kitchenware", "tech gadgets", "fashion accessories"],
        "mood": "aspirational, contextual, relatable",
    },
    "product_360": {
        "description": "Multi-angle product photography designed to show every angle and detail of the product for complete visual information.",
        "prompt_keywords": ["360 product photography", "multi-angle product", "product turntable", "all-angles product view"],
        "typical_industries": ["e-commerce", "tech products", "jewelry", "furniture"],
        "mood": "informative, comprehensive, detailed",
    },
    "product_scale": {
        "description": "Product photographed with scale references (hands, everyday objects) to communicate real-world size and proportion.",
        "prompt_keywords": ["product scale reference", "product in hand", "size comparison shot", "product proportion", "real-world scale"],
        "typical_industries": ["tech gadgets", "jewelry", "miniatures", "kitchenware"],
        "mood": "informative, relatable, tangible",
    },
    "product_deconstructed": {
        "description": "Product components artfully separated and arranged to showcase ingredients, parts, or construction quality.",
        "prompt_keywords": ["deconstructed product", "exploded view", "product components", "ingredients flat lay", "inside the product"],
        "typical_industries": ["food", "beauty", "tech", "watchmaking"],
        "mood": "transparent, detailed, educational",
    },
    "product_splash": {
        "description": "Dynamic product photography with liquid splashes, powder explosions, or other kinetic elements adding energy.",
        "prompt_keywords": ["product splash photography", "liquid splash", "dynamic product", "powder explosion", "kinetic product shot", "high-speed product"],
        "typical_industries": ["beverages", "cosmetics", "perfume", "food"],
        "mood": "dynamic, energetic, eye-catching",
    },
    "product_macro_detail": {
        "description": "Extreme close-up product photography revealing texture, craftsmanship, and material quality at microscopic level.",
        "prompt_keywords": ["macro product detail", "extreme close-up product", "texture detail shot", "craftsmanship close-up", "material quality macro"],
        "typical_industries": ["luxury goods", "watches", "jewelry", "textiles", "beauty"],
        "mood": "detailed, luxurious, quality-focused",
    },

    # ──────────────────────────────────────────────
    # FOOD & BEVERAGE
    # ──────────────────────────────────────────────
    "food_editorial": {
        "description": "Magazine-quality food photography with artistic plating, styled props, and dramatic lighting for editorial spreads.",
        "prompt_keywords": ["editorial food photography", "food magazine", "artistic plating", "styled food shoot", "dramatic food lighting"],
        "typical_industries": ["food magazines", "cookbook publishing", "gourmet restaurants"],
        "mood": "artistic, appetizing, dramatic",
    },
    "food_commercial": {
        "description": "Bright, appetizing food photography for advertising with hero plating, perfect garnish, and mouthwatering appeal.",
        "prompt_keywords": ["commercial food photography", "appetizing food shot", "hero food plating", "mouthwatering", "food advertising"],
        "typical_industries": ["restaurants", "food brands", "fast food", "CPG food"],
        "mood": "appetizing, bright, compelling",
    },
    "food_overhead": {
        "description": "Bird's-eye table photography showing complete place settings, multiple dishes, and the social context of dining.",
        "prompt_keywords": ["overhead food photography", "bird's eye dining", "table spread", "flat lay food", "social dining scene"],
        "typical_industries": ["restaurants", "food delivery", "catering", "hospitality"],
        "mood": "social, abundant, inviting",
    },
    "food_dark_moody": {
        "description": "Chiaroscuro food photography with dark backgrounds, dramatic side lighting, and rich saturated tones.",
        "prompt_keywords": ["dark moody food photography", "chiaroscuro food", "dark background food", "dramatic food lighting", "rich food tones"],
        "typical_industries": ["fine dining", "craft spirits", "artisan food", "cookbooks"],
        "mood": "moody, rich, artisanal",
    },
    "food_bright_airy": {
        "description": "Light, bright food photography with white or pastel backgrounds, natural window light, and fresh aesthetic.",
        "prompt_keywords": ["bright airy food photography", "natural light food", "white background food", "fresh food aesthetic", "light and clean food shot"],
        "typical_industries": ["healthy food", "bakeries", "brunch spots", "wellness food"],
        "mood": "fresh, light, clean",
    },
    "food_action": {
        "description": "Food in motion - pouring, drizzling, cutting, steam rising - capturing the dynamic moments of cooking and eating.",
        "prompt_keywords": ["food action shot", "pouring sauce", "drizzling honey", "steam rising", "food in motion", "cooking action"],
        "typical_industries": ["food brands", "cooking shows", "recipe content", "restaurants"],
        "mood": "dynamic, sensory, appetizing",
    },
    "beverage": {
        "description": "Drink-focused photography with condensation, ice, pour shots, and liquid dynamics creating thirst appeal.",
        "prompt_keywords": ["beverage photography", "drink condensation", "ice detail", "pour shot", "liquid dynamics", "thirst appeal"],
        "typical_industries": ["spirits", "soft drinks", "coffee", "wine", "craft beer"],
        "mood": "refreshing, dynamic, thirst-inducing",
    },

    # ──────────────────────────────────────────────
    # STILL LIFE & FINE ART
    # ──────────────────────────────────────────────
    "still_life_classic": {
        "description": "Traditional still life inspired by Dutch masters - carefully arranged objects with dramatic chiaroscuro lighting.",
        "prompt_keywords": ["classic still life", "Dutch master style", "carefully arranged objects", "chiaroscuro still life", "painterly photography"],
        "typical_industries": ["fine art", "luxury goods", "wine", "artisan products"],
        "mood": "painterly, rich, timeless",
    },
    "still_life_modern": {
        "description": "Contemporary minimalist still life with geometric arrangements, bold color blocking, and graphic sensibility.",
        "prompt_keywords": ["modern still life", "minimalist arrangement", "color blocking objects", "geometric composition", "contemporary still life"],
        "typical_industries": ["design magazines", "modern brands", "art direction", "home decor"],
        "mood": "modern, graphic, refined",
    },
    "still_life_found_object": {
        "description": "Artistic arrangement of everyday or found objects creating unexpected beauty and meaning through composition.",
        "prompt_keywords": ["found object still life", "everyday objects art", "unexpected beauty", "artistic arrangement", "poetic objects"],
        "typical_industries": ["fine art", "editorial", "gallery", "conceptual advertising"],
        "mood": "poetic, unexpected, contemplative",
    },
    "fine_art_photography": {
        "description": "Gallery-quality photography as art, with conceptual depth, technical mastery, and emotional resonance.",
        "prompt_keywords": ["fine art photography", "gallery quality", "conceptual photography", "artistic vision", "museum-quality image"],
        "typical_industries": ["galleries", "art collectors", "museum exhibitions", "limited edition prints"],
        "mood": "contemplative, profound, masterful",
    },
    "fine_art_nude": {
        "description": "Artistic figure photography celebrating the human form with classical posing, sculptural lighting, and fine art sensibility.",
        "prompt_keywords": ["fine art nude", "artistic figure study", "sculptural body lighting", "classical figure pose", "human form art"],
        "typical_industries": ["fine art galleries", "art publications", "sculpture reference"],
        "mood": "artistic, classical, sculptural",
    },

    # ──────────────────────────────────────────────
    # ARCHITECTURAL & INTERIOR
    # ──────────────────────────────────────────────
    "architectural_exterior": {
        "description": "Building exteriors showcasing architectural design, materials, and integration with surroundings. Often shot at twilight.",
        "prompt_keywords": ["architectural exterior photography", "building facade", "architectural design", "twilight architecture", "structural beauty"],
        "typical_industries": ["architecture firms", "real estate", "construction", "urban development"],
        "mood": "grand, precise, structured",
    },
    "architectural_interior": {
        "description": "Interior space photography showing room design, spatial flow, materials, and light interaction with careful perspective correction.",
        "prompt_keywords": ["interior architecture photography", "room design", "spatial composition", "interior lighting", "perspective-corrected interior"],
        "typical_industries": ["interior design", "real estate", "hospitality", "architecture"],
        "mood": "spacious, inviting, designed",
    },
    "real_estate": {
        "description": "Property listing photography with wide angles, HDR-balanced exposures, and warm inviting tones to sell spaces.",
        "prompt_keywords": ["real estate photography", "property listing", "wide angle interior", "HDR balanced room", "warm inviting space"],
        "typical_industries": ["real estate", "property development", "vacation rentals", "hospitality"],
        "mood": "inviting, spacious, welcoming",
    },
    "interior_design_editorial": {
        "description": "Magazine-quality interior photography showcasing design vision with styled vignettes and curated accessories.",
        "prompt_keywords": ["interior design editorial", "styled interior vignette", "design magazine shot", "curated home accessories", "aspirational interior"],
        "typical_industries": ["interior design magazines", "home decor brands", "furniture", "design firms"],
        "mood": "aspirational, curated, editorial",
    },

    # ──────────────────────────────────────────────
    # AUTOMOTIVE
    # ──────────────────────────────────────────────
    "automotive_studio": {
        "description": "Studio car photography with controlled lighting revealing body lines, paint depth, and design details.",
        "prompt_keywords": ["studio car photography", "automotive studio shot", "car body lines", "paint reflection", "controlled car lighting"],
        "typical_industries": ["automotive manufacturers", "car magazines", "dealerships"],
        "mood": "sleek, premium, precise",
    },
    "automotive_location": {
        "description": "Cars photographed in dramatic locations - mountain roads, desert highways, cityscapes - connecting vehicle to lifestyle.",
        "prompt_keywords": ["automotive location photography", "car on mountain road", "dramatic car location", "lifestyle automotive", "scenic car shot"],
        "typical_industries": ["automotive brands", "luxury car", "adventure vehicles", "SUV marketing"],
        "mood": "adventurous, aspirational, dramatic",
    },
    "automotive_detail": {
        "description": "Close-up automotive photography focusing on design details - headlights, wheels, interior materials, dashboard.",
        "prompt_keywords": ["automotive detail photography", "car headlight close-up", "wheel detail", "interior material", "dashboard design"],
        "typical_industries": ["automotive luxury", "car reviews", "aftermarket parts"],
        "mood": "detailed, premium, tactile",
    },
    "automotive_motion": {
        "description": "Cars in motion with motion blur backgrounds, rig shots, and speed dynamics conveying performance and power.",
        "prompt_keywords": ["automotive motion photography", "car rig shot", "motion blur background", "speed dynamic", "car in motion", "rolling shot"],
        "typical_industries": ["performance cars", "motorsport", "automotive advertising"],
        "mood": "dynamic, powerful, fast",
    },

    # ──────────────────────────────────────────────
    # LIFESTYLE & DOCUMENTARY
    # ──────────────────────────────────────────────
    "lifestyle_aspirational": {
        "description": "Styled but natural-looking imagery of people living their best life, connecting products to aspirational moments.",
        "prompt_keywords": ["aspirational lifestyle photography", "living your best life", "styled natural moment", "aspirational daily scene", "lifestyle brand imagery"],
        "typical_industries": ["lifestyle brands", "travel", "wellness", "home", "food"],
        "mood": "aspirational, warm, attainable luxury",
    },
    "lifestyle_authentic": {
        "description": "Genuinely unscripted moments capturing real emotions and interactions with minimal styling intervention.",
        "prompt_keywords": ["authentic lifestyle photography", "real moments", "unscripted interaction", "genuine emotion", "documentary lifestyle"],
        "typical_industries": ["nonprofit", "healthcare", "family brands", "community organizations"],
        "mood": "genuine, emotional, real",
    },
    "lifestyle_wellness": {
        "description": "Health and wellness lifestyle imagery with clean aesthetics, natural settings, and mindful activity portrayal.",
        "prompt_keywords": ["wellness lifestyle photography", "healthy living", "mindful activity", "yoga and meditation", "clean wellness aesthetic"],
        "typical_industries": ["wellness brands", "health food", "fitness", "meditation apps", "supplements"],
        "mood": "calm, healthy, balanced",
    },
    "lifestyle_travel": {
        "description": "Travel and adventure lifestyle photography capturing exploration, cultural experiences, and wanderlust moments.",
        "prompt_keywords": ["travel lifestyle photography", "wanderlust", "cultural exploration", "adventure moment", "destination experience"],
        "typical_industries": ["travel brands", "airlines", "hotels", "tourism boards", "luggage"],
        "mood": "adventurous, inspiring, wanderlust",
    },
    "documentary": {
        "description": "Truthful, unmanipulated photography capturing real events, people, and places with journalistic integrity.",
        "prompt_keywords": ["documentary photography", "journalistic", "unmanipulated", "real event capture", "truth in photography"],
        "typical_industries": ["journalism", "NGOs", "editorial", "news media"],
        "mood": "authentic, raw, truthful",
    },
    "photojournalism": {
        "description": "News-driven photography capturing the decisive moment with clarity, urgency, and narrative power.",
        "prompt_keywords": ["photojournalism", "decisive moment", "news photography", "candid action", "story-telling image"],
        "typical_industries": ["news organizations", "wire services", "magazines", "documentary"],
        "mood": "urgent, immediate, storytelling",
    },
    "street": {
        "description": "Candid urban photography capturing everyday life, characters, and juxtapositions in public spaces.",
        "prompt_keywords": ["street photography", "urban candid", "everyday life", "city scene", "decisive moment", "public space"],
        "typical_industries": ["art photography", "editorial", "urban brands", "city tourism"],
        "mood": "candid, observational, gritty",
    },
    "candid": {
        "description": "Unposed, spontaneous photography capturing genuine moments and natural expressions without direction.",
        "prompt_keywords": ["candid photography", "unposed moment", "spontaneous capture", "natural expression", "genuine interaction"],
        "typical_industries": ["weddings", "events", "family", "editorial"],
        "mood": "spontaneous, genuine, warm",
    },

    # ──────────────────────────────────────────────
    # NATURE, LANDSCAPE & OUTDOOR
    # ──────────────────────────────────────────────
    "landscape_epic": {
        "description": "Grand landscape photography with sweeping vistas, dramatic skies, and epic natural scenery.",
        "prompt_keywords": ["epic landscape photography", "sweeping vista", "dramatic sky", "grand natural scenery", "vast landscape"],
        "typical_industries": ["travel", "outdoor brands", "tourism", "wall art"],
        "mood": "epic, awe-inspiring, vast",
    },
    "landscape_intimate": {
        "description": "Close, personal landscape details - a single tree, a stream detail, forest floor - finding beauty in the small.",
        "prompt_keywords": ["intimate landscape", "landscape detail", "quiet nature", "small scene beauty", "personal landscape"],
        "typical_industries": ["fine art", "wellness", "nature publications"],
        "mood": "quiet, contemplative, intimate",
    },
    "nature_wildlife": {
        "description": "Wildlife photography capturing animals in their natural habitat with telephoto precision and behavioral storytelling.",
        "prompt_keywords": ["wildlife photography", "animal in habitat", "telephoto wildlife", "natural behavior", "wild animal portrait"],
        "typical_industries": ["nature magazines", "conservation", "outdoor brands", "education"],
        "mood": "wild, natural, awe-inspiring",
    },
    "aerial_drone": {
        "description": "Overhead aerial photography from drones revealing patterns, scale, and perspectives impossible from ground level.",
        "prompt_keywords": ["aerial drone photography", "overhead view", "drone perspective", "aerial pattern", "bird's eye landscape"],
        "typical_industries": ["real estate", "tourism", "agriculture", "construction", "outdoor adventure"],
        "mood": "expansive, revealing, modern",
    },
    "underwater": {
        "description": "Submerged photography with aquatic color palettes, light refraction, bubbles, and the ethereal quality of water.",
        "prompt_keywords": ["underwater photography", "submerged", "aquatic light", "water refraction", "bubble detail", "ethereal underwater"],
        "typical_industries": ["swimwear", "marine brands", "luxury resorts", "fine art"],
        "mood": "ethereal, mysterious, fluid",
    },

    # ──────────────────────────────────────────────
    # MACRO & SCIENTIFIC
    # ──────────────────────────────────────────────
    "macro": {
        "description": "Extreme close-up photography revealing details invisible to the naked eye with razor-thin depth of field.",
        "prompt_keywords": ["macro photography", "extreme close-up", "microscopic detail", "razor-thin depth of field", "invisible detail revealed"],
        "typical_industries": ["jewelry", "watchmaking", "beauty", "nature", "science"],
        "mood": "detailed, revealing, fascinating",
    },
    "scientific": {
        "description": "Precision photography for scientific documentation with accurate color, scale markers, and clinical clarity.",
        "prompt_keywords": ["scientific photography", "clinical precision", "accurate color", "documentation photography", "scale reference"],
        "typical_industries": ["pharmaceutical", "medical", "research", "forensics"],
        "mood": "precise, clinical, informative",
    },

    # ──────────────────────────────────────────────
    # WEDDING & EVENT
    # ──────────────────────────────────────────────
    "wedding_classic": {
        "description": "Timeless wedding photography with formal portraits, clean editing, and traditional coverage of key moments.",
        "prompt_keywords": ["classic wedding photography", "formal bridal portrait", "timeless wedding", "traditional ceremony", "elegant wedding"],
        "typical_industries": ["wedding photography", "bridal magazines", "wedding venues"],
        "mood": "timeless, elegant, romantic",
    },
    "wedding_photojournalistic": {
        "description": "Documentary-style wedding coverage capturing candid emotions, spontaneous moments, and the unfolding story of the day.",
        "prompt_keywords": ["photojournalistic wedding", "candid wedding moment", "wedding documentary", "spontaneous wedding emotion", "storytelling wedding"],
        "typical_industries": ["wedding photography", "editorial weddings"],
        "mood": "emotional, spontaneous, narrative",
    },
    "wedding_fine_art": {
        "description": "Fine-art inspired wedding photography with film-like tones, soft light, and an emphasis on beauty and aesthetics.",
        "prompt_keywords": ["fine art wedding photography", "film-inspired wedding", "soft romantic light", "ethereal wedding", "painterly wedding tones"],
        "typical_industries": ["luxury weddings", "destination weddings", "bridal editorial"],
        "mood": "ethereal, romantic, fine art",
    },
    "event": {
        "description": "Corporate and social event photography capturing speakers, interactions, decor, and atmosphere of gatherings.",
        "prompt_keywords": ["event photography", "corporate event", "social gathering", "speaker capture", "event atmosphere"],
        "typical_industries": ["corporate events", "conferences", "galas", "festivals"],
        "mood": "energetic, social, professional",
    },

    # ──────────────────────────────────────────────
    # CINEMATIC & FILM-INSPIRED
    # ──────────────────────────────────────────────
    "cinematic": {
        "description": "Photography emulating cinema with wide aspect ratios, color grading, dramatic lighting, and narrative framing.",
        "prompt_keywords": ["cinematic photography", "film still", "wide aspect ratio", "cinematic color grading", "dramatic cinema lighting", "movie scene"],
        "typical_industries": ["entertainment", "luxury brands", "automotive", "fashion campaigns"],
        "mood": "cinematic, dramatic, narrative",
    },
    "film_noir": {
        "description": "Inspired by 1940s-50s film noir - high contrast black and white, deep shadows, venetian blind light patterns, mystery.",
        "prompt_keywords": ["film noir photography", "high contrast black and white", "deep shadows", "venetian blind light", "noir mystery", "1940s aesthetic"],
        "typical_industries": ["entertainment", "fine art", "fashion editorial", "fragrance"],
        "mood": "mysterious, dark, dramatic",
    },
    "vintage_film": {
        "description": "Photography emulating analog film stocks - Kodak Portra warmth, Fuji color, Ilford grain, Polaroid instant.",
        "prompt_keywords": ["vintage film photography", "film grain", "analog film look", "Kodak Portra tones", "film emulation", "retro film aesthetic"],
        "typical_industries": ["fashion", "music", "lifestyle", "indie brands"],
        "mood": "nostalgic, warm, organic",
    },
    "retro_70s": {
        "description": "1970s-inspired photography with warm amber tones, soft focus, lens flare, and bohemian free-spirited aesthetic.",
        "prompt_keywords": ["70s retro photography", "amber warm tones", "soft focus vintage", "lens flare", "bohemian aesthetic", "1970s color palette"],
        "typical_industries": ["fashion", "music", "bohemian brands", "vintage-inspired"],
        "mood": "groovy, warm, free-spirited",
    },
    "retro_80s": {
        "description": "1980s-inspired photography with bold colors, neon accents, geometric shapes, and new wave pop culture energy.",
        "prompt_keywords": ["80s retro photography", "neon colors", "bold geometric", "new wave aesthetic", "synthwave visual", "1980s pop culture"],
        "typical_industries": ["entertainment", "gaming", "retro fashion", "nightlife"],
        "mood": "bold, neon, energetic",
    },
    "retro_90s": {
        "description": "1990s-inspired photography with grunge textures, oversaturated or desaturated tones, flash photography, and gen-X aesthetic.",
        "prompt_keywords": ["90s retro photography", "grunge texture", "flash photography", "gen-X aesthetic", "1990s nostalgia", "lo-fi film"],
        "typical_industries": ["fashion", "music", "youth brands", "streetwear"],
        "mood": "grungy, nostalgic, raw",
    },
    "retro_y2k": {
        "description": "Early 2000s Y2K aesthetic with metallic textures, futuristic elements, pink and chrome color palettes, and digital optimism.",
        "prompt_keywords": ["Y2K aesthetic photography", "metallic chrome", "futuristic 2000s", "pink and silver", "digital age", "millennium style"],
        "typical_industries": ["fashion", "beauty", "tech", "pop culture"],
        "mood": "futuristic, playful, shiny",
    },
    "analog_instant": {
        "description": "Polaroid and instant film aesthetic with soft edges, unique color shifts, white border framing, and spontaneous feel.",
        "prompt_keywords": ["Polaroid photography", "instant film", "soft color shift", "white border", "spontaneous capture", "instant print aesthetic"],
        "typical_industries": ["social media", "scrapbooking", "personal branding", "events"],
        "mood": "spontaneous, nostalgic, personal",
    },

    # ──────────────────────────────────────────────
    # BLACK & WHITE
    # ──────────────────────────────────────────────
    "black_and_white_classic": {
        "description": "Traditional black and white photography with full tonal range, deep blacks, and luminous highlights.",
        "prompt_keywords": ["classic black and white photography", "full tonal range", "deep blacks", "luminous highlights", "monochrome"],
        "typical_industries": ["fine art", "editorial", "fashion", "portraiture"],
        "mood": "timeless, dramatic, elegant",
    },
    "black_and_white_high_contrast": {
        "description": "Bold high-contrast black and white with crushed blacks, blown highlights, and graphic punch.",
        "prompt_keywords": ["high contrast black and white", "crushed blacks", "graphic monochrome", "bold shadow", "stark contrast"],
        "typical_industries": ["fashion editorial", "music", "sports", "fine art"],
        "mood": "bold, graphic, intense",
    },
    "black_and_white_low_contrast": {
        "description": "Soft, low-contrast black and white with gentle gradations and misty, ethereal quality.",
        "prompt_keywords": ["low contrast black and white", "soft monochrome", "gentle gradation", "misty ethereal", "quiet black and white"],
        "typical_industries": ["fine art", "maternity", "wedding", "nature"],
        "mood": "gentle, ethereal, dreamy",
    },

    # ──────────────────────────────────────────────
    # TECHNOLOGY & DIGITAL
    # ──────────────────────────────────────────────
    "tech_product": {
        "description": "Clean technology product photography with precise edge lighting, reflection control, and futuristic clean aesthetic.",
        "prompt_keywords": ["tech product photography", "clean edge lighting", "reflection control", "futuristic product", "device photography"],
        "typical_industries": ["consumer electronics", "smartphones", "laptops", "wearables", "smart home"],
        "mood": "clean, innovative, precise",
    },
    "tech_ui_showcase": {
        "description": "Device screen showcase photography displaying app interfaces, websites, or software on real devices in context.",
        "prompt_keywords": ["UI showcase photography", "device screen display", "app on phone", "website on laptop", "screen content photography"],
        "typical_industries": ["SaaS", "app developers", "tech companies", "digital products"],
        "mood": "modern, functional, contextual",
    },
    "tech_abstract": {
        "description": "Abstract technology-inspired visuals with data visualization aesthetics, circuit patterns, and digital textures.",
        "prompt_keywords": ["abstract technology visual", "data visualization", "digital texture", "circuit pattern", "tech abstract art"],
        "typical_industries": ["tech companies", "AI/ML", "cybersecurity", "fintech"],
        "mood": "futuristic, abstract, innovative",
    },

    # ──────────────────────────────────────────────
    # LUXURY & PREMIUM
    # ──────────────────────────────────────────────
    "luxury_minimal": {
        "description": "Ultra-minimal luxury photography with generous negative space, muted tones, and quiet sophistication.",
        "prompt_keywords": ["minimal luxury photography", "generous negative space", "muted luxury tones", "quiet sophistication", "understated elegance"],
        "typical_industries": ["luxury fashion", "high-end jewelry", "premium skincare", "luxury hospitality"],
        "mood": "sophisticated, quiet, exclusive",
    },
    "luxury_opulent": {
        "description": "Rich, opulent luxury photography with gold tones, rich textures, dramatic lighting, and unapologetic extravagance.",
        "prompt_keywords": ["opulent luxury photography", "gold tones", "rich texture", "extravagant setting", "lavish detail", "luxury excess"],
        "typical_industries": ["luxury brands", "high jewelry", "private aviation", "luxury real estate"],
        "mood": "opulent, extravagant, rich",
    },
    "luxury_heritage": {
        "description": "Heritage luxury photography emphasizing craftsmanship, tradition, history, and the timeless value of artisanship.",
        "prompt_keywords": ["heritage luxury photography", "craftsmanship detail", "artisan tradition", "timeless luxury", "legacy brand"],
        "typical_industries": ["heritage luxury houses", "watchmaking", "leather goods", "fine spirits"],
        "mood": "timeless, prestigious, crafted",
    },

    # ──────────────────────────────────────────────
    # BEAUTY & COSMETICS SPECIFIC
    # ──────────────────────────────────────────────
    "beauty_clean": {
        "description": "Clean beauty photography with natural makeup looks, dewy skin, and fresh minimalist aesthetic.",
        "prompt_keywords": ["clean beauty photography", "natural makeup", "dewy skin", "fresh minimal", "no-makeup makeup look"],
        "typical_industries": ["clean beauty brands", "natural skincare", "organic cosmetics"],
        "mood": "fresh, natural, pure",
    },
    "beauty_glam": {
        "description": "High-glam beauty photography with bold makeup, dramatic lashes, contouring, and magazine-cover perfection.",
        "prompt_keywords": ["glam beauty photography", "bold makeup", "dramatic lashes", "contour highlight", "magazine cover beauty"],
        "typical_industries": ["cosmetics brands", "makeup artists", "beauty magazines"],
        "mood": "glamorous, bold, striking",
    },
    "beauty_skin": {
        "description": "Skincare-focused photography showcasing skin quality, texture, luminosity, and the science of skincare.",
        "prompt_keywords": ["skincare photography", "skin texture close-up", "luminous skin", "before after skin", "skin science visual"],
        "typical_industries": ["skincare brands", "dermatology", "medical aesthetics"],
        "mood": "scientific, luminous, transformative",
    },
    "beauty_hair": {
        "description": "Hair-focused photography with movement, shine, texture, and the artistry of hairstyling.",
        "prompt_keywords": ["hair photography", "hair movement", "glossy hair shine", "hair texture detail", "hairstyling art"],
        "typical_industries": ["hair care brands", "salons", "styling tools", "hair color"],
        "mood": "flowing, shiny, textured",
    },
    "beauty_nails": {
        "description": "Nail art and manicure photography with precise detail, color accuracy, and hand posing artistry.",
        "prompt_keywords": ["nail photography", "manicure detail", "nail art close-up", "hand pose", "nail color accuracy"],
        "typical_industries": ["nail polish brands", "nail salons", "beauty publications"],
        "mood": "detailed, colorful, precise",
    },
    "beauty_fragrance": {
        "description": "Perfume and fragrance photography translating scent into visual metaphor through ethereal imagery and luxury materials.",
        "prompt_keywords": ["fragrance photography", "perfume bottle", "scent visual metaphor", "ethereal mist", "luxury fragrance shot"],
        "typical_industries": ["fragrance brands", "luxury perfume", "celebrity fragrance"],
        "mood": "ethereal, luxurious, sensory",
    },

    # ──────────────────────────────────────────────
    # JEWELRY & WATCHES
    # ──────────────────────────────────────────────
    "jewelry_studio": {
        "description": "Precision jewelry photography with controlled lighting to maximize sparkle, fire, and material reflections.",
        "prompt_keywords": ["studio jewelry photography", "diamond sparkle", "precious metal reflection", "jewelry lighting precision", "gem fire"],
        "typical_industries": ["fine jewelry", "engagement rings", "luxury watches", "fashion jewelry"],
        "mood": "sparkling, precise, luxurious",
    },
    "jewelry_lifestyle": {
        "description": "Jewelry worn in lifestyle contexts, connecting pieces to emotions, occasions, and personal style.",
        "prompt_keywords": ["lifestyle jewelry photography", "jewelry on skin", "accessory in context", "personal style jewelry", "jewelry and emotion"],
        "typical_industries": ["jewelry brands", "fashion accessories", "gifting"],
        "mood": "personal, emotional, aspirational",
    },
    "watch_macro": {
        "description": "Horological photography with extreme detail of dials, movements, and craftsmanship of fine timepieces.",
        "prompt_keywords": ["watch macro photography", "dial detail", "movement close-up", "horological precision", "timepiece craftsmanship"],
        "typical_industries": ["luxury watches", "horology magazines", "watch collectors"],
        "mood": "precise, mechanical, prestigious",
    },

    # ──────────────────────────────────────────────
    # CONCEPTUAL & ARTISTIC
    # ──────────────────────────────────────────────
    "surreal": {
        "description": "Surrealist photography bending reality with unexpected scale, impossible scenes, and dreamlike compositions.",
        "prompt_keywords": ["surreal photography", "impossible scene", "dreamlike composition", "reality distortion", "surrealist visual"],
        "typical_industries": ["fine art", "creative advertising", "editorial", "album covers"],
        "mood": "dreamlike, impossible, thought-provoking",
    },
    "abstract": {
        "description": "Abstract photography using form, color, line, and texture to create non-representational imagery.",
        "prompt_keywords": ["abstract photography", "non-representational", "form and color", "abstract texture", "visual abstraction"],
        "typical_industries": ["fine art", "corporate decor", "graphic design", "gallery"],
        "mood": "interpretive, bold, artistic",
    },
    "minimalist": {
        "description": "Reduction to essential elements - vast negative space, single subjects, geometric purity, and visual silence.",
        "prompt_keywords": ["minimalist photography", "negative space", "single subject", "geometric purity", "visual silence", "less is more"],
        "typical_industries": ["luxury brands", "modern design", "architecture", "gallery art"],
        "mood": "serene, pure, contemplative",
    },
    "double_exposure": {
        "description": "Multiple exposure technique blending two or more images for artistic overlay effects and visual poetry.",
        "prompt_keywords": ["double exposure photography", "multiple exposure", "image overlay", "blended imagery", "artistic exposure fusion"],
        "typical_industries": ["music industry", "fine art", "editorial", "personal branding"],
        "mood": "dreamy, layered, artistic",
    },
    "long_exposure": {
        "description": "Extended shutter time creating motion trails, silky water, star trails, and light painting effects.",
        "prompt_keywords": ["long exposure photography", "motion trail", "silky water", "star trails", "light painting", "time-stretched image"],
        "typical_industries": ["landscape", "architecture", "fine art", "automotive"],
        "mood": "ethereal, flowing, temporal",
    },
    "tilt_shift": {
        "description": "Selective focus technique creating miniature-world effects or precise plane-of-focus control for product and architecture.",
        "prompt_keywords": ["tilt-shift photography", "miniature effect", "selective focus plane", "toy-like scene", "Lensbaby effect"],
        "typical_industries": ["architecture", "urban planning", "product", "creative editorial"],
        "mood": "whimsical, precise, unique",
    },
    "infrared": {
        "description": "Infrared photography revealing invisible light spectrum with ethereal white foliage, dark skies, and surreal landscapes.",
        "prompt_keywords": ["infrared photography", "IR spectrum", "white foliage", "dark sky infrared", "surreal infrared landscape"],
        "typical_industries": ["fine art", "landscape", "experimental"],
        "mood": "surreal, otherworldly, ethereal",
    },

    # ──────────────────────────────────────────────
    # SOCIAL MEDIA & DIGITAL CONTENT
    # ──────────────────────────────────────────────
    "instagram_aesthetic": {
        "description": "Instagram-optimized photography with cohesive grid aesthetics, trend-aware styling, and engagement-driving composition.",
        "prompt_keywords": ["Instagram aesthetic", "social media optimized", "grid-worthy", "trend-driven visual", "engagement-optimized"],
        "typical_industries": ["all consumer brands", "influencers", "social media marketing"],
        "mood": "trendy, cohesive, shareable",
    },
    "tiktok_native": {
        "description": "TikTok-optimized vertical content with attention-grabbing first frames, trend-aware production, and fast-paced energy.",
        "prompt_keywords": ["TikTok native content", "vertical format", "attention-grabbing", "trend-aware", "fast-paced visual"],
        "typical_industries": ["youth brands", "entertainment", "beauty", "fashion", "food"],
        "mood": "energetic, viral, trend-forward",
    },
    "pinterest_optimized": {
        "description": "Pinterest-optimized tall-format imagery with text overlay space, aspirational styling, and save-worthy composition.",
        "prompt_keywords": ["Pinterest optimized", "tall format", "text overlay space", "aspirational styling", "save-worthy image"],
        "typical_industries": ["home decor", "DIY", "fashion", "food", "wedding"],
        "mood": "inspirational, saveable, aspirational",
    },

    # ──────────────────────────────────────────────
    # SPECIALTY STYLES
    # ──────────────────────────────────────────────
    "flat_design": {
        "description": "Photography styled to complement flat design aesthetics - clean lines, solid colors, geometric arrangements.",
        "prompt_keywords": ["flat design photography", "clean geometric", "solid color backdrop", "graphic design compatible", "clean line composition"],
        "typical_industries": ["tech companies", "SaaS", "digital products", "modern branding"],
        "mood": "clean, graphic, modern",
    },
    "brutalist": {
        "description": "Raw, unpolished aesthetic inspired by brutalist design - concrete textures, harsh lighting, stark compositions.",
        "prompt_keywords": ["brutalist photography", "raw concrete texture", "harsh industrial", "stark composition", "unpolished aesthetic"],
        "typical_industries": ["architecture", "avant-garde fashion", "independent music", "gallery art"],
        "mood": "raw, stark, confrontational",
    },
    "vaporwave": {
        "description": "Internet art aesthetic with pink/purple/cyan palettes, retro-futuristic elements, glitch effects, and 80s/90s nostalgia.",
        "prompt_keywords": ["vaporwave aesthetic", "pink purple cyan", "retro-futuristic", "glitch effect", "digital nostalgia", "vapor aesthetic"],
        "typical_industries": ["digital art", "music", "gaming", "youth culture"],
        "mood": "nostalgic, digital, surreal",
    },
    "wes_anderson": {
        "description": "Symmetrical compositions with pastel color palettes, whimsical staging, and the distinctive visual style of Wes Anderson films.",
        "prompt_keywords": ["Wes Anderson style", "symmetrical composition", "pastel color palette", "whimsical staging", "centered framing", "dollhouse aesthetic"],
        "typical_industries": ["hospitality", "retail", "creative branding", "editorial"],
        "mood": "whimsical, symmetrical, pastel",
    },
    "light_leak": {
        "description": "Photography featuring intentional light leaks, lens flares, and film imperfections for warm analog character.",
        "prompt_keywords": ["light leak photography", "lens flare", "film imperfection", "warm analog", "light artifact", "vintage film leak"],
        "typical_industries": ["music", "fashion", "indie brands", "personal projects"],
        "mood": "warm, imperfect, nostalgic",
    },
    "cross_processed": {
        "description": "Cross-processing film look with shifted colors, increased contrast, and the distinctive color casts of C-41/E-6 cross-processing.",
        "prompt_keywords": ["cross-processed photography", "color shift", "C-41 E-6 cross", "saturated color cast", "experimental film"],
        "typical_industries": ["fashion", "music", "lomography", "experimental"],
        "mood": "experimental, saturated, unexpected",
    },
    "cyanotype": {
        "description": "Blue-and-white cyanotype printing aesthetic, an early photographic process with distinctive Prussian blue tones.",
        "prompt_keywords": ["cyanotype photography", "Prussian blue", "sun print", "blueprint aesthetic", "alternative process"],
        "typical_industries": ["fine art", "botanical illustration", "gallery prints"],
        "mood": "historical, botanical, artistic",
    },
    "daguerreotype": {
        "description": "Aesthetic inspired by the earliest photography - silver-plate look, formal posing, sepia-metallic tones, and historical gravitas.",
        "prompt_keywords": ["daguerreotype style", "early photography", "silver plate look", "formal vintage pose", "antique photography"],
        "typical_industries": ["fine art", "historical recreation", "heritage brands"],
        "mood": "historical, formal, precious",
    },
    "tintype": {
        "description": "Civil War-era tintype aesthetic with dark backgrounds, slight blur, vintage patina, and ghostly quality.",
        "prompt_keywords": ["tintype photography", "wet plate collodion", "dark vintage portrait", "antique patina", "ghostly image quality"],
        "typical_industries": ["fine art", "historical", "specialty portraiture"],
        "mood": "ghostly, antique, solemn",
    },
    "holographic": {
        "description": "Holographic and iridescent aesthetic with rainbow light refractions, prismatic effects, and futuristic shimmer.",
        "prompt_keywords": ["holographic photography", "iridescent", "rainbow refraction", "prismatic effect", "futuristic shimmer"],
        "typical_industries": ["beauty", "fashion", "tech", "festival brands"],
        "mood": "futuristic, colorful, eye-catching",
    },
    "neon_glow": {
        "description": "Neon-lit photography with vibrant glowing colors against dark backgrounds, urban night energy, and electric atmosphere.",
        "prompt_keywords": ["neon glow photography", "neon light portrait", "vibrant night colors", "electric atmosphere", "urban neon"],
        "typical_industries": ["nightlife", "gaming", "entertainment", "urban fashion"],
        "mood": "electric, vibrant, nocturnal",
    },
    "golden_hour_portrait": {
        "description": "Portraits shot exclusively during golden hour with warm backlight, lens flare, and magical warm-toned atmosphere.",
        "prompt_keywords": ["golden hour portrait", "warm backlight", "sunset portrait", "golden sun flare", "magic hour face"],
        "typical_industries": ["wedding", "portrait", "lifestyle", "social media"],
        "mood": "warm, magical, golden",
    },
    "blue_hour_mood": {
        "description": "Photography during civil twilight with deep blue ambient light, city lights emerging, and contemplative mood.",
        "prompt_keywords": ["blue hour photography", "civil twilight", "deep blue ambient", "city lights emerging", "twilight mood"],
        "typical_industries": ["architecture", "cityscape", "luxury real estate", "hospitality"],
        "mood": "contemplative, serene, twilight",
    },
    "silhouette": {
        "description": "Strong backlighting reducing subjects to dark outlines against bright backgrounds for graphic, mysterious effect.",
        "prompt_keywords": ["silhouette photography", "backlit figure", "dark outline", "dramatic backlight", "shadow figure"],
        "typical_industries": ["fine art", "editorial", "music", "fitness"],
        "mood": "mysterious, graphic, dramatic",
    },
    "high_key": {
        "description": "Bright, low-contrast photography dominated by whites and light tones with minimal shadows and airy feel.",
        "prompt_keywords": ["high key photography", "bright white dominant", "low contrast", "airy bright", "overexposed aesthetic", "light and clean"],
        "typical_industries": ["beauty", "baby", "wedding", "healthcare", "skincare"],
        "mood": "bright, pure, optimistic",
    },
    "low_key": {
        "description": "Dark, moody photography dominated by shadows with selective highlights creating drama and mystery.",
        "prompt_keywords": ["low key photography", "dark dominant", "selective highlight", "shadow drama", "moody dark", "noir aesthetic"],
        "typical_industries": ["luxury", "spirits", "fine dining", "entertainment", "fragrance"],
        "mood": "moody, dramatic, mysterious",
    },
    "dutch_angle_style": {
        "description": "Deliberately tilted camera angle creating dynamic tension, unease, and visual energy in compositions.",
        "prompt_keywords": ["Dutch angle photography", "tilted frame", "dynamic camera angle", "visual tension", "canted shot"],
        "typical_industries": ["action sports", "music", "editorial", "fashion"],
        "mood": "dynamic, tense, energetic",
    },
    "panoramic": {
        "description": "Ultra-wide panoramic photography capturing sweeping horizontal scenes with epic scale and environmental context.",
        "prompt_keywords": ["panoramic photography", "ultra-wide scene", "sweeping horizontal", "epic panorama", "wide format"],
        "typical_industries": ["landscape", "real estate", "tourism", "architecture"],
        "mood": "epic, sweeping, immersive",
    },
    "composite_fantasy": {
        "description": "Multi-element composited photography creating fantasy scenes, impossible locations, and digital art-meets-photography.",
        "prompt_keywords": ["composite photography", "fantasy scene", "digital composite", "impossible location", "photo manipulation art"],
        "typical_industries": ["entertainment", "gaming", "book covers", "creative advertising"],
        "mood": "fantastical, imaginative, awe-inspiring",
    },
    "studio_clean": {
        "description": "Clean studio photography with controlled lighting, seamless backgrounds, and technical precision for versatile commercial use.",
        "prompt_keywords": ["clean studio photography", "seamless background", "controlled studio lighting", "technical precision", "professional studio"],
        "typical_industries": ["all product categories", "corporate", "e-commerce", "catalogs"],
        "mood": "clean, professional, controlled",
    },
    "reportage": {
        "description": "Story-driven documentary reportage capturing unfolding events with immediacy, context, and journalistic narrative.",
        "prompt_keywords": ["reportage photography", "story-driven documentary", "event unfolding", "journalistic narrative", "in-the-moment"],
        "typical_industries": ["journalism", "corporate communications", "NGO", "events"],
        "mood": "immediate, narrative, authentic",
    },
}
