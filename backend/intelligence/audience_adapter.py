"""
Platform-Aware Output Adapter.

Generates multiple output versions from a single pipeline run,
optimized for each target platform (Instagram, TikTok, YouTube, TV, etc.).

This module is CLIENT-CONTROLLED: the client chooses their target platforms,
and the adapter applies PREDEFINED rules per platform (not AI-decided).
The client can override any default.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field

from backend.models.enums import ImageAspectRatio, TargetPlatform
from backend.pipeline.config import PLATFORM_PROFILES, PlatformProfile

logger = logging.getLogger(__name__)


@dataclass
class PlatformOutputSpec:
    """Complete output specification for one platform version.

    Contains everything the assembler needs to produce a platform-optimized
    version of the final video.
    """

    platform: TargetPlatform
    profile: PlatformProfile
    output_suffix: str
    max_duration: int | None = None

    # Client overrides (None = use platform defaults)
    custom_resolution: str | None = None
    custom_aspect_ratio: ImageAspectRatio | None = None
    custom_fps: int | None = None
    custom_bitrate: str | None = None

    @property
    def resolution(self) -> str:
        return self.custom_resolution or self.profile.resolution

    @property
    def aspect_ratio(self) -> ImageAspectRatio:
        return self.custom_aspect_ratio or self.profile.aspect_ratio

    @property
    def fps(self) -> int:
        return self.custom_fps or self.profile.fps

    @property
    def video_bitrate(self) -> str:
        return self.custom_bitrate or self.profile.video_bitrate


class AudienceAdapter:
    """Generates platform-specific output specifications.

    Usage:
        adapter = AudienceAdapter()
        specs = adapter.get_output_specs(
            platforms=[TargetPlatform.YOUTUBE, TargetPlatform.INSTAGRAM_REELS],
            total_duration=25.0,
        )
        # Each spec tells the assembler how to encode one version
    """

    def get_output_specs(
        self,
        platforms: list[TargetPlatform],
        total_duration: float | None = None,
        overrides: dict[TargetPlatform, dict] | None = None,
    ) -> list[PlatformOutputSpec]:
        """Generate output specifications for requested platforms.

        Args:
            platforms: Target platforms chosen by the client.
            total_duration: Total video duration in seconds.
            overrides: Per-platform client overrides for resolution, fps, etc.

        Returns:
            List of PlatformOutputSpec, one per platform.
        """
        overrides = overrides or {}
        specs: list[PlatformOutputSpec] = []

        for platform in platforms:
            profile = PLATFORM_PROFILES.get(platform)
            if not profile:
                logger.warning(
                    "[AUDIENCE] No profile for platform %s, skipping",
                    platform.value,
                )
                continue

            # Check duration limits
            max_dur = profile.max_duration_seconds
            if max_dur and total_duration and total_duration > max_dur:
                logger.warning(
                    "[AUDIENCE] Video duration (%.1fs) exceeds %s limit (%ds). "
                    "The video will be trimmed to fit.",
                    total_duration,
                    platform.value,
                    max_dur,
                )

            # Apply client overrides
            client_overrides = overrides.get(platform, {})

            spec = PlatformOutputSpec(
                platform=platform,
                profile=profile,
                output_suffix=f"_{platform.value}",
                max_duration=max_dur,
                custom_resolution=client_overrides.get("resolution"),
                custom_aspect_ratio=client_overrides.get("aspect_ratio"),
                custom_fps=client_overrides.get("fps"),
                custom_bitrate=client_overrides.get("bitrate"),
            )

            specs.append(spec)
            logger.info(
                "[AUDIENCE] Platform %s: %s @ %dfps, %s",
                platform.value,
                spec.resolution,
                spec.fps,
                spec.video_bitrate,
            )

        if not specs:
            # Fallback to YouTube if no valid platforms
            logger.warning("[AUDIENCE] No valid platforms, defaulting to YouTube")
            youtube_profile = PLATFORM_PROFILES[TargetPlatform.YOUTUBE]
            specs.append(
                PlatformOutputSpec(
                    platform=TargetPlatform.YOUTUBE,
                    profile=youtube_profile,
                    output_suffix="",
                )
            )

        return specs

    def get_primary_spec(
        self,
        platforms: list[TargetPlatform],
    ) -> PlatformOutputSpec:
        """Get the primary (highest quality) output spec.

        Used for image generation aspect ratio decisions.
        Priority: TV > Cinema > YouTube > others.
        """
        priority_order = [
            TargetPlatform.CINEMA,
            TargetPlatform.TV_BROADCAST,
            TargetPlatform.YOUTUBE,
            TargetPlatform.LINKEDIN,
            TargetPlatform.FACEBOOK,
            TargetPlatform.INSTAGRAM_FEED,
            TargetPlatform.INSTAGRAM_REELS,
            TargetPlatform.TIKTOK,
            TargetPlatform.YOUTUBE_SHORTS,
        ]

        for priority in priority_order:
            if priority in platforms:
                profile = PLATFORM_PROFILES[priority]
                return PlatformOutputSpec(
                    platform=priority,
                    profile=profile,
                    output_suffix="",
                )

        # Default
        return PlatformOutputSpec(
            platform=TargetPlatform.YOUTUBE,
            profile=PLATFORM_PROFILES[TargetPlatform.YOUTUBE],
            output_suffix="",
        )
