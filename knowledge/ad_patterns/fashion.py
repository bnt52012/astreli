"""
Fashion industry advertising patterns.

Defines the visual language, pacing, and production style for fashion brand
advertisements and campaign films. Inspired by Gucci, Balenciaga, Nike Fashion,
Zara, Saint Laurent, and Acne Studios. Emphasises bold editorial vision,
dramatic poses, mixed lighting styles, high energy, and confident attitude.
"""

FASHION_PATTERN = {

    # ------------------------------------------------------------------
    # Scene flow — typical ad structure (8 scenes)
    # ------------------------------------------------------------------
    "scene_flow": [
        {
            "archetype": "location_establish",
            "duration": 2.5,
            "description": (
                "Strong location opener — raw concrete architecture, neon-lit "
                "Tokyo alley, sun-blasted desert highway, or brutalist "
                "stairwell. Sets tone and attitude instantly."
            ),
        },
        {
            "archetype": "full_look_reveal",
            "duration": 3.5,
            "description": (
                "Full-body reveal of model in the hero outfit — confident "
                "stance, editorial pose. The garment silhouette is the focal "
                "point. Shot slightly low angle for power."
            ),
        },
        {
            "archetype": "fabric_detail",
            "duration": 2.5,
            "description": (
                "Tight detail on fabric texture, stitching, or print — the "
                "camera almost touches the material. Shows construction "
                "quality and design detail."
            ),
        },
        {
            "archetype": "movement_sequence",
            "duration": 4.0,
            "description": (
                "Model in motion within the environment — walking with purpose, "
                "spinning on a street corner, climbing stairs two at a time. "
                "Garments move and flow with the body."
            ),
        },
        {
            "archetype": "editorial_portrait",
            "duration": 3.0,
            "description": (
                "Medium close-up editorial portrait — strong eye contact with "
                "camera, attitude-driven expression. Styled hair and makeup "
                "are visible and intentional."
            ),
        },
        {
            "archetype": "accessory_closeup",
            "duration": 2.5,
            "description": (
                "Hero accessory moment — shoes hitting pavement, bag swinging "
                "at hip, sunglasses being put on, or jewellery catching light. "
                "Product focus within lifestyle context."
            ),
        },
        {
            "archetype": "dynamic_lifestyle",
            "duration": 4.0,
            "description": (
                "High-energy lifestyle beat — group of models, skateboard kick, "
                "rooftop at sunset, or backstage chaos. Captures the culture "
                "and community around the brand."
            ),
        },
        {
            "archetype": "endframe",
            "duration": 2.5,
            "description": (
                "Brand logo and collection name — bold typography on a "
                "contrasting background or superimposed over the final action "
                "frame. Confident, no apology."
            ),
        },
    ],

    # ------------------------------------------------------------------
    # Visual signature
    # ------------------------------------------------------------------
    "visual_signature": {
        "color_temperature": "adaptive — warm 5500K for S/S, cool 4000K for F/W, mixed for streetwear",
        "contrast": "medium-high editorial punch with styled shadow direction",
        "saturation": "intentional extremes — either rich bold primaries or deliberately desaturated film tones",
        "grain": "visible 35mm film grain, analogue editorial texture throughout",
        "depth_of_field": "medium f/2.8-f/4, environment readable but soft, garment always sharp",
        "color_grade": "film-emulation grade — Kodak Portra warmth or Fuji Pro 400H coolness depending on season",
    },

    # ------------------------------------------------------------------
    # Lighting preferences — keys from lighting_setups.py
    # ------------------------------------------------------------------
    "lighting_preferences": [
        "golden_hour",
        "harsh_noon",
        "overcast_diffused",
        "beauty_dish",
        "neon_gel",
        "backlit",
        "rim_light",
        "window_light_dramatic",
        "high_key",
        "silhouette",
    ],

    # ------------------------------------------------------------------
    # Lens preferences — keys from lens_library.py
    # ------------------------------------------------------------------
    "lens_preferences": [
        "portrait_85mm_f18",
        "classic_35mm",
        "standard_50mm_f14",
        "zoom_70_200mm",
        "wide_24mm",
        "telephoto_135mm",
        "anamorphic_50mm",
    ],

    # ------------------------------------------------------------------
    # Movement style
    # ------------------------------------------------------------------
    "movement_style": {
        "camera": (
            "Dynamic and editorial — tracking shots alongside walking models, "
            "handheld with controlled energy, Steadicam orbits, and sharp "
            "whip-pans between looks. The camera moves with confidence."
        ),
        "subject": (
            "Powerful and intentional — runway-calibre walk, decisive pose "
            "transitions, hair toss, jacket shrug, mid-stride freeze. Every "
            "movement communicates attitude and self-possession."
        ),
        "pacing": (
            "Rhythmic and music-driven — cuts land on beats, sequences build "
            "momentum. Alternates between held editorial moments and bursts "
            "of kinetic energy. Never boring, never chaotic."
        ),
    },

    # ------------------------------------------------------------------
    # Transition preferences (ordered by preference)
    # ------------------------------------------------------------------
    "transition_preferences": [
        "hard_cut_on_beat",
        "match_cut_on_movement",
        "whip_pan",
        "quick_dissolve",
        "flash_frame",
        "jump_cut",
    ],

    # ------------------------------------------------------------------
    # Music style
    # ------------------------------------------------------------------
    "music_style": (
        "High-energy and genre-fluid — electronic beats with runway energy, "
        "dark indie synth-pop, trap-influenced bass with editorial restraint, "
        "or percussive minimal techno. Think Arca, SOPHIE, Jamie xx, or "
        "fashion show soundtracks by Michel Gaubert. The beat drives the edit."
    ),

    # ------------------------------------------------------------------
    # Banned elements — things to NEVER do
    # ------------------------------------------------------------------
    "banned_elements": [
        "unflattering low angles that distort garment proportions",
        "wrinkled, ill-fitting, or unpressed clothing visible on camera",
        "cluttered backgrounds that compete with the outfit for attention",
        "amateur snapshot composition or centred-subject tourist framing",
        "direct on-camera flash unless intentionally editorial and styled",
        "extreme wide-angle barrel distortion on the human body",
        "slow, lifeless pacing with no rhythmic structure",
        "corporate office or generic suburban settings",
        "stock-photo smiles or forced casual laughter",
        "overly smooth digital skin that removes all texture and character",
    ],

    # ------------------------------------------------------------------
    # Prompt modifiers — phrases appended to image generation prompts
    # ------------------------------------------------------------------
    "prompt_modifiers": [
        "high fashion editorial photography, Vogue cover quality",
        "runway presentation lighting, backstage energy",
        "fabric texture rendered with every thread and weave visible",
        "confident model stance with editorial attitude and intention",
        "architectural or urban background with clean graphic lines",
        "colour-coordinated environment complementing the outfit palette",
        "movement captured mid-stride, garments flowing with the body",
        "fashion week energy, decisive moment photography",
        "sharp focus on garment construction and silhouette",
        "intentional editorial crop and bold framing choices",
        "designer atelier atmosphere with raw creative energy",
        "fashion-forward hair and makeup, fully styled editorial look",
        "accessories placed with editorial intention and narrative",
        "seasonal mood matching collection theme and colour story",
        "street style documentary aesthetic, Parisian or Tokyo sidewalk",
        "Harper's Bazaar and i-D magazine campaign quality",
        "fabric draping emphasis showing silhouette and movement",
        "35mm film grain and Kodak Portra colour rendering",
        "strong directional golden-hour side light on the outfit",
        "dramatic shadow play on concrete or plaster walls",
        "anamorphic widescreen framing with oval bokeh highlights",
        "mixed artificial and natural light, editorial colour contrast",
    ],

    # ------------------------------------------------------------------
    # Video modifiers — phrases for Kling animation prompts
    # ------------------------------------------------------------------
    "video_modifiers": [
        "confident model walk toward camera with attitude",
        "fabric flowing and catching air with each stride",
        "hair toss in dramatic slow motion",
        "quick editorial pose transitions between held beats",
        "tracking shot alongside model walking down the street",
        "360-degree spin revealing outfit from every angle",
        "wind machine creating dramatic fabric and hair movement",
        "strobe flash effect punctuating the beat",
        "model turning head sharply with decisive eye contact",
        "shoes stepping into frame in stylised close-up",
        "jacket being thrown over shoulder in one fluid motion",
        "group of models walking in formation, runway style",
    ],

    # ------------------------------------------------------------------
    # Reference brands
    # ------------------------------------------------------------------
    "reference_brands": [
        "Gucci",
        "Balenciaga",
        "Saint Laurent",
        "Nike (fashion campaigns)",
        "Zara",
        "Acne Studios",
        "Jacquemus",
        "Prada",
        "Rick Owens",
        "Off-White",
        "Comme des Garçons",
        "Maison Margiela",
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
