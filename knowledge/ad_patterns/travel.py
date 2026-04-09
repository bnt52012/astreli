"""Travel and hospitality industry advertising patterns.

Defines the canonical visual language for luxury travel, airline, and
destination-tourism advertising.  Inspired by Four Seasons, Airbnb, Emirates,
and National Geographic: epic landscapes bathed in golden light, immersive
cultural moments, and a pervasive sense of wanderlust and freedom.
"""

TRAVEL_PATTERN = {
    "industry": "travel",

    # ------------------------------------------------------------------
    # Scene flow
    # ------------------------------------------------------------------
    "scene_flow": [
        {
            "archetype": "aerial_reveal",
            "duration": 5.0,
            "description": "Breathtaking drone ascent over destination — coastline, "
                           "mountain range, or ancient city at golden hour",
        },
        {
            "archetype": "arrival",
            "duration": 4.0,
            "description": "Traveler stepping off a boat, through an archway, "
                           "or onto a sun-drenched terrace for the first time",
        },
        {
            "archetype": "culture_detail",
            "duration": 3.0,
            "description": "Close-up of local craft, spice market colors, "
                           "hand-thrown pottery, or street food preparation",
        },
        {
            "archetype": "immersion",
            "duration": 4.0,
            "description": "Full-body experience — swimming in a cenote, hiking "
                           "a ridge trail, or riding a tuk-tuk through old streets",
        },
        {
            "archetype": "landscape_shift",
            "duration": 3.5,
            "description": "New location or dramatic time-of-day change — "
                           "sunrise desert dunes or twilight harbor lights",
        },
        {
            "archetype": "connection",
            "duration": 3.5,
            "description": "Genuine human moment — sharing a meal with locals, "
                           "laughing with a guide, or quiet couple on a balcony",
        },
        {
            "archetype": "climax_golden",
            "duration": 4.5,
            "description": "Hero landscape at peak golden hour — silhouette on "
                           "a cliff, infinity pool edge, or hot-air balloon at dawn",
        },
        {
            "archetype": "endframe",
            "duration": 3.0,
            "description": "Brand logo over lingering wide shot, destination "
                           "name and call-to-action fade in",
        },
    ],

    # ------------------------------------------------------------------
    # Visual signature
    # ------------------------------------------------------------------
    "visual_signature": {
        "color_temperature": "warm 5200-6000K, golden bias in exteriors",
        "contrast": "medium-high, rich tonal range for landscape depth",
        "saturation": "vibrant but natural — sky blues, terracotta, emerald foliage",
        "grain": "subtle organic grain for documentary authenticity",
        "depth_of_field": "deep f/8-f/11 landscapes, shallow f/2 for cultural details",
        "color_grade": "warm shadows, lifted blacks, sun-kissed highlight roll-off",
    },

    # ------------------------------------------------------------------
    # Lighting — keys from the canonical lighting_setups registry
    # ------------------------------------------------------------------
    "lighting_preferences": [
        "golden_hour",
        "blue_hour",
        "overcast_diffused",
        "backlit",
        "silhouette",
        "candle_firelight",
        "harsh_noon",
        "fog_haze",
        "window_light_soft",
        "moonlight_cool",
    ],

    # ------------------------------------------------------------------
    # Lens — keys from the canonical lens registry
    # ------------------------------------------------------------------
    "lens_preferences": [
        "wide_16mm",
        "wide_24mm",
        "standard_50mm_f18",
        "zoom_70_200mm",
        "ultra_wide_14mm",
        "classic_35mm",
        "anamorphic_75mm",
    ],

    # ------------------------------------------------------------------
    # Movement
    # ------------------------------------------------------------------
    "movement_style": {
        "camera": "sweeping aerial drone, smooth gimbal tracking walk-and-reveal, "
                  "slow crane rise, locked-off landscape wide",
        "subject": "walking into frame, gazing outward, hands touching textures, "
                   "spontaneous exploration gestures",
        "pacing": "unhurried discovery building to awe, breath-hold wide shots",
    },

    # ------------------------------------------------------------------
    # Transitions (ordered by preference)
    # ------------------------------------------------------------------
    "transition_preferences": [
        "cross-dissolve",
        "light leak fade",
        "aerial-to-aerial match move",
        "slow fade to black",
        "whip pan",
        "sun flare wipe",
    ],

    # ------------------------------------------------------------------
    # Audio
    # ------------------------------------------------------------------
    "music_style": (
        "world-instrument acoustic bed, warm indie folk guitar, ambient nature "
        "soundscape layered beneath — waves, birdsong, market chatter — building "
        "to an uplifting orchestral or choral swell at the climax"
    ),

    # ------------------------------------------------------------------
    # Banned elements
    # ------------------------------------------------------------------
    "banned_elements": [
        "overcrowded tourist-trap angles",
        "sterile corporate hotel marketing aesthetic",
        "passport and boarding-pass cliche props",
        "grey overcast flat-light weather",
        "stressed or rushed travel montages",
        "selfie-stick or phone-screen-in-frame shots",
        "overly posed model-catalogue body language",
        "stock watermark or low-resolution plates",
        "neon or artificial-colored lighting on nature",
        "luggage brand product placement",
    ],

    # ------------------------------------------------------------------
    # Prompt modifiers (20+)
    # ------------------------------------------------------------------
    "prompt_modifiers": [
        "National Geographic travel photography, editorial crop",
        "breathtaking landscape panorama, infinite depth",
        "golden hour destination photography, long warm shadows",
        "authentic local culture moment, unposed candid",
        "crystal-clear tropical water, visible coral detail",
        "ancient architecture dramatic low-angle perspective",
        "aerial drone sweeping coastal vista, parallax depth",
        "traveler silhouette against molten sunset sky",
        "exotic spice-market color explosion, shallow focus",
        "snow-capped peak above cloud inversion layer",
        "infinity pool vanishing edge overlooking ocean",
        "cobblestone European village, morning mist rising",
        "Saharan dune ripple pattern, raking sidelight",
        "overwater bungalow turquoise lagoon, Maldives tone",
        "northern lights aurora borealis curtain, wide field",
        "cherry blossom canopy, soft pink backlight",
        "African safari vehicle, golden grassland, telephoto compression",
        "Mediterranean whitewashed cliffside village, blue dome accent",
        "misty jungle waterfall, verdant fern foreground frame",
        "Conde Nast Traveler cover quality, aspirational mood",
        "rice terrace aerial, geometric green pattern",
        "night market lantern bokeh, warm amber highlights",
    ],

    # ------------------------------------------------------------------
    # Video modifiers (10+)
    # ------------------------------------------------------------------
    "video_modifiers": [
        "drone ascending from canopy to reveal vast landscape",
        "turquoise waves crashing on white-sand shore, slow motion",
        "traveler walking through ancient stone archway into light",
        "time-lapse sunset painting sky magenta to indigo",
        "longtail boat gliding across glass-still emerald water",
        "hot-air balloon lifting off at dawn, basket shadow on field",
        "train winding through alpine valley, window reflections",
        "aurora borealis curtain shimmering across star field",
        "palm fronds swaying in warm trade wind, lens flare peaking",
        "open-air market scene, fabrics billowing, spices pouring",
        "campfire sparks rising into Milky Way sky, slow motion",
    ],

    # ------------------------------------------------------------------
    # Reference brands
    # ------------------------------------------------------------------
    "reference_brands": [
        "Four Seasons",
        "Airbnb",
        "Emirates",
        "National Geographic Expeditions",
        "Aman Resorts",
        "Singapore Airlines",
        "Lonely Planet",
        "Virtuoso",
        "Belmond",
        "Six Senses",
        "Condé Nast Traveler",
        "SWISS International Air Lines",
    ],

    # ------------------------------------------------------------------
    # Typical durations (seconds)
    # ------------------------------------------------------------------
    "typical_durations": {
        "15s": 15,
        "30s": 30,
        "45s": 45,
        "60s": 60,
    },
}
