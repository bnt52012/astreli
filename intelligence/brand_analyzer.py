"""
Brand Analyzer — extracts brand visual identity from assets.

Automatic — the client doesn't configure this. Analysis of logo colors,
reference image styles, and brand name context generates a brand style
prefix prepended to every prompt.
"""
from __future__ import annotations

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class BrandAnalyzer:
    """Extracts brand visual identity and generates style prefix."""

    def analyze(
        self,
        logo_path: str | None = None,
        reference_images: list[str] | None = None,
        brand_name: str | None = None,
    ) -> str:
        """Analyze brand assets and return a style prefix.

        Args:
            logo_path: Path to brand logo.
            reference_images: Product/decor reference image paths.
            brand_name: Brand name for context.

        Returns:
            Brand style prefix string to prepend to prompts.
        """
        parts: list[str] = []

        # Extract colors from logo
        if logo_path and Path(logo_path).exists():
            colors = self._extract_logo_colors(logo_path)
            if colors:
                color_str = ", ".join(colors[:4])
                parts.append(f"brand color palette: {color_str}")

        # Analyze reference images for style
        if reference_images:
            style = self._analyze_reference_style(reference_images)
            if style:
                parts.append(style)

        # Brand name context
        if brand_name:
            # Known luxury brands get specific style hints
            brand_lower = brand_name.lower()
            brand_style = self._get_known_brand_style(brand_lower)
            if brand_style:
                parts.append(brand_style)
            else:
                parts.append(f"{brand_name} brand campaign")

        if not parts:
            return ""

        prefix = f"[Brand identity: {', '.join(parts)}]"
        logger.info("Brand prefix: %s", prefix[:100])
        return prefix

    def _extract_logo_colors(self, logo_path: str) -> list[str]:
        """Extract dominant colors from brand logo."""
        try:
            from PIL import Image
            from collections import Counter

            img = Image.open(logo_path).convert("RGB")
            img_small = img.resize((50, 50))
            pixels = list(img_small.getdata())

            # Filter out white, black, and near-transparent
            meaningful = [
                p for p in pixels
                if not (p[0] > 240 and p[1] > 240 and p[2] > 240)  # not white
                and not (p[0] < 15 and p[1] < 15 and p[2] < 15)  # not black
            ]

            if not meaningful:
                return []

            # Quantize to reduce color space
            quantized = [
                (r // 32 * 32, g // 32 * 32, b // 32 * 32)
                for r, g, b in meaningful
            ]
            counter = Counter(quantized)
            top_colors = counter.most_common(5)

            # Convert to descriptive names
            descriptions = []
            for (r, g, b), _ in top_colors:
                desc = self._rgb_to_name(r, g, b)
                if desc and desc not in descriptions:
                    descriptions.append(desc)

            return descriptions[:4]

        except Exception as e:
            logger.warning("Logo color extraction failed: %s", e)
            return []

    def _rgb_to_name(self, r: int, g: int, b: int) -> str:
        """Convert RGB to approximate color name."""
        if r > 180 and g < 80 and b < 80:
            return "rich red"
        if r > 180 and g > 140 and b < 80:
            return "warm gold"
        if r < 80 and g < 80 and b > 180:
            return "deep blue"
        if r < 80 and g > 150 and b < 80:
            return "emerald green"
        if r > 150 and g < 80 and b > 150:
            return "royal purple"
        if r > 200 and g > 150 and b > 150 and r > g:
            return "soft rose"
        if r > 160 and g > 120 and b < 100:
            return "warm bronze"
        if abs(r - g) < 30 and abs(g - b) < 30:
            if r > 150:
                return "silver grey"
            return "charcoal"
        if r < 100 and g > 100 and b > 120:
            return "teal"
        return ""

    def _analyze_reference_style(self, image_paths: list[str]) -> str:
        """Analyze reference images for overall visual style."""
        try:
            from PIL import Image
            import statistics

            brightnesses = []
            saturations = []

            for path_str in image_paths[:5]:
                path = Path(path_str)
                if not path.exists():
                    continue
                img = Image.open(path).convert("RGB").resize((100, 100))
                pixels = list(img.getdata())

                # Average brightness
                avg_brightness = sum(sum(p) / 3 for p in pixels) / len(pixels)
                brightnesses.append(avg_brightness)

                # Rough saturation estimate
                sat = sum(
                    max(p) - min(p) for p in pixels
                ) / len(pixels)
                saturations.append(sat)

            if not brightnesses:
                return ""

            avg_bright = statistics.mean(brightnesses)
            avg_sat = statistics.mean(saturations)

            style_parts = []
            if avg_bright > 170:
                style_parts.append("high-key bright aesthetic")
            elif avg_bright < 85:
                style_parts.append("low-key dark moody aesthetic")
            else:
                style_parts.append("balanced mid-tone aesthetic")

            if avg_sat > 100:
                style_parts.append("vibrant saturated colors")
            elif avg_sat < 40:
                style_parts.append("desaturated muted tones")

            return ", ".join(style_parts)

        except Exception as e:
            logger.warning("Reference style analysis failed: %s", e)
            return ""

    def _get_known_brand_style(self, brand: str) -> str:
        """Return style hints for well-known brands."""
        known = {
            "chanel": "Chanel minimalist elegance, black and white with gold accents, timeless Parisian chic",
            "dior": "Dior haute couture opulence, romantic femininity, garden of dreams aesthetic",
            "louis vuitton": "Louis Vuitton travel spirit, monogram heritage, bold modern luxury",
            "gucci": "Gucci maximalist eclectic, rich colors, renaissance meets street culture",
            "hermes": "Hermes artisanal luxury, equestrian heritage, warm earth tones, orange accent",
            "prada": "Prada intellectual luxury, minimal architectural, avant-garde sophistication",
            "nike": "Nike dynamic performance, bold contrast, inspirational athletic energy",
            "adidas": "Adidas clean sporty lines, trefoil heritage, street-to-sport crossover",
            "apple": "Apple clean minimalism, white space, precision product photography",
            "rolex": "Rolex timeless prestige, deep greens, precision craftsmanship detail",
            "cartier": "Cartier romantic luxury, red and gold, jewelry light play, panthère motif",
            "tiffany": "Tiffany blue elegance, romantic sparkle, clean sophisticated presentation",
        }
        for key, style in known.items():
            if key in brand:
                return style
        return ""
