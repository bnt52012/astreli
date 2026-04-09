"""
Image utilities — resize, format conversion, masking for fusion.
"""
from __future__ import annotations

import io
import logging
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

logger = logging.getLogger(__name__)


def load_image(path: str | Path) -> Image.Image:
    """Load image from path."""
    img = Image.open(str(path))
    img.load()
    return img


def resize_image(img: Image.Image, max_size: int = 1024) -> Image.Image:
    """Resize keeping aspect ratio, longest side = max_size."""
    w, h = img.size
    if max(w, h) <= max_size:
        return img
    ratio = max_size / max(w, h)
    new_w, new_h = int(w * ratio), int(h * ratio)
    return img.resize((new_w, new_h), Image.LANCZOS)


def image_to_bytes(img: Image.Image, fmt: str = "PNG") -> bytes:
    """Convert PIL Image to bytes."""
    buf = io.BytesIO()
    img.save(buf, format=fmt)
    return buf.getvalue()


def bytes_to_image(data: bytes) -> Image.Image:
    """Convert bytes to PIL Image."""
    return Image.open(io.BytesIO(data))


def image_to_base64(img: Image.Image, fmt: str = "PNG") -> str:
    """Convert PIL Image to base64 string."""
    import base64
    return base64.b64encode(image_to_bytes(img, fmt)).decode("utf-8")


def create_face_mask(
    image_size: tuple[int, int],
    face_center: tuple[int, int] | None = None,
    face_radius: int | None = None,
    feather_radius: int = 30,
) -> Image.Image:
    """Create a soft elliptical mask for face/head/neck area.

    If no face_center is given, assume center-top third of image
    (typical portrait framing).
    """
    w, h = image_size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)

    if face_center is None:
        cx = w // 2
        cy = h // 4  # Upper portion of image
    else:
        cx, cy = face_center

    if face_radius is None:
        face_radius = min(w, h) // 5

    # Draw ellipse for head + neck region
    head_w = int(face_radius * 1.3)
    head_h = int(face_radius * 1.8)  # Taller to include neck
    bbox = (cx - head_w, cy - face_radius, cx + head_w, cy + head_h)
    draw.ellipse(bbox, fill=255)

    # Gaussian blur for soft feathering
    mask = mask.filter(ImageFilter.GaussianBlur(radius=feather_radius))

    return mask


def create_body_mask(
    image_size: tuple[int, int],
    body_bbox: tuple[int, int, int, int] | None = None,
    feather_radius: int = 40,
) -> Image.Image:
    """Create a soft mask for the full body area."""
    w, h = image_size
    mask = Image.new("L", (w, h), 0)
    draw = ImageDraw.Draw(mask)

    if body_bbox is None:
        # Default: center 60% of image
        margin_x = int(w * 0.2)
        margin_top = int(h * 0.05)
        margin_bottom = int(h * 0.02)
        body_bbox = (margin_x, margin_top, w - margin_x, h - margin_bottom)

    draw.rectangle(body_bbox, fill=255)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=feather_radius))
    return mask


def composite_with_mask(
    background: Image.Image,
    foreground: Image.Image,
    mask: Image.Image,
) -> Image.Image:
    """Composite foreground onto background using mask.

    White in mask = foreground, Black = background.
    """
    bg = background.convert("RGBA")
    fg = foreground.convert("RGBA").resize(bg.size, Image.LANCZOS)
    m = mask.convert("L").resize(bg.size, Image.LANCZOS)
    result = Image.composite(fg, bg, m)
    return result.convert("RGB")


def detect_face_region(img: Image.Image) -> tuple[tuple[int, int], int] | None:
    """Try to detect face region using simple heuristics.

    Returns (center, radius) or None.
    For production, integrate with a face detection model.
    """
    # Simple heuristic: assume face is in upper-center third
    w, h = img.size
    center = (w // 2, h // 4)
    radius = min(w, h) // 5
    return center, radius


def validate_image(path: str | Path, min_resolution: int = 256) -> bool:
    """Validate image file exists and meets minimum resolution."""
    try:
        img = Image.open(str(path))
        w, h = img.size
        if min(w, h) < min_resolution:
            logger.warning("Image %s too small: %dx%d (min %d)", path, w, h, min_resolution)
            return False
        return True
    except Exception as e:
        logger.warning("Invalid image %s: %s", path, e)
        return False


def get_aspect_ratio_dimensions(aspect_ratio: str, base_size: int = 1024) -> tuple[int, int]:
    """Convert aspect ratio string to pixel dimensions."""
    ratios = {
        "16:9": (1024, 576),
        "9:16": (576, 1024),
        "1:1": (1024, 1024),
        "4:3": (1024, 768),
        "3:4": (768, 1024),
    }
    return ratios.get(aspect_ratio, (1024, 1024))
