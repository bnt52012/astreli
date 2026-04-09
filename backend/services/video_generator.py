"""
ÉTAPE 3 — Kling AI Video Generator

CHARACTER_PRODUCT mode:
  - Character scenes → Kling-Video-01 (human motion realism)
  - Product scenes   → Kling-V3 (object rotation, reflections)

PRODUCT_ONLY mode:
  - All scenes → Kling-V3

Async process: submit image + prompt → poll every 10s → download MP4.
"""
from __future__ import annotations

import asyncio
import logging
import time
import jwt
from pathlib import Path

import httpx

from backend.config import settings
from backend.models.schemas import PipelineMode, ScenePipeline, SceneType

logger = logging.getLogger(__name__)

KLING_CHARACTER_MODEL = "kling-v1"
KLING_PRODUCT_MODEL = "kling-v1-6"  # V3


class VideoGenerator:
    def __init__(self):
        self.base_url = settings.kling_base_url
        self._client: httpx.AsyncClient | None = None

    def _generate_jwt_token(self) -> str:
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
        if self._client is None or self._client.is_closed:
            token = self._generate_jwt_token()
            self._client = httpx.AsyncClient(
                base_url=self.base_url,
                headers={
                    "Authorization": f"Bearer {token}",
                    "Content-Type": "application/json",
                },
                timeout=60.0,
            )
        return self._client

    def _select_model(self, scene: ScenePipeline, mode: PipelineMode) -> str:
        if mode == PipelineMode.CHARACTER_PRODUCT and scene.analysis.type == SceneType.CHARACTER:
            return KLING_CHARACTER_MODEL
        return KLING_PRODUCT_MODEL

    async def submit_video_task(
        self,
        scene: ScenePipeline,
        mode: PipelineMode,
    ) -> str:
        """Submit an image-to-video generation task. Returns task_id."""
        client = await self._get_client()
        model = self._select_model(scene, mode)

        # Read image and encode to base64 data URI
        image_path = Path(scene.image_path)
        image_bytes = image_path.read_bytes()
        import base64
        b64 = base64.b64encode(image_bytes).decode()
        mime = "image/png" if image_path.suffix == ".png" else "image/jpeg"
        image_data_uri = f"data:{mime};base64,{b64}"

        payload = {
            "model_name": model,
            "input": {
                "image_url": image_data_uri,
                "prompt": scene.optimized_video_prompt,
                "duration": str(min(int(scene.analysis.duration), 10)),
                "cfg_scale": 0.5,
                "aspect_ratio": "16:9",
            },
        }

        response = await client.post(
            "/v1/videos/image2video",
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

        task_id = data["data"]["task_id"]
        logger.info(
            "Video task submitted: scene=%d, model=%s, task_id=%s",
            scene.analysis.id, model, task_id,
        )
        return task_id

    async def poll_video_task(self, task_id: str) -> dict:
        """Poll until video is ready. Returns {"status": ..., "video_url": ...}."""
        client = await self._get_client()

        for i in range(settings.kling_max_poll):
            response = await client.get(
                f"/v1/videos/image2video/{task_id}",
            )
            response.raise_for_status()
            data = response.json()["data"]

            status = data["task_status"]
            logger.debug("Poll %d: task=%s status=%s", i + 1, task_id, status)

            if status == "succeed":
                video_url = data["task_result"]["videos"][0]["url"]
                return {"status": "completed", "video_url": video_url}
            elif status == "failed":
                msg = data.get("task_status_msg", "Unknown error")
                return {"status": "failed", "error": msg}

            await asyncio.sleep(settings.kling_poll_interval)

        return {"status": "failed", "error": "Polling timeout"}

    async def download_video(self, video_url: str, output_path: Path) -> str:
        """Download the generated video clip."""
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.get(video_url)
            response.raise_for_status()
            output_path.write_bytes(response.content)
        logger.info("Video downloaded: %s", output_path)
        return str(output_path)

    async def generate_scene_video(
        self,
        scene: ScenePipeline,
        mode: PipelineMode,
        output_dir: Path,
    ) -> str:
        """Full flow: submit → poll → download. Returns local video path."""
        task_id = await self.submit_video_task(scene, mode)
        scene.video_job_id = task_id

        result = await self.poll_video_task(task_id)

        if result["status"] == "failed":
            raise RuntimeError(
                f"Video generation failed for scene {scene.analysis.id}: {result.get('error')}"
            )

        output_path = output_dir / f"scene_{scene.analysis.id}.mp4"
        return await self.download_video(result["video_url"], output_path)

    async def close(self):
        if self._client and not self._client.is_closed:
            await self._client.aclose()
