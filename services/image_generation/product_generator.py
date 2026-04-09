"""
PATH B: Product-only image generation via Gemini (Nano Banana 2).

Single-pass generation — no LoRA, no fusion needed.
"""
from __future__ import annotations

import logging
from pathlib import Path

from PIL import Image

from pipeline.config import settings, PIPELINE_DEFAULTS
from utils.image_utils import resize_image

logger = logging.getLogger(__name__)


class ProductGenerator:
    """Generates product-only scenes using Gemini."""

    def __init__(self) -> None:
        self.api_key = settings.gemini_api_key
        self.model = PIPELINE_DEFAULTS.gemini_model

    async def generate(
        self,
        prompt: str,
        output_path: Path,
        reference_images: list[Image.Image] | None = None,
        aspect_ratio: str = "16:9",
    ) -> Path:
        """Generate a product scene image.

        Args:
            prompt: Enriched product prompt.
            output_path: Where to save the result.
            reference_images: Product/decor reference PIL Images.
            aspect_ratio: Target aspect ratio.

        Returns:
            Path to saved image.
        """
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)

            contents: list = []

            # Reference images
            if reference_images:
                for i, ref_img in enumerate(reference_images):
                    ref_resized = resize_image(ref_img, max_size=768)
                    contents.append(ref_resized)
                    contents.append(f"Product reference {i+1}. ")

            # Generation prompt
            product_prompt = (
                f"Generate a photorealistic advertising product shot: {prompt}. "
                f"Professional commercial photography, no human figures. "
                f"Perfect product rendering with realistic materials, reflections, and lighting. "
                f"Aspect ratio: {aspect_ratio}."
            )
            contents.append(product_prompt)

            response = client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"],
                ),
            )

            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(output_path, "wb") as f:
                            f.write(part.inline_data.data)
                        logger.info("Product image generated: %s", output_path)
                        return output_path

            raise RuntimeError("Gemini returned no image for product scene")

        except ImportError:
            logger.error("google-genai package not installed")
            raise
        except Exception as e:
            logger.error("Product generation failed: %s", e)
            raise
