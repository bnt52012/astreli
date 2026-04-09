"""
Pass 1: Scene Generation via Gemini (Nano Banana 2).

Generates the COMPLETE scene: decor, lighting, product, atmosphere,
and a GENERIC human figure placeholder in the right pose.
"""
from __future__ import annotations

import logging
from pathlib import Path

from PIL import Image

from pipeline.config import settings, PIPELINE_DEFAULTS
from utils.image_utils import load_image, resize_image

logger = logging.getLogger(__name__)


class SceneGenerator:
    """Generates base scenes using Gemini image generation."""

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
        """Generate a scene image with Gemini.

        Args:
            prompt: Enriched prompt for the scene.
            reference_images: PIL Images for product/decor references.
            output_path: Where to save the result.
            aspect_ratio: Target aspect ratio.

        Returns:
            Path to saved image.
        """
        try:
            from google import genai
            from google.genai import types

            client = genai.Client(api_key=self.api_key)

            # Build contents list
            contents: list = []

            # Add reference images first
            if reference_images:
                for i, ref_img in enumerate(reference_images):
                    ref_resized = resize_image(ref_img, max_size=768)
                    contents.append(ref_resized)
                    contents.append(f"Reference image {i+1} above. ")

            # Add the generation prompt
            scene_prompt = (
                f"Generate a photorealistic advertising scene: {prompt}. "
                f"If a person is described, include a generic model/figure in the exact pose and position described. "
                f"The scene should look like it was shot by a professional advertising photographer. "
                f"Aspect ratio: {aspect_ratio}."
            )
            contents.append(scene_prompt)

            # Generate
            response = client.models.generate_content(
                model=self.model,
                contents=contents,
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT", "IMAGE"],
                ),
            )

            # Extract and save image
            if response.candidates:
                for part in response.candidates[0].content.parts:
                    if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                        img_data = part.inline_data.data
                        output_path.parent.mkdir(parents=True, exist_ok=True)
                        with open(output_path, "wb") as f:
                            f.write(img_data)
                        logger.info("Scene generated: %s", output_path)
                        return output_path

            raise RuntimeError("Gemini returned no image in response")

        except ImportError:
            logger.error("google-genai package not installed. pip install google-genai")
            raise
        except Exception as e:
            logger.error("Scene generation failed: %s", e)
            raise
