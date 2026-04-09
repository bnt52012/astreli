"""
Generate 5,000 detailed storyboard decompositions of high-end advertising videos
using GPT-4o-mini via direct OpenAI API calls.

Saves each storyboard as an individual JSON file in dataset/storyboards/{industry}/
Resumes automatically if interrupted.

Usage:
    python3 generate_storyboards.py
"""

import os
import json
import time
import concurrent.futures
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

BASE_DIR = Path("dataset/storyboards")
PROGRESS_FILE = BASE_DIR / "_progress_storyboards.json"
BASE_DIR.mkdir(parents=True, exist_ok=True)

# ===================================================================
# DISTRIBUTION — 5,000 total
# ===================================================================

INDUSTRIES = {
    "luxury": {
        "count": 700,
        "brands": [
            "Chanel", "Louis Vuitton", "Hermes", "Dior", "Gucci",
            "Prada", "Bottega Veneta", "Tom Ford", "Brunello Cucinelli",
            "Loro Piana", "Valentino", "Balenciaga", "Saint Laurent",
        ],
    },
    "beauty": {
        "count": 600,
        "brands": [
            "Estee Lauder", "Charlotte Tilbury", "Dior Beauty", "MAC Cosmetics",
            "NARS", "YSL Beauty", "Tom Ford Beauty", "Fenty Beauty",
            "La Mer", "Chanel Beauty", "Guerlain", "Pat McGrath Labs",
        ],
    },
    "fragrance": {
        "count": 600,
        "brands": [
            "Chanel No. 5", "Dior Sauvage", "Tom Ford Private Blend",
            "Le Labo", "Byredo", "Maison Francis Kurkdjian", "Jo Malone",
            "Acqua di Parma", "Creed", "Penhaligon's", "Frederic Malle",
            "Diptyque",
        ],
    },
    "jewelry_watches": {
        "count": 500,
        "brands": [
            "Rolex", "Cartier", "Tiffany & Co.", "Bulgari",
            "Van Cleef & Arpels", "Chopard", "Patek Philippe",
            "Omega", "Piaget", "Harry Winston", "Audemars Piguet",
            "Jaeger-LeCoultre",
        ],
    },
    "fashion": {
        "count": 500,
        "brands": [
            "Sandro", "Maje", "COS", "Massimo Dutti", "Reiss",
            "AllSaints", "Theory", "Zadig & Voltaire", "Isabel Marant",
            "Acne Studios", "A.P.C.", "Jacquemus", "Toteme",
        ],
    },
    "automotive": {
        "count": 400,
        "brands": [
            "Mercedes-Benz", "BMW", "Porsche", "Range Rover", "Audi",
            "Lexus", "Aston Martin", "Bentley", "Tesla", "Rolls-Royce",
            "Ferrari", "Lamborghini",
        ],
    },
    "sport": {
        "count": 400,
        "brands": [
            "Nike", "Lululemon", "On Running", "Adidas", "Arc'teryx",
            "Rapha", "Tracksmith", "Vuori", "Alo Yoga", "Hoka",
            "Salomon", "New Balance",
        ],
    },
    "food_beverage": {
        "count": 400,
        "brands": [
            "Nespresso", "Dom Perignon", "Godiva", "Veuve Clicquot",
            "Hennessy", "Moet & Chandon", "Macallan", "Grey Goose",
            "Patron", "Illy", "Ruinart", "Krug",
        ],
    },
    "tech": {
        "count": 300,
        "brands": [
            "Apple", "Bang & Olufsen", "Leica", "Dyson", "Bose",
            "Sony", "Hasselblad", "DJI", "Sonos", "Master & Dynamic",
            "Devialet", "Bowers & Wilkins",
        ],
    },
    "travel": {
        "count": 300,
        "brands": [
            "Aman Resorts", "Four Seasons", "Ritz-Carlton", "Belmond",
            "Mandarin Oriental", "Six Senses", "One&Only", "Rosewood",
            "Park Hyatt", "St. Regis", "Peninsula Hotels", "Cheval Blanc",
        ],
    },
    "real_estate": {
        "count": 200,
        "brands": [
            "Sotheby's International Realty", "Christie's Real Estate",
            "Knight Frank", "Engel & Volkers", "Compass Luxury",
            "Douglas Elliman", "Savills", "The Agency",
            "Hilton & Hyland", "Beauchamp Estates",
        ],
    },
}

FORMATS = ["15s", "30s", "45s", "60s"]

FORMAT_PLAN_RANGES = {
    "15s": (4, 6),
    "30s": (6, 10),
    "45s": (10, 14),
    "60s": (12, 18),
}

# ===================================================================
# SYSTEM PROMPT
# ===================================================================

SYSTEM_PROMPT = """You are a senior film editor and advertising creative director with 20 years of experience analyzing finished luxury and high-end advertising videos. Your specialty is reverse-engineering completed ads into precise plan-by-plan storyboard breakdowns.

Given an industry, brand, and format, you will INVENT a realistic, cinematic advertising video and decompose it plan by plan as if analyzing a finished film. Each plan must be technically precise with real cinematography terminology.

Return a single JSON object with this exact structure:
{
  "ad_title": "Campaign name",
  "brand": "Brand name",
  "industry": "industry_key",
  "format": "15s|30s|45s|60s",
  "total_plans": 8,
  "overall_pacing": "slow_luxury|medium_editorial|fast_dynamic",
  "color_grade": "description of overall color treatment",
  "plans": [
    {
      "plan_number": 1,
      "duration_seconds": 2.5,
      "shot_size": "extreme_close_up|close_up|medium_close|medium|medium_wide|wide|extreme_wide",
      "camera_movement": "static|pan_left|pan_right|tilt_up|tilt_down|tracking|dolly_in|dolly_out|orbit|crane|steadicam|handheld|zoom_in|zoom_out",
      "camera_speed": "very_slow|slow|medium|fast|whip",
      "subject": "what is in frame",
      "action": "what happens during this plan",
      "lighting": "specific lighting setup used",
      "lens_estimate": "estimated focal length and aperture",
      "composition": "rule of thirds, centered, etc",
      "transition_in": "how this plan starts",
      "transition_out": "how this plan ends",
      "audio": "what we hear",
      "mood": "emotional quality",
      "technical_notes": "any special technique"
    }
  ],
  "editing_rhythm": "description of cutting rhythm evolution",
  "music_description": "detailed music/sound design description",
  "key_creative_technique": "the ONE thing that makes this ad memorable"
}

Rules:
- The sum of plan durations must approximately match the format duration.
- Plan counts must be realistic for the format: 15s = 4-6 plans, 30s = 6-10, 45s = 10-14, 60s = 12-18.
- Use real cinematography terms: Rembrandt lighting, chiaroscuro, golden hour, etc.
- Vary shot sizes across the sequence — never repeat the same shot size consecutively.
- Include realistic camera movements appropriate to the brand and industry.
- Each plan must feel distinct and purposeful within the narrative arc.
- The final plan should always be an endframe/logo with the brand name.
- Be specific and varied — no two storyboards should feel identical.
- overall_pacing should match the industry: luxury = slow_luxury, sport = fast_dynamic, etc.
- color_grade should be specific: "desaturated teal shadows with warm amber highlights and lifted blacks" not just "warm".
- lens_estimate should include focal length and aperture: "85mm f/1.4" or "24mm f/2.8 tilt-shift"."""

# ===================================================================
# GENERATION
# ===================================================================

def load_progress():
    """Load progress from file, or scan existing files to rebuild."""
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    # Scan existing files to rebuild progress
    done_ids = set()
    for industry_key in INDUSTRIES:
        industry_dir = BASE_DIR / industry_key
        if industry_dir.exists():
            for f in industry_dir.glob("*.json"):
                done_ids.add(f.stem)
    return {"completed": len(done_ids), "errors": 0, "done_ids": list(done_ids)}


def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)


def generate_one(industry_key, brand, fmt, idx, max_retries=3):
    """Generate a single storyboard via direct API call with retry."""
    plan_min, plan_max = FORMAT_PLAN_RANGES[fmt]

    user_prompt = (
        f"Analyze a finished {industry_key} advertising video for {brand}. "
        f"Format: {fmt}. "
        f"The video should have between {plan_min} and {plan_max} plans. "
        f"Make this storyboard unique — vary the creative approach, pacing, "
        f"locations, and artistic techniques. "
        f"Be inventive with the campaign concept."
    )

    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.95,
                max_tokens=3000,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
            )

            content = response.choices[0].message.content
            storyboard = json.loads(content)

            # Ensure required fields
            storyboard["industry"] = industry_key
            storyboard["brand"] = brand
            storyboard["format"] = fmt

            return storyboard

        except Exception as e:
            if attempt < max_retries - 1:
                wait = (attempt + 1) * 5
                if "rate_limit" in str(e).lower() or "429" in str(e):
                    wait = 30
                time.sleep(wait)
            else:
                raise


def process_task(task, done_ids_set):
    """Process a single generation task. Returns (file_id, storyboard) or (file_id, error_str)."""
    industry_key, brand, fmt, idx = task
    file_id = f"{industry_key}_{idx:05d}"

    if file_id in done_ids_set:
        return None

    try:
        storyboard = generate_one(industry_key, brand, fmt, idx)

        # Save to file
        output_dir = BASE_DIR / industry_key
        output_dir.mkdir(parents=True, exist_ok=True)

        filepath = output_dir / f"{file_id}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(storyboard, f, indent=2, ensure_ascii=False)

        return ("OK", file_id)

    except Exception as e:
        return ("ERROR", file_id, str(e))


def run():
    """Main generation loop."""
    progress = load_progress()
    done_ids_set = set(progress["done_ids"])

    # Build task list
    tasks = []
    for industry_key, industry_cfg in INDUSTRIES.items():
        count = industry_cfg["count"]
        brands = industry_cfg["brands"]
        for i in range(count):
            brand = brands[i % len(brands)]
            fmt = FORMATS[i % len(FORMATS)]
            tasks.append((industry_key, brand, fmt, i))

    total = len(tasks)
    already_done = len(done_ids_set)

    print(f"Total: {total} storyboards")
    print(f"  Already done: {already_done}")
    print(f"  Remaining:    {total - already_done}")
    print(f"  Estimated cost: ~${(total - already_done) * 0.001:.2f}")
    print(f"\nStarting with 5 parallel workers...\n")

    if already_done >= total:
        print("All storyboards already generated.")
        return

    count = already_done
    errors = progress["errors"]

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        # Submit in batches
        batch_size = 100
        for batch_start in range(0, len(tasks), batch_size):
            batch = tasks[batch_start:batch_start + batch_size]

            futures = {}
            for task in batch:
                file_id = f"{task[0]}_{task[3]:05d}"
                if file_id in done_ids_set:
                    continue
                future = executor.submit(process_task, task, done_ids_set)
                futures[future] = file_id

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result is None:
                    continue

                if result[0] == "OK":
                    file_id = result[1]
                    count += 1
                    done_ids_set.add(file_id)
                    progress["done_ids"].append(file_id)
                    progress["completed"] = count

                    if count % 50 == 0:
                        pct = count / total * 100
                        print(f"  Progress: {count}/{total} ({pct:.1f}%) -- last: {file_id}")

                elif result[0] == "ERROR":
                    errors += 1
                    progress["errors"] = errors
                    err_id = result[1]
                    err_msg = result[2]
                    if errors % 10 == 0:
                        print(f"  Errors so far: {errors}")
                    if "rate_limit" in err_msg.lower() or "429" in err_msg:
                        print(f"  Rate limited -- pausing 30s...")
                        time.sleep(30)

            # Save progress after each batch
            save_progress(progress)

    # Final statistics
    print(f"\n{'=' * 60}")
    print(f"COMPLETED")
    print(f"  Total generated: {count}")
    print(f"  Errors:          {errors}")
    print(f"{'=' * 60}")

    # Per-industry stats
    print(f"\nPer-industry breakdown:")
    for industry_key in INDUSTRIES:
        industry_dir = BASE_DIR / industry_key
        if industry_dir.exists():
            n = len(list(industry_dir.glob("*.json")))
        else:
            n = 0
        target = INDUSTRIES[industry_key]["count"]
        print(f"  {industry_key:20s}: {n:5d} / {target}")


if __name__ == "__main__":
    run()
