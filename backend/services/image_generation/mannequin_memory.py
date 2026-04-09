"""
Mannequin Memory Manager.

Handles the persistent Gemini Pro chat session that maintains
face/body consistency across all personnage scenes.

This REPLACES LoRA fine-tuning: by sending mannequin reference photos
as the first message in a chat session and asking Gemini to memorize
the person's appearance, all subsequent scene generations within the
same session maintain visual identity consistency.

Key behaviors:
- Send multiple angles (face front, profile, full body) as first message
- Ask Gemini to CONFIRM what it sees (so we can verify memorization)
- Store Gemini's description for re-injection into subsequent prompts
- Handle wardrobe changes (same person, different outfit)
- If consistency drifts, re-introduce the mannequin
"""

from __future__ import annotations

import logging
from pathlib import Path

from google import genai
from google.genai import types

from backend.config import settings
from backend.pipeline.exceptions import ImageGenerationError
from backend.services.image_generation.reference_manager import ReferenceManager

logger = logging.getLogger(__name__)

MANNEQUIN_INTRODUCTION_PROMPT = """You are a cinematic photography AI creating images for a professional advertising campaign.

I am sharing reference photos of the person who will appear in this campaign.
Study these photos EXTREMELY carefully and memorize:

1. FACE: Exact facial structure, eye shape and color, nose shape, lip shape, eyebrow arch, jawline, skin tone and texture, any distinctive features (moles, dimples, freckles)
2. BODY: Body proportions, height impression, build, posture
3. HAIR: Color, texture, length, style, partline
4. SKIN: Exact skin tone, undertone (warm/cool/neutral), texture quality

In ALL future images I request, this person MUST be recognizably the SAME individual.
The identity must be unmistakable — as if photographed by a different photographer on a different day.

Please confirm you've memorized this person by describing them in detail. List every visual characteristic you observe."""

WARDROBE_CHANGE_INSTRUCTION = """IMPORTANT: In this scene, the same person is wearing a DIFFERENT outfit.
The person's face, body, skin tone, hair, and all physical features must remain EXACTLY the same.
ONLY the clothing/outfit changes. The person's identity must be unmistakable."""


class MannequinMemory:
    """Manages the Gemini Pro chat session for mannequin face consistency.

    The chat session acts as a persistent memory:
    1. First message: reference photos + memorization request
    2. Subsequent messages: scene generation requests within the same session
    3. Gemini maintains face/body consistency across all messages

    Attributes:
        chat: The active Gemini chat session (None until initialized).
        mannequin_description: Gemini's description of the mannequin.
    """

    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.chat: genai.ChatSession | None = None
        self.mannequin_description: str = ""
        self._ref_manager = ReferenceManager()
        self._is_initialized = False

    @property
    def is_initialized(self) -> bool:
        """Whether the mannequin memory has been established."""
        return self._is_initialized

    async def initialize(
        self,
        mannequin_image_paths: list[str],
        decor_image_paths: list[str] | None = None,
    ) -> str:
        """Initialize the chat session with mannequin reference photos.

        Sends reference photos as the first message and asks Gemini to
        confirm memorization by describing what it sees.

        Args:
            mannequin_image_paths: Paths to mannequin reference photos (up to 5).
            decor_image_paths: Optional decor reference images.

        Returns:
            Gemini's description of the mannequin (verification of memorization).

        Raises:
            ImageGenerationError: If initialization fails.
        """
        if not mannequin_image_paths:
            raise ImageGenerationError(
                "No mannequin reference images provided",
                model=settings.gemini_pro_model,
            )

        logger.info(
            "[MANNEQUIN] Initializing memory with %d reference photos",
            len(mannequin_image_paths),
        )

        # Prepare reference image parts
        mannequin_parts = self._ref_manager.prepare_parts(
            mannequin_image_paths[:5],
            max_images=5,
            label="mannequin",
        )

        if not mannequin_parts:
            raise ImageGenerationError(
                "Failed to load any mannequin reference images",
                model=settings.gemini_pro_model,
            )

        # Optionally include decor references (limited)
        decor_parts = []
        if decor_image_paths:
            decor_parts = self._ref_manager.prepare_parts(
                decor_image_paths[:3],
                max_images=3,
                label="decor",
            )

        # Build the introduction message
        all_parts: list[types.Part] = []
        all_parts.extend(mannequin_parts)
        if decor_parts:
            all_parts.extend(decor_parts)
        all_parts.append(types.Part.from_text(text=MANNEQUIN_INTRODUCTION_PROMPT))

        # Create persistent chat session
        self.chat = self.client.aio.chats.create(
            model=settings.gemini_pro_model,
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"],
                temperature=0.6,
            ),
        )

        try:
            response = await self.chat.send_message(all_parts)

            # Extract Gemini's description of the mannequin
            description = ""
            for part in response.candidates[0].content.parts:
                if part.text:
                    description += part.text

            self.mannequin_description = description
            self._is_initialized = True

            logger.info(
                "[MANNEQUIN] Memory initialized. Description: %s...",
                description[:200] if description else "(no description)",
            )

            return description

        except Exception as e:
            logger.error("[MANNEQUIN] Failed to initialize memory: %s", e)
            raise ImageGenerationError(
                f"Mannequin memory initialization failed: {e}",
                model=settings.gemini_pro_model,
            ) from e

    async def generate_scene(
        self,
        prompt: str,
        output_path: Path,
        has_wardrobe_change: bool = False,
        additional_refs: list[types.Part] | None = None,
    ) -> str:
        """Generate a personnage scene image using the persistent chat session.

        The chat session maintains face/body consistency with the reference
        photos from initialization.

        Args:
            prompt: The enriched image prompt for this scene.
            output_path: Where to save the generated image.
            has_wardrobe_change: If True, explicitly instruct Gemini about wardrobe change.
            additional_refs: Additional reference image Parts (decor, product).

        Returns:
            Path to the saved image.

        Raises:
            ImageGenerationError: If generation fails.
            RuntimeError: If the session is not initialized.
        """
        if not self._is_initialized or not self.chat:
            raise RuntimeError(
                "Mannequin memory not initialized. Call initialize() first."
            )

        # Build generation prompt
        parts: list[types.Part] = []

        if additional_refs:
            parts.extend(additional_refs)

        generation_prompt = (
            f"Generate a cinematic advertising photograph with the EXACT same person "
            f"from the reference photos. The person must be clearly recognizable — "
            f"same face, same features, same skin tone.\n\n"
            f"Scene: {prompt}\n\n"
            f"CRITICAL: Maintain PERFECT identity consistency with the reference photos."
        )

        if has_wardrobe_change:
            generation_prompt += f"\n\n{WARDROBE_CHANGE_INSTRUCTION}"

        # Re-inject mannequin description for reinforcement
        if self.mannequin_description:
            generation_prompt += (
                f"\n\nReminder — the person's appearance: "
                f"{self.mannequin_description[:500]}"
            )

        parts.append(types.Part.from_text(text=generation_prompt))

        try:
            response = await self.chat.send_message(parts)

            # Extract generated image
            for part in response.candidates[0].content.parts:
                if part.inline_data and part.inline_data.mime_type.startswith("image/"):
                    output_path.parent.mkdir(parents=True, exist_ok=True)
                    output_path.write_bytes(part.inline_data.data)
                    logger.info("[MANNEQUIN] Scene image saved: %s", output_path)
                    return str(output_path)

            raise ImageGenerationError(
                "Gemini Pro returned no image in response",
                model=settings.gemini_pro_model,
            )

        except ImageGenerationError:
            raise
        except Exception as e:
            raise ImageGenerationError(
                f"Personnage scene generation failed: {e}",
                model=settings.gemini_pro_model,
            ) from e
