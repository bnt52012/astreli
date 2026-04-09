"""
Scene Parser — Validates and normalizes GPT-4o JSON output.

Handles edge cases, malformed JSON, missing fields, and mode enforcement.
Converts raw GPT-4o output into validated SceneAnalysis objects.
"""

from __future__ import annotations

import json
import logging
import re
from typing import Any

from backend.models.enums import PipelineMode, SceneType, TransitionType
from backend.models.scene import SceneAnalysis
from backend.pipeline.exceptions import ScenarioAnalysisError

logger = logging.getLogger(__name__)

# Valid values for validation
VALID_CAMERA_MOVEMENTS = {
    "static", "dolly_in", "dolly_out", "orbit", "tracking",
    "crane_up", "crane_down", "pan_left", "pan_right",
    "zoom_in", "zoom_out", "handheld", "steadicam", "tilt_up", "tilt_down",
}

VALID_TRANSITIONS = {t.value for t in TransitionType}


def parse_gpt4o_response(
    raw_text: str,
    mode: PipelineMode,
) -> tuple[dict[str, Any], list[SceneAnalysis]]:
    """Parse and validate GPT-4o scenario analysis response.

    Args:
        raw_text: Raw JSON string from GPT-4o.
        mode: Pipeline mode for scene type enforcement.

    Returns:
        Tuple of (metadata dict, list of validated SceneAnalysis).

    Raises:
        ScenarioAnalysisError: If the response cannot be parsed or is invalid.
    """
    # Step 1: Parse JSON
    data = _extract_json(raw_text)

    # Step 2: Extract metadata
    metadata = {
        "concept": data.get("concept", ""),
        "tone": data.get("tone", ""),
        "visual_style": data.get("visual_style", ""),
        "target_audience": data.get("target_audience", ""),
        "narrative_arc": data.get("narrative_arc", ""),
    }

    # Step 3: Parse and validate scenes
    raw_scenes = data.get("scenes", [])
    if not raw_scenes:
        raise ScenarioAnalysisError(
            "GPT-4o returned no scenes",
            details={"raw_response": raw_text[:500]},
        )

    scenes: list[SceneAnalysis] = []
    for i, raw_scene in enumerate(raw_scenes):
        try:
            scene = _parse_single_scene(raw_scene, i + 1, mode)
            scenes.append(scene)
        except Exception as e:
            logger.warning(
                "[PARSER] Failed to parse scene %d: %s (skipping)", i + 1, e
            )
            continue

    if not scenes:
        raise ScenarioAnalysisError(
            "All scenes failed validation",
            details={"raw_scenes_count": len(raw_scenes)},
        )

    # Step 4: Ensure sequential IDs
    for i, scene in enumerate(scenes):
        scene.id = i + 1

    logger.info(
        "[PARSER] Parsed %d/%d scenes successfully",
        len(scenes),
        len(raw_scenes),
    )

    return metadata, scenes


def _extract_json(raw_text: str) -> dict[str, Any]:
    """Extract and parse JSON from GPT-4o response text.

    Handles markdown code fences and other common formatting issues.
    """
    text = raw_text.strip()

    # Remove markdown code fences
    if text.startswith("```"):
        lines = text.split("\n")
        # Remove first line (```json) and last line (```)
        if lines[-1].strip() in ("```", ""):
            lines = lines[1:-1]
        else:
            lines = lines[1:]
        text = "\n".join(lines).strip()

    # Try direct parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try to find JSON object in the text
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    raise ScenarioAnalysisError(
        "Could not parse GPT-4o response as JSON",
        details={"raw_text": text[:500]},
    )


def _parse_single_scene(
    raw: dict[str, Any],
    fallback_id: int,
    mode: PipelineMode,
) -> SceneAnalysis:
    """Parse and validate a single scene from GPT-4o output.

    Args:
        raw: Raw scene dictionary from GPT-4o.
        fallback_id: ID to use if not provided.
        mode: Pipeline mode for type enforcement.

    Returns:
        Validated SceneAnalysis.
    """
    # Scene type with mode enforcement
    raw_type = raw.get("type", "produit").lower().strip()

    # Map common variations
    type_map = {
        "character": "personnage",
        "character_product": "personnage",
        "person": "personnage",
        "model": "personnage",
        "mannequin": "personnage",
        "product": "produit",
        "packshot": "produit",
        "object": "produit",
        "title": "transition",
        "text": "transition",
        "title_card": "transition",
        "end_card": "transition",
    }
    normalized_type = type_map.get(raw_type, raw_type)

    # Enforce mode constraints
    if mode == PipelineMode.PRODUIT_UNIQUEMENT and normalized_type == "personnage":
        logger.warning(
            "[PARSER] Scene %d: forcing type from 'personnage' to 'produit' (PRODUIT_UNIQUEMENT mode)",
            fallback_id,
        )
        normalized_type = "produit"

    # Validate scene type
    try:
        scene_type = SceneType(normalized_type)
    except ValueError:
        logger.warning(
            "[PARSER] Scene %d: unknown type '%s', defaulting to 'produit'",
            fallback_id,
            normalized_type,
        )
        scene_type = SceneType.PRODUIT

    # Validate camera movement
    camera = raw.get("camera_movement", "static").lower().strip().replace(" ", "_")
    if camera not in VALID_CAMERA_MOVEMENTS:
        camera = "static"

    # Validate transition
    transition_raw = raw.get("transition", "fade").lower().strip()
    try:
        transition = TransitionType(transition_raw)
    except ValueError:
        transition = TransitionType.FADE

    # Validate duration
    duration = raw.get("duration", 5.0)
    try:
        duration = float(duration)
        duration = max(2.0, min(10.0, duration))
    except (TypeError, ValueError):
        duration = 5.0

    # Build SceneAnalysis
    return SceneAnalysis(
        id=raw.get("id", fallback_id),
        type=scene_type,
        goal=raw.get("goal", ""),
        description=raw.get("description", ""),
        image_prompt=raw.get("image_prompt", raw.get("description", "")),
        video_prompt=raw.get("video_prompt", ""),
        camera_movement=camera,
        lighting=raw.get("lighting", ""),
        duration=duration,
        transition=transition,
        needs_mannequin=bool(raw.get("needs_mannequin", scene_type == SceneType.PERSONNAGE)),
        needs_product=bool(raw.get("needs_product", scene_type == SceneType.PRODUIT)),
        needs_decor_ref=bool(raw.get("needs_decor_ref", False)),
        references_scene=raw.get("references_scene"),
        text_overlay=raw.get("text_overlay"),
    )
