"""
ÉTAPE 2 — Gemini Dual-Engine Image Generator

CHARACTER_PRODUCT mode:
  - Character scenes → Gemini Pro via persistent chat session (face memory)
  - Product scenes  → Gemini Flash one-shot

PRODUCT_ONLY mode:
  - All scenes → Gemini Flash one-shot
"""
from __future__ import annotations

import base64
import logging
from pathlib import Path

from google import genai
from google.genai import types

from backend.config import settings
from backend.models.schemas import PipelineMode, ScenePipeline, SceneType

logger = logging.getLogger(__name__)


class ImageGenerator:
    def __init__(self):
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self._character_chat = None  # persistent chat for face consistency

    async def initialize_character_session(
        self, mannequin_images: list[str], decor_images: list[str] | None = None
    ):
        """Open a persistent Gemini Pro chat session with mannequin reference images.
        This replaces LoRA — Gemini memorizes the face across the session."""

        reference_parts = []
        for img_path in mannequin_images:
            img_bytes = Path(img_path).read_bytes()
            mime = "image/jpeg" if img_path.lower().endswith((".jpg", ".jpeg")) else "image/png"
            reference_parts.append(types.Part.from_bytes(data=img_bytes, mime_type=mime))

        if decor_images:
            for img_path in decor_images[:4]:  # max 4 decor refs
                img_bytes = Path(img_path).read_bytes()
                mime = "image/jpeg" if img_path.lower().endswith((".jpg", ".jpeg")) else "image/png"
                reference_parts.append(types.Part.from_bytes(data=img_bytes, mime_type=mime))

        init_prompt = (
            "You are a cinematic photography AI. I'm sharing reference photos of a model/mannequin. "
            "Memorize this person's exact face, body proportions, skin tone, and features. "
            "In all future messages, when I ask you to generate an image featuring this person, "
            "you MUST maintain perfect visual consistency with these reference photos. "
            "The person must be recognizably the same individual in every generated image. "
            "Acknowledge that you've memorized the reference."
        )

        reference_parts.append(types.Part.from_text(text=init_prompt))

        self._character_chat = self.client.aio.chats.create(
            model=settings.gemini_pro_model,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                temperature=0.6,
            ),
        )

        response = await self._character_chat.send_message(reference_parts)
        logger.info("Character session initialized with %d reference images", len(mannequin_images))
        return response

    async def generate_character_image(
        self, scene: ScenePipeline, output_dir: Path
    ) -> str:
        """Generate a character scene image using persistent Gemini Pro chat."""
        if not self._character_chat:
            raise RuntimeError("Character session not initialized. Call initialize_character_session first.")

        prompt = (
            f"Generate a cinematic advertising photograph with the EXACT same person from the reference photos. "
            f"The person must be clearly recognizable — same face, same features.\n\n"
            f"Scene description: {scene.optimized_image_prompt}\n\n"
            f"CRITICAL: Maintain perfect identity consistency with the reference photos."
        )

        response = await self._character_chat.send_message(prompt)

        output_path = output_dir / f"scene_{scene.analysis.id}_character.png"
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                output_path.write_bytes(part.inline_data.data)
                logger.info("Character image saved: %s", output_path)
                return str(output_path)

        raise RuntimeError(f"No image generated for character scene {scene.analysis.id}")

    async def generate_product_image(
        self,
        scene: ScenePipeline,
        output_dir: Path,
        product_images: list[str] | None = None,
        decor_images: list[str] | None = None,
    ) -> str:
        """Generate a product scene image using Gemini Flash one-shot."""
        parts = []

        # Add reference images if available
        ref_images = (product_images or []) + (decor_images or [])
        for img_path in ref_images[:6]:
            img_bytes = Path(img_path).read_bytes()
            mime = "image/jpeg" if img_path.lower().endswith((".jpg", ".jpeg")) else "image/png"
            parts.append(types.Part.from_bytes(data=img_bytes, mime_type=mime))

        prompt = (
            f"Generate a cinematic product advertising photograph.\n\n"
            f"Scene: {scene.optimized_image_prompt}\n\n"
            f"Style: Professional product photography, studio quality, "
            f"perfect lighting, sharp focus on the product."
        )
        if ref_images:
            prompt += "\n\nUse the provided reference images for product appearance and environment."

        parts.append(types.Part.from_text(text=prompt))

        response = await self.client.aio.models.generate_content(
            model=settings.gemini_flash_model,
            contents=types.Content(parts=parts),
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                temperature=0.5,
            ),
        )

        output_path = output_dir / f"scene_{scene.analysis.id}_product.png"
        for part in response.candidates[0].content.parts:
            if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                output_path.write_bytes(part.inline_data.data)
                logger.info("Product image saved: %s", output_path)
                return str(output_path)

        raise RuntimeError(f"No image generated for product scene {scene.analysis.id}")

    async def generate_scene_image(
        self,
        scene: ScenePipeline,
        mode: PipelineMode,
        output_dir: Path,
        product_images: list[str] | None = None,
        decor_images: list[str] | None = None,
    ) -> str:
        """Route to the correct engine based on mode and scene type."""
        if mode == PipelineMode.CHARACTER_PRODUCT and scene.analysis.type == SceneType.CHARACTER:
            return await self.generate_character_image(scene, output_dir)
        else:
            return await self.generate_product_image(
                scene, output_dir, product_images, decor_images
            )
