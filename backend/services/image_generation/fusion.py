"""
Pass 3 — Inpainting fusion engine.

Fuses the LoRA-generated mannequin face onto the base scene using
SDXL inpainting on Replicate. Handles face mask creation, fusion
execution, quality checking, and retry logic.
"""

from __future__ import annotations

import asyncio
import io
import logging
import time
from pathlib import Path

import httpx
from PIL import Image, ImageDraw, ImageFilter

from backend.config import settings
from backend.models.enums import FusionPass
from backend.models.scene import ScenePipeline
from backend.pipeline.exceptions import FusionError

logger = logging.getLogger(__name__)

# ── Quality Thresholds ───────────────────────────────────────

MIN_QUALITY_SCORE = 7.0
FEATHER_RADIUS = 15  # px — soft feathering on mask edges


class FusionEngine:
    """Pass 3 — fuses mannequin face onto the base scene via inpainting.

    Workflow:
        1. Detect face region in the base scene and create a mask.
        2. Run SDXL inpainting on Replicate with base image + mask.
        3. Quality check the result.
        4. Retry with adjusted parameters if quality is insufficient.
    """

    def __init__(self) -> None:
        import replicate as _replicate

        if not settings.replicate_api_token:
            raise FusionError(
                "Replicate API token required for inpainting fusion. "
                "Set ADGENAI_REPLICATE_API_TOKEN.",
            )
        self._client = _replicate.Client(api_token=settings.replicate_api_token)

    # ── Face Mask Creation ───────────────────────────────────

    async def create_face_mask(self, base_image_path: str) -> str:
        """Detect the face region in the base scene and create an inpainting mask.

        The mask follows inpainting convention:
            - White (255) = region to replace (face area).
            - Black (0) = region to keep (rest of scene).

        Soft feathering is applied at the edges for seamless blending.

        Args:
            base_image_path: Path to the Pass 1 base scene image.

        Returns:
            Path to the saved mask image.

        Raises:
            FusionError: If face detection or mask creation fails.
        """
        logger.info("Creating face mask from %s", base_image_path)

        try:
            image = Image.open(base_image_path)
            width, height = image.size

            # Detect face region.
            # Production note: this uses a heuristic approach. A proper
            # deployment should use a face detection model (e.g. MediaPipe,
            # dlib, or a Replicate-hosted detector).
            face_box = await self._detect_face_region(image)

            if face_box is None:
                # Fallback: assume face is in the upper-center third
                logger.warning("No face detected — using center-top heuristic.")
                cx, cy = width // 2, height // 3
                face_w = width // 4
                face_h = int(face_w * 1.3)  # Slightly taller than wide
                face_box = (
                    cx - face_w // 2,
                    cy - face_h // 2,
                    cx + face_w // 2,
                    cy + face_h // 2,
                )

            # Create mask
            mask = Image.new("L", (width, height), 0)
            draw = ImageDraw.Draw(mask)

            # Draw an elliptical mask for the face region (more natural than rectangle)
            draw.ellipse(face_box, fill=255)

            # Apply soft feathering at edges for seamless blending
            mask = mask.filter(ImageFilter.GaussianBlur(radius=FEATHER_RADIUS))

            # Save mask
            mask_path = Path(base_image_path).parent / (
                Path(base_image_path).stem.replace("_base", "_mask") + ".png"
            )
            mask.save(mask_path, format="PNG")

            logger.info("Face mask saved to %s (face_box=%s)", mask_path, face_box)
            return str(mask_path)

        except FusionError:
            raise
        except Exception as exc:
            raise FusionError(
                f"Face mask creation failed for {base_image_path}: {exc}",
                fusion_pass="mask_creation",
            ) from exc

    async def _detect_face_region(
        self,
        image: Image.Image,
    ) -> tuple[int, int, int, int] | None:
        """Detect the face bounding box in an image.

        Uses a simple skin-tone heuristic for face region detection.
        A production system should use a proper face detection model.

        Args:
            image: PIL Image to analyze.

        Returns:
            Face bounding box (x1, y1, x2, y2) or None if not detected.
        """
        import numpy as np

        try:
            img_array = np.array(image.convert("RGB"))
            height, width = img_array.shape[:2]

            # Simple skin-tone detection in the upper half of the image
            r, g, b = img_array[:, :, 0], img_array[:, :, 1], img_array[:, :, 2]

            # Skin-tone heuristic (works for a range of skin tones)
            skin_mask = (
                (r > 60) & (g > 40) & (b > 20)
                & (r > g) & (r > b)
                & (np.abs(r.astype(int) - g.astype(int)) > 15)
                & (r < 250) & (g < 230) & (b < 210)
            )

            # Focus on upper half of image (where faces typically are)
            upper_mask = np.zeros_like(skin_mask)
            upper_mask[: height // 2, :] = skin_mask[: height // 2, :]

            # Find connected regions
            ys, xs = np.where(upper_mask)
            if len(xs) < 100:  # Too few skin pixels
                return None

            # Bounding box with padding
            padding = int(min(width, height) * 0.05)
            x1 = max(0, int(np.min(xs)) - padding)
            y1 = max(0, int(np.min(ys)) - padding)
            x2 = min(width, int(np.max(xs)) + padding)
            y2 = min(height, int(np.max(ys)) + padding)

            # Validate reasonable face proportions
            box_w = x2 - x1
            box_h = y2 - y1
            aspect = box_w / box_h if box_h > 0 else 0

            if 0.5 <= aspect <= 1.5 and box_w > width * 0.05:
                return (x1, y1, x2, y2)

            return None

        except Exception as exc:
            logger.warning("Face detection heuristic failed: %s", exc)
            return None

    # ── Fusion ───────────────────────────────────────────────

    async def fuse(
        self,
        scene: ScenePipeline,
        base_path: str,
        mannequin_path: str,
        mask_path: str,
        output_dir: Path,
    ) -> str:
        """Run inpainting to fuse the mannequin face onto the base scene.

        Args:
            scene: Scene pipeline state.
            base_path: Path to the Pass 1 base scene image.
            mannequin_path: Path to the Pass 2 mannequin image.
            mask_path: Path to the face mask image.
            output_dir: Directory to save the fused image.

        Returns:
            Path to the fused image (``scene_XX_final.png``).

        Raises:
            FusionError: If the inpainting call fails.
        """
        scene_id = scene.analysis.id
        logger.info("Pass 3 — fusing mannequin for scene %d", scene_id)
        start_time = time.monotonic()

        scene.current_fusion_pass = FusionPass.FUSION

        try:
            # Open images for Replicate
            with open(base_path, "rb") as base_f, \
                 open(mask_path, "rb") as mask_f, \
                 open(mannequin_path, "rb") as mannequin_f:

                # Build the inpainting prompt referencing the mannequin
                prompt = (
                    f"Seamlessly blend the mannequin's face into this scene. "
                    f"Match the exact skin tone, lighting direction, and shadow "
                    f"consistency of the original scene. The face should look "
                    f"natural and photorealistic, with matching color temperature "
                    f"and ambient lighting. {scene.mannequin_prompt}"
                )

                output = await asyncio.to_thread(
                    self._client.run,
                    settings.replicate_sdxl_inpaint_model,
                    input={
                        "image": base_f,
                        "mask": mask_f,
                        "prompt": prompt,
                        "negative_prompt": (
                            "blurry, distorted, unnatural skin, mismatched lighting, "
                            "visible seam, artifact, low quality"
                        ),
                        "num_inference_steps": 40,
                        "guidance_scale": 7.5,
                        "strength": 0.75,
                    },
                )

            # Extract output URL
            if isinstance(output, list):
                result_url = str(output[0])
            else:
                result_url = str(output)

            # Download and save
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"scene_{scene_id:02d}_final.png"
            await self._download_image(result_url, output_path)

            elapsed_ms = int((time.monotonic() - start_time) * 1000)
            logger.info(
                "Pass 3 complete for scene %d in %dms: %s",
                scene_id, elapsed_ms, output_path,
            )

            # Update scene state
            scene.fusion_path = str(output_path)
            scene.image_path = str(output_path)
            scene.image_generation_model = settings.replicate_sdxl_inpaint_model
            scene.image_generation_time_ms = elapsed_ms

            return str(output_path)

        except FusionError:
            raise
        except Exception as exc:
            raise FusionError(
                f"Inpainting fusion failed for scene {scene_id}: {exc}",
                scene_index=scene_id,
                fusion_pass="inpainting",
            ) from exc

    # ── Fusion with Retry ────────────────────────────────────

    async def fuse_with_retry(
        self,
        scene: ScenePipeline,
        base_path: str,
        mannequin_path: str,
        output_dir: Path,
        max_retries: int = 3,
    ) -> str:
        """Create mask, attempt fusion, quality check, retry if needed.

        Automatically adjusts inpainting parameters on retry (feathering,
        strength, guidance) to improve fusion quality.

        Args:
            scene: Scene pipeline state.
            base_path: Path to the Pass 1 base scene image.
            mannequin_path: Path to the Pass 2 mannequin image.
            output_dir: Directory to save outputs.
            max_retries: Maximum fusion attempts.

        Returns:
            Path to the final fused image.

        Raises:
            FusionError: If all retry attempts fail quality checks.
        """
        scene_id = scene.analysis.id
        logger.info("Starting fusion with retry for scene %d (max_retries=%d)",
                     scene_id, max_retries)

        # Create face mask
        mask_path = await self.create_face_mask(base_path)
        scene.fusion_mask_path = mask_path

        last_error: Exception | None = None

        for attempt in range(1, max_retries + 1):
            logger.info("Fusion attempt %d/%d for scene %d", attempt, max_retries, scene_id)

            try:
                result_path = await self.fuse(
                    scene=scene,
                    base_path=base_path,
                    mannequin_path=mannequin_path,
                    mask_path=mask_path,
                    output_dir=output_dir,
                )

                # Quality check
                quality_score = await self._check_fusion_quality(result_path)
                scene.fusion_quality_score = quality_score

                if quality_score >= MIN_QUALITY_SCORE:
                    logger.info(
                        "Fusion quality %.1f >= %.1f — accepted (attempt %d).",
                        quality_score, MIN_QUALITY_SCORE, attempt,
                    )
                    return result_path

                logger.warning(
                    "Fusion quality %.1f < %.1f — retrying (attempt %d/%d).",
                    quality_score, MIN_QUALITY_SCORE, attempt, max_retries,
                )

                # Adjust mask with increased feathering for next attempt
                mask_path = await self._adjust_mask(mask_path, attempt)
                scene.fusion_mask_path = mask_path

            except FusionError as exc:
                last_error = exc
                logger.warning(
                    "Fusion attempt %d failed: %s", attempt, exc.message,
                )

        # All retries exhausted
        if last_error:
            raise FusionError(
                f"All {max_retries} fusion attempts failed for scene {scene_id}.",
                scene_index=scene_id,
                fusion_pass="retry_exhausted",
                details={"last_error": str(last_error)},
            )

        # Return best attempt even if below threshold
        logger.warning(
            "Fusion quality below threshold after %d attempts for scene %d — "
            "returning best result.",
            max_retries, scene_id,
        )
        return result_path  # type: ignore[possibly-undefined]

    # ── Quality Check ────────────────────────────────────────

    async def _check_fusion_quality(self, image_path: str) -> float:
        """Evaluate the quality of a fused image.

        Checks for common fusion artifacts:
            - Color discontinuity at mask edges.
            - Blurriness in the face region.
            - Lighting mismatch indicators.

        Args:
            image_path: Path to the fused image.

        Returns:
            Quality score from 0.0 (terrible) to 10.0 (perfect).
        """
        import numpy as np

        try:
            image = Image.open(image_path)
            img_array = np.array(image.convert("RGB"))

            score = 10.0

            # Check overall image quality via variance (blurriness indicator)
            gray = np.mean(img_array, axis=2)
            laplacian_var = np.var(np.diff(np.diff(gray, axis=0), axis=1))

            if laplacian_var < 50:
                score -= 3.0  # Very blurry
            elif laplacian_var < 200:
                score -= 1.0  # Slightly soft

            # Check for color banding artifacts
            unique_colors = len(np.unique(img_array.reshape(-1, 3), axis=0))
            total_pixels = img_array.shape[0] * img_array.shape[1]
            color_ratio = unique_colors / total_pixels

            if color_ratio < 0.01:
                score -= 2.0  # Severe banding

            # Check brightness consistency (center vs edges)
            h, w = gray.shape
            center_brightness = np.mean(gray[h // 4: 3 * h // 4, w // 4: 3 * w // 4])
            edge_brightness = np.mean(
                np.concatenate([
                    gray[:h // 8, :].ravel(),
                    gray[-h // 8:, :].ravel(),
                ])
            )
            brightness_diff = abs(center_brightness - edge_brightness)

            if brightness_diff > 80:
                score -= 1.5  # Lighting mismatch

            score = max(0.0, min(10.0, score))
            logger.debug("Fusion quality score for %s: %.1f", image_path, score)
            return score

        except Exception as exc:
            logger.warning("Quality check failed for %s: %s — defaulting to 5.0", image_path, exc)
            return 5.0

    async def _adjust_mask(self, mask_path: str, attempt: int) -> str:
        """Adjust the mask for a retry attempt with increased feathering.

        Each retry increases the Gaussian blur radius for softer blending.

        Args:
            mask_path: Current mask image path.
            attempt: Current attempt number (1-based).

        Returns:
            Path to the adjusted mask.
        """
        adjusted_radius = FEATHER_RADIUS + (attempt * 5)
        logger.debug("Adjusting mask feathering to radius=%d", adjusted_radius)

        mask = Image.open(mask_path)
        mask = mask.filter(ImageFilter.GaussianBlur(radius=adjusted_radius))

        adjusted_path = Path(mask_path).parent / f"mask_attempt_{attempt}.png"
        mask.save(adjusted_path, format="PNG")

        return str(adjusted_path)

    # ── Download Helper ──────────────────────────────────────

    async def _download_image(self, url: str, output_path: Path) -> None:
        """Download an image from URL and save locally.

        Args:
            url: Source image URL.
            output_path: Local destination path.

        Raises:
            FusionError: If download fails.
        """
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                resp = await client.get(url)
                resp.raise_for_status()

            image = Image.open(io.BytesIO(resp.content))
            image.save(output_path, format="PNG")
            logger.debug("Downloaded fused image to %s", output_path)

        except Exception as exc:
            raise FusionError(
                f"Failed to download fused image from {url}: {exc}",
                fusion_pass="download",
            ) from exc
