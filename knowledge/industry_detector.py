"""
Industry Detector — auto-detects industry from scenario text.

The client NEVER specifies their industry. Detection is 100% automatic
using keyword analysis and semantic patterns. Each industry has 50+
keywords for robust matching. Supports hybrid campaigns (e.g. luxury + auto).
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class IndustryMatch:
    industry: str
    confidence: float
    matched_keywords: list[str]


# ── 50+ keywords per industry ──────────────────────────────────────────

INDUSTRY_KEYWORDS: dict[str, list[str]] = {
    "luxury": [
        "luxury", "luxe", "premium", "exclusive", "haute", "maison",
        "prestige", "elegant", "opulent", "refined", "sophisticat",
        "heritage", "craftsmanship", "artisan", "bespoke", "couture",
        "gold", "silk", "cashmere", "marble", "crystal", "velvet",
        "champagne", "caviar", "suite", "penthouse", "yacht", "villa",
        "black tie", "gala", "red carpet", "vip", "concierge",
        "savoir-faire", "atelier", "haute couture", "limited edition",
        "rare", "exquisite", "sumptuous", "indulgent", "patrician",
        "haute joaillerie", "grand cru", "first class", "private jet",
        "chauffeured", "monogram", "iconic", "timeless", "legacy",
        "collection privee", "hand-finished", "noble", "palatial",
    ],
    "beauty": [
        "beauty", "skincare", "skin care", "makeup", "make-up", "cosmetic",
        "foundation", "lipstick", "mascara", "serum", "cream", "moisturiz",
        "glow", "radiant", "complexion", "concealer", "blush", "eyeshadow",
        "primer", "contour", "highlight", "face mask", "cleanser", "toner",
        "exfoliat", "anti-aging", "wrinkle", "pore", "hydrat", "collagen",
        "retinol", "vitamin c", "spf", "sunscreen", "dermatolog",
        "luminous", "flawless", "natural beauty", "bare skin",
        "lip gloss", "eyeliner", "brow", "lash", "nail polish",
        "bronzer", "setting spray", "bb cream", "cc cream", "micellar",
        "niacinamide", "hyaluronic", "peptide", "ceramide", "squalane",
        "skin barrier", "dewy", "matte finish", "satin finish",
    ],
    "fashion": [
        "fashion", "clothing", "dress", "outfit", "collection", "runway",
        "model", "catwalk", "designer", "trend", "style", "garment",
        "fabric", "textile", "silk", "cotton", "linen", "denim",
        "jacket", "coat", "blazer", "trouser", "skirt", "shirt", "blouse",
        "accessory", "handbag", "bag", "shoes", "heel", "sneaker", "boot",
        "sunglasses", "scarf", "belt", "hat", "wear", "wardrobe",
        "season", "spring collection", "summer collection", "fall winter",
        "ready-to-wear", "pret-a-porter", "streetwear", "athleisure",
        "capsule collection", "lookbook", "editorial", "photoshoot",
        "mannequin", "fitting", "tailored", "draping", "embroidery",
        "print", "pattern", "silhouette", "avant-garde", "minimalist",
    ],
    "sport": [
        "sport", "athletic", "fitness", "training", "workout", "gym",
        "running", "marathon", "sprint", "soccer", "football", "basketball",
        "tennis", "golf", "swimming", "cycling", "yoga", "crossfit",
        "performance", "endurance", "strength", "speed", "agility",
        "jersey", "sneaker", "cleats", "equipment", "gear",
        "champion", "victory", "competition", "athlete", "player",
        "stadium", "court", "field", "track", "outdoor", "adventure",
        "hiking", "climbing", "surfing", "extreme", "adrenaline",
        "muscle", "sweat", "power", "determination", "discipline",
        "recovery", "warm-up", "cool-down", "personal best", "record",
        "team", "match", "league", "medal", "podium", "trophy",
    ],
    "food_beverage": [
        "food", "beverage", "drink", "restaurant", "chef", "cuisine",
        "recipe", "ingredient", "flavor", "taste", "delicious", "gourmet",
        "organic", "fresh", "farm", "harvest", "seasonal",
        "wine", "beer", "cocktail", "coffee", "tea", "juice", "water",
        "chocolate", "cheese", "bread", "pastry", "dessert", "cake",
        "appetit", "dining", "meal", "brunch", "lunch", "dinner",
        "kitchen", "cooking", "baking", "grilling", "roasting",
        "soda", "soft drink", "energy drink", "smoothie", "spirit",
        "whiskey", "vodka", "rum", "tequila", "gin",
        "plating", "garnish", "umami", "savory", "sweet",
        "crispy", "creamy", "crunchy", "tender", "juicy",
        "artisanal", "locally sourced", "plant-based", "vegan",
    ],
    "automotive": [
        "car", "automotive", "vehicle", "automobile", "drive", "driving",
        "engine", "motor", "horsepower", "torque", "speed", "acceleration",
        "suv", "sedan", "coupe", "convertible", "truck", "electric vehicle",
        "hybrid", "ev", "tesla", "bmw", "mercedes", "audi", "porsche",
        "ferrari", "lamborghini", "range rover", "lexus",
        "road", "highway", "asphalt", "track", "circuit", "race",
        "dashboard", "interior", "leather seats", "steering wheel",
        "headlight", "grill", "wheel", "tire", "carbon fiber",
        "mph", "km/h", "0-60", "autonomous", "self-driving",
        "aerodynamic", "chassis", "suspension", "turbo", "supercharged",
        "alloy", "panoramic roof", "infotainment", "navigation",
        "fuel efficiency", "range", "charging station", "regenerative",
    ],
    "tech": [
        "tech", "technology", "digital", "smart", "device", "gadget",
        "smartphone", "phone", "laptop", "tablet", "computer", "screen",
        "display", "processor", "chip", "ai", "artificial intelligence",
        "app", "software", "platform", "cloud", "data", "algorithm",
        "innovation", "future", "next-gen", "wireless", "bluetooth",
        "5g", "iot", "wearable", "smartwatch", "earbuds", "headphones",
        "camera", "sensor", "battery", "charging", "usb", "hdmi",
        "pixel", "resolution", "oled", "amoled", "retina",
        "startup", "silicon valley", "code", "programming",
        "machine learning", "neural network", "robot", "automation",
        "cybersecurity", "encryption", "biometric", "face id",
        "augmented reality", "virtual reality", "metaverse", "blockchain",
    ],
    "travel": [
        "travel", "destination", "vacation", "holiday", "getaway",
        "resort", "hotel", "beach", "island", "mountain", "city",
        "explore", "discover", "adventure", "journey", "trip",
        "flight", "airline", "airport", "cruise", "sail",
        "luggage", "passport", "booking", "reservation",
        "tropical", "paradise", "exotic", "scenic", "panoramic",
        "sunset", "sunrise", "ocean", "sea", "lake", "river",
        "forest", "jungle", "desert", "savanna", "glacier",
        "culture", "heritage", "landmark", "monument", "temple",
        "backpack", "excursion", "tour", "guide", "itinerary",
        "boutique hotel", "spa", "wellness", "retreat", "sanctuary",
        "first class", "business class", "lounge", "concierge",
        "wanderlust", "nomad", "off the beaten path", "hidden gem",
    ],
    "real_estate": [
        "real estate", "property", "home", "house", "apartment", "condo",
        "penthouse", "villa", "mansion", "residence", "living space",
        "interior", "architecture", "design", "renovation", "modern",
        "kitchen", "bathroom", "bedroom", "living room", "garden",
        "terrace", "balcony", "pool", "swimming pool", "garage",
        "square feet", "square meters", "floor plan", "blueprint",
        "neighborhood", "location", "view", "skyline", "waterfront",
        "investment", "mortgage", "lease", "rental", "for sale",
        "open house", "showing", "listing", "broker", "agent",
        "hardwood floors", "marble countertop", "stainless steel",
        "walk-in closet", "en-suite", "loft", "duplex", "townhouse",
        "curb appeal", "landscaping", "smart home", "home automation",
    ],
    "jewelry_watches": [
        "jewelry", "jewellery", "watch", "watches", "timepiece",
        "diamond", "gold", "silver", "platinum", "gemstone",
        "ring", "necklace", "bracelet", "earring", "pendant",
        "carat", "karat", "brilliant", "cut", "clarity",
        "ruby", "emerald", "sapphire", "pearl", "opal",
        "chronograph", "automatic", "mechanical", "quartz",
        "swiss", "horology", "complication", "tourbillon",
        "dial", "bezel", "crown", "strap",
        "rolex", "cartier", "tiffany", "bulgari", "omega",
        "precious", "heirloom", "handcraft", "engraving",
        "pavé", "solitaire", "eternity band", "tennis bracelet",
        "rose gold", "white gold", "yellow gold", "rhodium",
        "caliber", "movement", "winding", "power reserve",
        "water resistant", "luminous dial", "skeleton", "perpetual",
    ],
    "fragrance": [
        "fragrance", "perfume", "parfum", "scent", "aroma",
        "eau de", "cologne", "toilette", "essence", "elixir",
        "note", "top note", "heart note", "base note", "accord",
        "floral", "woody", "oriental", "citrus", "musk",
        "amber", "vanilla", "jasmine", "rose", "sandalwood",
        "oud", "bergamot", "patchouli", "vetiver", "cedar",
        "bottle", "flacon", "spray", "atomizer", "vaporize",
        "olfactory", "sillage", "longevity", "projection",
        "nose", "perfumer", "creation", "composition", "blend",
        "fresh", "aquatic", "gourmand", "spicy", "leather",
        "iris", "tuberose", "neroli", "ylang", "tonka",
        "incense", "myrrh", "labdanum", "ambroxan", "iso e super",
        "wrist", "pulse point", "vanity", "applies", "spritz",
        "dab", "mist", "trail", "dry down", "skin chemistry",
    ],
}


class IndustryDetector:
    """Auto-detects the industry from scenario text."""

    def detect(self, scenario: str) -> IndustryMatch:
        """Analyze scenario text and return the best industry match.

        Args:
            scenario: The client's scenario text.

        Returns:
            IndustryMatch with industry name, confidence, and matched keywords.
        """
        text = scenario.lower()
        scores: dict[str, tuple[float, list[str]]] = {}

        for industry, keywords in INDUSTRY_KEYWORDS.items():
            matched = []
            for kw in keywords:
                # Use word boundary matching for short words
                if len(kw) <= 3:
                    pattern = r"\b" + re.escape(kw) + r"\b"
                    if re.search(pattern, text):
                        matched.append(kw)
                else:
                    if kw in text:
                        matched.append(kw)

            if matched:
                # Score: number of unique matches, weighted by specificity
                score = len(matched) / len(keywords)
                scores[industry] = (score, matched)

        if not scores:
            logger.info("No industry detected, defaulting to luxury.")
            return IndustryMatch(industry="luxury", confidence=0.3, matched_keywords=[])

        # Sort by score
        best = max(scores.items(), key=lambda x: x[1][0])
        industry = best[0]
        confidence = min(1.0, best[1][0] * 5)  # Scale up, cap at 1.0
        matched = best[1][1]

        logger.info(
            "Detected industry: %s (confidence: %.2f, keywords: %s)",
            industry, confidence, matched[:5],
        )
        return IndustryMatch(
            industry=industry,
            confidence=confidence,
            matched_keywords=matched,
        )

    def detect_hybrid(self, scenario: str) -> list[IndustryMatch]:
        """Detect multiple industries for hybrid campaigns.

        Returns top 2 matches if both have reasonable confidence.
        """
        text = scenario.lower()
        results: list[IndustryMatch] = []

        for industry, keywords in INDUSTRY_KEYWORDS.items():
            matched = []
            for kw in keywords:
                if len(kw) <= 3:
                    pattern = r"\b" + re.escape(kw) + r"\b"
                    if re.search(pattern, text):
                        matched.append(kw)
                else:
                    if kw in text:
                        matched.append(kw)
            if matched:
                score = min(1.0, len(matched) / len(keywords) * 5)
                results.append(IndustryMatch(
                    industry=industry,
                    confidence=score,
                    matched_keywords=matched,
                ))

        results.sort(key=lambda x: x.confidence, reverse=True)
        # Return top 2 if second has > 0.3 confidence
        if len(results) >= 2 and results[1].confidence > 0.3:
            return results[:2]
        return results[:1] if results else [IndustryMatch("luxury", 0.3, [])]
