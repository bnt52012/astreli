"""
Nano Banana Pro — Gemini Pro Chat Session Manager.

Handles personnage (character) scene generation using a PERSISTENT
chat session with Gemini Pro for face/body consistency.

This is a thin wrapper around MannequinMemory that provides the
standard scene generation interface used by the DualGeminiEngine.
"""

from __future__ import annotations

import logging
import time
from pathlib import Path

from google.genai import types

from backend.config import settings
from backend.models.scene import ScenePipeline
from backend.pipeline.exceptions import ImageGenerationError
from backend.services.image_generation.mannequin_memory import MannequinMemory
from backend.services.image_generation.reference_manager import ReferenceManager

logger = logging.getLogger(__name__)


class NanaBananaPro:
    """Gemini Pro chat session for personnage scenes.

    Uses a persistent chat session (MannequinMemory) to maintain
    face/body consistency across all character scenes in the ad.

    Workflow:
    1. initialize() — send mannequin refs, establish memory
    2. generate() — generate each personnage scene within the session
    """

    def __init__(self) -> None:
        self.memory = MannequinMemory()
        self._ref_manager = ReferenceManager()

    @property
    def is_initialized(self) -> bool:
        return self.memory.is_initialized

    async def initialize(
        self,
        mannequin_paths: list[str],
        decor_paths: list[str] | None = None,
    ) -> str:
        """Initialize the Pro session with mannequin references.

        Returns Gemini's confirmation description.
        """
        return await self.memory.initialize(mannequin_paths, decor_paths)

    async def generate(
        self,
        scene: ScenePipeline,
        output_path: Path,
        product_paths: list[str] | None = None,
        decor_paths: list[str] | None = None,
    ) -> str:
        """Generate a personnage scene image.

        Args:
            scene: The scene pipeline state with enriched prompts.
            output_path: Where to save the generated image.
            product_paths: Product reference images (if product appears in scene).
            decor_paths: Decor reference images.

        Returns:
            Path to the saved image.
        """
        start_time = time.time()

        # Prepare additional reference Parts for this specific scene
        additional_refs: list[types.Part] = []

        if scene.context.requires_product_in_frame and product_paths:
            product_parts = self._ref_manager.prepare_parts(
                product_paths[:3], max_images=3, label="product-in-scene",
            )
            additional_refs.extend(product_parts)

        if scene.analysis.needs_decor_ref and decor_paths:
            decor_parts = self._ref_manager.prepare_parts(
                decor_paths[:2], max_images=2, label="decor-in-scene",
            )
            additional_refs.extend(decor_parts)

        result = await self.memory.generate_scene(
            prompt=scene.final_image_prompt,
            output_path=output_path,
            has_wardrobe_change=scene.context.has_wardrobe_change,
            additional_refs=additional_refs if additional_refs else None,
        )

        elapsed_ms = int((time.time() - start_time) * 1000)
        scene.image_generation_model = settings.gemini_pro_model
        scene.image_generation_time_ms = elapsed_ms

        logger.info(
            "[PRO] Scene %d generated in %dms: %s",
            scene.analysis.id,
            elapsed_ms,
            result,
        )

        return result
