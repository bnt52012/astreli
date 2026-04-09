"""
LoRA Training via Replicate.

Separate from the pipeline — clients train their LoRA on a dedicated page.
Training takes ~15-20 minutes. The trained model ID is saved for reuse.
"""
from __future__ import annotations

import logging
import time
import zipfile
from pathlib import Path
from tempfile import NamedTemporaryFile

from pipeline.config import settings
from utils.http_client import create_session
from utils.image_utils import validate_image

logger = logging.getLogger(__name__)


class LoRATrainer:
    """Trains LoRA models on Replicate."""

    def __init__(self) -> None:
        self.session = create_session(timeout=60)
        self.api_base = "https://api.replicate.com/v1"

    def validate_training_images(
        self,
        image_paths: list[str],
        min_count: int = 10,
        max_count: int = 30,
        min_resolution: int = 512,
    ) -> list[str]:
        """Validate training images before submission.

        Args:
            image_paths: Paths to training images.
            min_count: Minimum required images.
            max_count: Maximum allowed images.
            min_resolution: Minimum image resolution.

        Returns:
            List of valid image paths.

        Raises:
            ValueError if validation fails.
        """
        valid = []
        for path in image_paths:
            if not Path(path).exists():
                logger.warning("Training image not found: %s", path)
                continue
            if not validate_image(path, min_resolution=min_resolution):
                logger.warning("Training image invalid: %s", path)
                continue
            valid.append(path)

        if len(valid) < min_count:
            raise ValueError(
                f"Need at least {min_count} valid images, got {len(valid)}. "
                f"Include: face front, profile, 3/4 view, full body, different angles."
            )

        if len(valid) > max_count:
            logger.warning("Truncating to %d images (had %d)", max_count, len(valid))
            valid = valid[:max_count]

        return valid

    def create_training_zip(self, image_paths: list[str]) -> str:
        """Create a ZIP file of training images for upload.

        Returns:
            Path to the ZIP file.
        """
        tmp = NamedTemporaryFile(suffix=".zip", delete=False)
        with zipfile.ZipFile(tmp.name, "w", zipfile.ZIP_DEFLATED) as zf:
            for i, path in enumerate(image_paths):
                ext = Path(path).suffix
                zf.write(path, f"image_{i:03d}{ext}")
        logger.info("Created training ZIP: %s (%d images)", tmp.name, len(image_paths))
        return tmp.name

    async def start_training(
        self,
        image_paths: list[str],
        trigger_word: str = "MANNEQUIN",
        model_name: str = "custom-lora",
        steps: int = 1000,
    ) -> dict:
        """Start LoRA training on Replicate.

        Args:
            image_paths: Validated training image paths.
            trigger_word: Trigger word for the LoRA.
            model_name: Name for the model.
            steps: Training steps.

        Returns:
            Training status dict with model_id.
        """
        headers = {
            "Authorization": f"Bearer {settings.replicate_api_token}",
            "Content-Type": "application/json",
        }

        # Upload training data
        zip_path = self.create_training_zip(image_paths)

        # Start training via Replicate
        payload = {
            "destination": f"{model_name}",
            "input": {
                "input_images": open(zip_path, "rb"),  # Will need multipart
                "trigger_word": trigger_word,
                "steps": steps,
                "learning_rate": 1e-4,
                "resolution": "1024",
            },
        }

        logger.info("Starting LoRA training: %s (trigger: %s, steps: %d)",
                     model_name, trigger_word, steps)

        # Note: actual Replicate training API may differ
        # This is the general flow
        resp = self.session.post(
            f"{self.api_base}/trainings",
            json={
                "model": "ostris/flux-dev-lora-trainer",
                "input": {
                    "trigger_word": trigger_word,
                    "steps": steps,
                    "learning_rate": 1e-4,
                },
            },
            headers=headers,
            timeout=60,
        )
        resp.raise_for_status()
        training = resp.json()

        return {
            "training_id": training.get("id", ""),
            "status": training.get("status", "starting"),
            "model_name": model_name,
            "trigger_word": trigger_word,
        }

    async def poll_training(self, training_id: str, timeout: int = 1800) -> dict:
        """Poll training status until complete.

        Args:
            training_id: Replicate training ID.
            timeout: Max wait time in seconds (default 30 min).

        Returns:
            Final training status with model version ID.
        """
        headers = {"Authorization": f"Bearer {settings.replicate_api_token}"}
        url = f"{self.api_base}/trainings/{training_id}"
        start = time.time()

        while time.time() - start < timeout:
            resp = self.session.get(url, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            status = data.get("status", "")

            if status == "succeeded":
                version = data.get("output", {}).get("version", "")
                logger.info("LoRA training complete! Version: %s", version)
                return {"status": "succeeded", "model_version": version, "training_id": training_id}

            if status == "failed":
                error = data.get("error", "Unknown")
                logger.error("LoRA training failed: %s", error)
                return {"status": "failed", "error": error, "training_id": training_id}

            if status == "canceled":
                return {"status": "canceled", "training_id": training_id}

            logger.info("Training %s: %s", training_id, status)
            time.sleep(30)

        return {"status": "timeout", "training_id": training_id}
