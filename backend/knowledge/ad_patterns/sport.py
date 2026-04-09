"""
Sport and athletic advertising patterns.

Covers athletic apparel, fitness equipment, sports nutrition,
outdoor/adventure, and performance lifestyle brands.
Reference campaigns: Nike, Adidas, Under Armour, The North Face,
Gatorade, Peloton, GoPro, Patagonia.
"""

PATTERNS: dict = {
    "scene_flow": [
        {
            "scene_type": "arena_establish",
            "typical_duration": "2-4s",
            "purpose": "Set the stage — a stadium at dawn, a mountain trail in mist, a gritty gym, an empty track. Establish the arena where greatness happens.",
        },
        {
            "scene_type": "preparation_ritual",
            "typical_duration": "3-5s",
            "purpose": "The pre-performance ritual — lacing shoes, chalking hands, stretching, a deep breath. Builds anticipation and humanizes the athlete.",
        },
        {
            "scene_type": "peak_performance",
            "typical_duration": "3-6s",
            "purpose": "The explosive moment — a sprint, a dunk, a flip, a summit reach. Maximum physical intensity captured in dramatic slow motion or dynamic angles.",
        },
        {
            "scene_type": "detail_and_tech",
            "typical_duration": "2-3s",
            "purpose": "Close-up of product technology — sole flex, fabric stretch, moisture wicking, cushioning compression. Communicates innovation and engineering.",
        },
        {
            "scene_type": "grit_and_sweat",
            "typical_duration": "2-4s",
            "purpose": "Raw, visceral close-ups — sweat dripping, muscles straining, breath visible in cold air, dirt on knees. Authenticity and effort.",
        },
        {
            "scene_type": "triumph_moment",
            "typical_duration": "2-4s",
            "purpose": "The emotional peak — crossing the finish line, a fist pump, a team celebration, collapsing in relief. The payoff of all the effort.",
        },
        {
            "scene_type": "product_hero",
            "typical_duration": "2-3s",
            "purpose": "Product isolated or in context, paired with the performance moment. The shoe on the track, the jacket on the summit, the bottle mid-pour.",
        },
        {
            "scene_type": "motivational_close",
            "typical_duration": "2-3s",
            "purpose": "Brand mark with a tagline or call-to-action. Often over a final wide shot or fading athlete silhouette. Inspirational punctuation.",
        },
    ],
    "visual_signature": {
        "color_temperature": "Variable and environment-driven. Cool blue for dawn/night training. Warm amber for golden-hour outdoor. Neutral for studio/gym. Often pushed toward teal-orange color grading.",
        "contrast": "High. Deep blacks, punchy highlights. Sport imagery demands energy and visual impact. Shadows are used for drama, not subtlety.",
        "saturation": "Moderate to high on hero colors (brand colors, sky, skin), selectively desaturated on backgrounds. Cross-processed or bleach-bypass looks are common.",
        "grain": "Low to moderate. Clean for technology-focused product shots. Grittier grain for documentary-style training montages. Never distractingly noisy.",
        "depth_of_field": "Varies by scene. Ultra-shallow for emotional close-ups (f/1.4-f/2.0). Deep for action sequences where environment matters (f/5.6-f/11). Often uses selective focus to isolate athletes in crowds.",
    },
    "lighting_preferences": [
        {
            "name": "Rim-light hero",
            "description": "Strong backlight or three-quarter backlight creating a bright rim around the athlete's body. Separates the figure from a dark background. The signature sport-hero look.",
        },
        {
            "name": "Dawn / dusk natural",
            "description": "Low-angle golden or blue-hour sunlight. Long shadows, warm skin tones, dramatic sky. The 'training at sunrise' aesthetic.",
        },
        {
            "name": "Overhead stadium",
            "description": "High-output top-light simulating stadium or arena flood lights. Creates intense, slightly harsh illumination with sharp downward shadows.",
        },
        {
            "name": "Gym practical lights",
            "description": "Industrial fluorescents, hanging utility lights, and window light filtered through grime. Authentic gym atmosphere — gritty, unpolished, real.",
        },
        {
            "name": "Cross-light drama",
            "description": "Two opposing hard sources creating a cross-shadow pattern on the body. Sculpts musculature and creates maximum three-dimensionality.",
        },
        {
            "name": "Strobe freeze action",
            "description": "High-speed flash freezing peak athletic motion — water droplets suspended, hair mid-whip, muscles at maximum tension. Razor-sharp in-motion detail.",
        },
        {
            "name": "Silhouette backlight",
            "description": "Figure rendered as pure silhouette against a bright background — sunrise, stadium lights, or colored backdrop. Iconic and universal.",
        },
        {
            "name": "Underwater caustics",
            "description": "Dappled light patterns from water surface for swimming, surfing, or water-sport content. Dynamic, organic, and unique.",
        },
        {
            "name": "Spotlight isolation",
            "description": "Single focused beam in darkness, picking out the athlete like a stage performer. Theatrical and dramatic.",
        },
    ],
    "lens_preferences": [
        {
            "focal_length": "70-200mm",
            "aperture": "f/2.8",
            "use_case": "The workhorse sport lens. Compression for drama, reach for candid action, fast aperture for shallow depth in available light.",
        },
        {
            "focal_length": "24mm",
            "aperture": "f/1.4",
            "use_case": "Wide-angle action. Close to the athlete for immersive, in-the-moment perspectives. Exaggerates speed and proximity.",
        },
        {
            "focal_length": "16mm fisheye",
            "aperture": "f/2.8",
            "use_case": "Skate, BMX, and extreme sport POV. Distorted perspective that amplifies height and speed. Used sparingly for impact.",
        },
        {
            "focal_length": "50mm",
            "aperture": "f/1.4",
            "use_case": "Intimate training moments, preparation rituals, and emotional close-ups. Natural perspective for storytelling.",
        },
        {
            "focal_length": "400mm",
            "aperture": "f/2.8",
            "use_case": "Compressed telephoto for stadium and field shots. Stacks athletes against blurred crowds and backgrounds.",
        },
        {
            "focal_length": "14-24mm",
            "aperture": "f/2.8",
            "use_case": "Ultra-wide establishing shots of arenas, landscapes, and training environments. Creates epic scale and grandeur.",
        },
    ],
    "movement_style": {
        "camera_movement": "Dynamic, athletic, and purposeful. Tracking alongside a runner, crane rising with a jump, gimbal-stabilized following through an obstacle course. The camera moves AS the athlete moves — with energy and commitment. POV and body-mounted cameras for immersive perspectives.",
        "subject_movement": "Explosive and authentic. Real athletic motion, not posed simulation. Full-speed sprints, genuine lifts, actual sport performance. Slow motion at 120-240fps to reveal the beauty and physics of peak human movement.",
        "pacing": "Fast and rhythmic for montage sequences (0.5-1.5s cuts). Slower and more deliberate for emotional and preparation scenes (3-5s holds). The rhythm mirrors a heartbeat — building to climax.",
    },
    "transition_preferences": [
        "Hard cut on impact — a foot strike, a ball hit, a punch. Physical punctuation.",
        "Speed ramp — slow motion accelerating to real-time or vice versa within a single shot.",
        "Whip pan connecting two athletes or two locations at high speed.",
        "Match cut on motion — a runner's stride becomes a swimmer's stroke becomes a cyclist's pedal.",
        "Smash cut from stillness to explosive action — the calm-before-the-storm moment.",
        "Light flash or lens flare transition — simulating the burst of stadium lights or sunrise.",
        "Graphic overlay transition with stats, timing, or typographic elements.",
    ],
    "music_style": {
        "tempo": "120-160 BPM. Driving, building, escalating. Should match the cadence of running or the rhythm of a workout.",
        "instruments": "Deep sub-bass, aggressive drums, distorted synths, epic orchestral builds, taiko drums, staccato strings. Can range from hip-hop to cinematic orchestral depending on brand.",
        "mood": "Intense, empowering, relentless. The soundtrack to pushing past your limits. Builds from quiet determination to triumphant climax.",
        "avoid": "Gentle acoustic, ambient pads, anything passive or relaxing. Also avoid generic royalty-free 'motivational' tracks that sound like every other fitness video.",
    },
    "banned_elements": [
        "Fake or poorly simulated athletic motion — the athlete must look genuinely capable.",
        "Overly clean, pristine athletes — sport advertising needs sweat, dirt, and effort.",
        "Static, posed shots that look like catalog images rather than action captures.",
        "Slow, languid pacing without energy or momentum.",
        "Weak, flat lighting that fails to sculpt the body or create drama.",
        "Obvious green-screen or composited backgrounds that break immersion.",
        "Generic stock-photo athletes with perfect hair and makeup mid-workout.",
        "Tiny text disclaimers or legal copy dominating the visual frame.",
        "Outdated equipment or clearly non-performance-grade products.",
        "Patronizing or exclusionary messaging — modern sport advertising celebrates all bodies and abilities.",
        "Music that sounds like elevator music or generic corporate background.",
        "Overly saturated or neon color grading that looks like a video game.",
    ],
    "prompt_modifiers": [
        "athletic action photography, peak performance moment captured",
        "dramatic rim lighting on athlete, dark moody background",
        "slow motion water and sweat droplets frozen mid-air",
        "dawn training session, golden hour backlight on track",
        "gritty gym environment, chalk dust and iron textures",
        "extreme close-up of muscle definition under strain",
        "dynamic low-angle hero shot looking up at athlete",
        "trail running through misty mountain landscape at sunrise",
        "stadium atmosphere, flood lights creating hard top shadows",
        "cross-light sculpting athletic physique, high contrast",
        "authentic mid-action sports capture, genuine intensity",
        "product detail showing material technology and construction",
        "silhouette athlete against dramatic sky, epic scale",
        "underwater photography, dynamic swimmer with caustic light",
        "team huddle or celebration, authentic emotional connection",
        "shoe or equipment detail on textured surface, studio lit",
        "explosive starting-block launch, frozen with strobe flash",
        "endurance and determination, face showing effort and focus",
        "teal and orange color grade, cinematic sport film look",
        "POV action perspective, immersive first-person athletic viewpoint",
    ],
    "video_modifiers": [
        "240fps extreme slow motion capturing athletic impact moment",
        "speed ramp from slow motion to real-time explosive action",
        "gimbal tracking shot following runner at full sprint",
        "drone ascending reveal from athlete to epic landscape",
        "rapid-fire montage of training moments cut to beat drops",
        "POV body-mounted camera through obstacle course or trail",
        "crane shot rising with athlete's vertical jump or climb",
        "match-cut sequence linking different sports in continuous motion",
        "parallax reveal of product technology with animated cross-section",
        "countdown timer overlay building tension to start of action",
    ],
}
