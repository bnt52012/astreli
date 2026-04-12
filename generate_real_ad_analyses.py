"""
╔══════════════════════════════════════════════════════════════════════╗
║  AdGenAI — Real Advertising Video Analyses (1000 breakdowns)         ║
║                                                                      ║
║  Asks GPT-4o (not mini) to produce detailed technical breakdowns of  ║
║  real iconic campaigns from top-tier agencies (Ogilvy, BBDO, W+K,    ║
║  TBWA, Publicis, DDB, AKQA, Droga5, R/GA, Mother, Anomaly, 72andSunny║
║  Leo Burnett, Wieden+Kennedy, Saatchi & Saatchi).                    ║
║                                                                      ║
║  Each record contains a shot-by-shot plan with Kling + Gemini        ║
║  prompts that the enricher can later blend into new prompts.         ║
║                                                                      ║
║  Usage:                                                              ║
║    python3 generate_real_ad_analyses.py --run                        ║
║    python3 generate_real_ad_analyses.py --status                     ║
║                                                                      ║
║  Resumable via dataset/real_ads/_progress.json.                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import random
import sys
import time
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
_api_key = os.environ.get("OPENAI_API_KEY")
if not _api_key:
    print("❌ OPENAI_API_KEY is not set in the environment / .env", file=sys.stderr)
    sys.exit(1)
client = OpenAI(api_key=_api_key)

BASE_DIR = Path("dataset/real_ads")
PROGRESS_FILE = BASE_DIR / "_progress.json"
BASE_DIR.mkdir(parents=True, exist_ok=True)

MODEL = "gpt-4o"
MAX_WORKERS = 4
RETRY_LIMIT = 3
RATE_LIMIT_PAUSE = 30

# ─────────────────────────────────────────────────────────────────────
# Distribution — 1000 total
# ─────────────────────────────────────────────────────────────────────

INDUSTRY_TARGETS: dict[str, int] = {
    "luxury_fashion": 150,
    "beauty_cosmetics": 120,
    "fragrance_perfume": 120,
    "jewelry_watches": 100,
    "automotive": 100,
    "food_beverage_premium": 100,
    "tech_premium": 80,
    "travel_hospitality": 80,
    "sport_premium": 70,
    "real_estate": 40,
    "home_design": 40,
}

TOTAL_TARGET = sum(INDUSTRY_TARGETS.values())
assert TOTAL_TARGET == 1000

# Real-world brand pool per industry — drives sampling diversity.
INDUSTRY_BRANDS: dict[str, list[str]] = {
    "luxury_fashion": [
        "Chanel", "Hermès", "Louis Vuitton", "Dior", "Gucci", "Prada",
        "Saint Laurent", "Bottega Veneta", "Balenciaga", "Celine",
        "Burberry", "Loewe", "Valentino", "Fendi", "Givenchy",
        "Balmain", "Alexander McQueen", "Tom Ford", "Versace", "Dolce & Gabbana",
    ],
    "beauty_cosmetics": [
        "L'Oréal Paris", "Estée Lauder", "MAC", "NARS", "Chanel Beauté",
        "Dior Beauty", "Charlotte Tilbury", "Lancôme", "Maybelline",
        "Fenty Beauty", "YSL Beauté", "Tom Ford Beauty", "Clinique",
        "Shiseido", "Pat McGrath Labs", "Rare Beauty", "Hourglass",
        "Guerlain", "Clarins", "La Mer",
    ],
    "fragrance_perfume": [
        "Chanel N°5", "Dior Sauvage", "Tom Ford Private Blend", "Le Labo",
        "Byredo", "Maison Francis Kurkdjian", "Jo Malone", "Creed",
        "Penhaligon's", "Frederic Malle", "Acqua di Parma", "Diptyque",
        "Guerlain Shalimar", "Yves Saint Laurent Libre", "Armani Sì",
        "Miss Dior", "Chloé", "Gucci Bloom", "Viktor & Rolf Flowerbomb",
        "Calvin Klein CK One",
    ],
    "jewelry_watches": [
        "Rolex", "Cartier", "Tiffany & Co.", "Bulgari", "Van Cleef & Arpels",
        "Chopard", "Piaget", "Omega", "Patek Philippe", "Audemars Piguet",
        "Jaeger-LeCoultre", "IWC", "Vacheron Constantin", "Breitling",
        "Graff", "Harry Winston", "Boucheron", "Chaumet", "Messika", "Hublot",
    ],
    "automotive": [
        "Mercedes-Benz", "BMW", "Porsche", "Audi", "Lexus",
        "Land Rover", "Range Rover", "Maserati", "Aston Martin", "Bentley",
        "Rolls-Royce", "Ferrari", "Lamborghini", "McLaren", "Tesla",
        "Jaguar", "Polestar", "Genesis", "Lucid", "Rivian",
    ],
    "food_beverage_premium": [
        "Moët & Chandon", "Dom Pérignon", "Veuve Clicquot", "Hennessy",
        "Rémy Martin", "Johnnie Walker Blue", "Macallan", "Patrón",
        "Grey Goose", "Belvedere", "Perrier-Jouët", "Krug",
        "Nespresso", "Lavazza", "San Pellegrino", "Fiji Water",
        "Godiva", "Lindt", "Häagen-Dazs", "Evian",
    ],
    "tech_premium": [
        "Apple", "Bang & Olufsen", "Bose", "Sony", "Leica",
        "Dyson", "Bang Olufsen", "Samsung Galaxy", "Google Pixel",
        "Microsoft Surface", "Beats by Dre", "Sonos", "Peloton",
        "DJI", "GoPro", "Tesla", "Oura", "Nest", "Ring", "Rolls-Royce Spectre",
    ],
    "travel_hospitality": [
        "Aman Resorts", "Four Seasons", "Ritz-Carlton", "Mandarin Oriental",
        "Peninsula Hotels", "Bulgari Hotels", "Rosewood", "St. Regis",
        "Soho House", "Six Senses", "Belmond", "Cheval Blanc",
        "Emirates", "Singapore Airlines", "British Airways First",
        "Qatar Airways", "Orient Express", "Ritz Paris", "Le Bristol", "Claridge's",
    ],
    "sport_premium": [
        "Nike", "Adidas", "Lululemon", "On Running", "Hoka",
        "Arc'teryx", "Rapha", "Tracksmith", "Peloton", "Salomon",
        "The North Face", "Patagonia", "New Balance", "Asics",
        "Canada Goose", "Moncler", "Gymshark", "Wilson Tennis",
        "Oakley", "Specialized Bikes",
    ],
    "real_estate": [
        "Sotheby's International Realty", "Christie's International Real Estate",
        "Knight Frank", "Engel & Völkers", "Barnes International",
        "Compass", "Douglas Elliman", "Coldwell Banker Global Luxury",
        "Savills", "JLL", "The Agency", "Hilton & Hyland",
        "Corcoran", "Brown Harris Stevens", "Nest Seekers",
        "Williams & Williams", "Beauchamp Estates", "Aaron Kirman Group",
        "Halstead", "Eklund Gomes",
    ],
    "home_design": [
        "Roche Bobois", "B&B Italia", "Minotti", "Cassina", "Poltrona Frau",
        "Flos", "Artemide", "Tom Dixon", "Moooi", "Fritz Hansen",
        "Vitra", "Hermès Maison", "Ralph Lauren Home", "Baccarat",
        "Lalique", "Christofle", "Bernardaud", "Ligne Roset",
        "Knoll", "Louis Poulsen",
    ],
}

AGENCIES = [
    "Ogilvy", "BBDO", "Wieden+Kennedy", "TBWA", "Publicis",
    "DDB", "AKQA", "Droga5", "Leo Burnett", "Grey",
    "Havas", "Anomaly", "Mother", "72andSunny", "R/GA",
    "McCann", "Saatchi & Saatchi", "Serviceplan", "Goodby Silverstein & Partners",
    "FCB", "The&Partnership", "Dentsu", "Forsman & Bodenfors",
]

# ─────────────────────────────────────────────────────────────────────
# Prompt templates
# ─────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT = """You are a senior advertising creative director with encyclopedic knowledge of \
real iconic advertising campaigns from the world's best agencies (Ogilvy, BBDO, Wieden+Kennedy, \
TBWA, Publicis, DDB, AKQA, Droga5, Leo Burnett, Saatchi & Saatchi, Grey, Havas, Anomaly, Mother, \
72andSunny, R/GA, Goodby Silverstein & Partners, Serviceplan, Forsman & Bodenfors).

You will be asked to produce a TECHNICAL SHOT-BY-SHOT BREAKDOWN of a real (or realistically \
reconstructed) high-end advertising video. Your output will be used as gold-standard training \
data for an AI video generation pipeline, so every field must be precise, concrete and \
physically describable — NO vague language, NO marketing fluff.

CRITICAL:
- The `kling_prompt` field in each plan must be the EXACT prompt you would hand to Kling AI \
(image-to-video) to recreate that specific shot. Describe what MOVES, how the camera moves, \
the speed, the mood, and the physics of any materials. 2-4 sentences. No bullet points.
- The `gemini_prompt` field must be the EXACT prompt you would hand to Gemini Flash Image to \
generate the STARTING still of that shot. Include lens + aperture, lighting, composition, \
palette, textures. 3-5 sentences.
- Use real or plausibly realistic campaign names, real agencies, real awards when relevant.
- Return VALID JSON ONLY — no commentary, no markdown code fences.

JSON schema (strict):
{
  "campaign_name": "...",
  "brand": "...",
  "agency": "...",
  "year": 2024,
  "industry": "...",
  "awards": ["..."],
  "format": "30s TV spot",
  "total_duration_seconds": 30,
  "concept": "...",
  "plans": [
    {
      "plan_number": 1,
      "duration_seconds": 2.5,
      "shot_size": "extreme_close_up|close_up|medium_close|medium|wide|extreme_wide",
      "camera_movement": "static|dolly_in|dolly_out|orbit|zoom_in|zoom_out|pan_left|pan_right|crane_up|crane_down|tracking|handheld",
      "camera_speed": "very_slow|slow|medium|fast",
      "subject": "...",
      "action": "...",
      "kling_prompt": "...",
      "gemini_prompt": "...",
      "lighting": "...",
      "lens": "...",
      "transition_to_next": "cut|dissolve|fade|whip_pan|match_cut",
      "audio": "...",
      "why_it_works": "..."
    }
  ],
  "editing_rhythm": "...",
  "key_technique": "...",
  "kling_challenges": "...",
  "overall_mood": "..."
}

Target 5 to 9 plans per ad. Every plan must feel physically shootable."""


def _user_prompt(industry_key: str, brand: str, agency: str, idx: int) -> str:
    """Build a user prompt nudging GPT-4o toward a specific real campaign."""
    format_hint = random.choice([
        "30s TV spot", "60s TV spot", "15s social cut",
        "90s cinema trailer", "45s hero film", "30s digital spot",
    ])
    year = random.randint(2017, 2025)
    award_hint = random.choice([
        "Cannes Lions Gold", "Cannes Lions Silver", "Clio Gold",
        "D&AD Yellow Pencil", "One Show Gold", "Epica Gold",
        "ADC Gold Cube", "Effie Gold", "LIA Gold",
        "(no major award — commercial success)",
    ])

    return (
        f"Industry: {industry_key}\n"
        f"Brand: {brand}\n"
        f"Agency (preferred): {agency}\n"
        f"Format: {format_hint}\n"
        f"Likely year: {year}\n"
        f"Award reference: {award_hint}\n"
        f"Seed: {idx}\n\n"
        "Pick a REAL iconic campaign from this brand that matches the format and year range "
        "(or, if you don't have one, reconstruct a realistic high-craft campaign that this "
        "brand and agency could plausibly have produced). Produce the full JSON shot-by-shot "
        "breakdown per the schema. Every kling_prompt and gemini_prompt must be directly "
        "usable as-is in an AI pipeline."
    )


# ─────────────────────────────────────────────────────────────────────
# Progress management
# ─────────────────────────────────────────────────────────────────────

def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        try:
            return json.loads(PROGRESS_FILE.read_text())
        except json.JSONDecodeError:
            pass
    return {"completed": 0, "errors": 0, "done_ids": []}


def save_progress(progress: dict) -> None:
    PROGRESS_FILE.write_text(json.dumps(progress, indent=2))


# ─────────────────────────────────────────────────────────────────────
# Worker
# ─────────────────────────────────────────────────────────────────────

def generate_one(industry_key: str, brand: str, agency: str, idx: int) -> str:
    """Produce one real-ad analysis and write it to disk. Returns custom_id or ERROR:..."""
    custom_id = f"{industry_key}_{idx:05d}"
    output_dir = BASE_DIR / industry_key
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{custom_id}.json"

    if output_path.exists():
        return custom_id  # already written on a previous run

    user_msg = _user_prompt(industry_key, brand, agency, idx)

    for attempt in range(RETRY_LIMIT):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                temperature=0.7,
                max_tokens=4096,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_msg},
                ],
            )
            raw = response.choices[0].message.content or "{}"
            ad = json.loads(raw)
            ad["_custom_id"] = custom_id
            ad["_requested_brand"] = brand
            ad["_requested_agency"] = agency
            ad["_industry_key"] = industry_key
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(ad, f, indent=2, ensure_ascii=False)
            return custom_id

        except json.JSONDecodeError as e:
            if attempt == RETRY_LIMIT - 1:
                return f"ERROR:{custom_id}:invalid_json:{e}"
            time.sleep(2)
        except Exception as e:
            msg = str(e)
            if "rate_limit" in msg.lower() or "429" in msg:
                time.sleep(RATE_LIMIT_PAUSE)
            if attempt == RETRY_LIMIT - 1:
                return f"ERROR:{custom_id}:{msg[:200]}"
            time.sleep(2)
    return f"ERROR:{custom_id}:exhausted_retries"


def build_task_list() -> list[tuple[str, str, str, int]]:
    tasks: list[tuple[str, str, str, int]] = []
    for industry_key, count in INDUSTRY_TARGETS.items():
        brands = INDUSTRY_BRANDS[industry_key]
        for i in range(count):
            brand = brands[i % len(brands)]
            agency = AGENCIES[i % len(AGENCIES)]
            tasks.append((industry_key, brand, agency, i))
    return tasks


def run() -> None:
    progress = load_progress()
    tasks = build_task_list()
    total = len(tasks)
    done_ids = set(progress.get("done_ids", []))
    remaining = total - len(done_ids)

    print(f"📊 Total:       {total} analyses")
    print(f"✅ Already done: {len(done_ids)}")
    print(f"⏳ Remaining:    {remaining}")
    print(f"💰 Est. cost:    ~${remaining * 0.015:.2f}  (GPT-4o, ~4K out tokens)")
    print(f"🚀 Workers:      {MAX_WORKERS}\n")

    errors = progress.get("errors", 0)
    completed = len(done_ids)

    with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures: dict[concurrent.futures.Future, str] = {}
        for industry_key, brand, agency, idx in tasks:
            custom_id = f"{industry_key}_{idx:05d}"
            if custom_id in done_ids:
                continue
            fut = pool.submit(generate_one, industry_key, brand, agency, idx)
            futures[fut] = custom_id

        for fut in concurrent.futures.as_completed(futures):
            result = fut.result()
            if result.startswith("ERROR:"):
                errors += 1
                if errors % 5 == 0:
                    print(f"⚠️  {errors} errors so far — last: {result[:120]}")
            else:
                completed += 1
                done_ids.add(result)
                if completed % 25 == 0:
                    pct = completed / total * 100
                    print(f"📊 {completed}/{total} ({pct:.1f}%) — latest: {result}")
                if completed % 50 == 0:
                    progress["completed"] = completed
                    progress["errors"] = errors
                    progress["done_ids"] = sorted(done_ids)
                    save_progress(progress)

    progress["completed"] = completed
    progress["errors"] = errors
    progress["done_ids"] = sorted(done_ids)
    save_progress(progress)
    print(f"\n✅ Done. {completed}/{total} successful, {errors} errors.")


def status() -> None:
    progress = load_progress()
    done_ids = set(progress.get("done_ids", []))

    print(f"📊 REAL AD ANALYSES STATUS")
    print(f"   Total target: {TOTAL_TARGET}")
    print(f"   Completed:    {len(done_ids)}")
    print(f"   Errors:       {progress.get('errors', 0)}")
    print()
    for industry_key, count in INDUSTRY_TARGETS.items():
        ind_done = sum(1 for did in done_ids if did.startswith(industry_key))
        bar_len = int(40 * ind_done / count)
        bar = "█" * bar_len + "░" * (40 - bar_len)
        print(f"   {industry_key:<22} {bar} {ind_done}/{count}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate 1000 real-ad analyses with GPT-4o")
    parser.add_argument("--run", action="store_true", help="Generate the analyses")
    parser.add_argument("--status", action="store_true", help="Show progress")
    args = parser.parse_args()

    if args.status:
        status()
    elif args.run:
        run()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
