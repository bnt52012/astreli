"""
Prompt Optimization Engine

Transforms base prompts from GPT-4o into ultra-detailed,
cinematic, physically realistic, brand-consistent prompts
for both image and video generation.
"""
from __future__ import annotations

import json
import logging

from openai import AsyncOpenAI

from backend.config import settings
from backend.models.schemas import ScenePipeline

logger = logging.getLogger(__name__)

IMAGE_OPTIMIZER_SYSTEM = """You are a prompt engineer specializing in AI image generation.
Transform the given base prompt into an ULTRA-DETAILED cinematic photography prompt.

MANDATORY additions:
- Specific lens: 50mm f/1.4, 85mm f/1.2, 35mm f/2, etc.
- Lighting setup: key light type, fill, rim light, practical lights
- Texture details: skin pores, fabric weave, metal reflections, glass refraction
- Depth of field: shallow/deep, bokeh quality
- Color grading: teal-orange, warm golden, cool desaturated, etc.
- Composition: rule of thirds, leading lines, negative space
- Atmosphere: haze, dust particles, lens flare
- Resolution cue: "8K quality", "shot on ARRI Alexa"

Keep the original scene intent. Output ONLY the enhanced prompt, nothing else."""

VIDEO_OPTIMIZER_SYSTEM = """You are a prompt engineer for AI video generation.
Transform the given base prompt into a precise video motion prompt.

MANDATORY additions:
- Exact camera movement (smooth dolly in at 2cm/s, slow orbit 15°/s)
- Subject motion (hair flowing, fabric rippling, fingers touching product)
- Physics details (realistic weight, inertia, light caustics)
- Temporal pacing (start slow, accelerate, hold)
- Realism constraints (no morphing, no teleportation, natural motion blur)

Keep the original intent. Output ONLY the enhanced prompt, nothing else."""


class PromptOptimizer:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def optimize_image_prompt(
        self,
        base_prompt: str,
        visual_style: str = "",
        brand_tone: str = "",
    ) -> str:
        user_msg = f"Base prompt: {base_prompt}"
        if visual_style:
            user_msg += f"\nVisual style: {visual_style}"
        if brand_tone:
            user_msg += f"\nBrand tone: {brand_tone}"

        response = await self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": IMAGE_OPTIMIZER_SYSTEM},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.6,
            max_tokens=1024,
        )
        return response.choices[0].message.content.strip()

    async def optimize_video_prompt(
        self,
        base_prompt: str,
        camera_movement: str = "",
        duration: float = 5.0,
    ) -> str:
        user_msg = f"Base prompt: {base_prompt}"
        if camera_movement:
            user_msg += f"\nCamera movement: {camera_movement}"
        user_msg += f"\nDuration: {duration}s"

        response = await self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": VIDEO_OPTIMIZER_SYSTEM},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.6,
            max_tokens=1024,
        )
        return response.choices[0].message.content.strip()

    async def optimize_scene(
        self,
        scene: ScenePipeline,
        visual_style: str = "",
        brand_tone: str = "",
    ) -> ScenePipeline:
        """Optimize both image and video prompts for a scene."""
        scene.optimized_image_prompt = await self.optimize_image_prompt(
            scene.analysis.image_prompt,
            visual_style=visual_style,
            brand_tone=brand_tone,
        )
        scene.optimized_video_prompt = await self.optimize_video_prompt(
            scene.analysis.video_prompt,
            camera_movement=scene.analysis.camera_movement,
            duration=scene.analysis.duration,
        )
        logger.info("Prompts optimized for scene %d", scene.analysis.id)
        return scene
