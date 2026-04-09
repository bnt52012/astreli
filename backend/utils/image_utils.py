"""
Image utility functions for the AdGenAI pipeline.

Handles image loading, resizing for API limits, format validation,
EXIF orientation correction, and reference image preparation.
"""

from __future__ import annotations

import hashlib
import io
import logging
from pathlib import Path

from PIL import Image, ExifTags, ImageOps

logger = logging.getLogger(__name__)

# Gemini API limits
MAX_GEMINI_IMAGE_SIZE_PX = 2048
SUPPORTED_IMAGE_FORMATS = {"JPEG", "PNG", "WEBP", "BMP", "TIFF"}
MAX_IMAGE_FILE_SIZE_MB = 20


def load_and_prepare_image(
    path: str | Path,
    max_size: int = MAX_GEMINI_IMAGE_SIZE_PX,
    target_format: str = "PNG",
) -> Image.Image:
    """Load an image, fix orientation, and resize if too large.

    Args:
        path: Path to the image file.
        max_size: Maximum dimension (width or height) in pixels.
        target_format: Target format for conversion if needed.

    Returns:
        PIL Image object ready for API consumption.

    Raises:
        ValueError: If the image format is not supported.
        FileNotFoundError: If the image file doesn't exist.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {path}")

    img = Image.open(path)

    # Fix EXIF orientation (common with phone photos)
    img = ImageOps.exif_transpose(img)

    # Validate format
    if img.format and img.format.upper() not in SUPPORTED_IMAGE_FORMATS:
        logger.warning(
            "[IMAGE] Unsupported format %s for %s, converting to %s",
            img.format,
            path.name,
            target_format,
        )

    # Convert to RGB if needed (handles RGBA, CMYK, etc.)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGB")

    # Resize if exceeding max dimensions
    width, height = img.size
    if width > max_size or height > max_size:
        ratio = min(max_size / width, max_size / height)
        new_size = (int(width * ratio), int(height * ratio))
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        logger.info(
            "[IMAGE] Resized %s from %dx%d to %dx%d",
            path.name,
            width,
            height,
            new_size[0],
            new_size[1],
        )

    return img


def image_to_bytes(
    img: Image.Image,
    format: str = "PNG",
    quality: int = 95,
) -> tuple[bytes, str]:
    """Convert a PIL Image to bytes with the specified format.

    Args:
        img: PIL Image object.
        format: Output format (PNG, JPEG, WEBP).
        quality: JPEG/WebP quality (1-100).

    Returns:
        Tuple of (image bytes, MIME type).
    """
    buffer = io.BytesIO()

    if format.upper() == "JPEG" and img.mode == "RGBA":
        img = img.convert("RGB")

    img.save(buffer, format=format.upper(), quality=quality)
    buffer.seek(0)

    mime_map = {"PNG": "image/png", "JPEG": "image/jpeg", "WEBP": "image/webp"}
    mime = mime_map.get(format.upper(), "image/png")

    return buffer.getvalue(), mime


def compute_image_hash(path: str | Path) -> str:
    """Compute a SHA-256 hash of an image file for caching.

    Args:
        path: Path to the image file.

    Returns:
        Hex string of the SHA-256 hash.
    """
    hasher = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def validate_image_dimensions(
    path: str | Path,
    min_width: int = 64,
    min_height: int = 64,
    max_width: int = 8192,
    max_height: int = 8192,
) -> tuple[int, int]:
    """Validate image dimensions are within acceptable range.

    Args:
        path: Path to the image file.
        min_width: Minimum acceptable width.
        min_height: Minimum acceptable height.
        max_width: Maximum acceptable width.
        max_height: Maximum acceptable height.

    Returns:
        Tuple of (width, height).

    Raises:
        ValueError: If dimensions are outside acceptable range.
    """
    img = Image.open(path)
    width, height = img.size

    if width < min_width or height < min_height:
        raise ValueError(
            f"Image too small: {width}x{height} (minimum: {min_width}x{min_height})"
        )
    if width > max_width or height > max_height:
        raise ValueError(
            f"Image too large: {width}x{height} (maximum: {max_width}x{max_height})"
        )

    return width, height


def prepare_reference_batch(
    image_paths: list[str],
    max_images: int = 14,
    max_size: int = MAX_GEMINI_IMAGE_SIZE_PX,
) -> list[Image.Image]:
    """Prepare a batch of reference images for a Gemini API call.

    Loads, validates, resizes, and limits the number of images
    to stay within API constraints.

    Args:
        image_paths: List of file paths to reference images.
        max_images: Maximum number of images per API call (Gemini limit: 14).
        max_size: Maximum pixel dimension per image.

    Returns:
        List of prepared PIL Image objects.
    """
    if not image_paths:
        return []

    if len(image_paths) > max_images:
        logger.warning(
            "[IMAGE] Too many reference images (%d), limiting to %d",
            len(image_paths),
            max_images,
        )
        image_paths = image_paths[:max_images]

    prepared: list[Image.Image] = []
    for path in image_paths:
        try:
            img = load_and_prepare_image(path, max_size=max_size)
            prepared.append(img)
        except Exception as e:
            logger.warning("[IMAGE] Failed to load reference image %s: %s", path, e)
            continue

    logger.info("[IMAGE] Prepared %d reference images", len(prepared))
    return prepared


def extract_dominant_colors(
    path: str | Path,
    num_colors: int = 5,
) -> list[tuple[int, int, int]]:
    """Extract dominant colors from an image using quantization.

    Used by the brand analyzer to extract brand colors from logo/assets.

    Args:
        path: Path to the image file.
        num_colors: Number of dominant colors to extract.

    Returns:
        List of (R, G, B) tuples sorted by frequency.
    """
    img = Image.open(path)
    img = img.convert("RGB")

    # Resize to speed up quantization
    img = img.resize((150, 150), Image.Resampling.LANCZOS)

    # Quantize to reduce color space
    quantized = img.quantize(colors=num_colors, method=Image.Quantize.MEDIANCUT)
    palette = quantized.getpalette()

    if not palette:
        return []

    # Extract RGB triplets from palette
    colors: list[tuple[int, int, int]] = []
    for i in range(num_colors):
        idx = i * 3
        if idx + 2 < len(palette):
            colors.append((palette[idx], palette[idx + 1], palette[idx + 2]))

    return colors


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    """Convert RGB tuple to hex color string."""
    return f"#{rgb[0]:02x}{rgb[1]:02x}{rgb[2]:02x}"
