"""
Luxury goods advertising patterns.

Covers high-end lifestyle brands, premium consumer goods, private aviation,
yachting, fine dining, premium spirits, and aspirational lifestyle marketing.
Reference campaigns: Louis Vuitton, Rolls-Royce, Dom Perignon, Aman Resorts.
"""

PATTERNS: dict = {
    "scene_flow": [
        {
            "scene_type": "establishing_grandeur",
            "typical_duration": "3-5s",
            "purpose": "Set the aspirational tone with an iconic location or architectural detail — a palazzo courtyard, a sweeping marble staircase, or an aerial of a private estate at golden hour.",
        },
        {
            "scene_type": "material_intimacy",
            "typical_duration": "2-4s",
            "purpose": "Extreme close-up of texture and craftsmanship — hand-stitched leather, brushed gold hardware, the weave of cashmere — to communicate tactile quality.",
        },
        {
            "scene_type": "lifestyle_vignette",
            "typical_duration": "4-6s",
            "purpose": "A single, unhurried moment of elevated living — a figure silhouetted on a terrace at dusk, a hand lifting a crystal glass, a couple walking through a lantern-lit garden.",
        },
        {
            "scene_type": "product_hero",
            "typical_duration": "3-5s",
            "purpose": "The product presented in its most flattering context — centered, perfectly lit, with breathing room and a minimal but evocative background.",
        },
        {
            "scene_type": "emotional_resonance",
            "typical_duration": "2-4s",
            "purpose": "A contemplative close-up or slow-motion gesture that anchors the emotional promise — confidence, heritage, exclusivity, or quiet power.",
        },
        {
            "scene_type": "brand_seal",
            "typical_duration": "2-3s",
            "purpose": "Logo or wordmark on a clean field, often with a subtle texture (linen, marble, matte black) — restrained and final, like a wax seal on a letter.",
        },
    ],
    "visual_signature": {
        "color_temperature": "Warm-neutral (5200-5800K). Slight amber bias for evening scenes, cool steel for modern-minimalist luxury.",
        "contrast": "Medium-low. Deep blacks but open shadows — nothing crushed. Highlight roll-off should feel analog and gentle.",
        "saturation": "Desaturated 15-25% from reality. Colors are rich but never loud. Gold reads as champagne, red reads as burgundy, blue reads as navy.",
        "grain": "Fine, organic grain at ISO 200-400 equivalent. Enough to feel cinematic, never enough to feel amateur. Mimics medium-format film.",
        "depth_of_field": "Shallow to ultra-shallow. f/1.4-f/2.8 for lifestyle and detail shots. Deeper (f/5.6-f/8) only for grand architectural establishes.",
    },
    "lighting_preferences": [
        {
            "name": "Window-light portrait",
            "description": "Large, soft source from a single direction — mimics the light pouring through floor-to-ceiling windows in a luxury apartment. Gentle fall-off, minimal fill.",
        },
        {
            "name": "Chiaroscuro product",
            "description": "Dramatic side-light with controlled spill. Deep shadows on one side, luminous highlights on the other. Inspired by Old Master paintings.",
        },
        {
            "name": "Golden hour backlight",
            "description": "Warm, low-angle sun behind the subject creating rim light and lens flare. Fill provided by natural bounce or a subtle reflector.",
        },
        {
            "name": "Candlelight ambience",
            "description": "Practical warm sources (candles, fireplace, amber-gelled LEDs) as the dominant light. Skin glows, metals shimmer, everything else falls to shadow.",
        },
        {
            "name": "Overhead gallery light",
            "description": "Clean, diffused top-light as seen in high-end galleries and museums. Even illumination on horizontal surfaces, gentle shadows beneath objects.",
        },
        {
            "name": "Reflected pool light",
            "description": "Caustic light patterns bouncing off water onto ceilings and walls. Creates organic, undulating highlights that suggest a poolside or waterfront setting.",
        },
        {
            "name": "Tungsten practicals",
            "description": "Warm-toned table lamps, sconces, and pendants as the sole light sources. Pools of light with dark negative space between them. Intimate and residential.",
        },
        {
            "name": "Overcast diffusion",
            "description": "Soft, shadowless daylight filtered through clouds or sheer curtains. Ideal for showing true color and texture without harsh contrast.",
        },
    ],
    "lens_preferences": [
        {
            "focal_length": "85mm",
            "aperture": "f/1.4",
            "use_case": "Portrait and lifestyle. Flattering compression, beautiful bokeh, intimate perspective.",
        },
        {
            "focal_length": "50mm",
            "aperture": "f/1.2",
            "use_case": "Environmental storytelling. Natural field of view, fast enough for low-light practicals.",
        },
        {
            "focal_length": "100mm macro",
            "aperture": "f/2.8",
            "use_case": "Texture and detail — stitching, engravings, liquid surfaces, material grain.",
        },
        {
            "focal_length": "35mm",
            "aperture": "f/1.4",
            "use_case": "Architectural interiors and wider lifestyle scenes. Slight wide-angle without distortion.",
        },
        {
            "focal_length": "24-70mm",
            "aperture": "f/2.8",
            "use_case": "Versatile establishing and product-in-context shots. Controlled zoom range for cinematic framing.",
        },
        {
            "focal_length": "135mm",
            "aperture": "f/2.0",
            "use_case": "Compressed backgrounds, dreamy separation. Ideal for isolating a single subject against a blurred cityscape or landscape.",
        },
    ],
    "movement_style": {
        "camera_movement": "Slow, deliberate, and often on a dolly or slider. Gliding lateral tracks, gentle push-ins, and controlled crane descents. Never handheld. Movement should feel like floating through a space, not walking through it.",
        "subject_movement": "Minimal and purposeful. A turn of the head, a hand tracing a surface, a slow walk. Every gesture is choreographed to feel effortless. Avoid fidgeting, fast motion, or anything that reads as casual.",
        "pacing": "Unhurried. Allow frames to breathe. Hold on beauty shots 20-30% longer than feels necessary — the audience should want to linger.",
    },
    "transition_preferences": [
        "Slow dissolve (1.5-3s) — the signature luxury transition, one world melting into the next.",
        "Match cut on shape or texture — a watch dial dissolves into a full moon, leather grain becomes a desert landscape.",
        "Fade to black with a 1-2s hold — creates punctuation and gravitas between scenes.",
        "Seamless whip pan between two composed frames — adds energy when needed without breaking elegance.",
        "Light leak or flare transition — warm amber wash that bridges two golden-hour scenes.",
    ],
    "music_style": {
        "tempo": "60-90 BPM. Slow, measured, breathing.",
        "instruments": "Solo piano, string quartet, ambient pads, muted brass, occasional harp or celesta. Orchestral but restrained.",
        "mood": "Contemplative, aspirational, slightly melancholic. The feeling of standing alone in a beautiful place at twilight.",
        "avoid": "Upbeat pop, EDM drops, trap beats, stock-music energy, vocal hooks, anything that feels mass-market.",
    },
    "banned_elements": [
        "Price tags, discounts, sale language, or any mention of cost — luxury never justifies its price.",
        "Crowded scenes or large groups — exclusivity means solitude or intimate gatherings.",
        "Harsh direct flash or on-camera flash look — reads as paparazzi, not prestige.",
        "Neon colors, oversaturated palettes, or fluorescent lighting.",
        "Fast cuts under 1.5 seconds — urgency is the opposite of luxury.",
        "Stock-photo smiles or exaggerated expressions — emotion should be subtle and interior.",
        "Cluttered compositions — every frame should have clear negative space.",
        "Text-heavy overlays, bullet points, or infographic-style graphics.",
        "Visible branding from non-luxury brands in the frame.",
        "Shaky handheld footage, Dutch angles, or any camera work that feels unstable.",
        "Comedic or ironic tone — luxury takes itself seriously.",
        "Low-resolution textures or obviously AI-generated skin and fabric.",
    ],
    "prompt_modifiers": [
        "editorial luxury photography, Vogue-level production value",
        "shot on medium format Hasselblad, fine grain, rich tonal range",
        "soft directional window light, gentle shadow fall-off",
        "muted desaturated color palette, champagne and charcoal tones",
        "shallow depth of field, creamy bokeh, subject isolation",
        "architectural elegance, marble and brass details",
        "minimal composition with generous negative space",
        "golden hour warmth, amber rim light on skin",
        "tactile material close-up, visible thread and grain texture",
        "cinematic color grading, teal-and-amber split toning",
        "art-directed still life, museum-quality presentation",
        "high-end lifestyle editorial, aspirational and understated",
        "old-money aesthetic, quiet luxury, no visible logos",
        "European villa setting, natural stone and aged wood",
        "ultra-clean product photography on dark matte surface",
        "dramatic chiaroscuro lighting, Renaissance painting influence",
        "silk and velvet textures catching directional light",
        "contemplative mood, single figure in grand space",
        "precision focus on craftsmanship details and hand-finishing",
        "premium print-quality resolution, no artifacts, no noise",
    ],
    "video_modifiers": [
        "slow cinematic dolly push-in, smooth and deliberate",
        "60fps slow motion capturing material flow and liquid pour",
        "gentle parallax revealing depth and dimension of scene",
        "long dissolve transitions between scenes, 2-second crossfade",
        "subtle camera drift, barely perceptible lateral movement",
        "rack focus from foreground detail to background subject",
        "crane descent revealing a grand interior or landscape",
        "match-cut editing connecting product detail to lifestyle moment",
        "ambient particle effects — dust motes or light flares in beam",
        "smooth slider track across a tabletop product arrangement",
    ],
}
