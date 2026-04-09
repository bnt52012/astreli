"""
Pass 2 — LoRA SDXL mannequin generator.

Generates the client's mannequin in a pose matching the base scene from Pass 1.
Uses Gemini to analyze the base image for pose, lighting, and clothing details,
then runs the LoRA model on Replicate to produce a matching mannequin image.
"""

from __future__ import annotations

import asyncio
import io
import logging
import time
from pathlib import Path
from typing import Any

import httpx
from google import genai
from google.genai import types
from PIL import Image

from backend.config import settings
from backend.models.scene import ScenePipeline
from backend.pipeline.exceptions import LoRAGenerationError
from backend.services.lora.manager import LoRAManager

logger = logging.getLogger(__name__)

# ── Analysis Prompt ──────────────────────────────────────────

POSE_ANALYSIS_PROMPT = """\
Analyze this image of a scene containing a human figure. Extract the following
details as a JSON object:

{
    "head_angle": "description of head orientation (e.g. 'facing left', '3/4 right', 'forward')",
    "body_pose": "description of body position (e.g. 'standing upright', 'sitting cross-legged', 'walking')",
    "lighting_direction": "main light source direction (e.g. 'from upper left', 'above center', 'behind subject')",
    "clothing_description": "detailed description of what the figure is wearing",
    "background_context": "brief description of the scene background",
    "camera_angle": "camera perspective (e.g. 'eye level', 'slightly above', 'low angle')"
}

Return ONLY the JSON object, no other text.
"""


class MannequinGenerator:
    """Pass 2 — generates the client's mannequin via LoRA SDXL on Replicate.

    Workflow:
        1. Analyze the base scene (from Pass 1) to extract pose details.
        2. Build a LoRA prompt matching the extracted pose and lighting.
        3. Run the LoRA model on Replicate.
        4. Download and save the mannequin image.
    """

    def __init__(self) -> None:
        if not settings.gemini_api_key:
            raise LoRAGenerationError(
                "Gemini API key required for pose analysis. "
                "Set ADGENAI_GEMINI_API_KEY.",
            )
        self._gemini_client = genai.Client(api_key=settings.gemini_api_key)
        self._lora_manager = LoRAManager()

    # ── Pose Analysis ────────────────────────────────────────

    async def analyze_base_scene(self, base_image_path: str) -> dict[str, str]:
        """Analyze the base scene image to extract pose and lighting details.

        Sends the base image to Gemini for structured analysis of the
        generic figure's pose, head angle, lighting direction, and clothing.

        Args:
            base_image_path: Path to the Pass 1 base scene image.

        Returns:
            Dict with keys: ``head_angle``, ``body_pose``, ``lighting_direction``,
            ``clothing_description``, ``background_context``, ``camera_angle``.

        Raises:
            LoRAGenerationError: If pose analysis fails.
        """
        logger.info("Analyzing base scene for pose: %s", base_image_path)

        try:
            image = Image.open(base_image_path)

            response = await self._gemini_client.aio.models.generate_content(
                model=settings.gemini_image_model,
                contents=[
                    POSE_ANALYSIS_PROMPT,
                    types.Part.from_image(image),
                ],
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT"],
                ),
            )

            # Parse JSON from response text
            import json

            response_text = response.text.strip()
            # Handle markdown code blocks
            if response_text.startswith("```"):
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
                response_text = response_text.strip()

            analysis = json.loads(response_text)
            logger.info("Pose analysis complete: %s", analysis)
            return analysis

        except json.JSONDecodeError as exc:
            raise LoRAGenerationError(
                f"Failed to parse pose analysis JSON: {exc}",
                details={"raw_response": response_text[:500] if "response_text" in dir() else ""},
            ) from exc
        except Exception as exc:
            raise LoRAGenerationError(
                f"Pose analysis failed for {base_image_path}: {exc}",
            ) from exc

    # ── Mannequin Generation ─────────────────────────────────

    async def generate_mannequin(
        self,
        scene: ScenePipeline,
        base_analysis: dict[str, str],
        lora_model_id: str,
        output_dir: Path,
    ) -> str:
        """Generate the client's mannequin matching the base scene pose.

        Builds a LoRA prompt from the pose analysis and scene context,
        then runs the LoRA model on Replicate to produce a mannequin
        image that matches the base scene's composition.

        Args:
            scene: Scene pipeline state.
            base_analysis: Pose analysis dict from ``analyze_base_scene``.
            lora_model_id: Replicate LoRA model identifier.
            output_dir: Directory to save the mannequin image.

        Returns:
            Path to the saved mannequin image (``scene_XX_mannequin.png``).

        Raises:
            LoRAGenerationError: If mannequin generation fails.
        """
        scene_id = scene.analysis.id
        logger.info("Pass 2 — generating mannequin for scene %d with LoRA %s",
                     scene_id, lora_model_id)
        start_time = time.monotonic()

        # Build the mannequin prompt
        prompt = self._build_mannequin_prompt(scene, base_analysis)
        scene.mannequin_prompt = prompt

        try:
            # Generate via LoRA
            image_url = await self._lora_manager.generate_with_lora(
                model_id=lora_model_id,
                prompt=prompt,
                negative_prompt=(
                    "blurry, distorted face, extra limbs, bad anatomy, "
                    "low quality, watermark, text, deformed"
                ),
                width=1024,
                height=1024,
            )

            # Download and save
            output_dir.mkdir(parents=True, exist_ok=True)
            output_path = output_dir / f"scene_{scene_id:02d}_mannequin.png"

            await self._download_image(image_url, output_path)

            elapsed_ms = int((time.monotonic() - start_time) * 1000)
            logger.info(
                "Pass 2 complete for scene %d in %dms: %s",
                scene_id, elapsed_ms, output_path,
            )

            # Update scene state
            scene.mannequin_path = str(output_path)
            scene.lora_model_id = lora_model_id

            return str(output_path)

        except LoRAGenerationError:
            raise
        except Exception as exc:
            raise LoRAGenerationError(
                f"Mannequin generation failed for scene {scene_id}: {exc}",
                lora_model_id=lora_model_id,
                scene_index=scene_id,
            ) from exc

    # ── Prompt Building ──────────────────────────────────────

    def _build_mannequin_prompt(
        self,
        scene: ScenePipeline,
        base_analysis: dict[str, str],
    ) -> str:
        """Build the LoRA generation prompt from pose analysis and scene context.

        The prompt includes:
            - LoRA trigger word (MANNEQUIN by default).
            - Pose matching from the base analysis.
            - Lighting and camera angle matching.
            - Clothing description from the scenario.

        Args:
            scene: Scene pipeline state.
            base_analysis: Pose analysis from ``analyze_base_scene``.

        Returns:
            Fully constructed LoRA prompt string.
        """
        # Retrieve trigger word from metadata or default
        metadata = self._lora_manager.get_metadata(scene.lora_model_id or "")
        trigger_word = metadata.trigger_word if metadata else "MANNEQUIN"

        head_angle = base_analysis.get("head_angle", "facing forward")
        body_pose = base_analysis.get("body_pose", "standing upright")
        lighting = base_analysis.get("lighting_direction", "soft natural lighting")
        clothing = base_analysis.get("clothing_description", "")
        camera = base_analysis.get("camera_angle", "eye level")

        # Clothing from scenario enrichment takes priority
        scenario_clothing = scene.analysis.description if scene.analysis else ""

        prompt_parts = [
            f"{trigger_word} portrait photo",
            f"head {head_angle}",
            f"body {body_pose}",
            f"lighting: {lighting}",
            f"camera: {camera}",
        ]

        if clothing:
            prompt_parts.append(f"wearing: {clothing}")

        prompt_parts.extend([
            "professional advertising photography",
            "sharp focus, high detail, clean background",
            "8k, photorealistic, studio quality",
        ])

        return ", ".join(prompt_parts)

    # ── Download Helper ──────────────────────────────────────

    async def _download_image(self, url: str, output_path: Path) -> None:
        """Download an image from a URL and save it locally.

        Args:
            url: Source image URL.
            output_path: Local file path to save the image.

        Raises:
            LoRAGenerationError: If the download fails.
        """
        try:
            async with httpx.AsyncClient(timeout=60) as client:
                resp = await client.get(url)
                resp.raise_for_status()

            image = Image.open(io.BytesIO(resp.content))
            image.save(output_path, format="PNG")
            logger.debug("Downloaded mannequin image to %s (%dx%d)",
                         output_path, image.width, image.height)

        except Exception as exc:
            raise LoRAGenerationError(
                f"Failed to download mannequin image from {url}: {exc}",
            ) from exc
