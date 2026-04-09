"""
Audience Adapter — multi-platform output adaptation.

Generates correct aspect ratio and encoding per target platform.
Multiple versions from one pipeline run.
"""
from __future__ import annotations

import logging
import subprocess
from pathlib import Path

from models.enums import PLATFORM_ASPECT_RATIOS, PLATFORM_RESOLUTIONS, TargetPlatform

logger = logging.getLogger(__name__)


class AudienceAdapter:
    """Adapts pipeline output for multiple target platforms."""

    def get_platform_config(self, platform: TargetPlatform) -> dict[str, str]:
        """Get configuration for a specific platform.

        Returns:
            Dict with aspect_ratio, resolution, encoding hints.
        """
        return {
            "aspect_ratio": PLATFORM_ASPECT_RATIOS.get(platform, "16:9"),
            "resolution": PLATFORM_RESOLUTIONS.get(platform, "1920x1080"),
            "platform": platform.value,
        }

    def generate_platform_versions(
        self,
        source_video: Path,
        output_dir: Path,
        platforms: list[TargetPlatform],
    ) -> dict[str, Path]:
        """Generate platform-specific versions of the final video.

        Args:
            source_video: Path to the main assembled video.
            output_dir: Where to save platform versions.
            platforms: Target platforms.

        Returns:
            Dict mapping platform name to output path.
        """
        output_dir.mkdir(parents=True, exist_ok=True)
        results: dict[str, Path] = {}

        for platform in platforms:
            config = self.get_platform_config(platform)
            output_path = output_dir / f"final_{platform.value}.mp4"

            try:
                self._convert_for_platform(
                    source_video, output_path,
                    resolution=config["resolution"],
                    aspect_ratio=config["aspect_ratio"],
                )
                results[platform.value] = output_path
                logger.info("Generated %s version: %s", platform.value, output_path)
            except Exception as e:
                logger.error("Failed to generate %s version: %s", platform.value, e)

        return results

    def _convert_for_platform(
        self,
        source: Path,
        output: Path,
        resolution: str,
        aspect_ratio: str,
    ) -> None:
        """Convert video for a specific platform using FFmpeg."""
        w, h = resolution.split("x")

        cmd = [
            "ffmpeg", "-y", "-i", str(source),
            "-vf", (
                f"scale={w}:{h}:force_original_aspect_ratio=decrease,"
                f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black"
            ),
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            str(output),
        ]

        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg conversion failed: {result.stderr[:500]}")

    def get_image_dimensions(self, platform: TargetPlatform) -> tuple[int, int]:
        """Get image generation dimensions for a platform."""
        dims = {
            TargetPlatform.YOUTUBE: (1024, 576),
            TargetPlatform.INSTAGRAM_FEED: (1024, 1024),
            TargetPlatform.INSTAGRAM_STORY: (576, 1024),
            TargetPlatform.TIKTOK: (576, 1024),
            TargetPlatform.TV: (1024, 576),
            TargetPlatform.LINKEDIN: (1024, 1024),
        }
        return dims.get(platform, (1024, 576))
