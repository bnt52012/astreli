"""
Brand Visual Identity Analyzer.

Extracts brand visual DNA from uploaded assets (logo, reference images)
and generates a consistent style prefix that gets prepended to EVERY
image prompt. This ensures all scenes feel like the same campaign.

The client doesn't configure any of this - it's automatic from their
uploaded assets. They upload their logo and references, and every
generated image inherits their brand's visual language.
"""

from __future__ import annotations

import logging
from pathlib import Path

from backend.utils.image_utils import extract_dominant_colors, rgb_to_hex

logger = logging.getLogger(__name__)


class BrandAnalyzer:
    """Analyzes brand assets to extract visual identity for prompt consistency.

    Workflow:
    1. Extract dominant colors from logo
    2. Analyze reference images for common visual patterns
    3. Generate a brand style prefix string
    4. This prefix is prepended to EVERY image generation prompt
    """

    def __init__(self) -> None:
        self._brand_colors: list[str] = []
        self._brand_style_prefix: str = ""

    @property
    def brand_style_prefix(self) -> str:
        """The computed brand style prefix for prompt prepending."""
        return self._brand_style_prefix

    @property
    def brand_colors(self) -> list[str]:
        """Extracted brand colors as hex strings."""
        return self._brand_colors

    def analyze(
        self,
        logo_path: str | None = None,
        reference_images: list[str] | None = None,
        brand_name: str | None = None,
        brand_colors_override: list[str] | None = None,
        brand_tone: str | None = None,
    ) -> str:
        """Analyze brand assets and generate the style prefix.

        Args:
            logo_path: Path to the brand logo image.
            reference_images: Paths to brand reference/mood images.
            brand_name: Brand name for context.
            brand_colors_override: Client-specified hex colors (overrides extraction).
            brand_tone: Client-specified brand tone (e.g., "luxurious and modern").

        Returns:
            Brand style prefix string to prepend to all image prompts.
        """
        prefix_parts: list[str] = []

        # 1. Extract colors from logo
        if brand_colors_override:
            self._brand_colors = brand_colors_override
            logger.info("[BRAND] Using client-specified colors: %s", brand_colors_override)
        elif logo_path and Path(logo_path).exists():
            try:
                rgb_colors = extract_dominant_colors(logo_path, num_colors=4)
                self._brand_colors = [rgb_to_hex(c) for c in rgb_colors]
                logger.info("[BRAND] Extracted logo colors: %s", self._brand_colors)
            except Exception as e:
                logger.warning("[BRAND] Failed to extract logo colors: %s", e)

        # 2. Build color palette instruction
        if self._brand_colors:
            color_str = ", ".join(self._brand_colors[:4])
            prefix_parts.append(
                f"brand color palette: {color_str}, "
                f"subtly incorporate these colors in the scene's accent elements and lighting"
            )

        # 3. Analyze reference images for visual style
        if reference_images:
            valid_refs = [p for p in reference_images if Path(p).exists()]
            if valid_refs:
                style_hints = self._analyze_reference_style(valid_refs)
                if style_hints:
                    prefix_parts.append(style_hints)

        # 4. Brand tone instruction
        if brand_tone:
            prefix_parts.append(f"brand aesthetic: {brand_tone}")

        # 5. Brand name context
        if brand_name:
            prefix_parts.append(f"advertising campaign for {brand_name}")

        # 6. Consistency instruction
        if prefix_parts:
            prefix_parts.append(
                "maintain visual consistency across all scenes in this campaign"
            )

        self._brand_style_prefix = ", ".join(prefix_parts)

        logger.info(
            "[BRAND] Style prefix generated (%d chars): %s...",
            len(self._brand_style_prefix),
            self._brand_style_prefix[:100] if self._brand_style_prefix else "(empty)",
        )

        return self._brand_style_prefix

    def _analyze_reference_style(self, image_paths: list[str]) -> str:
        """Analyze reference images for common visual style patterns.

        Uses color analysis to determine the overall mood/palette of
        the brand's visual language from their existing assets.

        Args:
            image_paths: Validated paths to reference images.

        Returns:
            Style description string.
        """
        all_colors: list[tuple[int, int, int]] = []

        for path in image_paths[:6]:  # Limit analysis scope
            try:
                colors = extract_dominant_colors(path, num_colors=3)
                all_colors.extend(colors)
            except Exception as e:
                logger.debug("[BRAND] Could not analyze %s: %s", path, e)

        if not all_colors:
            return ""

        # Determine if the palette is warm, cool, or neutral
        warmth_scores = []
        for r, g, b in all_colors:
            # Simple warmth heuristic: red/yellow vs blue
            warmth = (r + g * 0.5) - (b * 1.5)
            warmth_scores.append(warmth)

        avg_warmth = sum(warmth_scores) / len(warmth_scores)

        # Determine brightness
        avg_brightness = sum(
            (r + g + b) / 3 for r, g, b in all_colors
        ) / len(all_colors)

        # Determine saturation (simplified)
        avg_saturation = sum(
            max(r, g, b) - min(r, g, b)
            for r, g, b in all_colors
        ) / len(all_colors)

        style_parts: list[str] = []

        if avg_warmth > 50:
            style_parts.append("warm color temperature")
        elif avg_warmth < -50:
            style_parts.append("cool color temperature")
        else:
            style_parts.append("neutral balanced color temperature")

        if avg_brightness > 170:
            style_parts.append("high-key bright aesthetic")
        elif avg_brightness < 85:
            style_parts.append("low-key moody aesthetic")

        if avg_saturation > 100:
            style_parts.append("vibrant saturated colors")
        elif avg_saturation < 40:
            style_parts.append("muted desaturated palette")

        return f"reference style: {', '.join(style_parts)}"
