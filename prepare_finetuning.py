"""
╔══════════════════════════════════════════════════════════════════════╗
║  AdGenAI — Fine-Tuning Dataset Preparation                           ║
║                                                                      ║
║  Converts dataset/scenarios/ (50K raw scenarios) into OpenAI         ║
║  fine-tuning JSONL format. Picks 10,000 diverse, high-quality        ║
║  examples, splits 90/10 into train + validation.                     ║
║                                                                      ║
║  Output:                                                             ║
║    dataset/finetuning/train.jsonl                                    ║
║    dataset/finetuning/val.jsonl                                      ║
║    dataset/finetuning/stats.json                                     ║
║                                                                      ║
║  Usage:                                                              ║
║    python3 prepare_finetuning.py                                     ║
║    python3 prepare_finetuning.py --max-examples 10000                ║
╚══════════════════════════════════════════════════════════════════════╝
"""
from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path
from typing import Any

SCENARIOS_DIR = Path("dataset/scenarios")
OUTPUT_DIR = Path("dataset/finetuning")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

DEFAULT_MAX = 10_000
DEFAULT_VAL_FRAC = 0.10
APPROX_TOKEN_LIMIT = 4096


# Keep in sync with services/scenario/prompts.py SYSTEM_PROMPT_*.
FT_SYSTEM_PROMPT = (
    "You are AdGenAI's scenario analysis engine. Given a client advertising "
    "scenario, an industry, a mode (personnage_et_produit or produit_uniquement), "
    "and a target duration, decompose the scenario into 4-6 cinematic scenes. "
    "Each scene must include: scene_number, scene_type (personnage|produit|"
    "transition), prompt_image (detailed photorealistic image prompt, 3-5 "
    "sentences), prompt_video (Kling-ready animation prompt, 2-3 sentences), "
    "duration_seconds (2.0-5.0), camera_movement (static|dolly_in|dolly_out|"
    "orbit|zoom_in|zoom_out|pan_left|pan_right|crane_up|crane_down|tracking|"
    "handheld), transition, needs_mannequin, needs_decor_ref, original_text. "
    "The client's scenario text is SACRED — never rewrite it, only decompose. "
    "Respond with valid JSON only."
)


def _approx_tokens(text: str) -> int:
    """Rough token estimate (~4 chars per token for English mixed content)."""
    return max(1, len(text) // 4)


def _load_scenario_files() -> list[Path]:
    """Walk dataset/scenarios/ for all .json files, skipping progress/meta."""
    return [
        p
        for p in SCENARIOS_DIR.rglob("*.json")
        if not p.name.startswith("_")
    ]


def _load_json(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _quality_ok(scenario: dict) -> bool:
    """Filter out scenarios that would make bad training pairs."""
    if not scenario.get("scenario_text"):
        return False
    scenes = scenario.get("scenes") or []
    if len(scenes) < 3 or len(scenes) > 9:
        return False
    for scene in scenes:
        if not scene.get("prompt_image") or not scene.get("prompt_video"):
            return False
        if not scene.get("camera_movement"):
            return False
    return True


def _build_user_content(scenario: dict) -> str:
    industry = scenario.get("industry", "luxury")
    mode = scenario.get("mode", "personnage_et_produit")
    duration = scenario.get("duration_total_seconds", 30)
    scenario_text = (scenario.get("scenario_text") or "").strip()
    return (
        f"Industry: {industry}\n"
        f"Mode: {mode}\n"
        f"Duration: {duration}s\n"
        f"Scenario:\n{scenario_text}"
    )


def _build_assistant_content(scenario: dict) -> str:
    """Return the canonical JSON the model should learn to emit."""
    scenes_out = []
    for i, scene in enumerate(scenario.get("scenes", []), start=1):
        scenes_out.append({
            "scene_number": scene.get("index", i),
            "scene_type": scene.get("scene_type", "produit"),
            "prompt_image": scene.get("prompt_image", ""),
            "prompt_video": scene.get("prompt_video", ""),
            "duration_seconds": float(scene.get("duration_seconds", 3.5)),
            "camera_movement": scene.get("camera_movement", "static"),
            "transition": scene.get("transition", "cut"),
            "needs_mannequin": bool(scene.get("needs_mannequin", False)),
            "needs_decor_ref": bool(scene.get("needs_decor_ref", False)),
            "original_text": scene.get("description", "") or scene.get("original_text", ""),
        })
    payload = {
        "total_scenes": len(scenes_out),
        "estimated_duration": sum(s["duration_seconds"] for s in scenes_out),
        "mood": scenario.get("mood", ""),
        "scenes": scenes_out,
    }
    return json.dumps(payload, ensure_ascii=False)


def _build_messages(scenario: dict) -> list[dict[str, str]]:
    return [
        {"role": "system", "content": FT_SYSTEM_PROMPT},
        {"role": "user", "content": _build_user_content(scenario)},
        {"role": "assistant", "content": _build_assistant_content(scenario)},
    ]


def _token_fits(messages: list[dict[str, str]], limit: int) -> bool:
    total = sum(_approx_tokens(m["content"]) for m in messages) + 20  # overhead
    return total <= limit


def _select_diverse(scenarios: list[dict], max_examples: int) -> list[dict]:
    """Round-robin across (industry, mode, scene_count) buckets for diversity."""
    buckets: dict[tuple, list[dict]] = defaultdict(list)
    for sc in scenarios:
        key = (
            (sc.get("industry") or "unknown").lower(),
            sc.get("mode", "unknown"),
            min(len(sc.get("scenes") or []), 9),
        )
        buckets[key].append(sc)

    for bucket in buckets.values():
        random.shuffle(bucket)

    # Round-robin draw until we hit max_examples or run out
    selected: list[dict] = []
    keys = list(buckets.keys())
    random.shuffle(keys)
    while len(selected) < max_examples:
        progressed = False
        for k in keys:
            if buckets[k]:
                selected.append(buckets[k].pop())
                progressed = True
                if len(selected) >= max_examples:
                    break
        if not progressed:
            break
    return selected


def prepare(max_examples: int, val_frac: float) -> None:
    files = _load_scenario_files()
    print(f"📂 Found {len(files)} scenario files under {SCENARIOS_DIR}")
    if not files:
        print("❌ Nothing to do. Run generate_50k_scenarios.py first.")
        return

    raw: list[dict] = []
    bad = 0
    for path in files:
        data = _load_json(path)
        if data is None:
            bad += 1
            continue
        if not _quality_ok(data):
            bad += 1
            continue
        raw.append(data)

    print(f"✅ {len(raw)} pass quality filter ({bad} skipped)")

    selected = _select_diverse(raw, max_examples)
    print(f"🎯 Selected {len(selected)} diverse examples (cap {max_examples})")

    # Build messages and token-filter
    rows: list[dict] = []
    dropped_oversize = 0
    for sc in selected:
        msgs = _build_messages(sc)
        if not _token_fits(msgs, APPROX_TOKEN_LIMIT):
            dropped_oversize += 1
            continue
        rows.append({"messages": msgs})
    print(f"📏 {len(rows)} fit under {APPROX_TOKEN_LIMIT} tokens ({dropped_oversize} dropped)")

    random.shuffle(rows)
    val_count = max(1, int(len(rows) * val_frac))
    val_rows = rows[:val_count]
    train_rows = rows[val_count:]

    train_path = OUTPUT_DIR / "train.jsonl"
    val_path = OUTPUT_DIR / "val.jsonl"

    with train_path.open("w", encoding="utf-8") as f:
        for row in train_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    with val_path.open("w", encoding="utf-8") as f:
        for row in val_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    # Distribution stats
    industry_counts: dict[str, int] = defaultdict(int)
    mode_counts: dict[str, int] = defaultdict(int)
    for r in rows:
        user = r["messages"][1]["content"]
        for line in user.splitlines():
            if line.startswith("Industry:"):
                industry_counts[line.split(":", 1)[1].strip()] += 1
            if line.startswith("Mode:"):
                mode_counts[line.split(":", 1)[1].strip()] += 1

    stats: dict[str, Any] = {
        "total_scenarios_found": len(files),
        "passed_quality": len(raw),
        "selected_diverse": len(selected),
        "written_rows": len(rows),
        "train_count": len(train_rows),
        "val_count": len(val_rows),
        "dropped_oversize": dropped_oversize,
        "industry_distribution": dict(sorted(industry_counts.items())),
        "mode_distribution": dict(sorted(mode_counts.items())),
        "system_prompt": FT_SYSTEM_PROMPT,
    }
    (OUTPUT_DIR / "stats.json").write_text(
        json.dumps(stats, indent=2, ensure_ascii=False)
    )

    print(f"\n✅ Wrote:")
    print(f"   {train_path}  ({len(train_rows)} rows)")
    print(f"   {val_path}    ({len(val_rows)} rows)")
    print(f"   {OUTPUT_DIR / 'stats.json'}")
    print(f"\n📊 Industries: {dict(sorted(industry_counts.items()))}")
    print(f"📊 Modes:      {dict(mode_counts)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare AdGenAI fine-tuning JSONL")
    parser.add_argument("--max-examples", type=int, default=DEFAULT_MAX)
    parser.add_argument("--val-frac", type=float, default=DEFAULT_VAL_FRAC)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    random.seed(args.seed)
    prepare(args.max_examples, args.val_frac)


if __name__ == "__main__":
    main()
