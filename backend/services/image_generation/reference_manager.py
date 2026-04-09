"""
Reference Image Manager.

Handles loading, validating, resizing, and batching of reference images
(mannequin, product, decor) for Gemini API calls.

Enforces API limits:
- Max 14 images per Gemini call
- Max 2048px per image dimension
- Supported formats only
"""

from __future__ import annotations

import logging
from pathlib import Path

from google.genai import types

from backend.utils.image_utils import (
    image_to_bytes,
    load_and_prepare_image,
    MAX_GEMINI_IMAGE_SIZE_PX,
)

logger = logging.getLogger(__name__)

MAX_IMAGES_PER_CALL = 14


class ReferenceManager:
    """Manages reference images for Gemini API calls.

    Handles the full lifecycle: load from disk, validate, resize to
    API limits, convert to Gemini Part objects, and batch within limits.
    """

    def __init__(self, max_size_px: int = MAX_GEMINI_IMAGE_SIZE_PX) -> None:
        self._max_size = max_size_px

    def prepare_parts(
        self,
        image_paths: list[str],
        max_images: int = MAX_IMAGES_PER_CALL,
        label: str = "reference",
    ) -> list[types.Part]:
        """Load and prepare reference images as Gemini Part objects.

        Args:
            image_paths: File paths to reference images.
            max_images: Maximum number of images to include.
            label: Label for logging.

        Returns:
            List of Gemini Part objects ready for API call.
        """
        if not image_paths:
            return []

        if len(image_paths) > max_images:
            logger.warning(
                "[REF] Too many %s images (%d), limiting to %d",
                label,
                len(image_paths),
                max_images,
            )
            image_paths = image_paths[:max_images]

        parts: list[types.Part] = []
        for path_str in image_paths:
            try:
                part = self._load_as_part(path_str)
                parts.append(part)
            except Exception as e:
                logger.warning(
                    "[REF] Failed to load %s image %s: %s",
                    label,
                    path_str,
                    e,
                )
                continue

        logger.info("[REF] Prepared %d %s image parts", len(parts), label)
        return parts

    def _load_as_part(self, path_str: str) -> types.Part:
        """Load a single image file as a Gemini Part.

        Handles resizing, format conversion, and EXIF correction.
        """
        img = load_and_prepare_image(path_str, max_size=self._max_size)
        img_bytes, mime_type = image_to_bytes(img, format="PNG")

        return types.Part.from_bytes(data=img_bytes, mime_type=mime_type)

    def allocate_budget(
        self,
        mannequin_paths: list[str],
        product_paths: list[str],
        decor_paths: list[str],
    ) -> tuple[int, int, int]:
        """Allocate the 14-image budget across reference types.

        Priority: mannequin > product > decor (face consistency is paramount).

        Args:
            mannequin_paths: Mannequin reference paths.
            product_paths: Product reference paths.
            decor_paths: Decor reference paths.

        Returns:
            Tuple of (mannequin_limit, product_limit, decor_limit).
        """
        total_budget = MAX_IMAGES_PER_CALL
        remaining = total_budget

        # Mannequins get priority (up to 5)
        mannequin_limit = min(len(mannequin_paths), 5, remaining)
        remaining -= mannequin_limit

        # Products get second priority (up to 4)
        product_limit = min(len(product_paths), 4, remaining)
        remaining -= product_limit

        # Decor gets the rest
        decor_limit = min(len(decor_paths), remaining)

        logger.debug(
            "[REF] Image budget: mannequin=%d, product=%d, decor=%d (of %d)",
            mannequin_limit,
            product_limit,
            decor_limit,
            total_budget,
        )

        return mannequin_limit, product_limit, decor_limit
