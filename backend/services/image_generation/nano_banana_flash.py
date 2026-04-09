"""
Nano Banana Flash — Gemini Flash One-Shot Generator.

Handles produit (product) scene generation using single one-shot
Gemini Flash calls. No chat session needed — each call is independent.

Used for:
- Product-only scenes (packshots, details, environment)
- Fallback when Gemini Pro fails on a personnage scene
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

from google import genai
from google.genai import types

from backend.config import settings
from backend.models.scene import ScenePipeline
from backend.pipeline.exceptions import ImageGenerationError
from backend.services.image_generation.reference_manager import ReferenceManager

logger = logging.getLogger(__name__)


class NanaBananaFlash:
    """Gemini Flash one-shot generator for product scenes.

    Each scene is generated independently — no session state.
    Reference images (product, decor) are passed per call.
    """

    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self._ref_manager = ReferenceManager()

    async def generate(
        self,
        scene: ScenePipeline,
        output_path: Path,
        product_paths: list[str] | None = None,
        decor_paths: list[str] | None = None,
    ) -> str:
        """Generate a product scene image with one-shot Gemini Flash call.

        Args:
            scene: Scene pipeline state with enriched prompts.
            output_path: Where to save the generated image.
            product_paths: Product reference image paths.
            decor_paths: Decor reference image paths.

        Returns:
            Path to the saved image.

        Raises:
            ImageGenerationError: If generation fails.
        """
        start_time = time.time()

        # Build content parts: references first, then prompt
        parts: list[types.Part] = []

        # Product references
        if product_paths:
            product_parts = self._ref_manager.prepare_parts(
                product_paths[:6], max_images=6, label="product",
            )
            parts.extend(product_parts)

        # Decor references
        if decor_paths:
            decor_parts = self._ref_manager.prepare_parts(
                decor_paths[:4], max_images=4, label="decor",
            )
            parts.extend(decor_parts)

        # Build prompt
        prompt = (
            f"Generate a cinematic product advertising photograph.\n\n"
            f"Scene: {scene.final_image_prompt}\n\n"
            f"Style: Professional product photography, studio quality, "
            f"perfect lighting, sharp focus on the product."
        )

        if product_paths or decor_paths:
            prompt += (
                "\n\nUse the provided reference images to match the product's "
                "exact appearance and the desired environment."
            )

        parts.append(types.Part.from_text(text=prompt))

        try:
            response = await self.client.aio.models.generate_content(
                model=settings.gemini_flash_model,
                contents=types.Content(parts=parts),
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"],
                    temperature=0.5,
                ),
            )

            # Extract generated image
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    output_path.write_bytes(part.inline_data.data)

                    elapsed_ms = int((time.time() - start_time) * 1000)
                    scene.image_generation_model = settings.gemini_flash_model
                    scene.image_generation_time_ms = elapsed_ms

                    logger.info(
                        "[FLASH] Scene %d generated in %dms: %s",
                        scene.analysis.id,
                        elapsed_ms,
                        output_path,
                    )
                    return str(output_path)

            raise ImageGenerationError(
                f"Gemini Flash returned no image for scene {scene.analysis.id}",
                model=settings.gemini_flash_model,
                scene_index=scene.analysis.id,
            )

        except ImageGenerationError:
            raise
        except Exception as e:
            raise ImageGenerationError(
                f"Product scene generation failed: {e}",
                model=settings.gemini_flash_model,
                scene_index=scene.analysis.id,
            ) from e
