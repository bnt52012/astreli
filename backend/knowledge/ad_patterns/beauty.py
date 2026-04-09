"""
Beauty and cosmetics advertising patterns.

Covers skincare, makeup, haircare, wellness, and personal care brands.
Reference campaigns: Charlotte Tilbury, Glossier, Dior Beauty, SK-II,
La Mer, Fenty Beauty, Olaplex.
"""

PATTERNS: dict = {
    "scene_flow": [
        {
            "scene_type": "skin_reveal",
            "typical_duration": "2-3s",
            "purpose": "Open on luminous, dewy skin in close-up — the aspirational 'after' that sells the promise before the product is even shown.",
        },
        {
            "scene_type": "ritual_moment",
            "typical_duration": "3-5s",
            "purpose": "The application ritual — fingers smoothing serum, a brush sweeping across a cheekbone, a mist settling on skin. Sensory and ASMR-adjacent.",
        },
        {
            "scene_type": "texture_showcase",
            "typical_duration": "2-4s",
            "purpose": "Macro shot of the product texture — cream swirl, pigment swatch, oil droplets, powder cloud. Communicates formulation quality.",
        },
        {
            "scene_type": "transformation_beat",
            "typical_duration": "3-5s",
            "purpose": "Before-to-after or bare-to-glam transition. Can be a time-lapse, a mirror reveal, or a confident turn toward camera.",
        },
        {
            "scene_type": "product_beauty_shot",
            "typical_duration": "2-4s",
            "purpose": "The hero packaging in a styled setting — surrounded by ingredients, on a vanity, or floating in an abstract environment.",
        },
        {
            "scene_type": "confidence_payoff",
            "typical_duration": "2-3s",
            "purpose": "The emotional reward — a genuine smile, a self-assured look, a moment of feeling beautiful. The 'why' behind the product.",
        },
        {
            "scene_type": "brand_close",
            "typical_duration": "2-3s",
            "purpose": "Logo, product name, and optional tagline. Often on a clean gradient or with a signature brand texture.",
        },
    ],
    "visual_signature": {
        "color_temperature": "Warm-neutral to slightly cool (5000-6000K). Skincare skews cooler and cleaner; makeup skews warmer and more glam.",
        "contrast": "Low to medium. Shadows are open and lifted. The look is bright and airy, never moody. Skin should glow, not be sculpted by harsh light.",
        "saturation": "Moderate. Skin tones are true-to-life but slightly enhanced. Product colors are vibrant and accurate — the lipstick red must match the actual shade.",
        "grain": "Minimal to none. Beauty demands pristine, smooth imagery. If grain is present, it is ultra-fine and only visible at pixel level.",
        "depth_of_field": "Moderate-shallow. f/2.0-f/4.0 for portraits, ultra-shallow for macro texture shots. Background should be soft but not unrecognizable.",
    },
    "lighting_preferences": [
        {
            "name": "Beauty dish key",
            "description": "22-inch beauty dish at 45 degrees above and slightly camera-left. Creates the classic beauty-campaign look with a nose shadow and glowing skin.",
        },
        {
            "name": "Ring light frontal",
            "description": "On-axis ring light for even, shadow-free illumination. Produces the signature circular catchlight in the eyes. Ideal for direct-to-camera makeup looks.",
        },
        {
            "name": "Clamshell lighting",
            "description": "Two soft sources — one above, one below the face, angled inward. Fills under-eye shadows and creates ultra-flattering, porcelain-skin illumination.",
        },
        {
            "name": "Butterfly / Paramount lighting",
            "description": "Key light directly above and in front of the subject. Creates a small shadow under the nose and defined cheekbones. Timeless glamour.",
        },
        {
            "name": "Backlit halo",
            "description": "Strong backlight creating a rim around hair and shoulders. Fill from the front keeps the face exposed. Hair appears luminous and voluminous.",
        },
        {
            "name": "Soft window wrap",
            "description": "Large diffused source simulating a north-facing window. Wraps around the face with minimal shadow. The go-to for skincare 'clean beauty' campaigns.",
        },
        {
            "name": "Colored gel accent",
            "description": "Rim or background lights gelled to match the product color palette — pink, coral, violet, or gold. Adds editorial flair without affecting skin tone accuracy.",
        },
        {
            "name": "High-key studio",
            "description": "Bright, even illumination with a white or light-colored background. Minimal shadows. Clean, clinical, trustworthy — ideal for dermatologist-backed brands.",
        },
        {
            "name": "Golden reflector bounce",
            "description": "Warm gold reflector as the fill source, catching natural light and bouncing it upward onto the face. Gives a sun-kissed, healthy glow.",
        },
    ],
    "lens_preferences": [
        {
            "focal_length": "85mm",
            "aperture": "f/1.8",
            "use_case": "Beauty portraits. Flattering perspective, smooth bokeh, no facial distortion.",
        },
        {
            "focal_length": "100mm macro",
            "aperture": "f/2.8",
            "use_case": "Product texture and skin detail. Captures pore-level detail for skincare, pigment particles for makeup.",
        },
        {
            "focal_length": "70-200mm",
            "aperture": "f/2.8",
            "use_case": "Editorial beauty at working distance. Versatile zoom for half-body to tight face crops without lens changes.",
        },
        {
            "focal_length": "50mm",
            "aperture": "f/1.4",
            "use_case": "Environmental beauty — model at a vanity, in a bathroom, or in a natural setting. Slightly wider context.",
        },
        {
            "focal_length": "105mm macro",
            "aperture": "f/2.8",
            "use_case": "Extreme close-ups of lip texture, eye detail, cream swatches, and ingredient macro photography.",
        },
    ],
    "movement_style": {
        "camera_movement": "Gentle and orbiting. Slow arc around the face, subtle push-in to the eyes or lips, smooth tilt from product to model. Movement should feel like admiring, not surveilling.",
        "subject_movement": "Tactile and sensory. Fingers gliding across skin, brushes sweeping, hair tossing in slow motion, lips pressing together after application. Every movement highlights the sensory experience of the product.",
        "pacing": "Medium-paced with moments of slowdown for texture shots. Quick enough to keep attention, slow enough to appreciate the beauty.",
    },
    "transition_preferences": [
        "Soft wipe following the direction of product application — a brush stroke wipes to the next scene.",
        "Morph cut between two similar facial angles — seamless and invisible.",
        "Splash or liquid transition — water, oil, or cream flowing across the frame bridges two scenes.",
        "Match cut from product swatch to model wearing the shade.",
        "Bloom / overexposure to white — a flash of light transitions to the next scene, feeling fresh and clean.",
        "Petal or particle dissolve — organic elements scatter to reveal the next frame.",
    ],
    "music_style": {
        "tempo": "90-120 BPM. Light, rhythmic, feel-good but not aggressive.",
        "instruments": "Airy synths, soft percussion, finger snaps, light guitar plucks, breathy vocal pads, marimba. Modern and feminine without being saccharine.",
        "mood": "Empowering, fresh, confident, playful. The feeling of getting ready and feeling good about yourself.",
        "avoid": "Heavy bass, aggressive drums, dark or moody tones, anything that feels clinical or serious unless the brand is explicitly medical-aesthetic.",
    },
    "banned_elements": [
        "Unrealistic skin retouching that removes all pores and texture — modern beauty celebrates real skin.",
        "Harsh, unflattering downlight or overhead fluorescent lighting.",
        "Dull, matte skin without any luminosity — beauty skin must glow.",
        "Visible product spills or messy application that looks accidental rather than artful.",
        "Clinical laboratory settings (unless specifically a derm-brand creative direction).",
        "Male-gaze framing or objectifying camera angles.",
        "Comparing skin tones or implying one shade is better than another.",
        "Before/after shots that shame the 'before' state.",
        "Overly busy backgrounds that compete with the face or product.",
        "Cheap-looking product packaging or poorly lit product shots.",
        "Flash photography look with hard shadows and blown highlights.",
        "Cartoonish or over-filtered skin that looks plastic.",
    ],
    "prompt_modifiers": [
        "beauty campaign photography, flawless luminous skin",
        "soft beauty dish lighting, gentle nose shadow, glowing complexion",
        "macro texture shot of cream, visible richness and formulation",
        "dewy glass-skin effect, light reflecting off hydrated surface",
        "editorial beauty portrait, high-end cosmetics campaign",
        "clean beauty aesthetic, minimal backdrop, natural radiance",
        "ring light catchlights in eyes, even shadow-free illumination",
        "product flatlay on marble surface with fresh botanicals",
        "slow-motion hair movement, backlit with golden rim light",
        "pigment swatch on skin, true-to-shade color accuracy",
        "closeup of lips with gloss, sharp detail on texture",
        "skincare ritual moment, fingers applying serum to cheek",
        "high-key bright studio, white background, clinical elegance",
        "soft-focus dreamy portrait with pastel color palette",
        "precision eye makeup detail, individual lash visibility",
        "fresh-faced no-makeup makeup look, natural sunlight",
        "ingredient hero shot, botanical extracts and natural oils",
        "vanity scene with soft warm practicals and mirror reflections",
        "clamshell lighting beauty setup, porcelain-smooth illumination",
        "confident self-care moment, genuine natural expression",
    ],
    "video_modifiers": [
        "slow-motion cream application, fingers gliding across dewy skin",
        "gentle orbit around model's face revealing makeup from every angle",
        "macro pour of serum or oil with viscous liquid dynamics",
        "hair toss in 120fps slow motion with backlit rim glow",
        "smooth push-in from half-body to extreme close-up on eyes",
        "product rotation on turntable with shifting colored light",
        "water splash around product packaging, droplets in slow motion",
        "time-lapse makeup transformation, bare skin to full glam",
        "soft rack focus from product in foreground to model behind",
        "brush stroke or swatch wipe transition between scenes",
    ],
}
