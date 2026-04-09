"""
ÉTAPE 4 — FFmpeg Final Assembly

Combines all video clips in scenario order:
- Uniform scaling to 1920x1080
- Scene transitions (fade / dissolve / wipe)
- Global fade-in / fade-out
- Background music with audio fade
- Brand logo overlay (top-right corner)
- H.264 professional quality export
"""
from __future__ import annotations

import asyncio
import logging
import shlex
from pathlib import Path

from backend.config import settings
from backend.models.schemas import ScenePipeline, TransitionType

logger = logging.getLogger(__name__)


class FFmpegAssembler:
    def __init__(self):
        self.ffmpeg = settings.ffmpeg_path
        self.resolution = settings.output_resolution
        self.codec = settings.output_codec
        self.preset = settings.output_preset
        self.crf = settings.output_crf

    async def _run(self, cmd: str) -> str:
        logger.info("FFmpeg: %s", cmd)
        proc = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            error = stderr.decode()
            logger.error("FFmpeg failed: %s", error)
            raise RuntimeError(f"FFmpeg error: {error}")
        return stdout.decode()

    def _build_transition_filter(
        self,
        scenes: list[ScenePipeline],
        transition_duration: float = 0.5,
    ) -> str:
        """Build the FFmpeg complex filtergraph for transitions between clips."""
        n = len(scenes)
        if n == 0:
            raise ValueError("No scenes to assemble")

        w, h = self.resolution.split("x")
        filters = []

        # Scale and set timing for each input
        for i in range(n):
            filters.append(
                f"[{i}:v]scale={w}:{h}:force_original_aspect_ratio=decrease,"
                f"pad={w}:{h}:(ow-iw)/2:(oh-ih)/2:black,"
                f"setsar=1,fps=30[v{i}]"
            )

        if n == 1:
            # Single scene: just add fade in/out
            filters.append(
                f"[v0]fade=t=in:st=0:d=0.5,fade=t=out:st=4:d=0.5[vout]"
            )
            return ";".join(filters), "[vout]"

        # Chain transitions between clips using xfade
        prev = "v0"
        offset = 0.0
        for i in range(1, n):
            scene = scenes[i]
            prev_duration = scenes[i - 1].analysis.duration
            offset += prev_duration - transition_duration

            transition = self._map_transition(scene.analysis.transition)
            out_label = f"xf{i}" if i < n - 1 else "xfinal"

            filters.append(
                f"[{prev}][v{i}]xfade=transition={transition}"
                f":duration={transition_duration}:offset={offset:.2f}[{out_label}]"
            )
            prev = out_label

        # Add global fade in/out
        filters.append(
            f"[{prev}]fade=t=in:st=0:d=0.8,fade=t=out:st=end:d=0.8[vout]"
        )

        return ";".join(filters), "[vout]"

    def _map_transition(self, transition: TransitionType) -> str:
        mapping = {
            TransitionType.FADE: "fade",
            TransitionType.DISSOLVE: "dissolve",
            TransitionType.WIPE: "wipeleft",
            TransitionType.CUT: "fade",  # instant cut simulated with very short fade
        }
        return mapping.get(transition, "fade")

    async def assemble(
        self,
        scenes: list[ScenePipeline],
        output_path: Path,
        music_path: str | None = None,
        logo_path: str | None = None,
    ) -> str:
        """Assemble all scene videos into the final ad."""
        if not scenes:
            raise ValueError("No scenes to assemble")

        # Verify all video paths exist
        for s in scenes:
            if not s.video_path or not Path(s.video_path).exists():
                raise FileNotFoundError(f"Missing video for scene {s.analysis.id}")

        # Build input arguments
        inputs = " ".join(f"-i {shlex.quote(s.video_path)}" for s in scenes)

        # Build filtergraph
        filter_complex, video_out = self._build_transition_filter(scenes)
        filter_parts = [filter_complex]

        # Logo overlay (if provided)
        final_video_label = video_out.strip("[]")
        if logo_path and Path(logo_path).exists():
            logo_idx = len(scenes)
            inputs += f" -i {shlex.quote(logo_path)}"
            filter_parts.append(
                f"[{logo_idx}:v]scale=120:-1[logo];"
                f"[{final_video_label}][logo]overlay=W-w-30:30[vlogo]"
            )
            final_video_label = "vlogo"

        # Audio: music track with fade
        audio_args = ""
        if music_path and Path(music_path).exists():
            inputs += f" -i {shlex.quote(music_path)}"
            audio_idx = len(scenes) + (1 if logo_path else 0)
            # Calculate total duration
            total_dur = sum(s.analysis.duration for s in scenes) - 0.5 * (len(scenes) - 1)
            audio_args = (
                f"-filter_complex_append "
                f"\"[{audio_idx}:a]afade=t=in:d=1.5,afade=t=out:st={total_dur - 2}:d=2,"
                f"atrim=0:{total_dur}[aout]\" "
                f"-map \"[aout]\""
            )
        else:
            audio_args = "-an"

        # Final command
        full_filter = ";".join(filter_parts)
        cmd = (
            f"{self.ffmpeg} -y {inputs} "
            f"-filter_complex \"{full_filter}\" "
            f"-map \"[{final_video_label}]\" {audio_args} "
            f"-c:v {self.codec} -preset {self.preset} -crf {self.crf} "
            f"-pix_fmt yuv420p -movflags +faststart "
            f"{shlex.quote(str(output_path))}"
        )

        await self._run(cmd)
        logger.info("Final video assembled: %s", output_path)
        return str(output_path)
