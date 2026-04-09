"""
Pass 3: Fusion via Inpainting.

Merges the base scene (Pass 1) with the mannequin face (Pass 2)
using inpainting. Soft feathering on mask edges for seamless blending.
"""
from __future__ import annotations

import logging
import time
from pathlib import Path

from PIL import Image

from pipeline.config import settings
from utils.http_client import create_session
from utils.image_utils import (
    composite_with_mask,
    create_face_mask,
    detect_face_region,
    image_to_base64,
    load_image,
)

logger = logging.getLogger(__name__)


class FusionEngine:
    """Fuses base scene with mannequin via inpainting."""

    def __init__(self) -> None:
        self.session = create_session(timeout=300)
        self.api_base = "https://api.replicate.com/v1"

    async def fuse(
        self,
        base_image_path: Path,
        mannequin_image_path: Path,
        output_path: Path,
        feather_radius: int = 30,
        use_api_inpainting: bool = True,
    ) -> Path:
        """Fuse the mannequin face onto the base scene.

        Strategy:
        1. Load both images
        2. Create face mask on the base image (where generic figure's face is)
        3. Either:
           a) Use Replicate inpainting API for professional fusion
           b) Use local PIL compositing as fallback

        Args:
            base_image_path: Path to base scene from Pass 1.
            mannequin_image_path: Path to mannequin from Pass 2.
            output_path: Where to save the fused result.
            feather_radius: Gaussian blur radius for mask edges.
            use_api_inpainting: Whether to use Replicate inpainting API.

        Returns:
            Path to fused image.
        """
        base_img = load_image(base_image_path)
        mannequin_img = load_image(mannequin_image_path)

        if use_api_inpainting and settings.replicate_api_token:
            try:
                return await self._fuse_with_replicate(
                    base_img, mannequin_img, output_path, feather_radius
                )
            except Exception as e:
                logger.warning("Replicate inpainting failed, falling back to local: %s", e)

        # Fallback: local PIL compositing
        return self._fuse_local(base_img, mannequin_img, output_path, feather_radius)

    async def _fuse_with_replicate(
        self,
        base_img: Image.Image,
        mannequin_img: Image.Image,
        output_path: Path,
        feather_radius: int,
    ) -> Path:
        """Use Replicate SDXL Inpainting for professional fusion."""
        import base64

        # Create mask for face area
        face_info = detect_face_region(base_img)
        if face_info:
            center, radius = face_info
        else:
            w, h = base_img.size
            center, radius = (w // 2, h // 4), min(w, h) // 5

        mask = create_face_mask(
            base_img.size,
            face_center=center,
            face_radius=radius,
            feather_radius=feather_radius,
        )

        headers = {
            "Authorization": f"Bearer {settings.replicate_api_token}",
            "Content-Type": "application/json",
        }

        # Prepare base64 images
        base_b64 = image_to_base64(base_img)
        mask_b64 = image_to_base64(mask)
        mannequin_b64 = image_to_base64(mannequin_img)

        payload = {
            "version": "stability-ai/stable-diffusion-xl-inpainting",
            "input": {
                "image": f"data:image/png;base64,{base_b64}",
                "mask": f"data:image/png;base64,{mask_b64}",
                "prompt": (
                    "Replace the face area with the reference face. "
                    "Maintain exact same lighting, skin tone continuity, "
                    "seamless blending at edges, photorealistic result. "
                    "Natural skin texture, no artifacts."
                ),
                "negative_prompt": (
                    "blurry, visible seams, mismatched lighting, "
                    "artifacts, distorted, unnatural skin"
                ),
                "guidance_scale": 8.0,
                "num_inference_steps": 35,
                "strength": 0.85,
            },
        }

        resp = self.session.post(
            f"{self.api_base}/predictions",
            json=payload,
            headers=headers,
            timeout=60,
        )
        resp.raise_for_status()
        prediction = resp.json()
        poll_url = prediction.get("urls", {}).get(
            "get", f"{self.api_base}/predictions/{prediction['id']}"
        )

        # Poll
        timeout = 300
        start = time.time()
        while time.time() - start < timeout:
            poll_resp = self.session.get(poll_url, headers=headers, timeout=30)
            poll_resp.raise_for_status()
            data = poll_resp.json()

            if data["status"] == "succeeded":
                url = data["output"]
                if isinstance(url, list):
                    url = url[0]
                img_resp = self.session.get(url, timeout=60)
                img_resp.raise_for_status()
                output_path.parent.mkdir(parents=True, exist_ok=True)
                with open(output_path, "wb") as f:
                    f.write(img_resp.content)
                logger.info("Fusion complete (Replicate): %s", output_path)
                return output_path

            if data["status"] in ("failed", "canceled"):
                raise RuntimeError(f"Inpainting {data['status']}: {data.get('error', '')}")

            time.sleep(5)

        raise TimeoutError("Inpainting timed out")

    def _fuse_local(
        self,
        base_img: Image.Image,
        mannequin_img: Image.Image,
        output_path: Path,
        feather_radius: int,
    ) -> Path:
        """Local PIL-based fusion as fallback."""
        logger.info("Using local PIL fusion...")

        face_info = detect_face_region(base_img)
        if face_info:
            center, radius = face_info
        else:
            w, h = base_img.size
            center, radius = (w // 2, h // 4), min(w, h) // 5

        mask = create_face_mask(
            base_img.size,
            face_center=center,
            face_radius=radius,
            feather_radius=feather_radius,
        )

        result = composite_with_mask(base_img, mannequin_img, mask)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        result.save(str(output_path), quality=95)
        logger.info("Fusion complete (local): %s", output_path)
        return output_path
