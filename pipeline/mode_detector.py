"""
Pipeline Mode Detector.

LoRA selected   -> MODE 1: PERSONNAGE + PRODUIT
No LoRA         -> MODE 2: PRODUIT UNIQUEMENT
"""
from __future__ import annotations

import logging
from models.enums import PipelineMode

logger = logging.getLogger(__name__)


class ModeDetector:
    @staticmethod
    def detect(lora_model_id: str | None) -> PipelineMode:
        if lora_model_id and lora_model_id.strip():
            logger.info("LoRA model detected (%s) -> PERSONNAGE + PRODUIT mode.", lora_model_id)
            return PipelineMode.PERSONNAGE_ET_PRODUIT
        logger.info("No LoRA model -> PRODUIT UNIQUEMENT mode.")
        return PipelineMode.PRODUIT_UNIQUEMENT

    @staticmethod
    def should_force_produit(scene_type: str, mode: PipelineMode) -> str:
        """In PRODUIT_UNIQUEMENT mode, force 'personnage' to 'produit'."""
        if mode == PipelineMode.PRODUIT_UNIQUEMENT and scene_type == "personnage":
            logger.warning("GPT-4o returned 'personnage' in PRODUIT_UNIQUEMENT mode - forcing to 'produit'.")
            return "produit"
        return scene_type
