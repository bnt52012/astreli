"""
ÉTAPE 1 — GPT-4o Scenario Analyzer
Art-directs the scenario: splits into scenes, tags character/product,
generates detailed image & video prompts.
"""
from __future__ import annotations

import json
import logging

from openai import AsyncOpenAI

from backend.config import settings
from backend.models.schemas import (
    PipelineMode,
    ScenarioAnalysisResult,
    SceneAnalysis,
)

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are an elite creative director for cinematic advertising.
You receive a marketing scenario and must decompose it into individual visual scenes
for an AI-powered ad pipeline.

RULES:
- Output ONLY valid JSON (no markdown fences, no commentary).
- Each scene must have a unique integer id starting at 1.
- image_prompt: English, ultra-detailed, cinematic photography style.
  Include lens (e.g. 85mm f/1.4), lighting (soft key light, rim light),
  textures, depth of field, color palette. Be specific about composition.
- video_prompt: describe the motion, camera movement, and physics.
- camera_movement: one of [static, dolly_in, dolly_out, orbit, tracking, crane_up, crane_down, pan_left, pan_right, zoom_in, zoom_out].
- lighting: describe the lighting setup for the scene.
- duration: 3-8 seconds per scene.
- transition: one of [fade, dissolve, wipe, cut].
- goal: one sentence describing the emotional/narrative purpose.
- Aim for 3-6 scenes total for a 15-30s spot.

{mode_instruction}

Return this exact JSON structure:
{{
  "concept": "one-line creative concept",
  "tone": "e.g. luxurious, energetic, minimal",
  "visual_style": "e.g. cinematic warm tones, high-contrast noir",
  "target_audience": "...",
  "narrative_arc": "hook → build → climax → payoff",
  "scenes": [
    {{
      "id": 1,
      "type": "character" or "product",
      "goal": "...",
      "description": "...",
      "image_prompt": "...",
      "video_prompt": "...",
      "camera_movement": "...",
      "lighting": "...",
      "duration": 5,
      "transition": "fade"
    }}
  ]
}}"""

CHARACTER_MODE_INSTRUCTION = """MODE: CHARACTER + PRODUCT
The client provided mannequin photos. You MUST tag each scene as either:
- "character": the mannequin/model appears in the scene
- "product": only the product is shown (no person)
Mix both types for a dynamic ad. Start with a character hook."""

PRODUCT_MODE_INSTRUCTION = """MODE: PRODUCT ONLY
No mannequin photos provided. ALL scenes must be tagged as "product".
Focus on the product itself: textures, reflections, details, environment."""


class ScenarioAnalyzer:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def analyze(
        self,
        scenario: str,
        mode: PipelineMode,
        project_id: str,
        brand_name: str | None = None,
        brand_tone: str | None = None,
    ) -> ScenarioAnalysisResult:
        mode_instruction = (
            CHARACTER_MODE_INSTRUCTION
            if mode == PipelineMode.CHARACTER_PRODUCT
            else PRODUCT_MODE_INSTRUCTION
        )

        system = SYSTEM_PROMPT.format(mode_instruction=mode_instruction)

        user_msg = f"Scenario: {scenario}"
        if brand_name:
            user_msg += f"\nBrand: {brand_name}"
        if brand_tone:
            user_msg += f"\nBrand tone: {brand_tone}"

        logger.info("Analyzing scenario with GPT-4o (mode=%s)", mode.value)

        response = await self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.7,
            max_tokens=4096,
            response_format={"type": "json_object"},
        )

        raw = response.choices[0].message.content
        data = json.loads(raw)

        scenes = [SceneAnalysis(**s) for s in data["scenes"]]

        result = ScenarioAnalysisResult(
            project_id=project_id,
            concept=data.get("concept", ""),
            tone=data.get("tone", ""),
            visual_style=data.get("visual_style", ""),
            target_audience=data.get("target_audience", ""),
            narrative_arc=data.get("narrative_arc", ""),
            scenes=scenes,
        )

        logger.info(
            "Scenario analyzed: %d scenes (%s)",
            len(scenes),
            ", ".join(s.type.value for s in scenes),
        )
        return result
