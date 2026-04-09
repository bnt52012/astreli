"""
Pass 1 — Nano Banana 2 (Gemini) scene base generator.

Generates the base scene image using Google's Gemini multimodal model.
For personnage scenes, the prompt is modified to include a GENERIC human
figure placeholder (same pose/clothing but no specific face) so that the
LoRA mannequin can be fused in during Pass 3.

For product-only scenes, generates the final image in a single shot.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

from google import genai
from google.genai import types

from backend.config import settings
from backend.models.enums import SceneType
from backend.models.scene import ScenePipeline
from backend.pipeline.exceptions import ImageGenerationError
from backend.services.image_generation.reference_manager import ReferenceManager

logger = logging.getLogger(__name__)


class SceneGenerator:
    """Pass 1 — generates base scene images via Gemini (Nano Banana 2).

    For PERSONNAGE scenes, produces a scene with a generic figure placeholder
    that will be replaced by the LoRA mannequin in later passes.

    For PRODUIT scenes, produces the final image directly.
    """

    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise ImageGenerationError(
                "Gemini API key required for scene generation. "
                "Set ADGENAI_GEMINI_API_KEY.",
            )
        self._client = genai.Client(api_key=settings.gemini_api_key)
        self._reference_manager = ReferenceManager()

    # ── Pass 1: Base Scene (Personnage) ──────────────────────

    async def generate_base_scene(
        self,
        scene: ScenePipeline,
        output_dir: Path,
        reference_images: list[str] | None = None,
    ) -> str:
        """Generate the base scene image with a generic figure placeholder.

        This is Pass 1 of the 3-pass fusion workflow. The prompt is modified
        to describe a GENERIC human figure in the intended pose and clothing,
        without specific facial features, so the LoRA mannequin face can be
        composited in Pass 3.

        Args:
            scene: Scene pipeline state with analysis and enriched prompts.
            output_dir: Directory to save the generated image.
            reference_images: Optional paths to reference images (decor, product).

        Returns:
            Path to the saved base scene image (``scene_XX_base.png``).

        Raises:
            ImageGenerationError: If Gemini generation fails.
        """
        scene_id = scene.analysis.id
        logger.info("Pass 1 — generating base scene for scene %d", scene_id)
        start_time = time.monotonic()

        # Build the prompt with generic figure placeholder
        base_prompt = scene.final_image_prompt
        placeholder_prompt = self._build_placeholder_prompt(base_prompt, scene)

        # Assemble content parts: prompt text + optional reference images
        content_parts: list[types.Part | str] = [placeholder_prompt]
        if reference_images:
            image_parts = await self._reference_manager.prepare_gemini_parts(reference_images)
            content_parts.extend(image_parts)

        try:
            response = await self._client.aio.models.generate_content(
                model=settings.gemini_image_model,
                contents=content_parts,
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"],
                ),
            )

            # Extract and save the image
            image_path = self._extract_and_save_image(
                response=response,
                output_dir=output_dir,
                filename=f"scene_{scene_id:02d}_base.png",
            )

            elapsed_ms = int((time.monotonic() - start_time) * 1000)
            logger.info(
                "Pass 1 complete for scene %d in %dms: %s",
                scene_id, elapsed_ms, image_path,
            )

            # Update scene state
            scene.scene_base_path = str(image_path)
            scene.scene_base_prompt = placeholder_prompt

            return str(image_path)

        except ImageGenerationError:
            raise
        except Exception as exc:
            raise ImageGenerationError(
                f"Gemini base scene generation failed for scene {scene_id}: {exc}",
                model=settings.gemini_image_model,
                scene_index=scene_id,
            ) from exc

    # ── One-Shot Product Scene ───────────────────────────────

    async def generate_product_scene(
        self,
        scene: ScenePipeline,
        output_dir: Path,
        reference_images: list[str] | None = None,
    ) -> str:
        """Generate a final product scene image in a single pass.

        Used for PRODUIT scenes that don't require mannequin fusion.
        The image is saved directly as the final scene output.

        Args:
            scene: Scene pipeline state.
            output_dir: Directory to save the generated image.
            reference_images: Optional paths to reference images.

        Returns:
            Path to the saved product scene image (``scene_XX_final.png``).

        Raises:
            ImageGenerationError: If Gemini generation fails.
        """
        scene_id = scene.analysis.id
        logger.info("Generating product scene (one-shot) for scene %d", scene_id)
        start_time = time.monotonic()

        prompt = scene.final_image_prompt

        # Assemble content parts
        content_parts: list[types.Part | str] = [prompt]
        if reference_images:
            image_parts = await self._reference_manager.prepare_gemini_parts(reference_images)
            content_parts.extend(image_parts)

        try:
            response = await self._client.aio.models.generate_content(
                model=settings.gemini_image_model,
                contents=content_parts,
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"],
                ),
            )

            image_path = self._extract_and_save_image(
                response=response,
                output_dir=output_dir,
                filename=f"scene_{scene_id:02d}_final.png",
            )

            elapsed_ms = int((time.monotonic() - start_time) * 1000)
            logger.info(
                "Product scene complete for scene %d in %dms: %s",
                scene_id, elapsed_ms, image_path,
            )

            # Update scene state for one-shot completion
            scene.image_path = str(image_path)
            scene.image_generation_model = settings.gemini_image_model
            scene.image_generation_time_ms = elapsed_ms

            return str(image_path)

        except ImageGenerationError:
            raise
        except Exception as exc:
            raise ImageGenerationError(
                f"Gemini product scene generation failed for scene {scene_id}: {exc}",
                model=settings.gemini_image_model,
                scene_index=scene_id,
            ) from exc

    # ── Helpers ───────────────────────────────────────────────

    def _build_placeholder_prompt(self, base_prompt: str, scene: ScenePipeline) -> str:
        """Modify the prompt to describe a generic human figure placeholder.

        The generic figure has the same pose and clothing as the intended
        mannequin but with nondescript facial features, making it suitable
        for face replacement in the fusion pass.

        Args:
            base_prompt: The enriched image prompt.
            scene: Scene pipeline state for context.

        Returns:
            Modified prompt with generic figure instructions.
        """
        placeholder_instruction = (
            "IMPORTANT: The human figure in this scene must have a GENERIC, "
            "nondescript face — smooth features without specific identity. "
            "The figure should match the described pose, clothing, and body "
            "position exactly, but the face must be plain and featureless "
            "enough to be replaced later. Do NOT generate a realistic face. "
            "Focus on accurate pose, clothing, lighting, and scene composition."
        )
        return f"{placeholder_instruction}\n\n{base_prompt}"

    def _extract_and_save_image(
        self,
        response: object,
        output_dir: Path,
        filename: str,
    ) -> Path:
        """Extract the generated image from Gemini response and save it.

        Args:
            response: Gemini API response object.
            output_dir: Target directory.
            filename: Output filename.

        Returns:
            Path to the saved image file.

        Raises:
            ImageGenerationError: If no image is found in the response.
        """
        from PIL import Image
        import io

        output_dir.mkdir(parents=True, exist_ok=True)
        output_path = output_dir / filename

        # Iterate through response parts to find image data
        if response.candidates:
            for part in response.candidates[0].content.parts:
                if hasattr(part, "inline_data") and part.inline_data is not None:
                    image_data = part.inline_data.data
                    image = Image.open(io.BytesIO(image_data))
                    image.save(output_path, format="PNG")
                    logger.debug("Saved image to %s (%dx%d)", output_path, image.width, image.height)
                    return output_path

        raise ImageGenerationError(
            f"No image found in Gemini response for {filename}. "
            "The model may have returned text-only output.",
            model=settings.gemini_image_model,
        )
