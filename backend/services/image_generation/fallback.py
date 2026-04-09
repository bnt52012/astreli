"""
Fallback Strategy for Image Generation.

If Gemini Pro fails on a personnage scene, automatically falls back
to Gemini Flash. The quality may be lower (no face consistency memory),
but the pipeline continues rather than failing entirely.

The client never sees the fallback — they just get an image.
"""

from __future__ import annotations

import logging
from pathlib import Path

from backend.models.scene import ScenePipeline
from backend.pipeline.exceptions import ImageGenerationError
from backend.services.image_generation.nano_banana_flash import NanaBananaFlash
from backend.services.image_generation.nano_banana_pro import NanaBananaPro

logger = logging.getLogger(__name__)


class FallbackStrategy:
    """Manages fallback from Gemini Pro to Gemini Flash.

    When Pro fails (timeout, rate limit, content filter), Flash can
    still generate the scene without face consistency. This is a
    graceful degradation — better than a missing scene.
    """

    def __init__(
        self,
        pro: NanaBananaPro,
        flash: NanaBananaFlash,
        max_pro_retries: int = 1,
    ) -> None:
        self._pro = pro
        self._flash = flash
        self._max_pro_retries = max_pro_retries

    async def generate_with_fallback(
        self,
        scene: ScenePipeline,
        output_path: Path,
        product_paths: list[str] | None = None,
        decor_paths: list[str] | None = None,
    ) -> str:
        """Try Pro first, fall back to Flash on failure.

        Args:
            scene: Scene to generate.
            output_path: Image output path.
            product_paths: Product reference images.
            decor_paths: Decor reference images.

        Returns:
            Path to the saved image.

        Raises:
            ImageGenerationError: If both Pro and Flash fail.
        """
        # Attempt 1: Gemini Pro (with session memory)
        if self._pro.is_initialized:
            for attempt in range(self._max_pro_retries + 1):
                try:
                    result = await self._pro.generate(
                        scene, output_path, product_paths, decor_paths,
                    )
                    return result
                except ImageGenerationError as e:
                    logger.warning(
                        "[FALLBACK] Pro failed for scene %d (attempt %d/%d): %s",
                        scene.analysis.id,
                        attempt + 1,
                        self._max_pro_retries + 1,
                        e.message,
                    )
                    if attempt < self._max_pro_retries:
                        continue
                    break
                except Exception as e:
                    logger.warning(
                        "[FALLBACK] Pro unexpected error for scene %d: %s",
                        scene.analysis.id,
                        e,
                    )
                    break

        # Attempt 2: Fallback to Flash
        logger.warning(
            "[FALLBACK] Falling back to Flash for personnage scene %d "
            "(face consistency may be reduced)",
            scene.analysis.id,
        )

        try:
            # Use a different output path to avoid conflicts
            fallback_path = output_path.with_name(
                output_path.stem + "_fallback" + output_path.suffix
            )
            result = await self._flash.generate(
                scene, fallback_path, product_paths, decor_paths,
            )
            scene.used_fallback = True
            return result

        except ImageGenerationError as e:
            raise ImageGenerationError(
                f"Both Pro and Flash failed for scene {scene.analysis.id}: {e.message}",
                model="both",
                scene_index=scene.analysis.id,
            ) from e
