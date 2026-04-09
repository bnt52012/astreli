"""
All enumeration types for the AdGenAI pipeline v3.0.

Centralized here to avoid circular imports and provide a single
source of truth for all classification constants.
"""

from __future__ import annotations

import enum


class PipelineMode(str, enum.Enum):
    """Pipeline execution mode, determined by LoRA model selection."""

    PERSONNAGE_ET_PRODUIT = "personnage_et_produit"
    """Character + Product mode. Client selected a LoRA mannequin model.
    3-pass fusion for personnage scenes: Nano Banana scene → LoRA SDXL → Inpainting.
    One-shot Nano Banana for produit scenes."""

    PRODUIT_UNIQUEMENT = "produit_uniquement"
    """Product Only mode. No LoRA selected. Single Nano Banana 2 engine for all scenes."""


class SceneType(str, enum.Enum):
    """Classification of an individual scene within the ad."""

    PERSONNAGE = "personnage"
    """Scene features the mannequin (even partially: hands, back, silhouette).
    Even if holding a product — if the mannequin is visible, it's personnage.
    Routes to 3-pass fusion: Nano Banana + LoRA SDXL + Inpainting."""

    PRODUIT = "produit"
    """NO mannequin visible. Pure product shot, packshot, object alone.
    Routes to Nano Banana 2 one-shot."""

    TRANSITION = "transition"
    """Title screen, logo alone, text overlay, slogan.
    Skips image generation — handled by FFmpeg."""


class TransitionType(str, enum.Enum):
    """FFmpeg xfade transition types between scenes."""

    FADE = "fade"
    DISSOLVE = "dissolve"
    WIPE_LEFT = "wipeleft"
    WIPE_RIGHT = "wiperight"
    WIPE_UP = "wipeup"
    WIPE_DOWN = "wipedown"
    SLIDE_LEFT = "slideleft"
    SLIDE_RIGHT = "slideright"
    CIRCLE_CROP = "circlecrop"
    RADIAL = "radial"
    SMOOTHLEFT = "smoothleft"
    SMOOTHRIGHT = "smoothright"
    SMOOTHUP = "smoothup"
    SMOOTHDOWN = "smoothdown"
    CUT = "cut"
    """Hard cut — implemented as zero-duration transition."""


class CameraMovement(str, enum.Enum):
    """Camera movement types for Kling video prompts."""

    STATIC = "static"
    PAN_LEFT = "pan_left"
    PAN_RIGHT = "pan_right"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    TRACKING = "tracking"
    ORBIT = "orbit"
    DOLLY_IN = "dolly_in"
    DOLLY_OUT = "dolly_out"
    CRANE_UP = "crane_up"
    CRANE_DOWN = "crane_down"
    TILT_UP = "tilt_up"
    TILT_DOWN = "tilt_down"
    HANDHELD = "handheld"
    STEADICAM = "steadicam"


class JobStatus(str, enum.Enum):
    """Pipeline job lifecycle states."""

    PENDING = "pending"
    ANALYZING = "analyzing"
    ENRICHING = "enriching"
    GENERATING_IMAGES = "generating_images"
    GENERATING_MANNEQUIN = "generating_mannequin"
    FUSING = "fusing"
    QUALITY_CHECK = "quality_check"
    GENERATING_VIDEOS = "generating_videos"
    ASSEMBLING = "assembling"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class AdCategory(str, enum.Enum):
    """Advertising industry — auto-detected from scenario by knowledge engine."""

    LUXURY = "luxury"
    BEAUTY = "beauty"
    FASHION = "fashion"
    SPORT = "sport"
    FOOD_BEVERAGE = "food_beverage"
    AUTOMOTIVE = "automotive"
    TECH = "tech"
    TRAVEL = "travel"
    REAL_ESTATE = "real_estate"
    JEWELRY_WATCHES = "jewelry_watches"
    FRAGRANCE = "fragrance"
    HEALTH = "health"
    GENERAL = "general"


class TargetPlatform(str, enum.Enum):
    """Output platform — determines aspect ratio, duration limits, encoding."""

    INSTAGRAM_REELS = "instagram_reels"
    INSTAGRAM_FEED = "instagram_feed"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    YOUTUBE_SHORTS = "youtube_shorts"
    TV_BROADCAST = "tv_broadcast"
    LINKEDIN = "linkedin"
    FACEBOOK = "facebook"
    WEB_BANNER = "web_banner"
    CINEMA = "cinema"


class ImageAspectRatio(str, enum.Enum):
    """Supported aspect ratios for image generation."""

    LANDSCAPE_16_9 = "16:9"
    PORTRAIT_9_16 = "9:16"
    SQUARE_1_1 = "1:1"
    LANDSCAPE_4_3 = "4:3"
    PORTRAIT_3_4 = "3:4"


class QualityLevel(str, enum.Enum):
    """Quality tier for generation and encoding settings."""

    DRAFT = "draft"
    """Fast iteration — lower quality, faster generation."""

    STANDARD = "standard"
    """Production quality — balanced speed/quality."""

    PREMIUM = "premium"
    """Maximum quality — slow, expensive, for final deliverables."""

    BROADCAST = "broadcast"
    """Broadcast-grade — highest bitrate, broadcast color space."""


class EmotionalTone(str, enum.Enum):
    """Emotional tone of a scene — used for prompt enrichment only."""

    LUXURY = "luxury"
    ENERGETIC = "energetic"
    INTIMATE = "intimate"
    DRAMATIC = "dramatic"
    PLAYFUL = "playful"
    MINIMALIST = "minimalist"
    NOSTALGIC = "nostalgic"
    POWERFUL = "powerful"
    SERENE = "serene"
    MYSTERIOUS = "mysterious"
    JOYFUL = "joyful"
    ELEGANT = "elegant"


class SceneArchetype(str, enum.Enum):
    """Scene archetype within advertising — determines optimal settings."""

    PRODUCT_HERO = "product_hero"
    LIFESTYLE = "lifestyle"
    PORTRAIT = "portrait"
    INTERACTION = "interaction"
    ESTABLISHING = "establishing"
    MACRO_DETAIL = "macro_detail"
    ENDFRAME = "endframe"
    PACKSHOT = "packshot"
    UNBOXING = "unboxing"
    BEFORE_AFTER = "before_after"
    TESTIMONIAL = "testimonial"
    ACTION = "action"
    MONTAGE = "montage"
    REVEAL = "reveal"
    AMBIENT = "ambient"


class FusionPass(str, enum.Enum):
    """The 3 passes of the personnage fusion workflow."""

    SCENE_BASE = "scene_base"
    """Pass 1: Nano Banana 2 generates complete scene with generic figure."""

    MANNEQUIN = "mannequin"
    """Pass 2: LoRA SDXL generates the client's mannequin in matching pose."""

    FUSION = "fusion"
    """Pass 3: Inpainting merges mannequin face onto scene base."""
