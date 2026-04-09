"""All enumerations used across the pipeline."""
from __future__ import annotations
from enum import Enum


class PipelineMode(str, Enum):
    PERSONNAGE_ET_PRODUIT = "personnage_et_produit"
    PRODUIT_UNIQUEMENT = "produit_uniquement"


class SceneType(str, Enum):
    PERSONNAGE = "personnage"
    PRODUIT = "produit"
    TRANSITION = "transition"


class CameraMovement(str, Enum):
    STATIC = "static"
    PAN_LEFT = "pan_left"
    PAN_RIGHT = "pan_right"
    ZOOM_IN = "zoom_in"
    ZOOM_OUT = "zoom_out"
    TRACKING = "tracking"
    ORBIT = "orbit"


class TransitionType(str, Enum):
    FADE = "fade"
    CUT = "cut"
    DISSOLVE = "dissolve"
    WIPE = "wipe"


class JobStatus(str, Enum):
    PENDING = "pending"
    ANALYZING = "analyzing"
    GENERATING_IMAGES = "generating_images"
    GENERATING_VIDEOS = "generating_videos"
    ASSEMBLING = "assembling"
    COMPLETED = "completed"
    FAILED = "failed"
    PARTIAL = "partial"


class QualityLevel(str, Enum):
    DRAFT = "draft"
    STANDARD = "standard"
    PREMIUM = "premium"


class TargetPlatform(str, Enum):
    YOUTUBE = "youtube"        # 16:9
    INSTAGRAM_FEED = "instagram_feed"  # 1:1
    INSTAGRAM_STORY = "instagram_story"  # 9:16
    TIKTOK = "tiktok"          # 9:16
    TV = "tv"                  # 16:9
    LINKEDIN = "linkedin"      # 1:1


class Industry(str, Enum):
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


PLATFORM_ASPECT_RATIOS: dict[TargetPlatform, str] = {
    TargetPlatform.YOUTUBE: "16:9",
    TargetPlatform.INSTAGRAM_FEED: "1:1",
    TargetPlatform.INSTAGRAM_STORY: "9:16",
    TargetPlatform.TIKTOK: "9:16",
    TargetPlatform.TV: "16:9",
    TargetPlatform.LINKEDIN: "1:1",
}

PLATFORM_RESOLUTIONS: dict[TargetPlatform, str] = {
    TargetPlatform.YOUTUBE: "1920x1080",
    TargetPlatform.INSTAGRAM_FEED: "1080x1080",
    TargetPlatform.INSTAGRAM_STORY: "1080x1920",
    TargetPlatform.TIKTOK: "1080x1920",
    TargetPlatform.TV: "1920x1080",
    TargetPlatform.LINKEDIN: "1080x1080",
}
