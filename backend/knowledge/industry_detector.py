"""
Industry Detector — Auto-detect advertising industry from scenario text.

Analyzes the scenario + optional reference image metadata to classify
the campaign's industry. The client NEVER specifies this manually —
it's 100% automatic.

Supports hybrid campaigns (e.g., fashion + fragrance) by returning
a primary industry and confidence score, plus secondary matches.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


@dataclass
class IndustryMatch:
    """Result of industry detection."""
    industry: str
    confidence: float  # 0.0 - 1.0
    matched_keywords: list[str] = field(default_factory=list)


@dataclass
class DetectionResult:
    """Full detection result with primary and secondary industries."""
    primary: IndustryMatch
    secondary: list[IndustryMatch] = field(default_factory=list)
    is_hybrid: bool = False


# ── Keyword Dictionaries ─────────────────────────────────────

INDUSTRY_KEYWORDS: dict[str, list[str]] = {
    "luxury": [
        "luxury", "luxurious", "opulent", "premium", "exclusive", "prestige",
        "haute", "elite", "refined", "sophisticated", "bespoke", "artisan",
        "craftsmanship", "heritage", "maison", "atelier", "first class",
        "five star", "vip", "high end", "upscale", "sumptuous",
    ],
    "beauty": [
        "beauty", "makeup", "cosmetic", "skincare", "skin care", "lipstick",
        "foundation", "mascara", "eyeshadow", "blush", "concealer", "primer",
        "serum", "moisturizer", "cream", "lotion", "cleanser", "toner",
        "anti-aging", "anti aging", "wrinkle", "glow", "radiant", "luminous",
        "complexion", "pore", "hydrating", "nourishing", "derma", "collagen",
        "retinol", "vitamin c", "hyaluronic", "exfoliate", "spa", "facial",
    ],
    "fashion": [
        "fashion", "clothing", "dress", "suit", "outfit", "collection",
        "runway", "couture", "prêt-à-porter", "ready to wear", "designer",
        "wardrobe", "garment", "textile", "fabric", "silk", "cotton",
        "leather", "denim", "linen", "cashmere", "wool", "satin",
        "embroidery", "pattern", "print", "tailor", "hem", "seam",
        "accessory", "handbag", "purse", "scarf", "hat", "sunglasses",
        "shoes", "heels", "sneakers", "boots", "sandals", "belt",
        "streetwear", "athleisure", "vintage", "retro", "trend",
    ],
    "sport": [
        "sport", "athletic", "fitness", "training", "workout", "exercise",
        "running", "marathon", "sprint", "jogging", "gym", "crossfit",
        "yoga", "pilates", "cycling", "swimming", "tennis", "football",
        "basketball", "soccer", "golf", "skiing", "surfing", "hiking",
        "climbing", "muscle", "strength", "endurance", "performance",
        "competition", "champion", "medal", "trophy", "team", "athlete",
        "sneaker", "sportswear", "activewear", "sweat", "energy drink",
    ],
    "food_beverage": [
        "food", "beverage", "drink", "cocktail", "wine", "beer", "coffee",
        "tea", "juice", "smoothie", "restaurant", "chef", "cuisine",
        "recipe", "ingredient", "flavor", "taste", "delicious", "gourmet",
        "organic", "fresh", "farm", "harvest", "chocolate", "dessert",
        "cake", "pastry", "bread", "cheese", "fruit", "vegetable",
        "spice", "herb", "meat", "seafood", "sushi", "pizza", "burger",
        "cereal", "snack", "appetizer", "entree", "plating", "garnish",
    ],
    "automotive": [
        "car", "automobile", "vehicle", "driving", "road", "highway",
        "engine", "horsepower", "acceleration", "speed", "turbo",
        "sedan", "suv", "coupe", "convertible", "truck", "van",
        "electric", "hybrid", "ev", "charging", "battery", "range",
        "interior", "dashboard", "steering", "wheel", "tire", "brake",
        "aerodynamic", "chassis", "suspension", "transmission", "gear",
        "bmw", "mercedes", "audi", "porsche", "ferrari", "lamborghini",
        "tesla", "lexus", "jaguar", "bentley", "rolls royce", "maserati",
    ],
    "tech": [
        "technology", "tech", "digital", "software", "app", "smartphone",
        "phone", "tablet", "laptop", "computer", "device", "gadget",
        "ai", "artificial intelligence", "machine learning", "cloud",
        "data", "algorithm", "interface", "ux", "ui", "screen", "display",
        "processor", "chip", "innovation", "startup", "silicon", "code",
        "wireless", "bluetooth", "wifi", "5g", "iot", "wearable",
        "smartwatch", "earbuds", "headphones", "speaker", "camera",
    ],
    "travel": [
        "travel", "vacation", "holiday", "destination", "journey",
        "adventure", "explore", "discover", "wanderlust", "getaway",
        "hotel", "resort", "spa", "beach", "island", "mountain",
        "city", "capital", "landmark", "monument", "museum", "temple",
        "airline", "flight", "cruise", "yacht", "train", "safari",
        "backpack", "luggage", "suitcase", "passport", "visa",
        "mediterranean", "caribbean", "tropical", "exotic", "paradise",
    ],
    "real_estate": [
        "real estate", "property", "apartment", "house", "villa",
        "penthouse", "condo", "residence", "home", "living space",
        "bedroom", "kitchen", "bathroom", "living room", "garden",
        "terrace", "balcony", "pool", "swimming pool", "garage",
        "architecture", "interior design", "renovation", "building",
        "square meters", "square feet", "floor plan", "open plan",
        "neighborhood", "location", "view", "panoramic", "skyline",
    ],
    "jewelry_watches": [
        "jewelry", "jewellery", "watch", "watches", "timepiece",
        "diamond", "gold", "silver", "platinum", "gem", "gemstone",
        "ruby", "sapphire", "emerald", "pearl", "crystal", "stone",
        "ring", "necklace", "bracelet", "earring", "pendant", "brooch",
        "chain", "carat", "karat", "setting", "bezel", "clasp",
        "chronograph", "movement", "dial", "strap", "crown", "case",
        "mechanical", "automatic", "quartz", "swiss", "horology",
        "rolex", "cartier", "tiffany", "bulgari", "omega", "patek",
    ],
    "fragrance": [
        "fragrance", "perfume", "parfum", "cologne", "scent", "aroma",
        "olfactory", "nose", "top note", "heart note", "base note",
        "accord", "bouquet", "essence", "extract", "eau de toilette",
        "eau de parfum", "bottle", "flacon", "spray", "mist", "diffuser",
        "oud", "musk", "amber", "vanilla", "jasmine", "rose", "bergamot",
        "sandalwood", "vetiver", "patchouli", "citrus", "floral", "woody",
        "oriental", "fresh", "aquatic", "gourmand", "chypre", "fougere",
    ],
    "health": [
        "health", "wellness", "medical", "pharmaceutical", "supplement",
        "vitamin", "mineral", "probiotic", "protein", "nutrition",
        "diet", "weight loss", "detox", "immunity", "sleep", "stress",
        "mental health", "therapy", "meditation", "mindfulness",
        "hospital", "clinic", "doctor", "nurse", "patient", "care",
    ],
}

# Keywords that strongly indicate luxury overlay (boosts luxury traits in any industry)
LUXURY_BOOSTERS = {
    "exclusive", "premium", "haute", "bespoke", "artisan", "heritage",
    "maison", "atelier", "refined", "sophisticated", "opulent", "prestige",
}


class IndustryDetector:
    """Auto-detect advertising industry from scenario text and context."""

    def __init__(self) -> None:
        self._compiled_patterns: dict[str, list[re.Pattern]] = {}
        for industry, keywords in INDUSTRY_KEYWORDS.items():
            self._compiled_patterns[industry] = [
                re.compile(rf"\b{re.escape(kw)}\b", re.IGNORECASE)
                for kw in keywords
            ]

    def detect(
        self,
        scenario: str,
        brand_name: str | None = None,
        reference_image_labels: list[str] | None = None,
    ) -> DetectionResult:
        """Detect the advertising industry from scenario text.

        Args:
            scenario: The full client scenario text.
            brand_name: Optional brand name for context.
            reference_image_labels: Optional labels/descriptions of uploaded images.

        Returns:
            DetectionResult with primary industry and optional secondary matches.
        """
        # Combine all text sources
        text = scenario
        if brand_name:
            text += f" {brand_name}"
        if reference_image_labels:
            text += " " + " ".join(reference_image_labels)

        # Score each industry
        scores: dict[str, IndustryMatch] = {}
        for industry, patterns in self._compiled_patterns.items():
            matched = []
            for pattern in patterns:
                if pattern.search(text):
                    matched.append(pattern.pattern.strip("\\b"))
            if matched:
                # Confidence based on keyword density
                confidence = min(1.0, len(matched) / 5.0)
                scores[industry] = IndustryMatch(
                    industry=industry,
                    confidence=round(confidence, 2),
                    matched_keywords=matched,
                )

        if not scores:
            return DetectionResult(
                primary=IndustryMatch(industry="general", confidence=0.5),
            )

        # Sort by confidence
        ranked = sorted(scores.values(), key=lambda m: m.confidence, reverse=True)
        primary = ranked[0]

        # Check for hybrid campaign
        secondary = [m for m in ranked[1:] if m.confidence >= 0.3]
        is_hybrid = len(secondary) > 0 and secondary[0].confidence >= 0.5

        # Boost luxury overlay if luxury keywords found in non-luxury primary
        if primary.industry != "luxury":
            luxury_matches = sum(
                1 for word in LUXURY_BOOSTERS
                if re.search(rf"\b{word}\b", text, re.IGNORECASE)
            )
            if luxury_matches >= 2 and "luxury" not in [s.industry for s in secondary]:
                secondary.insert(0, IndustryMatch(
                    industry="luxury",
                    confidence=min(0.6, luxury_matches * 0.2),
                    matched_keywords=list(LUXURY_BOOSTERS & set(text.lower().split())),
                ))
                is_hybrid = True

        return DetectionResult(
            primary=primary,
            secondary=secondary,
            is_hybrid=is_hybrid,
        )

    def detect_simple(self, scenario: str) -> str:
        """Quick detection returning just the primary industry name."""
        result = self.detect(scenario)
        return result.primary.industry
