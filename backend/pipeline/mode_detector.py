"""
Pipeline Mode Detection.

Determines whether the pipeline runs in PERSONNAGE+PRODUIT mode
(character + product, with Gemini Pro chat session for face consistency)
or PRODUIT UNIQUEMENT mode (product only, Gemini Flash one-shot).

The single deciding factor: did the client provide mannequin/model
reference photos that actually exist on disk?
"""

from __future__ import annotations

import logging
from pathlib import Path

from backend.models.enums import PipelineMode

logger = logging.getLogger(__name__)

# Supported image formats for reference photos
SUPPORTED_IMAGE_FORMATS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff", ".tif"}


class ModeDetector:
    """Detects pipeline mode based on mannequin reference images.

    The client's intent is binary:
    - Provided mannequin photos -> they want a character in their ad
    - No mannequin photos -> product-only ad

    We validate that provided paths actually point to real image files
    on disk to avoid starting a character session with missing references.
    """

    @staticmethod
    def detect(
        mannequin_image_paths: list[str] | None,
    ) -> tuple[PipelineMode, list[str]]:
        """Detect pipeline mode and return validated mannequin paths.

        Args:
            mannequin_image_paths: List of file paths to mannequin/model
                reference photos provided by the client.

        Returns:
            Tuple of (detected mode, list of validated image paths that
            exist on disk and have supported image extensions).
        """
        if not mannequin_image_paths:
            logger.info(
                "[MODE] PRODUIT UNIQUEMENT - No mannequin references provided"
            )
            return PipelineMode.PRODUIT_UNIQUEMENT, []

        # Validate each path: must exist and be a supported image format
        valid_paths: list[str] = []
        invalid_paths: list[str] = []

        for path_str in mannequin_image_paths:
            path = Path(path_str)
            if not path.exists():
                invalid_paths.append(path_str)
                logger.warning(
                    "[MODE] Mannequin reference not found on disk: %s", path_str
                )
                continue

            if path.suffix.lower() not in SUPPORTED_IMAGE_FORMATS:
                invalid_paths.append(path_str)
                logger.warning(
                    "[MODE] Unsupported image format for mannequin ref: %s", path_str
                )
                continue

            # Check file is not empty
            if path.stat().st_size < 100:
                invalid_paths.append(path_str)
                logger.warning(
                    "[MODE] Mannequin reference file is too small (likely corrupt): %s",
                    path_str,
                )
                continue

            valid_paths.append(path_str)

        if invalid_paths:
            logger.warning(
                "[MODE] Filtered out %d invalid mannequin reference(s): %s",
                len(invalid_paths),
                invalid_paths,
            )

        if valid_paths:
            logger.info(
                "[MODE] PERSONNAGE + PRODUIT - %d valid mannequin reference(s)",
                len(valid_paths),
            )
            return PipelineMode.PERSONNAGE_ET_PRODUIT, valid_paths
        else:
            logger.info(
                "[MODE] PRODUIT UNIQUEMENT - All %d mannequin references were invalid",
                len(mannequin_image_paths),
            )
            return PipelineMode.PRODUIT_UNIQUEMENT, []

    @staticmethod
    def validate_reference_images(
        image_paths: list[str] | None,
        label: str = "reference",
    ) -> list[str]:
        """Validate a list of reference image paths (product, decor, etc.).

        Args:
            image_paths: File paths to validate.
            label: Human-readable label for logging.

        Returns:
            List of paths that exist and are valid image files.
        """
        if not image_paths:
            return []

        valid: list[str] = []
        for path_str in image_paths:
            path = Path(path_str)
            if (
                path.exists()
                and path.suffix.lower() in SUPPORTED_IMAGE_FORMATS
                and path.stat().st_size >= 100
            ):
                valid.append(path_str)
            else:
                logger.warning("[VALIDATE] Invalid %s image: %s", label, path_str)

        logger.info(
            "[VALIDATE] %d/%d %s images validated",
            len(valid),
            len(image_paths),
            label,
        )
        return valid
