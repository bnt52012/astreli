"""
Video Animator — Routes scenes to the correct Fal.ai Kling model.

personnage scenes → Kling O1 Pro image-to-video (optimized for humans)
produit scenes    → Kling 2.5 Turbo Pro image-to-video (optimized for products)
"""
from __future__ import annotations

import logging
from pathlib import Path

from models.enums import SceneType
from models.scene import ScenePipeline
from pipeline.config import PIPELINE_DEFAULTS
from pipeline.exceptions import VideoGenerationError
from services.video_generation.task_manager import FalVideoTaskManager

logger = logging.getLogger(__name__)


class VideoAnimator:
    """Animates scene images into video clips via Fal.ai (Kling models)."""

    def __init__(self) -> None:
        self.task_manager = FalVideoTaskManager(timeout=PIPELINE_DEFAULTS.fal_timeout)

    async def animate_scene(
        self,
        scene: ScenePipeline,
        output_dir: Path,
    ) -> Path | None:
        """Animate a single scene using Fal.ai."""
        if not scene.final_image_path or not scene.final_image_path.exists():
            logger.warning("Scene %d has no image to animate.", scene.index)
            return None

        if scene.scene_type == SceneType.TRANSITION:
            logger.info("Scene %d is transition — skipping animation.", scene.index)
            return None

        # Route to the correct Fal model based on scene type.
        model = (
            PIPELINE_DEFAULTS.fal_model_human
            if scene.scene_type == SceneType.PERSONNAGE
            else PIPELINE_DEFAULTS.fal_model_product
        )

        prompt = scene.enriched_prompt_video or scene.prompt_video or ""
        video_path = output_dir / "videos" / f"scene_{scene.index:02d}.mp4"
        video_path.parent.mkdir(parents=True, exist_ok=True)

        try:
            result = await self.task_manager.submit_and_wait(
                model=model,
                image_path=scene.final_image_path,
                prompt=prompt,
                duration=scene.duration_seconds,
                aspect_ratio=scene.metadata.get("aspect_ratio", "16:9"),
                output_path=video_path,
            )

            scene.video_path = result
            scene.video_generated = True
            logger.info("Scene %d animated via %s: %s", scene.index, model, result)
            return result

        except Exception as e:
            logger.error("Scene %d animation failed (%s): %s", scene.index, model, e)
            raise VideoGenerationError(scene.index, str(e))

    async def animate_all(
        self,
        scenes: list[ScenePipeline],
        output_dir: Path,
    ) -> list[ScenePipeline]:
        """Animate all eligible scenes concurrently."""
        import asyncio

        tasks = []
        for scene in scenes:
            if scene.image_generated and not scene.failed:
                tasks.append(self._safe_animate(scene, output_dir))

        if tasks:
            await asyncio.gather(*tasks)

        animated = sum(1 for s in scenes if s.video_generated)
        logger.info("Animated %d/%d scenes.", animated, len(scenes))
        return scenes

    async def _safe_animate(self, scene: ScenePipeline, output_dir: Path) -> None:
        """Animate with error handling — don't fail the whole batch."""
        try:
            await self.animate_scene(scene, output_dir)
        except Exception as e:
            logger.error("Scene %d animation error (continuing): %s", scene.index, e)
            scene.mark_failed(f"Video animation: {e}")
