"""
Reference image manager — validate, resize, prepare for API calls.
"""
from __future__ import annotations

import logging
from pathlib import Path

from PIL import Image

from utils.image_utils import load_image, resize_image, validate_image

logger = logging.getLogger(__name__)


class ReferenceManager:
    """Manages reference images (product, decor, mannequin)."""

    def __init__(self, max_size: int = 768) -> None:
        self.max_size = max_size

    def prepare_references(
        self,
        product_photos: list[str] | None = None,
        decor_photos: list[str] | None = None,
    ) -> list[Image.Image]:
        """Load, validate, and resize reference images.

        Returns:
            List of PIL Image objects ready for API calls.
        """
        images: list[Image.Image] = []

        for photos, label in [
            (product_photos, "product"),
            (decor_photos, "decor"),
        ]:
            if not photos:
                continue
            for path_str in photos:
                path = Path(path_str)
                if not path.exists():
                    logger.warning("Reference %s not found: %s", label, path)
                    continue
                if not validate_image(path):
                    logger.warning("Invalid reference %s: %s", label, path)
                    continue
                try:
                    img = load_image(path)
                    img = resize_image(img, self.max_size)
                    images.append(img)
                    logger.debug("Loaded %s reference: %s", label, path)
                except Exception as e:
                    logger.warning("Failed to load %s reference %s: %s", label, path, e)

        logger.info("Prepared %d reference images.", len(images))
        return images

    def validate_mannequin_photos(
        self, paths: list[str], min_count: int = 5
    ) -> list[str]:
        """Validate mannequin training photos.

        Args:
            paths: List of image paths.
            min_count: Minimum number of valid photos required.

        Returns:
            List of valid paths.

        Raises:
            ValueError if not enough valid photos.
        """
        valid = []
        for p in paths:
            if validate_image(p, min_resolution=512):
                valid.append(p)
            else:
                logger.warning("Mannequin photo invalid: %s", p)

        if len(valid) < min_count:
            raise ValueError(
                f"Need at least {min_count} valid mannequin photos, got {len(valid)}"
            )

        return valid
