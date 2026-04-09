"""
Generate 10,000 synthetic advertising performance data points using GPT-4o-mini.

Uses direct OpenAI API calls with concurrent.futures for parallelism.
Saves progress and resumes automatically if interrupted.

Usage:
    python3 generate_performance_data.py --run
    python3 generate_performance_data.py --status
"""

import os
import json
import time
import random
import argparse
import concurrent.futures
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

BASE_DIR = Path("dataset/performance")
PROGRESS_FILE = BASE_DIR / "_progress_performance.json"
BASE_DIR.mkdir(parents=True, exist_ok=True)

# ===================================================================
# PLATFORM DISTRIBUTION (10,000 total)
# ===================================================================

PLATFORM_DISTRIBUTION = {
    "instagram_reels": 1500,
    "instagram_stories": 1000,
    "instagram_feed": 800,
    "tiktok": 1500,
    "youtube_preroll": 800,
    "youtube_standard": 700,
    "tv_15s": 600,
    "tv_30s": 600,
    "tv_60s": 400,
    "linkedin": 600,
    "facebook": 800,
    "pinterest": 700,
}

# ===================================================================
# INDUSTRIES (11 total)
# ===================================================================

INDUSTRIES = [
    "luxury",
    "beauty",
    "fragrance",
    "jewelry_watches",
    "fashion",
    "automotive",
    "sport",
    "food_beverage",
    "tech",
    "travel",
    "real_estate",
]

BRAND_TIERS = ["ultra_luxury", "luxury", "accessible_luxury", "premium"]

# Performance tier distribution: ~10% top_10pct, ~15% top_25pct, ~50% average, ~25% below_average
PERFORMANCE_TIERS = (
    ["top_10pct"] * 10
    + ["top_25pct"] * 15
    + ["average"] * 50
    + ["below_average"] * 25
)

# ===================================================================
# SYSTEM PROMPT
# ===================================================================

SYSTEM_PROMPT = """You are a senior performance marketing analyst at a top-tier advertising agency. You specialize in generating realistic advertising performance data based on real-world patterns.

Generate a single ad performance data point as JSON. The data must be REALISTIC and follow these rules:

1. PERFORMANCE DISTRIBUTION: Not all ads are top performers. Follow the requested performance_tier strictly.
2. METRIC CORRELATIONS: Metrics must correlate logically:
   - High view_completion_rate should correlate with higher engagement (likes, comments, shares)
   - Below-average ads should have low completion AND low engagement
   - Top performers have high completion AND high engagement
3. PLATFORM-SPECIFIC RANGES:
   - TikTok: higher completion rates (0.5-0.9), higher share_rate, lower CTR
   - Instagram Reels: moderate completion (0.4-0.8), high save_rate
   - Instagram Stories: lower completion (0.3-0.7), higher CTR (swipe up)
   - Instagram Feed: lower completion (0.3-0.6), high save_rate, high like_rate
   - YouTube preroll: lower completion (0.2-0.6), moderate CTR
   - YouTube standard: higher completion (0.4-0.8), lower CTR
   - TV (15s/30s/60s): completion is view-based (0.6-0.95), no CTR/save/share
   - LinkedIn: lower engagement overall, higher CTR for B2B
   - Facebook: moderate everything, older demographic patterns
   - Pinterest: high save_rate, moderate CTR, lower comment_rate
4. FORMAT EFFECTS:
   - Short-form (15s) typically has higher completion rates
   - Longer formats (60s) have lower completion but can drive deeper engagement
5. BRAND TIER EFFECTS:
   - ultra_luxury/luxury: lower CTR but higher save rates, slower pacing
   - sport/food_beverage: higher engagement rates overall
   - tech: moderate engagement, higher CTR
6. SCENE STRUCTURE: Use realistic scene archetypes from advertising:
   - product_hero, lifestyle, portrait, product_interaction, establishing, macro_detail, motion_action, endframe, silhouette, pov, hands_only, reveal, slow_motion, craftsmanship_detail, aspirational_moment
7. For TV platforms, set click_through_rate, save_rate, share_rate, like_rate, and comment_rate to 0.0 (not applicable).
8. All rates should be decimal (e.g., 0.034 not 3.4%).

Return ONLY valid JSON matching the exact schema requested. No markdown, no explanation."""

# ===================================================================
# HELPERS
# ===================================================================


def load_progress():
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {"completed": 0, "errors": 0, "done_ids": []}


def save_progress(progress):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(progress, f)


def scan_existing_files():
    """Scan output directories to find already-generated files."""
    done_ids = set()
    for platform in PLATFORM_DISTRIBUTION:
        platform_dir = BASE_DIR / platform
        if platform_dir.exists():
            for f in platform_dir.glob("*.json"):
                done_ids.add(f.stem)
    return done_ids


def build_user_prompt(platform, industry, brand_tier, performance_tier, index):
    """Build the user prompt for a single data point."""

    platform_format_map = {
        "instagram_reels": (15, "short-form vertical video"),
        "instagram_stories": (15, "vertical story ad"),
        "instagram_feed": (30, "square or vertical feed post video"),
        "tiktok": (15, "short-form vertical video"),
        "youtube_preroll": (15, "pre-roll skippable ad"),
        "youtube_standard": (30, "standard in-stream video ad"),
        "tv_15s": (15, "15-second TV commercial"),
        "tv_30s": (30, "30-second TV commercial"),
        "tv_60s": (60, "60-second TV commercial"),
        "linkedin": (30, "professional video ad"),
        "facebook": (15, "in-feed video ad"),
        "pinterest": (15, "promoted pin video"),
    }

    format_seconds, format_desc = platform_format_map[platform]

    return f"""Generate a realistic ad performance data point with these specifications:

- platform: "{platform}" ({format_desc})
- industry: "{industry}"
- brand_tier: "{brand_tier}"
- performance_tier: "{performance_tier}"
- format_seconds: {format_seconds}

Return JSON with this exact structure:
{{
  "industry": "{industry}",
  "brand_tier": "{brand_tier}",
  "platform": "{platform}",
  "format_seconds": {format_seconds},
  "num_scenes": <int 2-12>,
  "scene_structure": [<list of scene archetype strings>],
  "has_mannequin": <bool>,
  "mannequin_screen_time_pct": <int 0-100>,
  "product_screen_time_pct": <int 0-100>,
  "pacing": "<slow|medium|fast>",
  "avg_scene_duration": <float>,
  "dominant_transition": "<cut|dissolve|fade>",
  "color_mood": "<warm|cool|neutral|vibrant|muted>",
  "lighting_style": "<natural|studio|dramatic|mixed>",
  "has_text_overlay": <bool>,
  "has_voiceover": <bool>,
  "has_music": <bool>,
  "music_style": "<ambient|upbeat|classical|electronic|acoustic>",
  "cta_type": "<none|shop_now|learn_more|swipe_up|visit_website>",
  "engagement_metrics": {{
    "view_completion_rate": <float 0-1>,
    "avg_watch_time_seconds": <float>,
    "like_rate": <float 0-1>,
    "comment_rate": <float 0-1>,
    "share_rate": <float 0-1>,
    "click_through_rate": <float 0-1>,
    "save_rate": <float 0-1>
  }},
  "performance_tier": "{performance_tier}",
  "key_success_factor": "<one sentence>",
  "optimization_suggestion": "<one sentence>"
}}

Make the creative attributes (scenes, pacing, transitions, etc.) realistic for a {industry} {brand_tier} brand on {platform}. Ensure metrics match the {performance_tier} tier."""


def generate_one(platform, index, industry, brand_tier, performance_tier, done_ids):
    """Generate a single performance data point via direct API call."""
    file_id = f"{platform}_{index:05d}"

    if file_id in done_ids:
        return None

    user_prompt = build_user_prompt(platform, industry, brand_tier, performance_tier, index)

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                temperature=0.9,
                max_tokens=1500,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_prompt},
                ],
            )

            content = response.choices[0].message.content
            data = json.loads(content)
            data["_file_id"] = file_id

            # Save to file
            output_dir = BASE_DIR / platform
            output_dir.mkdir(parents=True, exist_ok=True)

            with open(output_dir / f"{file_id}.json", "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            return file_id

        except Exception as e:
            error_str = str(e)
            if attempt < max_retries - 1:
                if "rate_limit" in error_str.lower() or "429" in error_str:
                    time.sleep(30)
                else:
                    time.sleep(5)
            else:
                return f"ERROR:{file_id}:{e}"

    return f"ERROR:{file_id}:max_retries_exceeded"


# ===================================================================
# MAIN LOGIC
# ===================================================================


def build_task_list():
    """Build the full list of tasks with randomized industry/tier assignments."""
    random.seed(42)  # Reproducible assignments
    tasks = []

    for platform, count in PLATFORM_DISTRIBUTION.items():
        for i in range(count):
            industry = random.choice(INDUSTRIES)
            brand_tier = random.choice(BRAND_TIERS)
            performance_tier = random.choice(PERFORMANCE_TIERS)
            tasks.append((platform, i, industry, brand_tier, performance_tier))

    return tasks


def run():
    """Launch the generation of all performance data points."""
    # Scan existing files to determine what's done
    done_ids = scan_existing_files()
    progress = load_progress()
    # Merge file-based and progress-based tracking
    done_ids.update(progress.get("done_ids", []))

    tasks = build_task_list()
    total = len(tasks)
    already_done = sum(1 for t in tasks if f"{t[0]}_{t[1]:05d}" in done_ids)

    print(f"Total: {total} data points")
    print(f"  Already done: {already_done}")
    print(f"  Remaining:    {total - already_done}")
    print(f"  Est. cost:    ~${(total - already_done) * 0.0004:.2f}")
    print(f"\nLaunching with 5 parallel workers...\n")

    count = already_done
    errors = progress.get("errors", 0)
    batch_size = 100

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for batch_start in range(0, len(tasks), batch_size):
            batch = tasks[batch_start:batch_start + batch_size]

            futures = {}
            for task_args in batch:
                platform, idx, industry, brand_tier, perf_tier = task_args
                file_id = f"{platform}_{idx:05d}"

                if file_id in done_ids:
                    continue

                future = executor.submit(
                    generate_one, platform, idx, industry,
                    brand_tier, perf_tier, done_ids,
                )
                futures[future] = file_id

            for future in concurrent.futures.as_completed(futures):
                result = future.result()
                if result is None:
                    continue
                elif isinstance(result, str) and result.startswith("ERROR:"):
                    errors += 1
                    if errors % 10 == 0:
                        print(f"  Warning: {errors} errors so far")
                    if "rate_limit" in result.lower() or "429" in result:
                        print(f"  Rate limit hit -- pausing 30s...")
                        time.sleep(30)
                else:
                    count += 1
                    done_ids.add(result)
                    progress["done_ids"] = list(done_ids)
                    progress["completed"] = count
                    progress["errors"] = errors

                    if count % 100 == 0:
                        pct = count / total * 100
                        print(f"  Progress: {count}/{total} ({pct:.1f}%) -- last: {result}")

            # Save progress after each batch
            save_progress(progress)

    # Final statistics
    print(f"\n{'=' * 60}")
    print(f"DONE")
    print(f"  Total generated: {count}")
    print(f"  Errors:          {errors}")
    print(f"{'=' * 60}")

    print(f"\n  Per platform:")
    for platform, target in PLATFORM_DISTRIBUTION.items():
        platform_dir = BASE_DIR / platform
        actual = len(list(platform_dir.glob("*.json"))) if platform_dir.exists() else 0
        print(f"    {platform:<20}: {actual:>5}/{target}")


def status():
    """Display current progress."""
    done_ids = scan_existing_files()
    tasks = build_task_list()
    total = len(tasks)
    done = len(done_ids)
    pct = done / total * 100 if total > 0 else 0

    print(f"\nPROGRESS: {done}/{total} ({pct:.1f}%)")

    progress = load_progress()
    print(f"  Errors: {progress.get('errors', 0)}\n")

    for platform, target in PLATFORM_DISTRIBUTION.items():
        platform_dir = BASE_DIR / platform
        actual = len(list(platform_dir.glob("*.json"))) if platform_dir.exists() else 0
        pct_p = actual / target * 100 if target > 0 else 0
        bar_filled = int(pct_p / 5)
        bar = "#" * bar_filled + "." * (20 - bar_filled)
        print(f"  {platform:<20} {bar} {actual:>5}/{target} ({pct_p:.0f}%)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate 10,000 synthetic ad performance data points"
    )
    parser.add_argument("--run", action="store_true", help="Launch generation")
    parser.add_argument("--status", action="store_true", help="Show progress")
    args = parser.parse_args()

    if args.run:
        run()
    elif args.status:
        status()
    else:
        parser.print_help()
        print("\nRun: python3 generate_performance_data.py --run")
