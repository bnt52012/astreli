"""
Fal.ai Task Manager — submit image-to-video tasks via fal-client.

Replaces the previous direct Kling API integration. Fal.ai proxies to Kling's
video models on a pay-as-you-go basis, so there is no JWT / access-key dance.
fal-client reads FAL_KEY from the environment automatically.
"""
from __future__ import annotations

import asyncio
import logging
from pathlib import Path

import requests

logger = logging.getLogger(__name__)


class FalVideoTaskManager:
    """Submits image-to-video jobs to Fal.ai and downloads the results."""

    def __init__(self, timeout: int = 600) -> None:
        self.timeout = timeout

    async def submit_and_wait(
        self,
        model: str,
        image_path: Path,
        prompt: str,
        duration: float,
        aspect_ratio: str,
        output_path: Path,
    ) -> Path:
        """Embed the scene image as a data URI, submit the fal job, download the clip.

        We bypass fal's storage upload API (which has its own balance gate and
        permissioning) by sending the image inline as a base64 data URI. This
        is simpler, avoids an extra round-trip, and works on any valid FAL_KEY.

        Args:
            model: Fal model id, e.g. "fal-ai/kling-video/v2.5-turbo/pro/image-to-video".
            image_path: Local path to the scene image to animate.
            prompt: Video animation prompt.
            duration: Desired duration in seconds (clamped to "5" or "10").
            aspect_ratio: e.g. "16:9", "9:16", "1:1".
            output_path: Where to save the downloaded MP4.

        Returns:
            Path to the downloaded video file.
        """
        import base64
        import fal_client

        loop = asyncio.get_event_loop()

        # 1. Encode the scene image as a data URI.
        img_bytes = image_path.read_bytes()
        suffix = image_path.suffix.lstrip(".").lower() or "png"
        mime = "image/jpeg" if suffix in ("jpg", "jpeg") else f"image/{suffix}"
        b64 = base64.b64encode(img_bytes).decode("ascii")
        image_url = f"data:{mime};base64,{b64}"
        logger.info(
            "Fal INLINE: %s (%d bytes → %d chars data URI)",
            image_path, len(img_bytes), len(image_url),
        )

        # 2. Submit the job. Fal only supports "5" or "10" second durations.
        dur_str = "10" if float(duration) > 7.5 else "5"

        # Safety net: Kling needs scene CONTENT, not just camera directives.
        # If the caller only sent camera instructions (or nothing), add a
        # neutral content hint so the model has a subject to animate.
        safe_prompt = (prompt or "").strip()
        if not safe_prompt:
            safe_prompt = (
                "Cinematic subtle motion on the subject in the reference image, "
                "preserving composition and lighting exactly."
            )
            logger.warning("Fal received EMPTY prompt — using neutral fallback")

        # Fal's prompt field accepts up to 2500 chars. We send the FULL
        # Kling-optimized prompt from build_kling_video_prompt(); the only
        # clipping is Fal's own hard limit.
        final_prompt = safe_prompt[:2500]
        if len(safe_prompt) > 2500:
            logger.warning(
                "Fal prompt truncated from %d → 2500 chars (model hard limit)",
                len(safe_prompt),
            )

        arguments = {
            "image_url": image_url,
            "prompt": final_prompt,
            "duration": dur_str,
            "aspect_ratio": aspect_ratio,
        }

        def _on_queue_update(update):
            # Log Fal's in-queue progress updates (includes logs from the model).
            try:
                cls = type(update).__name__
                if hasattr(update, "logs") and update.logs:
                    for entry in update.logs[-3:]:
                        msg = entry.get("message") if isinstance(entry, dict) else str(entry)
                        logger.info("Fal [%s] %s", cls, msg)
                else:
                    logger.info("Fal [%s] status update", cls)
            except Exception:
                pass

        logger.info(
            "Fal SUBMIT → %s | duration=%s aspect=%s prompt_len=%d",
            model, dur_str, aspect_ratio, len(prompt or ""),
        )

        print(f"\n{'='*60}", flush=True)
        print(f"FAL VIDEO PROMPT FOR SCENE:", flush=True)
        print(f"Model: {model}", flush=True)
        print(f"Prompt ({len(final_prompt)} chars): {final_prompt}", flush=True)
        print(f"Duration: {dur_str}", flush=True)
        print(f"Aspect: {aspect_ratio}", flush=True)
        print(f"{'='*60}\n", flush=True)

        try:
            result = await loop.run_in_executor(
                None,
                lambda: fal_client.subscribe(
                    model,
                    arguments=arguments,
                    with_logs=True,
                    on_queue_update=_on_queue_update,
                ),
            )
        except Exception as e:
            logger.error("Fal SUBMIT failed for model %s: %s", model, e)
            raise

        logger.info("Fal RESULT ← %s", str(result)[:400])

        # 3. Extract the video URL from the result payload.
        video_url = None
        if isinstance(result, dict):
            video = result.get("video") or {}
            if isinstance(video, dict):
                video_url = video.get("url")
            elif isinstance(video, str):
                video_url = video
        if not video_url:
            raise RuntimeError(f"Fal returned no video URL: {result}")

        # 4. Download the video locally.
        return await self._download_video(video_url, output_path)

    async def _download_video(self, url: str, output_path: Path) -> Path:
        """Download a remote video file to disk."""
        logger.info("Fal DOWNLOAD: %s → %s", url, output_path)
        loop = asyncio.get_event_loop()
        resp = await loop.run_in_executor(
            None,
            lambda: requests.get(url, timeout=180),
        )
        resp.raise_for_status()

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(resp.content)

        size = output_path.stat().st_size
        if size < 1024:
            raise IOError(f"Downloaded video too small ({size} bytes): {output_path}")

        logger.info("Fal video downloaded: %s (%d bytes)", output_path, size)
        return output_path


# Backwards-compat alias — other modules still import KlingTaskManager.
KlingTaskManager = FalVideoTaskManager
