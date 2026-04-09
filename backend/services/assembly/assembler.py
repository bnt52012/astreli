"""
FFmpeg Video Assembler — Step 4 of the AdGenAI Pipeline.

Combines all scene video clips into the final ad:
- Uniform scaling to target resolution
- Scene transitions (xfade with 15+ types)
- Global fade in/out
- Background music with audio fade
- Brand logo overlay (configurable position)
- H.264 professional encoding

Handles both single-clip and multi-clip scenarios.
"""

from __future__ import annotations

import asyncio
import logging
import shlex
from pathlib import Path

from backend.models.enums import QualityLevel
from backend.models.scene import ScenePipeline
from backend.pipeline.config import PIPELINE_DEFAULTS
from backend.pipeline.exceptions import AssemblyError, MissingClipError
from backend.services.assembly.audio_mixer import build_audio_filter
from backend.services.assembly.encoder import get_encoding_args
from backend.services.assembly.logo_overlay import build_logo_filter
from backend.services.assembly.transitions import (
    build_xfade_filter,
    get_transition_duration,
)

logger = logging.getLogger(__name__)


class VideoAssembler:
    """FFmpeg-based video assembly orchestrator.

    Builds complex FFmpeg filter graphs for professional video output
    with transitions, audio, and logo overlay.
    """

    def __init__(
        self,
        ffmpeg_path: str = "ffmpeg",
        quality: QualityLevel = QualityLevel.PREMIUM,
        resolution: str = "1920x1080",
        fps: int = 30,
    ) -> None:
        self._ffmpeg = ffmpeg_path
        self._quality = quality
        self._resolution = resolution
        self._fps = fps

    async def assemble(
        self,
        scenes: list[ScenePipeline],
        output_path: Path,
        music_path: str | None = None,
        logo_path: str | None = None,
    ) -> str:
        """Assemble all scene videos into the final ad.

        Args:
            scenes: Completed scenes with video paths, sorted by ID.
            output_path: Path for the final output file.
            music_path: Optional background music file path.
            logo_path: Optional brand logo PNG path.

        Returns:
            Path to the assembled video.

        Raises:
            AssemblyError: If FFmpeg fails.
            MissingClipError: If a scene's video file is missing.
        """
        if not scenes:
            raise AssemblyError("No scenes to assemble")

        # Validate all clips exist
        for s in scenes:
            if not s.video_path or not Path(s.video_path).exists():
                raise MissingClipError(s.analysis.id, s.video_path or "None")

        # Sort by scene ID
        scenes = sorted(scenes, key=lambda s: s.analysis.id)

        if len(scenes) == 1:
            return await self._assemble_single(scenes[0], output_path, music_path, logo_path)

        return await self._assemble_multi(scenes, output_path, music_path, logo_path)

    async def _assemble_single(
        self,
        scene: ScenePipeline,
        output_path: Path,
        music_path: str | None,
        logo_path: str | None,
    ) -> str:
        """Handle single-clip assembly (just encoding + optional overlays)."""
        w, h = self._resolution.split("x")
        inputs = f"-i {shlex.quote(scene.video_path)}"
        filters = [
            f"[0:v]scale={w}:{h}:force_original_aspect_ratio=decrease,"
            f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black,"
            f"setsar=1,fps={self._fps},"
            f"fade=t=in:st=0:d={PIPELINE_DEFAULTS.fade_in_duration},"
            f"fade=t=out:st={max(0, scene.analysis.duration - PIPELINE_DEFAULTS.fade_out_duration)}"
            f":d={PIPELINE_DEFAULTS.fade_out_duration}[vout]"
        ]
        video_label = "vout"

        input_count = 1
        # Logo overlay
        if logo_path and Path(logo_path).exists():
            inputs += f" -i {shlex.quote(logo_path)}"
            logo_filter = build_logo_filter(input_count, video_label, "vlogo")
            filters.append(logo_filter)
            video_label = "vlogo"
            input_count += 1

        # Audio
        audio_args = "-an"
        if music_path and Path(music_path).exists():
            inputs += f" -i {shlex.quote(music_path)}"
            audio_filter, audio_label = build_audio_filter(
                input_count, scene.analysis.duration,
            )
            filters.append(audio_filter)
            audio_args = f'-map "[{audio_label}]"'
            input_count += 1

        encoding = get_encoding_args(self._quality, self._resolution, self._fps)

        cmd = (
            f'{self._ffmpeg} -y {inputs} '
            f'-filter_complex "{";".join(filters)}" '
            f'-map "[{video_label}]" {audio_args} '
            f'{encoding} '
            f'{shlex.quote(str(output_path))}'
        )

        await self._run_ffmpeg(cmd)
        return str(output_path)

    async def _assemble_multi(
        self,
        scenes: list[ScenePipeline],
        output_path: Path,
        music_path: str | None,
        logo_path: str | None,
    ) -> str:
        """Handle multi-clip assembly with transitions."""
        n = len(scenes)
        w, h = self._resolution.split("x")

        # Build inputs
        inputs = " ".join(f"-i {shlex.quote(s.video_path)}" for s in scenes)
        input_count = n
        filters: list[str] = []

        # Scale each input
        for i in range(n):
            filters.append(
                f"[{i}:v]scale={w}:{h}:force_original_aspect_ratio=decrease,"
                f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black,"
                f"setsar=1,fps={self._fps}[v{i}]"
            )

        # Chain xfade transitions
        prev = "v0"
        offset = 0.0
        transition_dur = PIPELINE_DEFAULTS.transition_duration_seconds

        for i in range(1, n):
            scene = scenes[i]
            prev_duration = scenes[i - 1].analysis.duration
            t_dur = get_transition_duration(scene.analysis.transition, transition_dur)
            offset += prev_duration - t_dur

            out_label = f"xf{i}" if i < n - 1 else "xfinal"
            xfade = build_xfade_filter(
                prev, f"v{i}", out_label,
                scene.analysis.transition, offset, t_dur,
            )
            filters.append(xfade)
            prev = out_label

        # Global fade in/out
        total_dur = self._calculate_total_duration(scenes, transition_dur)
        fade_out_start = max(0, total_dur - PIPELINE_DEFAULTS.fade_out_duration)
        filters.append(
            f"[{prev}]fade=t=in:st=0:d={PIPELINE_DEFAULTS.fade_in_duration},"
            f"fade=t=out:st={fade_out_start:.2f}:d={PIPELINE_DEFAULTS.fade_out_duration}[vout]"
        )
        video_label = "vout"

        # Logo overlay
        if logo_path and Path(logo_path).exists():
            inputs += f" -i {shlex.quote(logo_path)}"
            logo_filter = build_logo_filter(input_count, video_label, "vlogo")
            filters.append(logo_filter)
            video_label = "vlogo"
            input_count += 1

        # Audio
        audio_args = "-an"
        if music_path and Path(music_path).exists():
            inputs += f" -i {shlex.quote(music_path)}"
            audio_filter, audio_label = build_audio_filter(
                input_count, total_dur,
            )
            filters.append(audio_filter)
            audio_args = f'-map "[{audio_label}]"'
            input_count += 1

        encoding = get_encoding_args(self._quality, self._resolution, self._fps)
        full_filter = ";".join(filters)

        cmd = (
            f'{self._ffmpeg} -y {inputs} '
            f'-filter_complex "{full_filter}" '
            f'-map "[{video_label}]" {audio_args} '
            f'{encoding} '
            f'{shlex.quote(str(output_path))}'
        )

        await self._run_ffmpeg(cmd)
        logger.info("[ASSEMBLY] Final video: %s", output_path)
        return str(output_path)

    def _calculate_total_duration(
        self,
        scenes: list[ScenePipeline],
        transition_dur: float,
    ) -> float:
        """Calculate total video duration accounting for transition overlaps."""
        total = sum(s.analysis.duration for s in scenes)
        overlaps = (len(scenes) - 1) * transition_dur
        return total - overlaps

    async def _run_ffmpeg(self, cmd: str) -> str:
        """Execute an FFmpeg command."""
        logger.info("[ASSEMBLY] Running FFmpeg command")
        logger.debug("[ASSEMBLY] CMD: %s", cmd)

        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()

        if proc.returncode != 0:
            error_text = stderr.decode(errors="replace")
            raise AssemblyError(
                f"FFmpeg exited with code {proc.returncode}",
                ffmpeg_stderr=error_text,
            )

        return stdout.decode(errors="replace")
