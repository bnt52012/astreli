"""
FFmpeg Video Assembler — final pipeline step.

Assembles all video clips in scenario order with transitions,
music, and logo overlay.
"""
from __future__ import annotations

import json
import logging
import subprocess
from pathlib import Path
from typing import Any

from models.scene import ScenePipeline
from pipeline.config import PIPELINE_DEFAULTS
from pipeline.exceptions import AssemblyError
from services.assembly.audio_mixer import AudioMixer
from services.assembly.logo_overlay import LogoOverlay
from services.assembly.transitions import TransitionBuilder

logger = logging.getLogger(__name__)


class VideoAssembler:
    """Assembles final video from scene clips using FFmpeg."""

    def __init__(self) -> None:
        self.fps = PIPELINE_DEFAULTS.ffmpeg_fps
        self.resolution = PIPELINE_DEFAULTS.ffmpeg_resolution
        self.crf = PIPELINE_DEFAULTS.ffmpeg_crf
        self.preset = PIPELINE_DEFAULTS.ffmpeg_preset
        self.transition_builder = TransitionBuilder()
        self.audio_mixer = AudioMixer()
        self.logo_overlay = LogoOverlay()

    def assemble(
        self,
        scenes: list[ScenePipeline],
        output_path: Path,
        music_path: str | None = None,
        logo_path: str | None = None,
    ) -> Path:
        """Assemble all scene clips into final video.

        Args:
            scenes: List of scenes with video_path set.
            output_path: Where to save the final video.
            music_path: Optional background music file.
            logo_path: Optional brand logo for overlay.

        Returns:
            Path to the final assembled video.
        """
        # Collect valid clips
        clips = [
            s for s in scenes
            if s.video_path and s.video_path.exists() and not s.failed
        ]

        if not clips:
            raise AssemblyError("No valid video clips to assemble.")

        output_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            if len(clips) == 1:
                result = self._assemble_single(clips[0], output_path, music_path, logo_path)
            else:
                result = self._assemble_multiple(clips, output_path, music_path, logo_path)

            logger.info("Final video assembled: %s", result)
            return result

        except subprocess.CalledProcessError as e:
            raise AssemblyError(f"FFmpeg failed: {e.stderr}")
        except Exception as e:
            raise AssemblyError(f"Assembly failed: {e}")

    def _assemble_single(
        self,
        scene: ScenePipeline,
        output_path: Path,
        music_path: str | None,
        logo_path: str | None,
    ) -> Path:
        """Handle single clip — just re-encode with effects."""
        filters = [f"scale={self.resolution}:force_original_aspect_ratio=decrease,pad={self.resolution}:(ow-iw)/2:(oh-ih)/2"]

        # Fade in/out
        filters.append("fade=t=in:st=0:d=0.5")
        filters.append(f"fade=t=out:st={max(0, scene.duration_seconds - 0.5)}:d=0.5")

        cmd = ["ffmpeg", "-y", "-i", str(scene.video_path)]

        filter_str = ",".join(filters)

        if logo_path and Path(logo_path).exists():
            logo_filter = self.logo_overlay.build_filter(logo_path)
            cmd.extend(["-i", logo_path])
            filter_str = f"[0:v]{filter_str}[main];{logo_filter}"
            cmd.extend(["-filter_complex", filter_str, "-map", "[out]"])
        else:
            cmd.extend(["-vf", filter_str])

        # Audio
        if music_path and Path(music_path).exists():
            cmd.extend(["-i", music_path, "-shortest"])
            cmd.extend(["-af", self.audio_mixer.build_fade_filter(scene.duration_seconds)])

        cmd.extend([
            "-c:v", "libx264",
            "-preset", self.preset,
            "-crf", str(self.crf),
            "-pix_fmt", "yuv420p",
            "-r", str(self.fps),
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            str(output_path),
        ])

        logger.info("FFmpeg single clip: %s", " ".join(cmd))
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return output_path

    def _assemble_multiple(
        self,
        clips: list[ScenePipeline],
        output_path: Path,
        music_path: str | None,
        logo_path: str | None,
    ) -> Path:
        """Assemble multiple clips with transitions."""
        # Step 1: Create concat file with normalized clips
        concat_dir = output_path.parent / "concat_temp"
        concat_dir.mkdir(exist_ok=True)

        normalized_paths = []
        for i, scene in enumerate(clips):
            norm_path = concat_dir / f"norm_{i:03d}.mp4"
            self._normalize_clip(scene.video_path, norm_path)
            normalized_paths.append(norm_path)

        # Step 2: Build FFmpeg complex filter for transitions
        if len(normalized_paths) <= 1:
            # Shouldn't happen but safety
            import shutil
            shutil.copy2(str(normalized_paths[0]), str(output_path))
            return output_path

        # Build concat with transitions
        temp_concat = concat_dir / "concat_list.txt"
        with open(temp_concat, "w") as f:
            for p in normalized_paths:
                f.write(f"file '{p}'\n")

        cmd = [
            "ffmpeg", "-y",
            "-f", "concat", "-safe", "0", "-i", str(temp_concat),
        ]

        # Build video filter
        vfilters = [f"scale={self.resolution}:force_original_aspect_ratio=decrease,pad={self.resolution}:(ow-iw)/2:(oh-ih)/2"]
        total_duration = sum(s.duration_seconds for s in clips)
        vfilters.append("fade=t=in:st=0:d=0.5")
        vfilters.append(f"fade=t=out:st={max(0, total_duration - 0.5)}:d=0.5")

        # Logo overlay
        if logo_path and Path(logo_path).exists():
            cmd.extend(["-i", logo_path])
            vfilter_str = ",".join(vfilters)
            logo_filter = self.logo_overlay.build_filter(logo_path)
            cmd.extend(["-filter_complex", f"[0:v]{vfilter_str}[main];{logo_filter}"])
            cmd.extend(["-map", "[out]"])
        else:
            cmd.extend(["-vf", ",".join(vfilters)])

        # Audio
        if music_path and Path(music_path).exists():
            cmd.extend(["-i", music_path, "-shortest"])
            cmd.extend(["-af", self.audio_mixer.build_fade_filter(total_duration)])

        cmd.extend([
            "-c:v", "libx264",
            "-preset", self.preset,
            "-crf", str(self.crf),
            "-pix_fmt", "yuv420p",
            "-r", str(self.fps),
            "-c:a", "aac", "-b:a", "192k",
            "-movflags", "+faststart",
            str(output_path),
        ])

        logger.info("FFmpeg multi-clip assembly: %d clips", len(clips))
        subprocess.run(cmd, check=True, capture_output=True, text=True)

        # Cleanup temp
        import shutil
        shutil.rmtree(concat_dir, ignore_errors=True)

        return output_path

    def _normalize_clip(self, input_path: Path, output_path: Path) -> None:
        """Normalize a clip to standard resolution and fps."""
        cmd = [
            "ffmpeg", "-y", "-i", str(input_path),
            "-vf", f"scale={self.resolution}:force_original_aspect_ratio=decrease,pad={self.resolution}:(ow-iw)/2:(oh-ih)/2,fps={self.fps}",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-an",
            str(output_path),
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
