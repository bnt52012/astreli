"""
Image Generation Engine — Routes scenes to the correct generation path.

PATH A: "personnage" scenes -> 3-pass LoRA SDXL + Nano Banana 2 FUSION
PATH B: "produit" scenes -> Nano Banana 2 (Gemini) one-shot
PATH C: "transition" scenes -> skip (handled by FFmpeg)
"""
from __future__ import annotations

import logging
from pathlib import Path

from models.enums import SceneType
from models.scene import ScenePipeline
from pipeline.config import settings
from pipeline.exceptions import ImageGenerationError
from services.image_generation.cache import ImageCache
from services.image_generation.fusion import FusionEngine
from services.image_generation.mannequin_generator import MannequinGenerator
from services.image_generation.product_generator import ProductGenerator
from services.image_generation.reference_manager import ReferenceManager
from services.image_generation.scene_generator import SceneGenerator

logger = logging.getLogger(__name__)


class ImageGenerationEngine:
    """Orchestrates image generation for all scene types."""

    def __init__(
        self,
        lora_model_id: str | None = None,
        lora_trigger_word: str = "MANNEQUIN",
        cache_dir: Path | None = None,
    ) -> None:
        self.lora_model_id = lora_model_id
        self.lora_trigger_word = lora_trigger_word
        self.scene_gen = SceneGenerator()
        self.product_gen = ProductGenerator()
        self.mannequin_gen = MannequinGenerator(
            lora_model_id=lora_model_id or "",
            trigger_word=lora_trigger_word,
        )
        self.fusion = FusionEngine()
        self.ref_manager = ReferenceManager()
        self.cache = ImageCache(cache_dir=cache_dir)

    async def generate_scene_image(
        self,
        scene: ScenePipeline,
        output_dir: Path,
        product_photos: list[str] | None = None,
        decor_photos: list[str] | None = None,
    ) -> Path | None:
        """Generate the final image for a scene.

        Returns:
            Path to the final image, or None if scene is a transition.

        Raises:
            ImageGenerationError on failure.
        """
        # PATH C: Transitions — no image needed
        if scene.scene_type == SceneType.TRANSITION:
            logger.info("Scene %d is transition — skipping image generation.", scene.index)
            return None

        # Check cache
        cache_key = self.cache.compute_key(scene.enriched_prompt_image or scene.prompt_image)
        cached = self.cache.get(cache_key)
        if cached:
            logger.info("Scene %d: cache hit.", scene.index)
            scene.final_image_path = cached
            scene.image_generated = True
            return cached

        try:
            if scene.scene_type == SceneType.PERSONNAGE:
                result = await self._generate_personnage(scene, output_dir, product_photos, decor_photos)
            else:
                result = await self._generate_produit(scene, output_dir, product_photos, decor_photos)

            if result:
                scene.final_image_path = result
                scene.image_generated = True
                self.cache.put(cache_key, result)
                logger.info("Scene %d: image generated -> %s", scene.index, result)

            return result

        except Exception as e:
            logger.error("Scene %d image generation failed: %s", scene.index, e)
            raise ImageGenerationError(scene.index, str(e))

    async def _generate_personnage(
        self,
        scene: ScenePipeline,
        output_dir: Path,
        product_photos: list[str] | None,
        decor_photos: list[str] | None,
    ) -> Path:
        """PATH A: 3-pass LoRA fusion workflow.

        Pass 1: Gemini generates base scene with generic figure
        Pass 2: LoRA SDXL generates mannequin with matching pose/lighting
        Pass 3: Inpainting fuses mannequin face onto base scene
        """
        scene.generation_attempts += 1
        img_dir = output_dir / "images"

        prompt = scene.enriched_prompt_image or scene.prompt_image

        # ── PASS 1: Scene generation (Gemini / Nano Banana 2) ────────
        logger.info("Scene %d Pass 1: Generating base scene with Gemini...", scene.index)
        ref_images = self.ref_manager.prepare_references(product_photos, decor_photos)

        base_path = img_dir / f"scene_{scene.index:02d}_base.png"
        base_path = await self.scene_gen.generate(
            prompt=prompt,
            output_path=base_path,
            reference_images=ref_images,
            aspect_ratio=scene.metadata.get("aspect_ratio", "16:9"),
        )
        scene.base_image_path = base_path

        # ── PASS 2: Mannequin generation (LoRA SDXL / Replicate) ────
        logger.info("Scene %d Pass 2: Generating mannequin with LoRA...", scene.index)
        mannequin_prompt = self._build_mannequin_prompt(prompt, scene)
        mannequin_path = img_dir / f"scene_{scene.index:02d}_mannequin.png"
        mannequin_path = await self.mannequin_gen.generate(
            prompt=mannequin_prompt,
            output_path=mannequin_path,
        )
        scene.mannequin_image_path = mannequin_path

        # ── PASS 3: Fusion (Inpainting) ─────────────────────────────
        logger.info("Scene %d Pass 3: Fusing scene + mannequin...", scene.index)
        fused_path = img_dir / f"scene_{scene.index:02d}_final.png"
        fused_path = await self.fusion.fuse(
            base_image_path=base_path,
            mannequin_image_path=mannequin_path,
            output_path=fused_path,
        )
        scene.fused_image_path = fused_path

        return fused_path

    async def _generate_produit(
        self,
        scene: ScenePipeline,
        output_dir: Path,
        product_photos: list[str] | None,
        decor_photos: list[str] | None,
    ) -> Path:
        """PATH B: Gemini one-shot product generation."""
        scene.generation_attempts += 1
        img_dir = output_dir / "images"

        prompt = scene.enriched_prompt_image or scene.prompt_image
        ref_images = self.ref_manager.prepare_references(product_photos, decor_photos)

        final_path = img_dir / f"scene_{scene.index:02d}_final.png"
        final_path = await self.product_gen.generate(
            prompt=prompt,
            output_path=final_path,
            reference_images=ref_images,
            aspect_ratio=scene.metadata.get("aspect_ratio", "16:9"),
        )

        return final_path

    def _build_mannequin_prompt(self, base_prompt: str, scene: ScenePipeline) -> str:
        """Build LoRA prompt matching the base scene's pose/lighting.

        Analyzes the base prompt to extract pose, angle, lighting details
        and includes them in the LoRA prompt.
        """
        # Extract directional/pose hints from the base prompt
        pose_hints = []

        lower = base_prompt.lower()
        # Head/gaze direction
        if "facing left" in lower or "profile left" in lower:
            pose_hints.append("head turned to the left, profile view")
        elif "facing right" in lower or "profile right" in lower:
            pose_hints.append("head turned to the right, profile view")
        elif "three quarter" in lower or "3/4" in lower:
            pose_hints.append("three-quarter view angle")
        else:
            pose_hints.append("facing forward, looking at camera")

        # Body pose
        if "sitting" in lower:
            pose_hints.append("sitting pose")
        elif "walking" in lower:
            pose_hints.append("walking pose, mid-stride")
        elif "standing" in lower:
            pose_hints.append("standing pose")
        elif "holding" in lower:
            pose_hints.append("hands positioned as if holding an object")

        # Lighting
        if "golden hour" in lower or "warm light" in lower:
            pose_hints.append("warm golden hour lighting")
        elif "studio" in lower:
            pose_hints.append("studio lighting setup")
        elif "natural light" in lower:
            pose_hints.append("natural daylight")

        # Framing
        if "close-up" in lower or "closeup" in lower:
            pose_hints.append("close-up framing, head and shoulders")
        elif "full body" in lower or "full-body" in lower:
            pose_hints.append("full body framing")
        elif "medium shot" in lower:
            pose_hints.append("medium shot, waist up")

        pose_desc = ", ".join(pose_hints)

        return (
            f"{self.lora_trigger_word}, portrait photograph, {pose_desc}, "
            f"photorealistic, 8K detail, natural skin texture, "
            f"sharp focus on face, professional photography"
        )
