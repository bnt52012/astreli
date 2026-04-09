"""
Scene Archetypes — 25 canonical advertising scene types with full technical specifications.

Each archetype defines optimal duration, camera movements, transitions, lighting setups,
lens choices, prompt templates, modifiers, and industry applicability. These archetypes
serve as building blocks for automated ad sequence generation.

Archetype keys match the canonical names used throughout the pipeline:
    product_hero_shot, lifestyle_context, model_portrait_closeup, product_interaction,
    environment_establishing, macro_detail, motion_action, unboxing_reveal,
    silhouette_artistic, pov_first_person, hands_only, ingredient_component,
    before_after_transform, split_screen, slow_motion_moment, time_lapse,
    reflection_mirror, aerial_drone, social_group, behind_the_scenes,
    text_overlay_title, packshot_endframe, scale_comparison, seasonal_holiday,
    call_to_action
"""

SCENE_ARCHETYPES = {

    # ─────────────────────────────────────────────
    # 1. PRODUCT HERO SHOT
    # ─────────────────────────────────────────────
    "product_hero_shot": {
        "name": "Product Hero Shot",
        "description": (
            "The product commands full attention with dramatic lighting, a clean or "
            "gradient background, and premium composition. This is the money shot."
        ),
        "optimal_duration_range": (3, 6),
        "recommended_camera_movements": [
            "slow_orbit",
            "push_in",
            "static",
            "crane_up",
        ],
        "recommended_transitions_in": ["dissolve", "fade_from_black", "light_wipe"],
        "recommended_transitions_out": ["dissolve", "fade_to_black", "cut"],
        "recommended_lighting": [
            "three_point",
            "rim_light",
            "product_dark_field",
            "product_light_field",
            "chiaroscuro",
        ],
        "recommended_lenses": [
            "standard_50mm_f14",
            "portrait_85mm_f14",
            "macro_100mm",
            "tilt_shift_24mm",
        ],
        "gemini_prompt_template": (
            "A stunning hero shot of {product} centered against a {background} background. "
            "{lighting_description}. The product gleams with {material_quality}, "
            "photographed at eye level with shallow depth of field. {style_notes}"
        ),
        "kling_prompt_template": (
            "Camera slowly orbits around {product} on a {background} surface. "
            "Light sweeps across the product revealing {material_quality}. "
            "Smooth, cinematic, 4K quality. {motion_notes}"
        ),
        "image_modifiers": [
            "dramatic product hero lighting",
            "premium surface reflections",
            "studio-quality color rendering",
            "razor-sharp focus on product",
            "luxurious material texture",
        ],
        "video_modifiers": [
            "slow rotation revealing all angles",
            "light sweep across surface highlights",
            "smooth cinematic orbit",
        ],
        "industries": [
            "luxury", "beauty", "tech", "automotive", "jewelry_watches",
            "fragrance", "fashion", "food_beverage",
        ],
    },

    # ─────────────────────────────────────────────
    # 2. LIFESTYLE CONTEXT
    # ─────────────────────────────────────────────
    "lifestyle_context": {
        "name": "Lifestyle Context",
        "description": (
            "The product or model placed within an aspirational real-world setting. "
            "Environment tells the brand story and anchors the product in daily life."
        ),
        "optimal_duration_range": (3, 6),
        "recommended_camera_movements": [
            "tracking",
            "pan_right",
            "pan_left",
            "static",
            "dolly_in",
        ],
        "recommended_transitions_in": ["dissolve", "cut", "wipe"],
        "recommended_transitions_out": ["dissolve", "cut"],
        "recommended_lighting": [
            "golden_hour",
            "window_light_soft",
            "overcast_diffused",
            "three_point",
            "high_key",
        ],
        "recommended_lenses": [
            "classic_35mm",
            "standard_50mm_f14",
            "wide_24mm",
            "zoom_24_70mm",
        ],
        "gemini_prompt_template": (
            "{subject} in a {environment} setting, naturally interacting with {product}. "
            "{lighting_description}. The scene feels authentic and aspirational, "
            "with {environment_details} visible in the background. {style_notes}"
        ),
        "kling_prompt_template": (
            "Camera gently tracks {subject} moving through {environment}. "
            "Natural ambient light. {product} is visible and contextually placed. "
            "Cinematic color grading. {motion_notes}"
        ),
        "image_modifiers": [
            "lifestyle context photography",
            "natural environment setting",
            "aspirational scene composition",
            "authentic lived-in feel",
            "editorial quality framing",
        ],
        "video_modifiers": [
            "natural movement through environment",
            "gentle camera tracking with parallax",
            "ambient environmental motion",
        ],
        "industries": [
            "fashion", "beauty", "food_beverage", "travel", "real_estate",
            "sport", "tech", "luxury",
        ],
    },

    # ─────────────────────────────────────────────
    # 3. MODEL PORTRAIT CLOSEUP
    # ─────────────────────────────────────────────
    "model_portrait_closeup": {
        "name": "Model Portrait Closeup",
        "description": (
            "Tight framing on the model's face or upper body, emphasizing emotion, "
            "beauty, and connection. Skin texture and expression are paramount."
        ),
        "optimal_duration_range": (2, 5),
        "recommended_camera_movements": [
            "static",
            "slow_push_in",
            "subtle_drift",
        ],
        "recommended_transitions_in": ["dissolve", "cut"],
        "recommended_transitions_out": ["dissolve", "cut"],
        "recommended_lighting": [
            "rembrandt",
            "butterfly",
            "beauty_dish",
            "ring_light",
            "clamshell",
            "loop",
            "window_light_soft",
        ],
        "recommended_lenses": [
            "portrait_85mm_f14",
            "telephoto_135mm",
            "standard_50mm_f14",
            "petzval",
            "helios_44_2",
        ],
        "gemini_prompt_template": (
            "Close-up portrait of {model_description}, {expression} expression. "
            "{lighting_description}. Shallow depth of field with {background_treatment}. "
            "Skin rendered with natural clarity. {style_notes}"
        ),
        "kling_prompt_template": (
            "Camera holds a close-up on {model_description}'s face. "
            "Subtle {expression} expression shift. {lighting_description}. "
            "Gentle eye movement, natural breathing motion. {motion_notes}"
        ),
        "image_modifiers": [
            "portrait photography with catch lights",
            "sharp focus on eyes",
            "flattering beauty lighting",
            "natural skin texture rendering",
            "creamy bokeh background",
        ],
        "video_modifiers": [
            "subtle head turn or expression change",
            "gentle eye movement with natural blinks",
            "slow push-in building intimacy",
        ],
        "industries": [
            "beauty", "fashion", "fragrance", "jewelry_watches", "luxury",
        ],
    },

    # ─────────────────────────────────────────────
    # 4. PRODUCT INTERACTION
    # ─────────────────────────────────────────────
    "product_interaction": {
        "name": "Product Interaction",
        "description": (
            "A model actively engages with the product — holding, applying, tasting, "
            "or demonstrating. The interaction communicates use and desirability."
        ),
        "optimal_duration_range": (3, 5),
        "recommended_camera_movements": [
            "zoom_in",
            "static",
            "tracking",
            "dolly_in",
        ],
        "recommended_transitions_in": ["cut", "dissolve"],
        "recommended_transitions_out": ["cut", "dissolve"],
        "recommended_lighting": [
            "three_point",
            "window_light_soft",
            "beauty_dish",
            "high_key",
            "overcast_diffused",
        ],
        "recommended_lenses": [
            "standard_50mm_f14",
            "zoom_24_70mm",
            "portrait_85mm_f14",
            "classic_35mm",
        ],
        "gemini_prompt_template": (
            "{model_description} {interaction_verb} {product} with natural ease. "
            "{lighting_description}. Medium shot framing shows both the model's "
            "expression and the product clearly. {style_notes}"
        ),
        "kling_prompt_template": (
            "{model_description} reaches for and {interaction_verb} {product}. "
            "Camera slowly pushes in to frame the interaction. "
            "Natural, deliberate gesture. {motion_notes}"
        ),
        "image_modifiers": [
            "natural product interaction captured",
            "hands and product well-lit",
            "authentic gesture mid-action",
            "clean medium-shot framing",
            "editorial product placement",
        ],
        "video_modifiers": [
            "natural gesture animation with product",
            "deliberate product manipulation",
            "camera push-in following the action",
        ],
        "industries": [
            "beauty", "food_beverage", "tech", "fashion", "sport",
            "luxury", "fragrance",
        ],
    },

    # ─────────────────────────────────────────────
    # 5. ENVIRONMENT ESTABLISHING
    # ─────────────────────────────────────────────
    "environment_establishing": {
        "name": "Environment Establishing Shot",
        "description": (
            "A wide shot that sets the scene, establishing location, mood, and "
            "narrative context before the viewer meets the product or subject."
        ),
        "optimal_duration_range": (3, 7),
        "recommended_camera_movements": [
            "pan_right",
            "pan_left",
            "crane_up",
            "dolly_out",
            "static",
        ],
        "recommended_transitions_in": ["fade_from_black", "dissolve", "wipe"],
        "recommended_transitions_out": ["dissolve", "cut"],
        "recommended_lighting": [
            "golden_hour",
            "blue_hour",
            "overcast_diffused",
            "cinematic_teal_orange",
            "fog_haze",
        ],
        "recommended_lenses": [
            "wide_24mm",
            "ultra_wide_14mm",
            "zoom_24_70mm",
            "anamorphic_50mm",
            "tilt_shift_24mm",
        ],
        "gemini_prompt_template": (
            "Wide establishing shot of {environment}. {lighting_description}. "
            "The scene conveys {mood} with {environment_details}. "
            "Cinematic composition with leading lines. {style_notes}"
        ),
        "kling_prompt_template": (
            "Camera slowly pans across {environment}, revealing the full scope of the location. "
            "{lighting_description}. Atmospheric depth with layered planes. {motion_notes}"
        ),
        "image_modifiers": [
            "wide cinematic establishing shot",
            "dramatic landscape composition",
            "atmospheric depth and scale",
            "leading lines guiding the eye",
            "environmental storytelling",
        ],
        "video_modifiers": [
            "slow pan or tilt revealing environment",
            "parallax between foreground and background layers",
            "atmospheric haze adding depth",
        ],
        "industries": [
            "travel", "real_estate", "automotive", "luxury", "fashion",
            "sport", "food_beverage",
        ],
    },

    # ─────────────────────────────────────────────
    # 6. MACRO DETAIL
    # ─────────────────────────────────────────────
    "macro_detail": {
        "name": "Macro Detail",
        "description": (
            "Extreme close-up revealing texture, craftsmanship, material quality, "
            "or ingredient purity that the naked eye might miss."
        ),
        "optimal_duration_range": (2, 4),
        "recommended_camera_movements": [
            "slow_push_in",
            "rack_focus",
            "static",
            "lateral_slide",
        ],
        "recommended_transitions_in": ["dissolve", "cut"],
        "recommended_transitions_out": ["dissolve", "cut"],
        "recommended_lighting": [
            "raking_texture",
            "product_backlit_glow",
            "rim_light",
            "tabletop_product",
            "product_light_field",
        ],
        "recommended_lenses": [
            "macro_100mm",
            "telephoto_135mm",
            "portrait_85mm_f14",
            "tilt_shift_24mm",
        ],
        "gemini_prompt_template": (
            "Extreme macro close-up of {detail_subject} on {product}. "
            "{lighting_description}. Every {texture_type} is rendered with forensic clarity. "
            "Razor-thin depth of field. {style_notes}"
        ),
        "kling_prompt_template": (
            "Camera glides across the surface of {product}, revealing {detail_subject} "
            "in extreme close-up. Rack focus shifts between texture planes. {motion_notes}"
        ),
        "image_modifiers": [
            "macro photography at extreme magnification",
            "texture and material detail visible",
            "razor-thin depth of field",
            "raking light across surface",
            "forensic clarity on craftsmanship",
        ],
        "video_modifiers": [
            "slow pull-focus through detail planes",
            "camera gliding across textured surface",
            "micro-movements revealing material quality",
        ],
        "industries": [
            "jewelry_watches", "beauty", "food_beverage", "luxury",
            "tech", "fashion", "automotive",
        ],
    },

    # ─────────────────────────────────────────────
    # 7. MOTION ACTION
    # ─────────────────────────────────────────────
    "motion_action": {
        "name": "Motion / Action",
        "description": (
            "Dynamic movement scene — running, jumping, dancing, driving, or sports. "
            "Energy, momentum, and physicality define the frame."
        ),
        "optimal_duration_range": (2, 5),
        "recommended_camera_movements": [
            "tracking",
            "handheld",
            "whip_pan",
            "crane_down",
            "dolly_in",
        ],
        "recommended_transitions_in": ["cut", "whip_pan", "smash_cut"],
        "recommended_transitions_out": ["cut", "smash_cut", "dissolve"],
        "recommended_lighting": [
            "cinematic_teal_orange",
            "backlit",
            "rim_light",
            "golden_hour",
            "high_key",
        ],
        "recommended_lenses": [
            "zoom_24_70mm",
            "wide_24mm",
            "zoom_70_200mm",
            "classic_35mm",
            "anamorphic_50mm",
        ],
        "gemini_prompt_template": (
            "{subject} in dynamic motion — {action_description}. "
            "{lighting_description}. Frozen at peak action with {motion_quality}. "
            "Wide dynamic composition. {style_notes}"
        ),
        "kling_prompt_template": (
            "{subject} bursts into {action_description}. Camera tracks the movement "
            "with {camera_style}. High energy, cinematic motion blur on extremities. "
            "{motion_notes}"
        ),
        "image_modifiers": [
            "frozen motion at peak action",
            "dynamic body position",
            "controlled motion blur on extremities",
            "high-energy composition",
            "dramatic directional lighting",
        ],
        "video_modifiers": [
            "explosive kinetic movement",
            "dynamic camera following action",
            "speed ramping for impact",
        ],
        "industries": [
            "sport", "automotive", "fashion", "tech", "food_beverage",
        ],
    },

    # ─────────────────────────────────────────────
    # 8. UNBOXING REVEAL
    # ─────────────────────────────────────────────
    "unboxing_reveal": {
        "name": "Unboxing Reveal",
        "description": (
            "The product emerges from premium packaging. Anticipation builds as "
            "layers peel away to reveal the product in its first-impression glory."
        ),
        "optimal_duration_range": (4, 8),
        "recommended_camera_movements": [
            "zoom_in",
            "crane_down",
            "static",
            "slow_push_in",
        ],
        "recommended_transitions_in": ["cut", "dissolve"],
        "recommended_transitions_out": ["dissolve", "cut"],
        "recommended_lighting": [
            "high_key",
            "three_point",
            "product_light_field",
            "beauty_dish",
            "window_light_soft",
        ],
        "recommended_lenses": [
            "standard_50mm_f14",
            "zoom_24_70mm",
            "classic_35mm",
            "macro_100mm",
        ],
        "gemini_prompt_template": (
            "Overhead view of {product} being revealed from {packaging_description}. "
            "{lighting_description}. Premium packaging materials visible. "
            "The product emerges pristine. {style_notes}"
        ),
        "kling_prompt_template": (
            "Hands carefully open {packaging_description}, revealing {product} inside. "
            "Camera pushes in as the lid lifts. Light catches the product surface. "
            "{motion_notes}"
        ),
        "image_modifiers": [
            "premium unboxing moment captured",
            "luxurious packaging materials visible",
            "anticipation and reveal composition",
            "clean overhead or three-quarter angle",
            "pristine product first impression",
        ],
        "video_modifiers": [
            "lid opening with tissue paper parting",
            "product emerging from packaging",
            "light catching product surface on reveal",
        ],
        "industries": [
            "tech", "luxury", "beauty", "jewelry_watches", "fashion",
            "fragrance",
        ],
    },

    # ─────────────────────────────────────────────
    # 9. SILHOUETTE ARTISTIC
    # ─────────────────────────────────────────────
    "silhouette_artistic": {
        "name": "Silhouette Artistic",
        "description": (
            "The subject rendered as a dramatic shadow outline against a bright or "
            "colored background. Mystery, mood, and form take precedence over detail."
        ),
        "optimal_duration_range": (2, 5),
        "recommended_camera_movements": [
            "static",
            "slow_push_in",
            "pan_right",
        ],
        "recommended_transitions_in": ["fade_from_black", "dissolve"],
        "recommended_transitions_out": ["fade_to_black", "dissolve"],
        "recommended_lighting": [
            "silhouette",
            "backlit",
            "golden_hour",
            "blue_hour",
            "neon_gel",
        ],
        "recommended_lenses": [
            "classic_35mm",
            "standard_50mm_f14",
            "wide_24mm",
            "anamorphic_75mm",
        ],
        "gemini_prompt_template": (
            "Dramatic silhouette of {subject} against {background_light_source}. "
            "Only the outline is visible, creating {mood} atmosphere. "
            "Strong backlight with {color_tone} tones. {style_notes}"
        ),
        "kling_prompt_template": (
            "Silhouetted {subject} moves slowly against {background_light_source}. "
            "Only the dark outline shifts. Background light pulses gently. {motion_notes}"
        ),
        "image_modifiers": [
            "dramatic silhouette photography",
            "strong backlit outline",
            "mystery and mood composition",
            "form over detail",
            "high-contrast light and shadow",
        ],
        "video_modifiers": [
            "silhouette posing or walking against light",
            "background light shifting color or intensity",
            "slow reveal from shadow",
        ],
        "industries": [
            "fragrance", "fashion", "luxury", "sport", "automotive",
        ],
    },

    # ─────────────────────────────────────────────
    # 10. POV FIRST PERSON
    # ─────────────────────────────────────────────
    "pov_first_person": {
        "name": "POV First Person",
        "description": (
            "Shot from the viewer's perspective, placing the audience inside the "
            "experience. Creates immediacy and personal connection with the product."
        ),
        "optimal_duration_range": (2, 5),
        "recommended_camera_movements": [
            "handheld",
            "dolly_in",
            "head_bob",
            "tracking",
        ],
        "recommended_transitions_in": ["cut", "whip_pan"],
        "recommended_transitions_out": ["cut", "dissolve"],
        "recommended_lighting": [
            "overcast_diffused",
            "golden_hour",
            "window_light_soft",
            "high_key",
            "three_point",
        ],
        "recommended_lenses": [
            "wide_24mm",
            "classic_35mm",
            "ultra_wide_14mm",
            "fisheye_8mm",
        ],
        "gemini_prompt_template": (
            "First-person POV looking down at {product_or_scene}. "
            "The viewer's hands {interaction_description}. "
            "{lighting_description}. Immersive and personal. {style_notes}"
        ),
        "kling_prompt_template": (
            "First-person perspective: hands reach toward {product_or_scene}. "
            "Subtle handheld camera sway. Natural head-bob movement. "
            "{lighting_description}. {motion_notes}"
        ),
        "image_modifiers": [
            "first-person POV perspective",
            "viewer's hands visible in frame",
            "immersive personal viewpoint",
            "wide-angle slight distortion",
            "natural environmental context",
        ],
        "video_modifiers": [
            "handheld camera sway for realism",
            "reaching and interacting from viewer perspective",
            "natural head-bob walking motion",
        ],
        "industries": [
            "tech", "food_beverage", "sport", "travel", "automotive",
        ],
    },

    # ─────────────────────────────────────────────
    # 11. HANDS ONLY
    # ─────────────────────────────────────────────
    "hands_only": {
        "name": "Hands Only",
        "description": (
            "Tight framing on hands interacting with the product — applying, "
            "opening, assembling, or demonstrating. Universal and identity-neutral."
        ),
        "optimal_duration_range": (2, 4),
        "recommended_camera_movements": [
            "static",
            "slow_push_in",
            "overhead_static",
        ],
        "recommended_transitions_in": ["cut", "dissolve"],
        "recommended_transitions_out": ["cut", "dissolve"],
        "recommended_lighting": [
            "beauty_dish",
            "window_light_soft",
            "tabletop_product",
            "high_key",
            "three_point",
        ],
        "recommended_lenses": [
            "macro_100mm",
            "standard_50mm_f14",
            "portrait_85mm_f14",
            "zoom_24_70mm",
        ],
        "gemini_prompt_template": (
            "Close-up of well-groomed hands {interaction_verb} {product} against "
            "{background}. {lighting_description}. Only hands and product visible. "
            "Clean, minimal composition. {style_notes}"
        ),
        "kling_prompt_template": (
            "Hands carefully {interaction_verb} {product}. Camera holds steady on "
            "the deliberate gesture. Soft top light. Clean background. {motion_notes}"
        ),
        "image_modifiers": [
            "hands close-up photography",
            "product interaction detail",
            "clean minimal background",
            "soft directional top light",
            "deliberate gesture captured",
        ],
        "video_modifiers": [
            "deliberate hand gesture with product",
            "product manipulation in close-up",
            "smooth controlled movements",
        ],
        "industries": [
            "beauty", "food_beverage", "tech", "jewelry_watches", "luxury",
            "fragrance",
        ],
    },

    # ─────────────────────────────────────────────
    # 12. INGREDIENT / COMPONENT
    # ─────────────────────────────────────────────
    "ingredient_component": {
        "name": "Ingredient / Component",
        "description": (
            "Individual ingredients, raw materials, or product components displayed "
            "in isolation or arranged as a deconstructed composition."
        ),
        "optimal_duration_range": (2, 4),
        "recommended_camera_movements": [
            "static",
            "overhead_static",
            "slow_pan",
            "rack_focus",
        ],
        "recommended_transitions_in": ["cut", "dissolve"],
        "recommended_transitions_out": ["cut", "dissolve"],
        "recommended_lighting": [
            "tabletop_product",
            "product_light_field",
            "product_backlit_glow",
            "high_key",
            "raking_texture",
        ],
        "recommended_lenses": [
            "macro_100mm",
            "standard_50mm_f14",
            "tilt_shift_24mm",
            "portrait_85mm_f14",
        ],
        "gemini_prompt_template": (
            "Deconstructed flat-lay of {ingredients_list} arranged around {product}. "
            "{lighting_description}. Each component is crisp and identifiable. "
            "Clean {background} surface. {style_notes}"
        ),
        "kling_prompt_template": (
            "Ingredients appear one by one around {product} in an overhead composition. "
            "Each element drops or slides into position. {lighting_description}. {motion_notes}"
        ),
        "image_modifiers": [
            "ingredient flat-lay photography",
            "deconstructed product composition",
            "each component sharply rendered",
            "curated arrangement from above",
            "clean surface background",
        ],
        "video_modifiers": [
            "ingredients assembling into composition",
            "items placed one by one from above",
            "rack focus between components",
        ],
        "industries": [
            "food_beverage", "beauty", "fragrance", "tech", "luxury",
        ],
    },

    # ─────────────────────────────────────────────
    # 13. BEFORE / AFTER TRANSFORM
    # ─────────────────────────────────────────────
    "before_after_transform": {
        "name": "Before / After Transformation",
        "description": (
            "A side-by-side or sequential comparison showing the product's effect. "
            "Lighting and composition remain consistent to isolate the change."
        ),
        "optimal_duration_range": (4, 8),
        "recommended_camera_movements": [
            "static",
            "lateral_slide",
            "wipe_reveal",
        ],
        "recommended_transitions_in": ["cut", "dissolve"],
        "recommended_transitions_out": ["dissolve", "wipe", "cut"],
        "recommended_lighting": [
            "high_key",
            "beauty_dish",
            "three_point",
            "window_light_soft",
            "overcast_diffused",
        ],
        "recommended_lenses": [
            "standard_50mm_f14",
            "portrait_85mm_f14",
            "zoom_24_70mm",
            "classic_35mm",
        ],
        "gemini_prompt_template": (
            "Side-by-side comparison: left shows {before_state}, right shows "
            "{after_state} after using {product}. Identical {lighting_description} "
            "and framing in both halves. Clear, convincing difference. {style_notes}"
        ),
        "kling_prompt_template": (
            "A wipe transition reveals the transformation: {before_state} morphs into "
            "{after_state}. Camera holds steady. Lighting remains consistent. "
            "{product} appears in the center. {motion_notes}"
        ),
        "image_modifiers": [
            "before-and-after split composition",
            "matched lighting both sides",
            "clear visible transformation",
            "consistent framing and angle",
            "convincing product efficacy",
        ],
        "video_modifiers": [
            "morph or wipe transition between states",
            "time-lapse transformation sequence",
            "static camera with matched conditions",
        ],
        "industries": [
            "beauty", "food_beverage", "tech", "real_estate", "sport",
        ],
    },

    # ─────────────────────────────────────────────
    # 14. SPLIT SCREEN
    # ─────────────────────────────────────────────
    "split_screen": {
        "name": "Split Screen",
        "description": (
            "Two or more simultaneous viewpoints shown in a divided frame. "
            "Used for comparison, parallel narratives, or multi-angle coverage."
        ),
        "optimal_duration_range": (3, 6),
        "recommended_camera_movements": [
            "static",
            "synchronized_push_in",
            "lateral_slide",
        ],
        "recommended_transitions_in": ["wipe", "cut", "split_reveal"],
        "recommended_transitions_out": ["wipe", "cut", "dissolve"],
        "recommended_lighting": [
            "high_key",
            "three_point",
            "overcast_diffused",
            "beauty_dish",
            "window_light_soft",
        ],
        "recommended_lenses": [
            "standard_50mm_f14",
            "zoom_24_70mm",
            "classic_35mm",
            "portrait_85mm_f14",
        ],
        "gemini_prompt_template": (
            "Split-screen composition: left panel shows {panel_a_content}, right panel "
            "shows {panel_b_content}. Both halves share {lighting_description}. "
            "Clean dividing line. {style_notes}"
        ),
        "kling_prompt_template": (
            "Split-screen: two synchronized views. Left: {panel_a_content}. "
            "Right: {panel_b_content}. Both panels animate simultaneously. "
            "Clean vertical divider. {motion_notes}"
        ),
        "image_modifiers": [
            "split-screen dual composition",
            "clean vertical or horizontal divide",
            "matched exposure across panels",
            "parallel visual narrative",
            "balanced composition both halves",
        ],
        "video_modifiers": [
            "synchronized motion in both panels",
            "split screen reveal animation",
            "parallel narratives converging",
        ],
        "industries": [
            "tech", "beauty", "sport", "food_beverage", "automotive",
        ],
    },

    # ─────────────────────────────────────────────
    # 15. SLOW MOTION MOMENT
    # ─────────────────────────────────────────────
    "slow_motion_moment": {
        "name": "Slow Motion Moment",
        "description": (
            "A key moment captured in slow motion to emphasize impact, beauty, or "
            "drama — liquid pours, hair flips, fabric flows, or impacts."
        ),
        "optimal_duration_range": (2, 5),
        "recommended_camera_movements": [
            "static",
            "tracking",
            "slow_push_in",
            "crane_up",
        ],
        "recommended_transitions_in": ["cut", "dissolve", "speed_ramp"],
        "recommended_transitions_out": ["cut", "dissolve", "speed_ramp"],
        "recommended_lighting": [
            "backlit",
            "rim_light",
            "golden_hour",
            "cinematic_teal_orange",
            "chiaroscuro",
        ],
        "recommended_lenses": [
            "zoom_70_200mm",
            "telephoto_135mm",
            "portrait_85mm_f14",
            "anamorphic_75mm",
            "zoom_24_70mm",
        ],
        "gemini_prompt_template": (
            "{subject} captured at the peak of {slow_motion_moment}. "
            "{lighting_description}. Every droplet, strand, or particle is frozen "
            "in exquisite detail. High-speed photography aesthetic. {style_notes}"
        ),
        "kling_prompt_template": (
            "{subject} in ultra-slow motion: {slow_motion_moment}. "
            "Time stretches as {detail_description} moves through the air. "
            "Cinematic lighting with rim highlights. {motion_notes}"
        ),
        "image_modifiers": [
            "high-speed frozen-motion photography",
            "every particle and droplet visible",
            "peak-action moment captured",
            "dramatic rim light on movement",
            "ultra-sharp detail in motion",
        ],
        "video_modifiers": [
            "ultra-slow-motion replay at 240fps+",
            "speed ramp from real-time to slow",
            "particles and elements drifting in air",
        ],
        "industries": [
            "beauty", "food_beverage", "sport", "fragrance", "fashion",
            "automotive",
        ],
    },

    # ─────────────────────────────────────────────
    # 16. TIME LAPSE
    # ─────────────────────────────────────────────
    "time_lapse": {
        "name": "Time Lapse",
        "description": (
            "Accelerated passage of time — day to night, crowds flowing, clouds "
            "racing, or a process completing. Compression of time creates drama."
        ),
        "optimal_duration_range": (3, 8),
        "recommended_camera_movements": [
            "static",
            "slow_pan",
            "hyperlapse_tracking",
        ],
        "recommended_transitions_in": ["dissolve", "fade_from_black"],
        "recommended_transitions_out": ["dissolve", "fade_to_black"],
        "recommended_lighting": [
            "golden_hour",
            "blue_hour",
            "overcast_diffused",
            "cinematic_teal_orange",
            "window_light_dramatic",
        ],
        "recommended_lenses": [
            "wide_24mm",
            "ultra_wide_14mm",
            "standard_50mm_f14",
            "tilt_shift_24mm",
            "zoom_24_70mm",
        ],
        "gemini_prompt_template": (
            "Time-lapse frame showing {time_lapse_subject} mid-transition. "
            "{lighting_description} captures the {time_span} compressed into "
            "a single moment. Motion blur on moving elements. {style_notes}"
        ),
        "kling_prompt_template": (
            "Time-lapse of {time_lapse_subject} over {time_span}. Clouds race, "
            "shadows sweep, {changing_elements}. Camera remains locked. "
            "Smooth accelerated motion. {motion_notes}"
        ),
        "image_modifiers": [
            "time-lapse long-exposure aesthetic",
            "motion blur on moving elements",
            "static elements razor-sharp",
            "dramatic light transition visible",
            "compressed-time composition",
        ],
        "video_modifiers": [
            "accelerated time-lapse photography",
            "day-to-night or dawn-to-dusk transition",
            "hyperlapse with stabilized movement",
        ],
        "industries": [
            "travel", "real_estate", "food_beverage", "beauty", "tech",
            "automotive",
        ],
    },

    # ─────────────────────────────────────────────
    # 17. REFLECTION / MIRROR
    # ─────────────────────────────────────────────
    "reflection_mirror": {
        "name": "Reflection / Mirror",
        "description": (
            "Subject or product reflected in a mirror, water, glass, or polished "
            "surface. Doubles the composition and adds visual sophistication."
        ),
        "optimal_duration_range": (3, 5),
        "recommended_camera_movements": [
            "static",
            "lateral_slide",
            "slow_push_in",
        ],
        "recommended_transitions_in": ["dissolve", "cut"],
        "recommended_transitions_out": ["dissolve", "cut"],
        "recommended_lighting": [
            "window_light_dramatic",
            "three_point",
            "rim_light",
            "reflective_surface",
            "chiaroscuro",
        ],
        "recommended_lenses": [
            "standard_50mm_f14",
            "portrait_85mm_f14",
            "classic_35mm",
            "anamorphic_50mm",
        ],
        "gemini_prompt_template": (
            "{subject} reflected in {reflective_surface}. Both the real subject and "
            "its reflection are composed symmetrically. {lighting_description}. "
            "The reflection adds depth and narrative. {style_notes}"
        ),
        "kling_prompt_template": (
            "Camera moves between {subject} and its reflection in {reflective_surface}. "
            "The boundary between real and reflected blurs. "
            "{lighting_description}. {motion_notes}"
        ),
        "image_modifiers": [
            "mirror reflection composition",
            "doubled subject symmetry",
            "reflective surface rendered clearly",
            "visual depth through reflection",
            "sophisticated dual-plane framing",
        ],
        "video_modifiers": [
            "camera crossing between real and reflected",
            "reflection revealing different angle",
            "water or glass surface ripple effect",
        ],
        "industries": [
            "beauty", "fragrance", "fashion", "luxury", "jewelry_watches",
            "automotive",
        ],
    },

    # ─────────────────────────────────────────────
    # 18. AERIAL / DRONE
    # ─────────────────────────────────────────────
    "aerial_drone": {
        "name": "Aerial / Drone",
        "description": (
            "Bird's-eye or elevated drone perspective showing scale, geography, "
            "or architectural context from above."
        ),
        "optimal_duration_range": (3, 7),
        "recommended_camera_movements": [
            "drone_ascending",
            "drone_orbit",
            "drone_flyover",
            "drone_reveal",
            "crane_up",
        ],
        "recommended_transitions_in": ["fade_from_black", "dissolve", "cut"],
        "recommended_transitions_out": ["dissolve", "cut", "fade_to_black"],
        "recommended_lighting": [
            "golden_hour",
            "blue_hour",
            "overcast_diffused",
            "cinematic_teal_orange",
        ],
        "recommended_lenses": [
            "wide_24mm",
            "ultra_wide_14mm",
            "zoom_24_70mm",
        ],
        "gemini_prompt_template": (
            "Aerial drone shot looking down on {aerial_subject}. "
            "{lighting_description}. The vast scale of {environment} is visible. "
            "Geometric patterns and leading lines from above. {style_notes}"
        ),
        "kling_prompt_template": (
            "Drone ascends above {aerial_subject}, revealing {environment} in full scale. "
            "{lighting_description}. Smooth stabilized aerial movement. {motion_notes}"
        ),
        "image_modifiers": [
            "aerial drone photography",
            "bird's-eye geometric perspective",
            "vast scale and context",
            "stabilized aerial clarity",
            "dramatic landscape from above",
        ],
        "video_modifiers": [
            "drone ascending or sweeping across terrain",
            "smooth orbital aerial movement",
            "dramatic reveal from altitude",
        ],
        "industries": [
            "travel", "real_estate", "automotive", "sport", "luxury",
        ],
    },

    # ─────────────────────────────────────────────
    # 19. SOCIAL GROUP
    # ─────────────────────────────────────────────
    "social_group": {
        "name": "Social Group",
        "description": (
            "Multiple people sharing an experience — laughing, celebrating, dining, "
            "or collaborating. Conveys community, belonging, and shared joy."
        ),
        "optimal_duration_range": (3, 6),
        "recommended_camera_movements": [
            "tracking",
            "pan_right",
            "dolly_out",
            "handheld",
            "static",
        ],
        "recommended_transitions_in": ["cut", "dissolve"],
        "recommended_transitions_out": ["cut", "dissolve"],
        "recommended_lighting": [
            "golden_hour",
            "overcast_diffused",
            "three_point",
            "high_key",
            "window_light_soft",
        ],
        "recommended_lenses": [
            "classic_35mm",
            "wide_24mm",
            "zoom_24_70mm",
            "standard_50mm_f14",
        ],
        "gemini_prompt_template": (
            "A group of {group_description} {group_activity} together in {environment}. "
            "{lighting_description}. Genuine connection and {emotion} are palpable. "
            "{product} is contextually present. {style_notes}"
        ),
        "kling_prompt_template": (
            "Group of {group_description} {group_activity}. Camera moves through the "
            "group capturing candid moments. Natural laughter and interaction. "
            "{lighting_description}. {motion_notes}"
        ),
        "image_modifiers": [
            "candid group photography",
            "genuine human connection",
            "natural laughter and interaction",
            "diverse group composition",
            "environmental context visible",
        ],
        "video_modifiers": [
            "candid group movement and interaction",
            "camera drifting through social moment",
            "natural conversational gestures",
        ],
        "industries": [
            "food_beverage", "travel", "fashion", "tech", "sport",
            "luxury",
        ],
    },

    # ─────────────────────────────────────────────
    # 20. BEHIND THE SCENES
    # ─────────────────────────────────────────────
    "behind_the_scenes": {
        "name": "Behind the Scenes",
        "description": (
            "A peek behind the curtain — the workshop, kitchen, studio, or factory "
            "where the product is made. Authenticity and craft narrative."
        ),
        "optimal_duration_range": (3, 6),
        "recommended_camera_movements": [
            "handheld",
            "tracking",
            "pan_left",
            "dolly_in",
        ],
        "recommended_transitions_in": ["cut", "dissolve"],
        "recommended_transitions_out": ["cut", "dissolve"],
        "recommended_lighting": [
            "window_light_dramatic",
            "overcast_diffused",
            "three_point",
            "golden_hour",
            "fog_haze",
        ],
        "recommended_lenses": [
            "classic_35mm",
            "wide_24mm",
            "standard_50mm_f14",
            "zoom_24_70mm",
        ],
        "gemini_prompt_template": (
            "Behind-the-scenes view of {bts_subject} in {workspace}. "
            "{lighting_description}. Raw, authentic atmosphere with {craft_details} "
            "visible. Documentary aesthetic. {style_notes}"
        ),
        "kling_prompt_template": (
            "Camera follows {bts_subject} through {workspace}. Hands craft, tools move, "
            "{craft_details} unfold naturally. Handheld documentary style. {motion_notes}"
        ),
        "image_modifiers": [
            "behind-the-scenes documentary style",
            "authentic craft environment",
            "raw workshop or studio setting",
            "tools and materials visible",
            "artisan narrative composition",
        ],
        "video_modifiers": [
            "handheld documentary camera movement",
            "crafting process in real time",
            "authentic workspace atmosphere",
        ],
        "industries": [
            "food_beverage", "luxury", "fashion", "beauty", "jewelry_watches",
        ],
    },

    # ─────────────────────────────────────────────
    # 21. TEXT OVERLAY / TITLE
    # ─────────────────────────────────────────────
    "text_overlay_title": {
        "name": "Text Overlay / Title Card",
        "description": (
            "A frame designed to carry typography — headlines, statistics, or brand "
            "messaging. Visual real-estate is reserved for text placement."
        ),
        "optimal_duration_range": (2, 4),
        "recommended_camera_movements": [
            "static",
            "subtle_drift",
            "slow_zoom_out",
        ],
        "recommended_transitions_in": ["fade_from_black", "dissolve", "cut"],
        "recommended_transitions_out": ["cut", "dissolve", "fade_to_black"],
        "recommended_lighting": [
            "high_key",
            "low_key",
            "product_dark_field",
            "overcast_diffused",
            "neon_gel",
        ],
        "recommended_lenses": [
            "standard_50mm_f14",
            "wide_24mm",
            "classic_35mm",
        ],
        "gemini_prompt_template": (
            "Clean background plate for text overlay: {background_description}. "
            "{lighting_description}. Large negative space in {text_area} for headline. "
            "Subtle texture or gradient. {style_notes}"
        ),
        "kling_prompt_template": (
            "Minimal animated background: {background_description}. "
            "Gentle motion provides visual interest without competing with text. "
            "Large clear area for overlay. {motion_notes}"
        ),
        "image_modifiers": [
            "text-friendly negative space",
            "clean background for typography",
            "subtle texture or gradient",
            "high contrast for readability",
            "brand-appropriate color palette",
        ],
        "video_modifiers": [
            "subtle background animation for text plate",
            "gentle movement without distraction",
            "kinetic typography support composition",
        ],
        "industries": [
            "tech", "fashion", "beauty", "food_beverage", "sport",
            "luxury", "automotive", "travel",
        ],
    },

    # ─────────────────────────────────────────────
    # 22. PACKSHOT / ENDFRAME
    # ─────────────────────────────────────────────
    "packshot_endframe": {
        "name": "Packshot / Endframe",
        "description": (
            "The final frame of the ad — product centered, logo present, tagline "
            "space reserved. Clean, authoritative, and brand-aligned."
        ),
        "optimal_duration_range": (2, 4),
        "recommended_camera_movements": [
            "static",
            "slow_push_in",
        ],
        "recommended_transitions_in": ["fade_from_black", "dissolve"],
        "recommended_transitions_out": ["fade_to_black", "hold"],
        "recommended_lighting": [
            "product_light_field",
            "three_point",
            "high_key",
            "beauty_dish",
            "product_dark_field",
        ],
        "recommended_lenses": [
            "standard_50mm_f14",
            "portrait_85mm_f14",
            "tilt_shift_24mm",
        ],
        "gemini_prompt_template": (
            "Clean packshot of {product} centered against {background}. "
            "{lighting_description}. Space reserved for logo at {logo_position} "
            "and tagline at {tagline_position}. Premium, authoritative. {style_notes}"
        ),
        "kling_prompt_template": (
            "{product} fades in or lands gently at center frame. Logo animates in at "
            "{logo_position}. {lighting_description}. Subtle light shimmer. {motion_notes}"
        ),
        "image_modifiers": [
            "clean brand endframe composition",
            "logo and tagline placement space",
            "minimal elegant presentation",
            "authoritative product packshot",
            "brand-aligned color palette",
        ],
        "video_modifiers": [
            "logo fade-in or reveal animation",
            "subtle product light shimmer",
            "clean static hold for final frame",
        ],
        "industries": [
            "beauty", "luxury", "tech", "fashion", "food_beverage",
            "fragrance", "automotive", "jewelry_watches", "sport",
        ],
    },

    # ─────────────────────────────────────────────
    # 23. SCALE COMPARISON
    # ─────────────────────────────────────────────
    "scale_comparison": {
        "name": "Scale Comparison",
        "description": (
            "The product shown alongside a familiar reference object to communicate "
            "its actual size — coins, hands, everyday items, or environments."
        ),
        "optimal_duration_range": (2, 4),
        "recommended_camera_movements": [
            "static",
            "dolly_out",
            "slow_zoom_out",
        ],
        "recommended_transitions_in": ["cut", "dissolve"],
        "recommended_transitions_out": ["cut", "dissolve"],
        "recommended_lighting": [
            "high_key",
            "three_point",
            "tabletop_product",
            "window_light_soft",
            "overcast_diffused",
        ],
        "recommended_lenses": [
            "standard_50mm_f14",
            "zoom_24_70mm",
            "wide_24mm",
            "classic_35mm",
        ],
        "gemini_prompt_template": (
            "{product} placed next to {reference_object} for scale. "
            "{lighting_description}. Both objects are sharp and clearly sized. "
            "Clean {background} surface. {style_notes}"
        ),
        "kling_prompt_template": (
            "Camera pulls back from {product} to reveal {reference_object} beside it, "
            "establishing scale. Clean surface, even lighting. {motion_notes}"
        ),
        "image_modifiers": [
            "scale comparison photography",
            "familiar reference object beside product",
            "both subjects in sharp focus",
            "clean surface for clear sizing",
            "informative yet aesthetic composition",
        ],
        "video_modifiers": [
            "camera pulling back to reveal scale reference",
            "reference object placed beside product",
            "smooth zoom out establishing size",
        ],
        "industries": [
            "tech", "jewelry_watches", "food_beverage", "beauty", "luxury",
        ],
    },

    # ─────────────────────────────────────────────
    # 24. SEASONAL / HOLIDAY
    # ─────────────────────────────────────────────
    "seasonal_holiday": {
        "name": "Seasonal / Holiday",
        "description": (
            "Product framed within seasonal or holiday context — Christmas, summer, "
            "Valentine's Day, or cultural celebrations. Timely and emotionally resonant."
        ),
        "optimal_duration_range": (3, 6),
        "recommended_camera_movements": [
            "slow_push_in",
            "static",
            "crane_down",
            "pan_right",
        ],
        "recommended_transitions_in": ["dissolve", "fade_from_black", "wipe"],
        "recommended_transitions_out": ["dissolve", "fade_to_black"],
        "recommended_lighting": [
            "golden_hour",
            "window_light_soft",
            "high_key",
            "chiaroscuro",
            "neon_gel",
        ],
        "recommended_lenses": [
            "standard_50mm_f14",
            "classic_35mm",
            "zoom_24_70mm",
            "portrait_85mm_f14",
            "petzval",
        ],
        "gemini_prompt_template": (
            "{product} in a {season_or_holiday} setting with {seasonal_props}. "
            "{lighting_description}. Warm, festive atmosphere with {color_palette}. "
            "Emotionally inviting composition. {style_notes}"
        ),
        "kling_prompt_template": (
            "{seasonal_props} gently animate around {product} in a {season_or_holiday} scene. "
            "{lighting_description}. Snowfall, confetti, or petals drift softly. {motion_notes}"
        ),
        "image_modifiers": [
            "seasonal themed product photography",
            "holiday props and decorations",
            "warm emotionally resonant palette",
            "festive atmospheric elements",
            "timely cultural context",
        ],
        "video_modifiers": [
            "seasonal particles drifting gently",
            "warm holiday lighting animation",
            "festive environmental movement",
        ],
        "industries": [
            "food_beverage", "fashion", "beauty", "luxury", "jewelry_watches",
            "fragrance", "tech",
        ],
    },

    # ─────────────────────────────────────────────
    # 25. CALL TO ACTION
    # ─────────────────────────────────────────────
    "call_to_action": {
        "name": "Call to Action",
        "description": (
            "The conversion frame — designed to drive the viewer to act. Product "
            "visible, CTA text space, urgency or benefit clearly communicated."
        ),
        "optimal_duration_range": (2, 4),
        "recommended_camera_movements": [
            "static",
            "slow_push_in",
        ],
        "recommended_transitions_in": ["dissolve", "cut", "fade_from_black"],
        "recommended_transitions_out": ["fade_to_black", "hold"],
        "recommended_lighting": [
            "high_key",
            "product_light_field",
            "three_point",
            "beauty_dish",
            "neon_gel",
        ],
        "recommended_lenses": [
            "standard_50mm_f14",
            "classic_35mm",
            "zoom_24_70mm",
        ],
        "gemini_prompt_template": (
            "{product} prominently displayed with clear space for CTA button or text "
            "at {cta_position}. {lighting_description}. {benefit_statement} is visually "
            "implied. Clean, high-contrast, action-oriented. {style_notes}"
        ),
        "kling_prompt_template": (
            "{product} pulses subtly with a highlight glow. Space clears for CTA "
            "overlay at {cta_position}. Background simplifies to draw focus. "
            "{motion_notes}"
        ),
        "image_modifiers": [
            "call-to-action ready composition",
            "clear CTA button placement space",
            "high-contrast action-oriented design",
            "product prominently featured",
            "urgency-driving visual hierarchy",
        ],
        "video_modifiers": [
            "subtle product highlight pulse",
            "background simplifying for CTA focus",
            "motion directing eye to action area",
        ],
        "industries": [
            "tech", "beauty", "fashion", "food_beverage", "sport",
            "luxury", "automotive", "travel", "real_estate",
        ],
    },
}


# ─────────────────────────────────────────────────────────────────────────────
# Convenience accessors
# ─────────────────────────────────────────────────────────────────────────────

ALL_ARCHETYPE_KEYS = list(SCENE_ARCHETYPES.keys())

def get_archetype(name: str) -> dict:
    """Return archetype dict by key, or raise KeyError."""
    return SCENE_ARCHETYPES[name]

def archetypes_for_industry(industry: str) -> list[str]:
    """Return list of archetype keys that list *industry* in their industries."""
    return [
        key for key, arch in SCENE_ARCHETYPES.items()
        if industry in arch["industries"]
    ]
