"""
Pipeline-specific configuration and validation.

Extends the base application settings with pipeline-specific
defaults, model mappings, and generation parameters.
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path

from backend.models.enums import (
    ImageAspectRatio,
    QualityLevel,
    SceneType,
    TargetPlatform,
)


# ── Model Configuration ──────────────────────────────────────


@dataclass(frozen=True)
class GeminiModelConfig:
    """Configuration for a Gemini image generation model."""

    model_name: str
    max_images_per_request: int = 14
    max_image_size_px: int = 2048
    supported_aspect_ratios: tuple[str, ...] = ("16:9", "9:16", "1:1", "4:3", "3:4")
    default_temperature: float = 0.6
    response_modalities: tuple[str, ...] = ("TEXT", "IMAGE")


@dataclass(frozen=True)
class KlingModelConfig:
    """Configuration for a Kling video generation model."""

    model_name: str
    min_duration: int = 2
    max_duration: int = 10
    supported_aspect_ratios: tuple[str, ...] = ("16:9", "9:16", "1:1")
    default_cfg_scale: float = 0.5


# Default model configurations
GEMINI_PRO_CONFIG = GeminiModelConfig(
    model_name="gemini-2.0-flash-exp",
    default_temperature=0.6,
)

GEMINI_FLASH_CONFIG = GeminiModelConfig(
    model_name="gemini-2.0-flash-exp",
    default_temperature=0.5,
)

KLING_VIDEO01_CONFIG = KlingModelConfig(
    model_name="kling-v1",
)

KLING_V3_CONFIG = KlingModelConfig(
    model_name="kling-v1-6",
)


# ── Platform Output Profiles ─────────────────────────────────


@dataclass(frozen=True)
class PlatformProfile:
    """Output configuration for a target platform."""

    platform: TargetPlatform
    aspect_ratio: ImageAspectRatio
    resolution: str
    max_duration_seconds: int | None
    fps: int = 30
    video_bitrate: str = "8M"
    audio_bitrate: str = "192k"


PLATFORM_PROFILES: dict[TargetPlatform, PlatformProfile] = {
    TargetPlatform.INSTAGRAM_REELS: PlatformProfile(
        platform=TargetPlatform.INSTAGRAM_REELS,
        aspect_ratio=ImageAspectRatio.PORTRAIT_9_16,
        resolution="1080x1920",
        max_duration_seconds=90,
    ),
    TargetPlatform.INSTAGRAM_FEED: PlatformProfile(
        platform=TargetPlatform.INSTAGRAM_FEED,
        aspect_ratio=ImageAspectRatio.SQUARE_1_1,
        resolution="1080x1080",
        max_duration_seconds=60,
    ),
    TargetPlatform.TIKTOK: PlatformProfile(
        platform=TargetPlatform.TIKTOK,
        aspect_ratio=ImageAspectRatio.PORTRAIT_9_16,
        resolution="1080x1920",
        max_duration_seconds=60,
    ),
    TargetPlatform.YOUTUBE: PlatformProfile(
        platform=TargetPlatform.YOUTUBE,
        aspect_ratio=ImageAspectRatio.LANDSCAPE_16_9,
        resolution="1920x1080",
        max_duration_seconds=None,
    ),
    TargetPlatform.YOUTUBE_SHORTS: PlatformProfile(
        platform=TargetPlatform.YOUTUBE_SHORTS,
        aspect_ratio=ImageAspectRatio.PORTRAIT_9_16,
        resolution="1080x1920",
        max_duration_seconds=60,
    ),
    TargetPlatform.TV_BROADCAST: PlatformProfile(
        platform=TargetPlatform.TV_BROADCAST,
        aspect_ratio=ImageAspectRatio.LANDSCAPE_16_9,
        resolution="1920x1080",
        max_duration_seconds=None,
        fps=25,
        video_bitrate="25M",
        audio_bitrate="320k",
    ),
    TargetPlatform.LINKEDIN: PlatformProfile(
        platform=TargetPlatform.LINKEDIN,
        aspect_ratio=ImageAspectRatio.LANDSCAPE_16_9,
        resolution="1920x1080",
        max_duration_seconds=600,
    ),
    TargetPlatform.FACEBOOK: PlatformProfile(
        platform=TargetPlatform.FACEBOOK,
        aspect_ratio=ImageAspectRatio.LANDSCAPE_16_9,
        resolution="1920x1080",
        max_duration_seconds=240,
    ),
    TargetPlatform.CINEMA: PlatformProfile(
        platform=TargetPlatform.CINEMA,
        aspect_ratio=ImageAspectRatio.LANDSCAPE_16_9,
        resolution="3840x2160",
        max_duration_seconds=None,
        fps=24,
        video_bitrate="50M",
        audio_bitrate="320k",
    ),
}


# ── Quality Presets ───────────────────────────────────────────


@dataclass(frozen=True)
class QualityPreset:
    """FFmpeg encoding parameters for a quality level."""

    preset: str
    crf: int
    video_bitrate: str | None = None  # None = let CRF control quality


QUALITY_PRESETS: dict[QualityLevel, QualityPreset] = {
    QualityLevel.DRAFT: QualityPreset(preset="fast", crf=28),
    QualityLevel.STANDARD: QualityPreset(preset="medium", crf=22),
    QualityLevel.PREMIUM: QualityPreset(preset="slow", crf=18),
    QualityLevel.BROADCAST: QualityPreset(preset="slow", crf=15, video_bitrate="25M"),
}


# ── Cost Estimation ───────────────────────────────────────────


@dataclass(frozen=True)
class APICostRates:
    """Per-unit cost rates for API calls (USD).

    These are approximate rates and should be updated as pricing changes.
    """

    # OpenAI GPT-4o
    gpt4o_input_per_1k_tokens: float = 0.005
    gpt4o_output_per_1k_tokens: float = 0.015

    # Google Gemini (image generation is currently free in preview)
    gemini_pro_per_image: float = 0.00
    gemini_flash_per_image: float = 0.00

    # Kling AI
    kling_per_second_video01: float = 0.014
    kling_per_second_v3: float = 0.014


DEFAULT_COST_RATES = APICostRates()


# ── Pipeline Defaults ─────────────────────────────────────────


@dataclass
class PipelineDefaults:
    """Default pipeline settings that can be overridden per project."""

    # Image generation
    image_aspect_ratio: ImageAspectRatio = ImageAspectRatio.LANDSCAPE_16_9
    max_reference_images_per_call: int = 14
    max_mannequin_references: int = 5
    mannequin_max_pixel_size: int = 2048

    # Video generation
    default_video_duration: float = 5.0
    kling_poll_interval_seconds: int = 10
    kling_max_poll_timeout_seconds: int = 600
    kling_max_concurrent_tasks: int = 4

    # Quality
    quality_level: QualityLevel = QualityLevel.PREMIUM
    quality_check_enabled: bool = True
    quality_threshold: float = 0.7
    max_regeneration_attempts: int = 2

    # Assembly
    transition_duration_seconds: float = 0.5
    fade_in_duration: float = 0.8
    fade_out_duration: float = 0.8
    logo_scale_width: int = 120
    logo_padding: int = 30
    audio_fade_in: float = 1.5
    audio_fade_out: float = 2.0

    # Output
    target_platforms: list[TargetPlatform] = field(
        default_factory=lambda: [TargetPlatform.YOUTUBE]
    )

    # Caching
    cache_enabled: bool = True


PIPELINE_DEFAULTS = PipelineDefaults()
