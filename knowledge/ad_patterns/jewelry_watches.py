"""Advertising patterns for the jewelry and watches industry.

Defines the JEWELRY_WATCHES_PATTERN dictionary capturing the visual language,
pacing, lighting, and cinematic conventions used by premium jewelry and
horlogerie brands such as Cartier, Rolex, Tiffany & Co., and Bulgari.
Emphasis on macro precision, specular brilliance, reflective-surface control,
and dark-field product photography.
"""

JEWELRY_WATCHES_PATTERN = {
    "industry": "jewelry_watches",

    # ------------------------------------------------------------------
    # Scene flow
    # ------------------------------------------------------------------
    "scene_flow": [
        {
            "archetype": "dark_reveal",
            "duration": 4.0,
            "description": "Product emerges from total darkness via a single precise light sweep across polished metal or gemstone surface",
        },
        {
            "archetype": "macro_detail",
            "duration": 3.5,
            "description": "Extreme close-up of watch dial indices, diamond facets, or movement gears with razor-thin depth of field",
        },
        {
            "archetype": "craftsmanship",
            "duration": 3.0,
            "description": "Brief glimpse of hand-finishing, engraving, or stone-setting suggesting master artisan heritage",
        },
        {
            "archetype": "lifestyle_elegance",
            "duration": 4.0,
            "description": "Product worn on wrist or décolletage in an opulent context: gala, private jet, palazzo interior",
        },
        {
            "archetype": "light_play",
            "duration": 3.5,
            "description": "Controlled light rakes across surface producing scintillation, fire, or metallic luster bloom",
        },
        {
            "archetype": "interaction_ritual",
            "duration": 3.0,
            "description": "Deliberate fastening of clasp, winding of crown, or gentle placement on velvet cushion",
        },
        {
            "archetype": "hero_pedestal",
            "duration": 4.0,
            "description": "Full product floating or resting on reflective obsidian surface, perfectly lit from multiple controlled sources",
        },
        {
            "archetype": "endframe_logo",
            "duration": 3.0,
            "description": "Product centered on deep black with embossed brand wordmark, tagline, and subtle sparkle accent",
        },
    ],

    # ------------------------------------------------------------------
    # Visual signature
    # ------------------------------------------------------------------
    "visual_signature": {
        "color_temperature": "cool neutral to warm gold, 4500-5500 K depending on metal type",
        "contrast": "high with deep true blacks and brilliant specular peaks",
        "saturation": "selective — gemstone hues vivid, everything else muted to near-monochrome",
        "grain": "none, absolute optical clarity required to resolve micro detail",
        "depth_of_field": "extreme shallow f/2 for hero isolation or deep f/11-f/16 for full-product sharpness",
        "color_grade": "cool silver for platinum and white gold, warm amber for yellow gold and rose gold",
    },

    # ------------------------------------------------------------------
    # Lighting preferences — references to lighting setup keys
    # ------------------------------------------------------------------
    "lighting_preferences": [
        "product_dark_field",
        "product_light_field",
        "product_backlit_glow",
        "rim_light",
        "low_key",
        "chiaroscuro",
        "ring_light",
        "beauty_dish",
        "raking_texture",
        "candle_firelight",
    ],

    # ------------------------------------------------------------------
    # Lens preferences — references to lens keys
    # ------------------------------------------------------------------
    "lens_preferences": [
        "macro_100mm",
        "macro_105mm",
        "portrait_85mm_f14",
        "telephoto_135mm",
        "tilt_shift_45mm",
        "standard_50mm_f14",
        "petzval",
    ],

    # ------------------------------------------------------------------
    # Movement style
    # ------------------------------------------------------------------
    "movement_style": {
        "camera": "ultra-slow precision orbits, controlled macro dolly, motorized slider at sub-millimeter speed",
        "subject": "static product with light moving across surfaces; occasional deliberate human hand interaction",
        "pacing": "hypnotic and reverent, each frame composed as a still-life painting, minimum 3-second holds",
    },

    # ------------------------------------------------------------------
    # Transition preferences (ordered)
    # ------------------------------------------------------------------
    "transition_preferences": [
        "light flare wipe revealing next shot",
        "long cross-dissolve through specular highlight",
        "fade to black with sparkle residue",
        "match cut on circular forms (dial to gemstone)",
        "slow iris from macro detail to wider framing",
        "hard cut on rhythmic tick of second hand",
    ],

    # ------------------------------------------------------------------
    # Music style
    # ------------------------------------------------------------------
    "music_style": "minimal piano over clockwork sound design, crystalline chime accents, restrained orchestral strings with metronomic pulse",

    # ------------------------------------------------------------------
    # Banned elements
    # ------------------------------------------------------------------
    "banned_elements": [
        "fast editing or jump cuts",
        "casual everyday settings or mundane backgrounds",
        "visible fingerprints, smudges, or dust on metal or glass",
        "cheap or uncontrolled reflections in polished surfaces",
        "harsh flat overhead lighting",
        "cluttered or busy backgrounds",
        "handheld camera shake",
        "text-heavy lower thirds or price callouts",
        "comedic or slapstick tone",
        "stock-footage lifestyle filler",
    ],

    # ------------------------------------------------------------------
    # Prompt modifiers (20+)
    # ------------------------------------------------------------------
    "prompt_modifiers": [
        "haute horlogerie photography, museum-quality display lighting",
        "diamond fire and brilliance visible through precise illumination",
        "polished metal mirror finish reflecting controlled environment",
        "Swiss movement mechanism through exhibition caseback",
        "black velvet background with deep velvety shadows",
        "macro detail resolving every facet and inclusion",
        "sapphire crystal anti-reflective coating visible",
        "warm gold luster on brushed and polished surfaces",
        "platinum cool silver sheen under neutral daylight balance",
        "Cartier campaign opulence and timeless elegance",
        "Rolex Oyster Perpetual precision and authority",
        "ruby and emerald saturated color depth rendering",
        "wrist shot on dark marble with shallow depth of field",
        "crown knurling and case profile detail",
        "chronograph subdial precision engineering",
        "pearl nacre iridescent luster shifting with angle",
        "pavé diamond micro-setting catching light uniformly",
        "clasp deployment mechanism engineering beauty",
        "heritage complication — tourbillon, perpetual calendar, minute repeater",
        "obsidian reflective surface with controlled gradient falloff",
        "guilloche dial pattern under raking light",
        "titanium matte texture contrasting polished bezel",
        "gemstone halo setting radiating brilliance",
        "art deco geometric motifs in jewelry design",
    ],

    # ------------------------------------------------------------------
    # Video modifiers (10+)
    # ------------------------------------------------------------------
    "video_modifiers": [
        "single light source sweeping across dial indices revealing each marker",
        "slow 360-degree rotation on turntable showing every angle",
        "second hand ticking with audible precision click",
        "diamond catching directional light and scattering spectral fire",
        "deployant clasp opening and closing in smooth mechanical motion",
        "tourbillon cage rotating through exhibition caseback",
        "crown being pulled to position two and slowly wound",
        "light refracting through gemstone facets casting prismatic patterns on surface",
        "bracelet links articulating like liquid metal as product is laid flat",
        "watch placed on velvet cushion with controlled gentle impact",
        "engraving tool cutting fine lines into caseback in macro",
        "gemstone tester probe touching diamond with green confirmation glow",
    ],

    # ------------------------------------------------------------------
    # Reference brands
    # ------------------------------------------------------------------
    "reference_brands": [
        "Cartier",
        "Rolex",
        "Tiffany & Co.",
        "Bulgari",
        "Patek Philippe",
        "Audemars Piguet",
        "Harry Winston",
        "Van Cleef & Arpels",
        "Chopard",
        "Omega",
        "Jaeger-LeCoultre",
        "Graff",
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
