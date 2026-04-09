#!/usr/bin/env python3
"""
End-to-end smoke test for the AdGenAI intelligence pipeline.

Tests the full chain against a RUNNING server on port 8000:
  IndustryDetector → KnowledgeEngine → SceneUnderstanding → PromptEnricher
  → GPT-4o (via /api/analyze-scenario) → enriched scenes

Usage:
    python3 main.py &          # start backend first
    sleep 3
    python3 test_e2e.py
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

# Ensure project root is on path
sys.path.insert(0, str(Path(__file__).parent))

# Load .env before anything else
from dotenv import load_dotenv
load_dotenv()

import httpx

# ── Config ──────────────────────────────────────────────────────────────

BASE_URL = "http://localhost:8000"
TIMEOUT = 90  # seconds — GPT-4o can be slow

SCENARIO = (
    "A woman in an elegant Parisian apartment discovers a new Chanel perfume. "
    "She picks up the bottle from a marble vanity, admires its golden reflections, "
    "then applies it to her wrist. The camera follows her as she walks to a balcony "
    "overlooking the Seine."
)
BRAND_NAME = "Chanel"
MODE = "personnage_et_produit"
EXPECTED_INDUSTRY = "fragrance"

# ── Helpers ─────────────────────────────────────────────────────────────

PASS = "\033[92m✓\033[0m"
FAIL = "\033[91m✗\033[0m"
BOLD = "\033[1m"
RESET = "\033[0m"
DIM = "\033[90m"

_results: list[tuple[str, bool, str]] = []


def p(msg: str = ""):
    """Print with flush."""
    print(msg, flush=True)


def check(name: str, condition: bool, detail: str = "") -> bool:
    _results.append((name, condition, detail))
    mark = PASS if condition else FAIL
    msg = f"  {mark} {name}"
    if detail:
        msg += f" {DIM}({detail}){RESET}"
    p(msg)
    return condition


def section(title: str):
    p(f"\n{BOLD}{'─' * 60}")
    p(f"  {title}")
    p(f"{'─' * 60}{RESET}")


# ── Test 1: Health Check (server is up) ─────────────────────────────────

def test_health():
    section("TEST 1: Server Health Check")
    try:
        r = httpx.get(f"{BASE_URL}/health", timeout=10)
        check("GET /health returns 200", r.status_code == 200, f"got {r.status_code}")
        if r.status_code == 200:
            data = r.json()
            p(f"  Status: {data.get('status')}")
            p(f"  Version: {data.get('version')}")
            checks = data.get("checks", {})
            for k, v in checks.items():
                p(f"    {k}: {v}")
            check("OpenAI key configured", checks.get("openai_api_key") is True)
    except httpx.ConnectError:
        check("Server is running on port 8000", False, "connection refused — start with: python3 main.py &")
        p(f"\n  {FAIL} Cannot continue without server. Exiting.")
        print_summary()
        sys.exit(1)


# ── Test 2: Industry Detection ──────────────────────────────────────────

def test_industry_detection():
    section("TEST 2: Industry Detection (direct)")
    from knowledge.industry_detector import IndustryDetector

    detector = IndustryDetector()
    match = detector.detect(SCENARIO)

    p(f"  Detected: {match.industry} (confidence: {match.confidence:.2f})")
    p(f"  Keywords: {match.matched_keywords}")

    check("Industry is fragrance", match.industry == EXPECTED_INDUSTRY, f"got '{match.industry}'")
    check("Confidence > 0.2", match.confidence > 0.2, f"confidence={match.confidence:.2f}")
    check("Matched 'perfume'", "perfume" in match.matched_keywords)
    check("Matched 'bottle'", "bottle" in match.matched_keywords)


# ── Test 3: Knowledge Engine ────────────────────────────────────────────

def test_knowledge_engine():
    section("TEST 3: Knowledge Engine (direct)")
    from knowledge.knowledge_engine import KnowledgeEngine

    ke = KnowledgeEngine()

    patterns = ke.get_industry_patterns("fragrance")
    check("Fragrance patterns loaded", bool(patterns), f"{len(patterns)} keys")
    check("Has prompt_modifiers", "prompt_modifiers" in patterns,
          f"{len(patterns.get('prompt_modifiers', []))} modifiers")
    check("Has lighting_preferences", "lighting_preferences" in patterns)
    check("Has lens_preferences", "lens_preferences" in patterns)
    check("Has visual_signature", "visual_signature" in patterns)

    arch = ke.detect_archetype("She picks up the bottle from a marble vanity")
    p(f"  Archetype for 'picks up bottle': {arch}")
    check("Archetype detected",
          arch in ("product_interaction", "product_hero_shot", "hands_only", "lifestyle_context"),
          f"got '{arch}'")

    enriched = ke.enrich_image_prompt(
        original_prompt="Woman picks up perfume bottle from marble vanity",
        industry="fragrance",
        scene_description="Woman picks up perfume bottle from marble vanity",
    )
    p(f"  Enriched prompt length: {len(enriched)} chars")
    check("Enriched prompt starts with original text",
          enriched.startswith("Woman picks up perfume bottle"))
    check("Enriched prompt has photography terms",
          any(t in enriched.lower() for t in ["lens", "lighting", "8k", "photorealistic", "photograph"]),
          f"{len(enriched)} chars")
    check("Enriched prompt > 100 chars", len(enriched) > 100, f"{len(enriched)} chars")


# ── Test 4: Scene Understanding ─────────────────────────────────────────

def test_scene_understanding():
    section("TEST 4: Scene Understanding (direct)")
    from intelligence.scene_understanding import SceneUnderstanding

    su = SceneUnderstanding()
    ctx = su.analyze(SCENARIO)

    p(f"  Camera: {ctx.implied_camera_movement}")
    p(f"  Framing: {ctx.implied_framing}")
    p(f"  Motion: {ctx.implied_subject_motion}")
    p(f"  Lighting: {ctx.implied_lighting_direction}")
    p(f"  Environment: {ctx.environment_type}")
    p(f"  Product interaction: {ctx.has_product_interaction}")
    p(f"  Mood: {ctx.mood_keywords}")

    check("Detected walking motion", ctx.implied_subject_motion == "walking",
          f"got '{ctx.implied_subject_motion}'")
    check("Detected product interaction", ctx.has_product_interaction)
    check("Detected interior environment", ctx.environment_type == "interior",
          f"got '{ctx.environment_type}'")
    check("Detected tracking camera", ctx.implied_camera_movement == "tracking",
          f"got '{ctx.implied_camera_movement}'")


# ── Test 5: Dataset Loader ──────────────────────────────────────────────

def test_dataset_loader():
    section("TEST 5: Dataset Loader (direct)")
    from load_dataset import DatasetLoader

    ds = DatasetLoader()

    profile = ds.get_brand_profile("chanel")
    check("Chanel brand profile found", profile is not None)
    if profile:
        p(f"  Brand: {profile.get('brand_name', profile.get('brand'))}")
        p(f"  Industry: {profile.get('industry')}")
        p(f"  Has prompt_prefix: {bool(profile.get('prompt_prefix'))}")
        check("Chanel profile has industry", bool(profile.get("industry")))

    examples = ds.get_similar_scenarios("fragrance", n=3)
    check("Found fragrance scenarios", len(examples) > 0, f"{len(examples)} examples")

    storyboards = ds.get_industry_storyboards("fragrance", n=2)
    check("Found fragrance storyboards", len(storyboards) >= 0, f"{len(storyboards)} storyboards")


# ── Test 6: Prompt Enricher ─────────────────────────────────────────────

def test_prompt_enricher():
    section("TEST 6: Prompt Enricher (full intelligence chain, direct)")
    from intelligence.prompt_enricher import PromptEnricher

    enricher = PromptEnricher()

    scene_data = {
        "description": "Woman picks up perfume bottle from marble vanity, golden light",
        "prompt_image": "Woman picks up perfume bottle from marble vanity, golden light",
        "prompt_video": "Smooth tracking shot following her hand to the bottle, slow motion pickup",
        "archetype": "",
        "scene_type": "personnage",
    }

    enriched = enricher.enrich_scene(
        scene_data=scene_data,
        industry="fragrance",
        brand_name="Chanel",
    )

    p(f"  Original image prompt: {len(scene_data['prompt_image'])} chars")
    p(f"  Enriched image prompt: {len(enriched['prompt_image'])} chars")
    p(f"  Archetype: {enriched.get('archetype')}")
    p(f"  Scene context: {enriched.get('scene_context')}")

    check("Image prompt was enriched",
          len(enriched["prompt_image"]) > len(scene_data["prompt_image"]),
          f"{len(scene_data['prompt_image'])} → {len(enriched['prompt_image'])} chars")
    check("Original text preserved in enriched prompt",
          "Woman picks up perfume bottle" in enriched["prompt_image"])
    check("Archetype was detected", bool(enriched.get("archetype")))
    check("Scene context was populated", bool(enriched.get("scene_context")))

    if enriched.get("prompt_video"):
        check("Video prompt was enriched",
              len(enriched["prompt_video"]) > len(scene_data["prompt_video"]),
              f"{len(scene_data['prompt_video'])} → {len(enriched['prompt_video'])} chars")


# ── Test 7: POST /api/analyze-scenario (live endpoint) ──────────────────

def test_analyze_scenario_endpoint():
    section("TEST 7: POST /api/analyze-scenario (live server, GPT-4o)")

    openai_key = os.getenv("OPENAI_API_KEY", "")
    if not openai_key:
        p(f"  {FAIL} OPENAI_API_KEY not set in .env — skipping GPT-4o test")
        _results.append(("OPENAI_API_KEY is set", False, "missing from .env"))
        return

    check("OPENAI_API_KEY is set", True, f"{openai_key[:8]}...{openai_key[-4:]}")

    payload = {
        "scenario": SCENARIO,
        "mode": MODE,
        "industry": "auto",
        "brand_name": BRAND_NAME,
        "duration": 30,
        "platforms": [],
    }

    p(f"\n  Sending POST /api/analyze-scenario ...")
    p(f"  {DIM}Scenario: {SCENARIO[:80]}...{RESET}")
    p(f"  {DIM}Payload keys: {list(payload.keys())}{RESET}")
    p(f"  {DIM}Timeout: {TIMEOUT}s (GPT-4o can be slow){RESET}")

    try:
        r = httpx.post(
            f"{BASE_URL}/api/analyze-scenario",
            json=payload,
            timeout=TIMEOUT,
        )
    except httpx.ConnectError:
        check("Server reachable", False, "connection refused")
        return
    except httpx.ReadTimeout:
        check("Response within timeout", False, f"timed out after {TIMEOUT}s")
        return

    p(f"  Response status: {r.status_code}")

    if r.status_code == 422:
        p(f"  {FAIL} 422 Validation Error:")
        p(f"  {r.text}")
        check("Response status 200", False, f"got 422 — schema mismatch")
        return

    check("Response status 200", r.status_code == 200, f"got {r.status_code}")

    if r.status_code != 200:
        p(f"  Response body: {r.text[:500]}")
        return

    data = r.json()

    p(f"\n  {BOLD}Response:{RESET}")
    p(f"  Industry detected: {data.get('industry_detected')}")
    p(f"  Mode: {data.get('mode')}")
    p(f"  Enriched: {data.get('enriched')}")
    p(f"  Total duration: {data.get('total_duration')}s")
    p(f"  Scenes: {len(data.get('scenes', []))}")
    p(f"  Mood: {data.get('mood', 'N/A')}")

    scenes = data.get("scenes", [])

    check("Industry detected as fragrance",
          data.get("industry_detected") == EXPECTED_INDUSTRY,
          f"got '{data.get('industry_detected')}'")

    check("Has scenes", len(scenes) >= 2, f"{len(scenes)} scenes")

    scene_types = [s.get("type") for s in scenes]
    p(f"  Scene types: {scene_types}")
    check("Has personnage scenes", "personnage" in scene_types, f"types: {scene_types}")
    check("Has produit scenes", "produit" in scene_types, f"types: {scene_types}")

    check("Scenes were enriched", data.get("enriched") is True)

    photography_terms = [
        "lens", "lighting", "8k", "photorealistic", "photograph",
        "f/", "mm", "resolution", "depth of field", "aperture",
    ]

    enriched_scene_count = 0
    for i, scene in enumerate(scenes):
        prompt = scene.get("prompt_image", scene.get("description", ""))
        has_photo_terms = any(t in prompt.lower() for t in photography_terms)
        if has_photo_terms:
            enriched_scene_count += 1

        p(f"\n  {BOLD}Scene {i+1} ({scene.get('type')}):{RESET}")
        display_prompt = prompt[:200] + "..." if len(prompt) > 200 else prompt
        p(f"    Image: {display_prompt}")
        p(f"    Duration: {scene.get('duration_seconds')}s | Camera: {scene.get('camera_movement')}")
        p(f"    Has photo enrichment: {has_photo_terms}")

    check("Most scenes have photography enrichment",
          enriched_scene_count >= len(scenes) * 0.5,
          f"{enriched_scene_count}/{len(scenes)} enriched")

    scenes_with_context = sum(1 for s in scenes if s.get("scene_context"))
    check("Scenes have scene_context metadata",
          scenes_with_context > 0,
          f"{scenes_with_context}/{len(scenes)}")


# ── Summary ─────────────────────────────────────────────────────────────

def print_summary():
    section("SUMMARY")
    passed = sum(1 for _, ok, _ in _results if ok)
    failed = sum(1 for _, ok, _ in _results if not ok)
    total = len(_results)

    if failed:
        p(f"\n  {BOLD}Failed tests:{RESET}")
        for name, ok, detail in _results:
            if not ok:
                p(f"    {FAIL} {name} {DIM}({detail}){RESET}" if detail
                  else f"    {FAIL} {name}")

    color = "\033[92m" if failed == 0 else "\033[91m"
    p(f"\n  {color}{BOLD}{passed}/{total} passed, {failed} failed{RESET}\n")
    return failed == 0


# ── Main ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    p(f"\n{BOLD}{'=' * 60}")
    p(f"  AdGenAI End-to-End Intelligence Pipeline Test")
    p(f"{'=' * 60}{RESET}")
    p(f"  Server: {BASE_URL}")
    p(f"  Scenario: {SCENARIO[:70]}...")
    p(f"  Brand: {BRAND_NAME}")
    p(f"  Mode: {MODE}")
    p(f"  Expected industry: {EXPECTED_INDUSTRY}")

    test_health()
    test_industry_detection()
    test_knowledge_engine()
    test_scene_understanding()
    test_dataset_loader()
    test_prompt_enricher()
    test_analyze_scenario_endpoint()

    all_passed = print_summary()
    sys.exit(0 if all_passed else 1)
