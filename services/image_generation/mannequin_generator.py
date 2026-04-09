"""
Pass 2: Mannequin Generation via LoRA SDXL on Replicate.

Generates the mannequin with the client's trained LoRA model,
matching the pose/angle/lighting from the base scene (Pass 1).
"""
from __future__ import annotations

import logging
import time
from pathlib import Path

import requests

from pipeline.config import settings, PIPELINE_DEFAULTS
from utils.http_client import create_session

logger = logging.getLogger(__name__)


class MannequinGenerator:
    """Generates mannequin images using LoRA SDXL on Replicate."""

    def __init__(self, lora_model_id: str, trigger_word: str = "MANNEQUIN") -> None:
        self.lora_model_id = lora_model_id
        self.trigger_word = trigger_word
        self.session = create_session(timeout=300)
        self.api_base = "https://api.replicate.com/v1"

    async def generate(
        self,
        prompt: str,
        output_path: Path,
        negative_prompt: str = "",
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
    ) -> Path:
        """Generate mannequin image with LoRA.

        Args:
            prompt: Prompt including trigger word + pose/lighting details.
            output_path: Where to save the result.
            negative_prompt: What to avoid.
            num_inference_steps: SDXL inference steps.
            guidance_scale: CFG scale.

        Returns:
            Path to the generated mannequin image.
        """
        if not self.lora_model_id:
            raise ValueError("No LoRA model ID configured")

        if not negative_prompt:
            negative_prompt = (
                "blurry, low quality, distorted, deformed face, "
                "extra fingers, bad anatomy, watermark, text, "
                "oversaturated, cartoon, illustration, painting"
            )

        headers = {
            "Authorization": f"Bearer {settings.replicate_api_token}",
            "Content-Type": "application/json",
        }

        # Submit prediction
        payload = {
            "version": self.lora_model_id,
            "input": {
                "prompt": prompt,
                "negative_prompt": negative_prompt,
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale,
                "width": 1024,
                "height": 1024,
                "scheduler": "K_EULER_ANCESTRAL",
            },
        }

        logger.info("Submitting LoRA generation to Replicate...")
        resp = self.session.post(
            f"{self.api_base}/predictions",
            json=payload,
            headers=headers,
            timeout=60,
        )
        resp.raise_for_status()
        prediction = resp.json()
        prediction_id = prediction["id"]
        poll_url = prediction.get("urls", {}).get("get", f"{self.api_base}/predictions/{prediction_id}")

        # Poll for completion
        timeout = 300
        start = time.time()
        while time.time() - start < timeout:
            poll_resp = self.session.get(poll_url, headers=headers, timeout=30)
            poll_resp.raise_for_status()
            status_data = poll_resp.json()
            status = status_data["status"]

            if status == "succeeded":
                output_url = status_data["output"]
                if isinstance(output_url, list):
                    output_url = output_url[0]
                return await self._download_image(output_url, output_path)

            if status == "failed":
                error = status_data.get("error", "Unknown error")
                raise RuntimeError(f"LoRA generation failed: {error}")

            if status == "canceled":
                raise RuntimeError("LoRA generation was canceled")

            logger.debug("LoRA prediction %s: %s", prediction_id, status)
            time.sleep(5)

        raise TimeoutError(f"LoRA generation timed out after {timeout}s")

    async def _download_image(self, url: str, output_path: Path) -> Path:
        """Download the generated image."""
        output_path.parent.mkdir(parents=True, exist_ok=True)
        resp = self.session.get(url, timeout=60)
        resp.raise_for_status()
        with open(output_path, "wb") as f:
            f.write(resp.content)
        logger.info("Mannequin image downloaded: %s (%d bytes)", output_path, len(resp.content))
        return output_path
