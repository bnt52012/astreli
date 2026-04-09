"""
Generate 500 detailed visual identity profiles for real premium/luxury brands
using GPT-4o-mini via direct OpenAI API calls.

Saves each profile as individual JSON in dataset/brand_profiles/{industry}/

Usage:
    python3 generate_brand_profiles.py --run
    python3 generate_brand_profiles.py --status
"""

import os
import json
import time
import argparse
import concurrent.futures
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

BASE_DIR = Path("dataset/brand_profiles")
PROGRESS_FILE = BASE_DIR / "_progress.json"
BASE_DIR.mkdir(parents=True, exist_ok=True)

MAX_RETRIES = 3

# =====================================================================
# 500 BRANDS — 12 INDUSTRIES
# =====================================================================

BRAND_LIST = {
    "luxury_fashion": [
        "Chanel", "Hermes", "Louis Vuitton", "Dior", "Gucci",
        "Prada", "Valentino", "Balenciaga", "Bottega Veneta", "Saint Laurent",
        "Givenchy", "Fendi", "Loewe", "Celine", "Burberry",
        "Versace", "Alexander McQueen", "Tom Ford", "Dolce & Gabbana", "Balmain",
        "Loro Piana", "Brunello Cucinelli", "Zegna", "Moncler", "Max Mara",
        "Ferragamo", "Etro", "Missoni", "Lanvin", "Chloe",
        "Stella McCartney", "Rick Owens", "Maison Margiela", "Ann Demeulemeester",
        "Dries Van Noten", "Oscar de la Renta", "Carolina Herrera", "Elie Saab",
        "Marchesa", "Proenza Schouler", "Thom Browne", "Jil Sander",
        "Vivienne Westwood", "Jean Paul Gaultier", "Kenzo", "Mugler",
        "Schiaparelli", "Alaia", "The Row", "Sacai",
        "Berluti", "Issey Miyake", "Comme des Garcons", "Off-White",
        "Amiri", "Palm Angels", "Fear of God", "Courrges",
        "Rabanne", "Peter Do", "Ulla Johnson", "Simone Rocha",
        "Erdem", "Zimmermann", "Temperley London",
    ],
    "accessible_luxury": [
        "Sandro", "Maje", "COS", "Massimo Dutti", "Reiss",
        "AllSaints", "Theory", "Zadig & Voltaire", "Isabel Marant", "Acne Studios",
        "A.P.C.", "Ganni", "Jacquemus", "Nanushka", "Toteme",
        "AMI Paris", "Anine Bing", "Sezane", "ba&sh", "IRO",
        "Equipment", "Vince", "Club Monaco", "Rag & Bone", "Citizens of Humanity",
        "Sandro Homme", "The Kooples", "Claudie Pierlot", "Madewell", "J.Crew Collection",
    ],
    "beauty": [
        "Chanel Beauty", "Dior Beauty", "La Mer", "SK-II", "Estee Lauder",
        "La Prairie", "Sisley Paris", "Guerlain", "Tom Ford Beauty", "Charlotte Tilbury",
        "Pat McGrath Labs", "NARS", "MAC Cosmetics", "Bobbi Brown", "Laura Mercier",
        "Hourglass", "Byredo Makeup", "Augustinus Bader", "Tatcha", "Drunk Elephant",
        "Glossier", "Fenty Beauty", "Rare Beauty", "Lancome", "YSL Beauty",
        "Armani Beauty", "Cle de Peau", "Sulwhasoo", "Natura Bisse", "111Skin",
        "iS Clinical", "SkinCeuticals", "Dr. Barbara Sturm", "Oribe", "Kerastase",
        "Aesop Skincare", "Vintner's Daughter", "Sunday Riley", "Kiehl's", "Fresh",
        "Chantecaille", "Sisley Hair", "La Roche-Posay", "Dermalogica", "Omorovicza",
        "Eve Lom", "REN Clean Skincare", "Tata Harper", "Supergoop", "Merit Beauty",
        "Saie", "Tower 28", "Kosas", "Rose Inc", "Westman Atelier",
    ],
    "fragrance": [
        "Chanel Fragrance", "Dior Parfums", "Tom Ford Private Blend", "Le Labo",
        "Byredo", "Maison Francis Kurkdjian", "Jo Malone", "Acqua di Parma",
        "Diptyque", "Creed", "Penhaligon's", "Frederic Malle", "Amouage",
        "Initio Parfums", "Parfums de Marly", "Xerjoff", "Memo Paris",
        "Maison Margiela Replica", "Aesop Fragrance", "Serge Lutens",
        "Clive Christian", "Roja Parfums", "Tiziana Terenzi", "Nishane",
        "Vilhelm Parfumerie", "DS & Durga", "Escentric Molecules", "Juliette Has a Gun",
        "Clean Reserve", "Malin+Goetz", "Boy Smells", "Carriere Freres",
        "Cire Trudon", "Santa Maria Novella", "Floris London",
        "Atelier Cologne", "Kilian Paris", "Hermetica", "Goldfield & Banks",
        "Mancera", "Montale", "Ormonde Jayne", "Laboratorio Olfattivo",
        "Miller Harris", "Heeley",
    ],
    "jewelry_watches": [
        "Cartier", "Rolex", "Patek Philippe", "Tiffany & Co.", "Bulgari",
        "Van Cleef & Arpels", "Chopard", "Harry Winston", "Graff", "Piaget",
        "Audemars Piguet", "Omega", "Jaeger-LeCoultre", "Vacheron Constantin",
        "IWC Schaffhausen", "Breitling", "TAG Heuer", "Hublot", "Boucheron",
        "Chaumet", "Messika", "Pomellato", "Buccellati", "David Yurman",
        "Mikimoto", "De Beers", "Breguet", "A. Lange & Sohne", "Panerai",
        "Zenith", "Tudor", "Grand Seiko", "Richard Mille", "Girard-Perregaux",
        "Blancpain", "Bell & Ross", "Longines", "Chanel Watches", "Hermes Watches",
        "Fred", "Dior Joaillerie", "Repossi", "Tasaki", "Tiffany High Jewelry",
        "Roberto Coin", "Marco Bicego", "Temple St. Clair", "Verdura", "Boghossian",
        "Moussaieff",
    ],
    "automotive": [
        "Rolls-Royce", "Bentley", "Ferrari", "Lamborghini", "Porsche",
        "Mercedes-Benz", "BMW", "Audi", "Aston Martin", "Maserati",
        "McLaren", "Bugatti", "Pagani", "Range Rover", "Lexus",
        "Genesis", "Volvo", "Tesla", "Lucid Motors", "Rivian",
        "Polestar", "Jaguar", "Alfa Romeo", "Lotus", "Cadillac",
        "Lincoln", "Infiniti", "Acura", "Mercedes-AMG", "BMW M",
        "Koenigsegg", "Rimac", "Pininfarina", "De Tomaso", "Hispano Suiza",
        "Alpine", "Cupra", "Lancia", "DS Automobiles", "Maybach",
    ],
    "sport": [
        "Nike", "Adidas", "Lululemon", "On Running", "Arc'teryx",
        "Rapha", "Tracksmith", "Satisfy Running", "Vuori", "Alo Yoga",
        "Hoka", "Salomon", "New Balance", "Asics", "The North Face",
        "Patagonia", "Canada Goose", "Rhone", "Ten Thousand", "Gymshark",
        "Allbirds", "Under Armour", "Puma", "Reebok", "Brooks Running",
        "Outdoor Voices", "Sweaty Betty", "NOBULL", "Sorel", "Columbia Sportswear",
        "Fila Premium", "Mizuno", "Descente", "Bogner", "Kjus",
    ],
    "food_beverage": [
        "Dom Perignon", "Moet & Chandon", "Veuve Clicquot", "Nespresso", "Krug",
        "Ruinart", "Hennessy", "Macallan", "Grey Goose", "Patron",
        "Godiva", "Laduree", "La Maison du Chocolat", "Pierre Herme", "Fauchon",
        "TWG Tea", "Mariage Freres", "Fortnum & Mason", "Clase Azul", "Illy",
        "Lavazza", "Don Julio", "Remy Martin", "Louis Roederer", "Laurent-Perrier",
        "Perrier-Jouet", "Penfolds", "Opus One", "Starbucks Reserve", "Blue Bottle Coffee",
        "Beluga Caviar", "Petrossian", "Valrhona", "Neuhaus", "Lindt Excellence",
        "Bollinger", "Taittinger", "Pol Roger", "Johnnie Walker Blue", "Glenfiddich",
        "Dalmore", "Hibiki", "Yamazaki", "Armand de Brignac", "Sassicaia",
        "Chateau Margaux", "Romanee-Conti", "Screaming Eagle", "Harlan Estate",
    ],
    "tech": [
        "Apple", "Samsung", "Sony", "Bang & Olufsen", "Bose",
        "Dyson", "Leica", "Hasselblad", "DJI", "Sonos",
        "Master & Dynamic", "Devialet", "Bowers & Wilkins", "Sennheiser", "KEF",
        "McIntosh", "Naim Audio", "Cambridge Audio", "Focal", "Linn",
        "Technics", "Marshall", "Nothing", "Google Pixel", "Microsoft Surface",
        "Breitling Audio", "Balmuda", "Rimowa Electronic Tag", "LG Signature",
        "Meze Audio", "Astell & Kern", "Chord Electronics", "Moon Audio",
        "HiFiMAN", "Audeze",
    ],
    "travel": [
        "Four Seasons", "Aman Resorts", "Ritz-Carlton", "Mandarin Oriental", "Peninsula Hotels",
        "Rosewood", "Six Senses", "One&Only", "Belmond", "Park Hyatt",
        "Waldorf Astoria", "St. Regis", "Bulgari Hotels", "Cheval Blanc", "Raffles",
        "Banyan Tree", "Soneva", "Oberoi Hotels", "Como Hotels", "Singita",
        "Emirates First Class", "Singapore Airlines Suites", "Etihad First Class",
        "Crystal Cruises", "Regent Seven Seas", "Silversea", "Aman Jet",
        "Abercrombie & Kent", "Scott Dunn", "Black Tomato",
        "Explora Journeys", "Seabourn", "Oceania Cruises", "Viking Expedition",
        "White Desert", "Nihi Sumba", "Amanpuri", "Anantara",
        "Fairmont", "Rocco Forte Hotels",
    ],
    "real_estate": [
        "Sotheby's International Realty", "Christie's Real Estate", "Knight Frank",
        "Engel & Volkers", "Barnes International", "Compass Luxury",
        "Douglas Elliman", "Coldwell Banker Global Luxury", "Savills", "Beauchamp Estates",
        "Strutt & Parker", "The Agency", "Hilton & Hyland", "Brown Harris Stevens",
        "Corcoran", "Nest Seekers", "Aaron Kirman Group", "Elliman", "JLL Luxury",
        "Halstead", "Concierge Auctions", "Kuper Sotheby's", "Berkshire Hathaway HomeServices",
        "Briggs Freeman Sotheby's", "ONE Sotheby's",
    ],
    "home_design": [
        "Restoration Hardware", "B&B Italia", "Poltrona Frau", "Minotti", "Cassina",
        "Flos", "Artemide", "Louis Poulsen", "Tom Dixon", "Moooi",
        "Hermes Maison", "Ralph Lauren Home", "Ligne Roset", "Knoll", "Fritz Hansen",
        "Vitra", "Baccarat", "Lalique", "Christofle", "Bernardaud",
        "Roche Bobois", "Fendi Casa", "Armani Casa", "Zara Home", "West Elm",
        "Edra", "Paola Lenti", "Flexform", "De Padova", "Giorgetti",
    ],
}

# =====================================================================
# SYSTEM PROMPT
# =====================================================================

SYSTEM_PROMPT = """You are a senior brand strategist and creative director with 25 years of experience working with the world's top luxury, premium, and lifestyle brands. You have an encyclopedic knowledge of brand visual identities, campaign histories, creative directors, and the nuances that distinguish each brand's aesthetic DNA.

Your task is to generate a comprehensive visual identity profile for the given brand. Be extremely specific and accurate:

- Hex colors MUST be as close as possible to the brand's actual brand colors (e.g., Tiffany blue is #0ABAB5, Hermes orange is #F37021, Chanel black/white, etc.)
- Typography descriptions must reflect the brand's actual font choices
- Photography DNA must reflect the brand's actual campaign aesthetic
- Reference campaigns must be REAL campaigns that actually existed
- Competitive sets must be accurate market positioning
- Prompt prefixes and modifiers must be actionable for AI image generation

Return a single JSON object with the exact schema specified. Be precise, not generic. Every brand should feel distinct and recognizable from its profile alone.

IMPORTANT: The prompt_prefix should be 2-3 sentences written in prompt-engineering language that captures the brand's visual DNA. The prompt_modifiers should be 10-15 specific keywords/phrases useful for AI image generation. The banned_elements should list 8-12 things that would NEVER appear in this brand's advertising."""

USER_TEMPLATE = """Generate a detailed visual identity profile for the brand: {brand_name}
Industry category: {industry}

Return a JSON object with this exact structure:
{{
  "brand_name": "{brand_name}",
  "industry": "{industry}",
  "brand_tier": "ultra_luxury|luxury|accessible_luxury|premium",
  "founded_year": <integer year>,
  "country_of_origin": "<country>",
  "brand_essence": "<one sentence core identity>",
  "target_audience": {{
    "age_range": "<e.g. 25-45>",
    "gender": "predominantly female|predominantly male|unisex",
    "lifestyle": "<description>",
    "income_level": "<description>"
  }},
  "visual_identity": {{
    "primary_colors": ["#hex1", "#hex2", "#hex3"],
    "secondary_colors": ["#hex4", "#hex5"],
    "color_mood": "<how colors are used>",
    "typography_style": "<serif|sans-serif|mixed> — <font personality description>",
    "logo_style": "<logo aesthetic description>",
    "overall_aesthetic": "<minimalist|maximalist|classic|modern|avant-garde>"
  }},
  "photography_dna": {{
    "lighting_style": "<typical lighting in their ads>",
    "color_grading": "<typical color treatment>",
    "composition_style": "<typical framing>",
    "model_casting": "<typical model look>",
    "retouching_level": "natural|polished|heavy",
    "preferred_lenses": "<typical focal lengths>",
    "environment_preferences": ["<typical settings>"],
    "texture_focus": "<emphasized textures>"
  }},
  "prompt_prefix": "<2-3 sentences to prepend to every AI image prompt for this brand>",
  "prompt_modifiers": ["<10-15 specific prompt keywords>"],
  "banned_elements": ["<8-12 things that should NEVER appear>"],
  "mood_keywords": ["<10-15 emotional words>"],
  "reference_campaigns": ["<3-5 iconic campaigns or creative directors>"],
  "competitive_set": ["<3-5 competitor brands>"],
  "seasonal_variations": {{
    "spring_summer": "<how visual identity shifts for SS>",
    "fall_winter": "<how visual identity shifts for FW>",
    "holiday": "<how visual identity shifts for holidays>"
  }}
}}

Be extremely specific to {brand_name}. Use accurate hex brand colors, real campaign references, and precise visual language."""


# =====================================================================
# HELPERS
# =====================================================================

def brand_to_filename(brand_name):
    """Convert brand name to snake_case filename."""
    name = brand_name.lower()
    for char in ["'", "'", ".", ",", "&", "+", "(", ")"]:
        name = name.replace(char, "")
    name = name.replace(" - ", "_").replace("-", "_").replace(" ", "_")
    # collapse multiple underscores
    while "__" in name:
        name = name.replace("__", "_")
    return name.strip("_")


def load_progress():
    """Load progress from disk."""
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {"completed": 0, "errors": 0, "done_ids": []}


def save_progress(progress):
    """Save progress to disk."""
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)


def scan_existing_files():
    """Scan existing brand profile files to build the set of already-done IDs."""
    done = set()
    for industry in BRAND_LIST:
        industry_dir = BASE_DIR / industry
        if industry_dir.exists():
            for f in industry_dir.glob("*.json"):
                done.add(f"{industry}/{f.stem}")
    return done


def generate_one(industry, brand_name):
    """Generate a single brand profile via direct API call with retries."""
    file_id = f"{industry}/{brand_to_filename(brand_name)}"

    user_msg = USER_TEMPLATE.format(brand_name=brand_name, industry=industry)

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.7,
                max_tokens=3000,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
            )

            content = response.choices[0].message.content
            profile = json.loads(content)

            # Ensure correct brand name and industry in output
            profile["brand_name"] = brand_name
            profile["industry"] = industry

            # Save to file
            output_dir = BASE_DIR / industry
            output_dir.mkdir(parents=True, exist_ok=True)
            filename = brand_to_filename(brand_name)
            filepath = output_dir / f"{filename}.json"

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(profile, f, indent=2, ensure_ascii=False)

            return file_id

        except Exception as e:
            error_str = str(e)
            if attempt < MAX_RETRIES:
                wait = 2 ** attempt
                if "rate_limit" in error_str.lower() or "429" in error_str:
                    wait = 30
                time.sleep(wait)
            else:
                return f"ERROR:{file_id}:{error_str}"

    return f"ERROR:{file_id}:max_retries_exceeded"


# =====================================================================
# MAIN
# =====================================================================

def run():
    """Run the brand profile generation."""
    progress = load_progress()

    # Scan existing files to determine what's already done
    existing = scan_existing_files()
    progress["done_ids"] = list(existing)
    progress["completed"] = len(existing)

    # Build task list
    tasks = []
    for industry, brands in BRAND_LIST.items():
        for brand_name in brands:
            file_id = f"{industry}/{brand_to_filename(brand_name)}"
            if file_id not in existing:
                tasks.append((industry, brand_name))

    total = sum(len(brands) for brands in BRAND_LIST.values())
    already_done = len(existing)

    print(f"Total brands: {total}")
    print(f"Already done: {already_done}")
    print(f"Remaining:    {len(tasks)}")
    print(f"Estimated cost: ~${len(tasks) * 0.001:.2f}")
    print(f"\nStarting with 5 parallel workers...\n")

    if not tasks:
        print("Nothing to do -- all profiles already generated.")
        return

    count = already_done
    errors = progress["errors"]

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = {}
        for industry, brand_name in tasks:
            future = executor.submit(generate_one, industry, brand_name)
            futures[future] = f"{industry}/{brand_name}"

        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result is None:
                continue
            elif isinstance(result, str) and result.startswith("ERROR:"):
                errors += 1
                print(f"  ERROR: {result}")
                progress["errors"] = errors
                # Rate limit pause
                if "rate_limit" in result.lower() or "429" in result:
                    print("  Rate limited -- pausing 30s...")
                    time.sleep(30)
            else:
                count += 1
                progress["done_ids"].append(result)
                progress["completed"] = count
                progress["errors"] = errors

                if count % 25 == 0:
                    pct = count / total * 100
                    print(f"  Progress: {count}/{total} ({pct:.1f}%)")
                    save_progress(progress)

    save_progress(progress)

    # Final statistics
    print(f"\n{'=' * 60}")
    print(f"COMPLETE")
    print(f"  Total generated: {count}")
    print(f"  Errors:          {errors}")
    print(f"{'=' * 60}")
    print(f"\nBy industry:")
    for industry in BRAND_LIST:
        industry_dir = BASE_DIR / industry
        actual = len(list(industry_dir.glob("*.json"))) if industry_dir.exists() else 0
        target = len(BRAND_LIST[industry])
        print(f"  {industry:<22} : {actual:>3}/{target}")


def status():
    """Show current progress."""
    total = sum(len(brands) for brands in BRAND_LIST.values())
    existing = scan_existing_files()
    done = len(existing)
    print(f"\nProgress: {done}/{total} ({done / total * 100:.1f}%)")
    print()
    for industry in BRAND_LIST:
        industry_dir = BASE_DIR / industry
        actual = len(list(industry_dir.glob("*.json"))) if industry_dir.exists() else 0
        target = len(BRAND_LIST[industry])
        pct = actual / target * 100 if target > 0 else 0
        bar = "#" * int(pct / 5) + "." * (20 - int(pct / 5))
        print(f"  {industry:<22} {bar} {actual:>3}/{target} ({pct:.0f}%)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate 500 brand visual identity profiles")
    parser.add_argument("--run", action="store_true", help="Start generation")
    parser.add_argument("--status", action="store_true", help="Show progress")
    args = parser.parse_args()

    if args.run:
        run()
    elif args.status:
        status()
    else:
        parser.print_help()
        print("\nRun: python3 generate_brand_profiles.py --run")
