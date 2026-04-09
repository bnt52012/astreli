"""
Fashion advertising patterns.

Covers ready-to-wear, streetwear, haute couture, athleisure, denim,
and seasonal collection campaigns.
Reference campaigns: Zara, Balenciaga, Nike (fashion collabs),
Jacquemus, COS, Acne Studios, Prada.
"""

PATTERNS: dict = {
    "scene_flow": [
        {
            "scene_type": "mood_establish",
            "typical_duration": "2-4s",
            "purpose": "Set the world of the collection — an urban rooftop, an empty gallery, a sun-bleached Mediterranean alley, or a brutalist parking structure. Location IS the mood board.",
        },
        {
            "scene_type": "full_look_reveal",
            "typical_duration": "3-5s",
            "purpose": "Head-to-toe outfit shown in motion — a confident walk, a turn, a stride. The garment must move to communicate drape, fit, and silhouette.",
        },
        {
            "scene_type": "detail_insert",
            "typical_duration": "1-3s",
            "purpose": "Tight shot of a design detail — stitching, hardware, a label, fabric texture, a zipper pull. Communicates craftsmanship and intentionality.",
        },
        {
            "scene_type": "editorial_pose",
            "typical_duration": "2-4s",
            "purpose": "A styled, composed moment — the model in a striking pose against a graphic backdrop. This is the frame that becomes the campaign image.",
        },
        {
            "scene_type": "movement_energy",
            "typical_duration": "2-4s",
            "purpose": "Dynamic motion — running, dancing, spinning, jumping. Fabric in flight, hair catching wind, garments revealing their construction through movement.",
        },
        {
            "scene_type": "group_styling",
            "typical_duration": "3-5s",
            "purpose": "Multiple looks together — a crew walking in formation, friends in a car, a lineup against a wall. Shows the range of the collection and community.",
        },
        {
            "scene_type": "brand_identity",
            "typical_duration": "2-3s",
            "purpose": "Collection name, season, logo. Often typographically bold, sometimes overlaid on the final lifestyle frame.",
        },
    ],
    "visual_signature": {
        "color_temperature": "Variable by collection mood. Cool and desaturated for avant-garde. Warm and sun-drenched for resort/summer. Neutral-accurate for commercial.",
        "contrast": "Medium to high. Fashion tolerates — even celebrates — harder contrast than beauty or luxury. Deep shadows can add drama and edge.",
        "saturation": "Depends on brand position. Editorial fashion often desaturates. Streetwear pops colors. High fashion mutes to near-monochrome. Always intentional, never default.",
        "grain": "Moderate grain is welcomed, especially for editorial and streetwear. Can reference 35mm film (Portra 400, Tri-X) or Polaroid aesthetics. Adds raw authenticity.",
        "depth_of_field": "Variable. Shallow for portrait-driven campaigns, deeper for environmental/street shots where context matters. f/2.8-f/5.6 range.",
    },
    "lighting_preferences": [
        {
            "name": "Hard direct sunlight",
            "description": "Unfiltered sun creating sharp shadows and bright highlights. The look of a spontaneous street shoot. Authentic, raw, and unapologetic.",
        },
        {
            "name": "Overcast editorial",
            "description": "Flat, even daylight under cloud cover. No shadows. Colors are muted and true. The signature Scandinavian-fashion look.",
        },
        {
            "name": "Single bare bulb",
            "description": "One exposed tungsten or LED source creating a point-light effect. Hard shadows, dramatic fall-off. Industrial and edgy.",
        },
        {
            "name": "Neon and mixed color",
            "description": "Colored neon signs, LED panels, and urban light pollution as the light source. Creates split-color effects on skin and fabric. Streetwear and nightlife.",
        },
        {
            "name": "Softbox editorial",
            "description": "Large studio softbox at 45 degrees for controlled, flattering light that still has direction and shape. The commercial fashion standard.",
        },
        {
            "name": "Dappled natural light",
            "description": "Sunlight filtered through trees, blinds, or architectural elements creating patterns of light and shadow across the body and garment.",
        },
        {
            "name": "Strobe freeze",
            "description": "High-power strobe freezing fast motion — fabric mid-flow, hair mid-whip, a jump at apex. Sharp and dynamic.",
        },
        {
            "name": "Backlit silhouette",
            "description": "Strong backlight rendering the model as a silhouette or near-silhouette. Emphasizes silhouette and body line over detail.",
        },
    ],
    "lens_preferences": [
        {
            "focal_length": "35mm",
            "aperture": "f/2.0",
            "use_case": "Street-style and environmental fashion. Captures the model in context — the city, the architecture, the energy.",
        },
        {
            "focal_length": "50mm",
            "aperture": "f/1.4",
            "use_case": "The classic fashion lens. Natural perspective, fast enough for any light. Works for everything from lookbook to editorial.",
        },
        {
            "focal_length": "85mm",
            "aperture": "f/1.8",
            "use_case": "Half-body and portrait framing. Beautiful subject separation. The go-to for campaign hero shots.",
        },
        {
            "focal_length": "24mm",
            "aperture": "f/2.8",
            "use_case": "Wide environmental shots, group styling, architectural context. Slight wide-angle energy without fisheye distortion.",
        },
        {
            "focal_length": "135mm",
            "aperture": "f/2.0",
            "use_case": "Runway and compressed street shots. Stacks background elements for graphic compositions.",
        },
        {
            "focal_length": "28mm",
            "aperture": "f/2.0",
            "use_case": "Documentary-style fashion. Close-quarters shooting with environmental context. The Terry Richardson / Juergen Teller aesthetic.",
        },
    ],
    "movement_style": {
        "camera_movement": "Energetic and varied. Tracking shots following a walking model, handheld following a run, smooth Steadicam orbits, and occasional snap-zooms or whip pans for editorial energy.",
        "subject_movement": "Confident and expressive. Walking with purpose, hair flips, garment adjustments, leaning against walls, lounging with attitude. Movement should show how the clothing lives on a body.",
        "pacing": "Fast editorial cuts (0.5-2s per shot) interspersed with held beauty moments (3-4s). The rhythm should feel like a playlist — verses and choruses.",
    },
    "transition_preferences": [
        "Hard cut on the beat — the dominant fashion-film transition. Clean, decisive, rhythmic.",
        "Jump cut within a single pose sequence — editorial energy, time compression, attitude.",
        "Whip pan connecting two locations or two outfits — physical energy as transition.",
        "Flash frame — a single white or colored frame between cuts for strobe-like punctuation.",
        "Split screen or tiled grid showing multiple looks simultaneously.",
        "Graphic wipe with typography or brand element sweeping across the frame.",
    ],
    "music_style": {
        "tempo": "100-140 BPM. Driving but not aggressive. Should make you want to walk with confidence.",
        "instruments": "Deep bass, crisp hi-hats, minimal synths, filtered vocals, sampled textures. Electronic but with organic undertones. Think fashion-show soundtrack.",
        "mood": "Cool, confident, slightly aloof. The energy of walking into a room and owning it. Can range from moody and dark to bright and playful depending on the collection.",
        "avoid": "Generic pop, cheesy EDM, anything that sounds like a shopping-mall playlist. Also avoid overly somber classical unless explicitly avant-garde.",
    },
    "banned_elements": [
        "Stiff, awkward posing — models must look natural and confident, never like mannequins.",
        "Wrinkled or ill-fitting garments — every piece must be steamed and styled to perfection.",
        "Cluttered or distracting backgrounds that compete with the clothing.",
        "Overly retouched skin that looks plastic — fashion celebrates character and individuality.",
        "Dutch angles or extreme tilts used without editorial intent.",
        "Low-quality fabric textures that look synthetic or cheap.",
        "Dated styling references (unless intentionally retro with clear creative direction).",
        "Generic model expressions — vacant stares without intention or purpose.",
        "Visible tags, pins, or styling clips left in frame by accident.",
        "Harsh on-camera flash without artistic intent (paparazzi look when not desired).",
        "Static, lifeless flat-lays without styling or context.",
        "Mismatched color temperatures between lighting sources (unless intentionally mixed).",
    ],
    "prompt_modifiers": [
        "high fashion editorial photography, Vogue Italia aesthetic",
        "shot on 35mm film, Kodak Portra 400 color rendition",
        "hard sunlight casting sharp geometric shadows on model",
        "confident model stride, garment in motion, fabric flowing",
        "brutalist concrete architecture as fashion backdrop",
        "overcast Scandinavian light, muted tones, minimal styling",
        "streetwear editorial, urban environment, neon at night",
        "tight crop on garment construction detail, visible stitching",
        "group fashion editorial, diverse models, coordinated collection",
        "graphic composition, strong leading lines, architectural framing",
        "raw editorial aesthetic, imperfect and authentic, film grain",
        "lookbook-style clean shot, full outfit head to toe",
        "motion blur on walking figure, sense of speed and confidence",
        "color-blocked backdrop matching garment accent color",
        "editorial pose against minimal white wall, strong shadow play",
        "layered outfit detail, texture contrast between fabrics",
        "night-shoot fashion editorial, city lights and reflections",
        "haute couture atelier setting, behind-the-scenes craftsmanship",
        "sun-drenched resort collection, warm Mediterranean palette",
        "monochrome fashion story, black and white with deep contrast",
    ],
    "video_modifiers": [
        "tracking shot following model walking through urban corridor",
        "120fps slow motion fabric movement, silk catching air",
        "rhythmic hard cuts synced to music beat, editorial pacing",
        "handheld close-follow documentary style, raw energy",
        "smooth Steadicam orbit around a posed model, 360-degree reveal",
        "whip pan transition between outfit changes, same location",
        "split-screen two models walking in parallel, synchronized",
        "strobe-lit freeze frames within continuous motion sequence",
        "drone pull-back from street-level model to cityscape context",
        "snap zoom from wide establishing to tight detail in single shot",
    ],
}
