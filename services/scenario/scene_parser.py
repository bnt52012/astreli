"""
Scene parser — validates and normalizes GPT-4o responses.
"""
from __future__ import annotations

import logging
from typing import Any

from models.enums import CameraMovement, PipelineMode, SceneType, TransitionType
from pipeline.config import PIPELINE_DEFAULTS
from pipeline.exceptions import NoScenesError
from pipeline.mode_detector import ModeDetector

logger = logging.getLogger(__name__)

VALID_CAMERA = {m.value for m in CameraMovement}
VALID_TRANSITIONS = {t.value for t in TransitionType}
VALID_SCENE_TYPES = {s.value for s in SceneType}


class SceneParser:
    """Parse, validate, and normalize GPT-4o scene output."""

    def parse_and_validate(
        self, raw: dict[str, Any], mode: PipelineMode
    ) -> dict[str, Any]:
        scenes = raw.get("scenes", [])
        if not scenes:
            raise NoScenesError()

        validated_scenes: list[dict[str, Any]] = []

        for i, scene in enumerate(scenes):
            vs = self._validate_scene(scene, i + 1, mode)
            validated_scenes.append(vs)

        if not validated_scenes:
            raise NoScenesError()

        total_duration = sum(s["duration_seconds"] for s in validated_scenes)

        return {
            "total_scenes": len(validated_scenes),
            "estimated_duration": total_duration,
            "mood": raw.get("mood", ""),
            "color_palette": raw.get("color_palette", []),
            "scenes": validated_scenes,
        }

    def _validate_scene(
        self, scene: dict[str, Any], default_num: int, mode: PipelineMode
    ) -> dict[str, Any]:
        # Scene type
        scene_type = str(scene.get("scene_type", "produit")).lower().strip()
        if scene_type not in VALID_SCENE_TYPES:
            logger.warning("Invalid scene_type '%s', defaulting to 'produit'.", scene_type)
            scene_type = "produit"
        # Force produit in product-only mode
        scene_type = ModeDetector.should_force_produit(scene_type, mode)

        # Duration
        duration = float(scene.get("duration_seconds", 4.0))
        duration = max(PIPELINE_DEFAULTS.min_scene_duration,
                       min(PIPELINE_DEFAULTS.max_scene_duration, duration))

        # Camera movement
        camera = str(scene.get("camera_movement", "static")).lower().strip()
        if camera not in VALID_CAMERA:
            camera = "static"

        # Transition
        transition = str(scene.get("transition", "cut")).lower().strip()
        if transition not in VALID_TRANSITIONS:
            transition = "cut"

        # Needs mannequin
        needs_mannequin = scene_type == "personnage"

        return {
            "scene_number": scene.get("scene_number", default_num),
            "scene_type": scene_type,
            "prompt_image": str(scene.get("prompt_image", "")),
            "prompt_video": str(scene.get("prompt_video", "")),
            "duration_seconds": duration,
            "camera_movement": camera,
            "transition": transition,
            "needs_mannequin": needs_mannequin,
            "needs_decor_ref": bool(scene.get("needs_decor_ref", False)),
            "original_text": str(scene.get("original_text", "")),
        }
