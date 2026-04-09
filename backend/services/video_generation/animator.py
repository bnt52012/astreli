"""
Kling AI Video Animator — Step 3 of the AdGenAI Pipeline.

Orchestrates video generation for all scenes:
- personnage scenes → kling-v1 (human motion realism)
- produit scenes → kling-v1-6 (product rotation, reflections)

All tasks are submitted concurrently and polled in parallel.
"""

from __future__ import annotations

import asyncio
import base64
import logging
import time
from pathlib import Path

import jwt
import httpx

from backend.config import settings
from backend.models.enums import PipelineMode, SceneType
from backend.models.scene import ScenePipeline
from backend.pipeline.exceptions import (
    AuthenticationError,
    VideoGenerationError,
)
from backend.services.video_generation.download import download_video
from backend.services.video_generation.kling_v3 import KLING_V3_MODEL
from backend.services.video_generation.kling_video01 import KLING_VIDEO01_MODEL
from backend.services.video_generation.task_manager import TaskManager
from backend.utils.http_client import create_resilient_client

logger = logging.getLogger(__name__)


class VideoAnimator:
    """Kling AI video generation orchestrator.

    Handles JWT authentication, task submission, concurrent polling,
    and video download for all scenes in parallel.
    """

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None
        self._task_manager = TaskManager(
            poll_interval=settings.kling_poll_interval,
            max_timeout=settings.kling_poll_interval * settings.kling_max_poll,
            max_concurrent=4,
        )

    def _generate_jwt(self) -> str:
        """Generate JWT token for Kling API authentication."""
        now = int(time.time())
        payload = {
            "iss": settings.kling_api_key,
            "exp": now + 1800,
            "nbf": now - 5,
            "iat": now,
        }
        return jwt.encode(payload, settings.kling_api_secret, algorithm="HS256")

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create the HTTP client with current JWT."""
        if self._client is None or self._client.is_closed:
            token = self._generate_jwt()
            self._client = create_resilient_client(
                base_url=settings.kling_base_url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                timeout=60.0,
            )
        return self._client

    def _select_model(self, scene: ScenePipeline, mode: PipelineMode) -> str:
        """Select the appropriate Kling model for a scene."""
        if (
            mode == PipelineMode.PERSONNAGE_ET_PRODUIT
            and scene.analysis.type == SceneType.PERSONNAGE
        ):
            return KLING_VIDEO01_MODEL
        return KLING_V3_MODEL

    async def submit_task(
        self,
        scene: ScenePipeline,
        mode: PipelineMode,
    ) -> str:
        """Submit an image-to-video generation task to Kling.

        Args:
            scene: Scene with generated image.
            mode: Pipeline mode for model selection.

        Returns:
            Kling task ID.

        Raises:
            VideoGenerationError: If submission fails.
        """
        client = await self._get_client()
        model = self._select_model(scene, mode)

        # Encode image as base64 data URI
        image_path = Path(scene.image_path)
        if not image_path.exists():
            raise VideoGenerationError(
                f"Image file not found: {image_path}",
                scene_index=scene.analysis.id,
            )

        image_bytes = image_path.read_bytes()
        b64 = base64.b64encode(image_bytes).decode()
        suffix = image_path.suffix.lower()
        mime = "image/png" if suffix == ".png" else "image/jpeg"
        data_uri = f"data:{mime};base64,{b64}"

        payload = {
            "model_name": model,
            "input": {
                "image_url": data_uri,
                "prompt": scene.final_video_prompt,
                "duration": str(min(int(scene.analysis.duration), 10)),
                "cfg_scale": 0.5,
                "aspect_ratio": "16:9",
            },
        }

        try:
            response = await client.post("/v1/videos/image2video", json=payload)
            response.raise_for_status()
            data = response.json()

            task_id = data["data"]["task_id"]
            scene.video_job_id = task_id
            scene.video_generation_model = model

            logger.info(
                "[VIDEO] Task submitted: scene=%d, model=%s, task=%s",
                scene.analysis.id, model, task_id,
            )
            return task_id

        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                raise AuthenticationError("kling") from e
            raise VideoGenerationError(
                f"Kling submission failed (HTTP {e.response.status_code})",
                model=model,
                scene_index=scene.analysis.id,
            ) from e
        except Exception as e:
            raise VideoGenerationError(
                f"Kling submission failed: {e}",
                model=model,
                scene_index=scene.analysis.id,
            ) from e

    async def poll_task(self, task_id: str) -> dict:
        """Poll a single task's status.

        Returns:
            Dict with "status" (completed/failed/processing) and optional "video_url"/"error".
        """
        client = await self._get_client()

        response = await client.get(f"/v1/videos/image2video/{task_id}")
        response.raise_for_status()
        data = response.json()["data"]

        status = data.get("task_status", "")

        if status == "succeed":
            video_url = data["task_result"]["videos"][0]["url"]
            return {"status": "completed", "video_url": video_url}
        elif status == "failed":
            msg = data.get("task_status_msg", "Unknown error")
            return {"status": "failed", "error": msg}
        else:
            return {"status": "processing"}

    async def generate_all_scenes(
        self,
        scenes: list[ScenePipeline],
        mode: PipelineMode,
        output_dir: Path,
    ) -> list[ScenePipeline]:
        """Generate videos for all ready scenes concurrently.

        Submits all tasks, polls in parallel, downloads results.

        Args:
            scenes: Scenes with generated images (status="image_ready").
            mode: Pipeline mode.
            output_dir: Directory for output videos.

        Returns:
            Updated scenes with video paths and statuses.
        """
        ready_scenes = [s for s in scenes if s.is_ready_for_video]
        if not ready_scenes:
            logger.warning("[VIDEO] No scenes ready for video generation")
            return scenes

        # Step 1: Submit all tasks concurrently
        logger.info("[VIDEO] Submitting %d video tasks concurrently", len(ready_scenes))

        submit_tasks = [self.submit_task(scene, mode) for scene in ready_scenes]
        submit_results = await asyncio.gather(*submit_tasks, return_exceptions=True)

        # Register successful submissions for polling
        task_manager = TaskManager(
            poll_interval=settings.kling_poll_interval,
            max_timeout=settings.kling_poll_interval * settings.kling_max_poll,
        )

        submitted_scenes: dict[str, ScenePipeline] = {}
        for scene, result in zip(ready_scenes, submit_results):
            if isinstance(result, Exception):
                scene.status = "video_failed"
                scene.error = str(result)
                logger.error(
                    "[VIDEO] Submit failed for scene %d: %s",
                    scene.analysis.id, result,
                )
            else:
                task_id = result
                task_manager.register_task(scene.analysis.id, task_id, scene.kling_model)
                submitted_scenes[task_id] = scene

        # Step 2: Poll all tasks concurrently
        if submitted_scenes:
            logger.info("[VIDEO] Polling %d tasks concurrently", len(submitted_scenes))
            completed_tasks = await task_manager.poll_all(self.poll_task)

            # Step 3: Download completed videos
            download_tasks = []
            for task in completed_tasks:
                scene = submitted_scenes.get(task.task_id)
                if not scene:
                    continue

                if task.status == "completed" and task.video_url:
                    video_path = output_dir / f"scene_{scene.analysis.id:03d}.mp4"
                    download_tasks.append(
                        self._download_and_update(scene, task.video_url, video_path)
                    )
                else:
                    scene.status = "video_failed"
                    scene.error = task.error or "Unknown failure"

            if download_tasks:
                await asyncio.gather(*download_tasks, return_exceptions=True)

        return scenes

    async def _download_and_update(
        self,
        scene: ScenePipeline,
        video_url: str,
        output_path: Path,
    ) -> None:
        """Download video and update scene status."""
        try:
            start_time = time.time()
            path = await download_video(video_url, output_path)
            elapsed_ms = int((time.time() - start_time) * 1000)

            scene.video_path = path
            scene.video_url = video_url
            scene.video_generation_time_ms = elapsed_ms
            scene.status = "video_ready"

            logger.info(
                "[VIDEO] Scene %d video ready (%dms): %s",
                scene.analysis.id, elapsed_ms, path,
            )
        except Exception as e:
            scene.status = "video_failed"
            scene.error = str(e)
            logger.error(
                "[VIDEO] Download failed for scene %d: %s",
                scene.analysis.id, e,
            )

    async def close(self) -> None:
        """Close the HTTP client."""
        if self._client and not self._client.is_closed:
            await self._client.aclose()
