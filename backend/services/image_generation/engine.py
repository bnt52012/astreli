"""
Dual Gemini Engine — Image Generation Orchestrator.

Routes scenes to the correct Gemini model:
- personnage scenes → Nano Banana Pro (persistent chat session)
- produit scenes → Nano Banana Flash (one-shot)
- transition scenes → skip (no image needed)

Handles:
- Automatic fallback (Pro fails → Flash)
- Scene-level caching
- Quality checking with regeneration
- Reference image management across both engines
"""

from __future__ import annotations

import logging
from pathlib import Path

from backend.models.enums import PipelineMode, SceneType
from backend.models.scene import ScenePipeline
from backend.pipeline.exceptions import ImageGenerationError
from backend.services.image_generation.cache import ImageCache
from backend.services.image_generation.fallback import FallbackStrategy
from backend.services.image_generation.nano_banana_flash import NanaBananaFlash
from backend.services.image_generation.nano_banana_pro import NanaBananaPro

logger = logging.getLogger(__name__)


class DualGeminiEngine:
    """Orchestrates dual Gemini image generation.

    Manages the Pro chat session (for personnage) and Flash one-shot
    (for produit), with automatic fallback and caching.

    Usage:
        engine = DualGeminiEngine(cache_dir=Path("cache/"))
        await engine.initialize_character_session(mannequin_paths)
        for scene in scenes:
            path = await engine.generate_scene(scene, mode, output_dir, ...)
    """

    def __init__(self, cache_dir: Path | None = None, cache_enabled: bool = True) -> None:
        self._pro = NanaBananaPro()
        self._flash = NanaBananaFlash()
        self._fallback = FallbackStrategy(self._pro, self._flash)
        self._cache = ImageCache(
            cache_dir=cache_dir or Path("/tmp/adgenai_cache"),
            enabled=cache_enabled,
        )

    async def initialize_character_session(
        self,
        mannequin_paths: list[str],
        decor_paths: list[str] | None = None,
    ) -> str:
        """Initialize the Gemini Pro chat session with mannequin references.

        Must be called before generating any personnage scenes.

        Args:
            mannequin_paths: Validated mannequin reference image paths.
            decor_paths: Optional decor reference paths.

        Returns:
            Gemini's description of the mannequin.
        """
        return await self._pro.initialize(mannequin_paths, decor_paths)

    async def generate_scene(
        self,
        scene: ScenePipeline,
        mode: PipelineMode,
        output_dir: Path,
        product_paths: list[str] | None = None,
        decor_paths: list[str] | None = None,
    ) -> str:
        """Generate an image for a single scene.

        Routes to the correct engine based on mode and scene type.
        Checks cache first, falls back on failure.

        Args:
            scene: Scene pipeline state.
            mode: Pipeline mode.
            output_dir: Directory for output images.
            product_paths: Product reference image paths.
            decor_paths: Decor reference image paths.

        Returns:
            Path to the generated/cached image.

        Raises:
            ImageGenerationError: If generation fails (after fallback attempts).
        """
        # Skip transition scenes
        if scene.analysis.type == SceneType.TRANSITION:
            logger.info("[ENGINE] Skipping transition scene %d", scene.analysis.id)
            scene.status = "skipped"
            return ""

        # Check cache
        ref_paths = (product_paths or []) + (decor_paths or [])
        cache_key = self._cache.compute_cache_key(
            prompt=scene.final_image_prompt,
            reference_paths=ref_paths,
            model=scene.gemini_model,
        )
        cached = self._cache.get(cache_key)
        if cached:
            scene.image_path = cached
            scene.cache_hit = True
            scene.status = "image_ready"
            return cached

        # Route to correct engine
        output_path = output_dir / f"scene_{scene.analysis.id:03d}_{scene.analysis.type.value}.png"

        try:
            if (
                mode == PipelineMode.PERSONNAGE_ET_PRODUIT
                and scene.analysis.type == SceneType.PERSONNAGE
            ):
                # Personnage → Pro with fallback to Flash
                result = await self._fallback.generate_with_fallback(
                    scene, output_path, product_paths, decor_paths,
                )
            else:
                # Produit → Flash direct
                result = await self._flash.generate(
                    scene, output_path, product_paths, decor_paths,
                )

            # Cache the result
            self._cache.put(
                cache_key, result, scene.final_image_prompt, scene.gemini_model,
            )

            scene.image_path = result
            scene.status = "image_ready"
            return result

        except ImageGenerationError:
            scene.status = "image_failed"
            raise
        except Exception as e:
            scene.status = "image_failed"
            raise ImageGenerationError(
                f"Image generation failed for scene {scene.analysis.id}: {e}",
                scene_index=scene.analysis.id,
            ) from e
