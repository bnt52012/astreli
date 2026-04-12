"""
AdGenAI — FastAPI Entry Point.

Replaces traditional ad film shoots (EUR 50K-500K) with a 100% AI pipeline.
Marketing teams upload their scenario and assets, get a broadcast-quality
advertising video in minutes for a few dollars.

Endpoints:
  POST /pipeline/run          — Run the full pipeline
  POST /pipeline/estimate     — Cost estimation (analysis only)
  GET  /pipeline/status/{id}  — Check pipeline status
  POST /lora/train            — Train a new LoRA model
  GET  /lora/models           — List trained LoRA models
  GET  /health                — Health check
"""
from __future__ import annotations

import asyncio
import logging
import os
import random
import sys
import uuid as uuid_mod
from datetime import datetime
from pathlib import Path
from typing import Any, List, Optional
from urllib.parse import urlparse

try:
    from dotenv import load_dotenv
    # Load .env before reading fine-tune ID so run_finetuning.py writes are picked up.
    load_dotenv()
except ImportError:
    pass

# Fine-tuned model ID (written by run_finetuning.py on success). Falls back to
# vanilla gpt-4o for /api/analyze-scenario if unset or if the FT call errors.
FINETUNED_MODEL_ID = os.environ.get("FINETUNED_MODEL_ID", "").strip() or None
SCENARIO_FALLBACK_MODEL = "gpt-4o"

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from fastapi import FastAPI, HTTPException, BackgroundTasks, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, validator

from models.schemas import (
    CostEstimate,
    LoRAModel,
    LoRATrainingRequest,
    PipelineRequest,
    PipelineResult,
    PipelineStatus,
)
from pipeline.config import settings
from pipeline.orchestrator import PipelineOrchestrator
from utils.logging_config import setup_logging

# ── Logging ──────────────────────────────────────────────────────────
setup_logging(level="INFO")
logger = logging.getLogger(__name__)

# ── App ──────────────────────────────────────────────────────────────
app = FastAPI(
    title="AdGenAI",
    description="AI-powered advertising video production pipeline",
    version="3.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def _startup_warm_caches() -> None:
    """Warm expensive caches at boot so the first request isn't slow.

    - Loads the 1000 real-ad analyses (dataset/real_ads/) into KnowledgeEngine.
    - Logs whether a fine-tuned scenario model will be used.
    """
    try:
        from knowledge.knowledge_engine import KnowledgeEngine
        ke = KnowledgeEngine()
        count = ke.load_real_ads()
        logger.info("[startup] real-ad analyses loaded: %d", count)
    except Exception as e:
        logger.warning("[startup] failed to warm real-ads cache: %s", e)

    if FINETUNED_MODEL_ID:
        logger.info(
            "[startup] scenario model: FINETUNED_MODEL_ID=%s (fallback=%s)",
            FINETUNED_MODEL_ID, SCENARIO_FALLBACK_MODEL,
        )
    else:
        logger.info(
            "[startup] scenario model: %s (no fine-tuned model set)",
            SCENARIO_FALLBACK_MODEL,
        )

# ── In-memory job tracking ───────────────────────────────────────────
_jobs: dict[str, dict[str, Any]] = {}


def _progress_callback(project_id: str):
    """Create a progress callback that updates the job store."""
    def callback(data: dict[str, Any]) -> None:
        _jobs[project_id] = {
            "project_id": project_id,
            "status": data.get("step", "running"),
            "progress": data.get("progress", 0.0),
            "message": data.get("message", ""),
        }
    return callback


# ── Pipeline Endpoints ───────────────────────────────────────────────

@app.post("/pipeline/run", response_model=None)
async def run_pipeline(request: PipelineRequest, background_tasks: BackgroundTasks):
    """Run the full AdGenAI pipeline.

    The pipeline runs in the background. Use /pipeline/status/{project_id}
    to check progress.
    """
    import uuid
    project_id = str(uuid.uuid4())[:8]

    _jobs[project_id] = {
        "project_id": project_id,
        "status": "queued",
        "progress": 0.0,
        "message": "Pipeline queued...",
    }

    async def run_bg():
        orchestrator = PipelineOrchestrator(
            on_progress=_progress_callback(project_id),
        )
        try:
            result = await orchestrator.run(
                project_id=project_id,
                scenario=request.scenario,
                lora_model_id=request.lora_model_id,
                product_photos=request.product_photos,
                decor_photos=request.decor_photos,
                logo_path=request.logo_path,
                music_path=request.music_path,
                brand_name=request.brand_name,
                aspect_ratio=request.aspect_ratio,
            )
            _jobs[project_id] = {
                "project_id": project_id,
                "status": result.get("status", "completed"),
                "progress": 1.0,
                "message": "Complete",
                "result": result,
            }
        except Exception as e:
            _jobs[project_id] = {
                "project_id": project_id,
                "status": "failed",
                "progress": 0.0,
                "message": str(e),
            }
            logger.exception("Pipeline failed for %s", project_id)

    background_tasks.add_task(lambda: asyncio.run(run_bg()))

    return {"project_id": project_id, "status": "queued", "message": "Pipeline started."}


@app.post("/pipeline/estimate")
async def estimate_cost(request: PipelineRequest):
    """Estimate pipeline cost without running generation."""
    orchestrator = PipelineOrchestrator()
    try:
        estimate = await orchestrator.estimate_cost(
            scenario=request.scenario,
            lora_model_id=request.lora_model_id,
        )
        return estimate
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/pipeline/status/{project_id}")
async def pipeline_status(project_id: str):
    """Check pipeline progress."""
    job = _jobs.get(project_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")
    return job


@app.get("/pipeline/result/{project_id}")
async def pipeline_result(project_id: str):
    """Get pipeline result with download link."""
    job = _jobs.get(project_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Project {project_id} not found")

    result = job.get("result")
    if not result:
        return {"status": job.get("status"), "message": "Not yet complete"}

    return result


@app.get("/pipeline/download/{project_id}")
async def download_video(project_id: str):
    """Download the final video."""
    job = _jobs.get(project_id)
    if not job or not job.get("result"):
        raise HTTPException(status_code=404, detail="Video not ready")

    video_path = Path(job["result"].get("output_video", ""))
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video file not found")

    return FileResponse(
        path=str(video_path),
        media_type="video/mp4",
        filename=f"adgenai_{project_id}.mp4",
    )


# ── LoRA Endpoints ───────────────────────────────────────────────────

@app.post("/lora/train")
async def train_lora(request: LoRATrainingRequest, background_tasks: BackgroundTasks):
    """Start LoRA training for a mannequin."""
    from services.lora.trainer import LoRATrainer
    from services.lora.manager import LoRAManager

    trainer = LoRATrainer()

    try:
        valid = trainer.validate_training_images(request.training_images)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    import uuid
    model_id = str(uuid.uuid4())[:8]

    async def train_bg():
        try:
            result = await trainer.start_training(
                image_paths=valid,
                trigger_word=request.trigger_word,
                model_name=request.name,
            )
            # Poll for completion
            poll_result = await trainer.poll_training(result["training_id"])

            if poll_result["status"] == "succeeded":
                manager = LoRAManager()
                manager.save_model(
                    model_id=model_id,
                    name=request.name,
                    trigger_word=request.trigger_word,
                    replicate_version=poll_result.get("model_version", ""),
                )
        except Exception as e:
            logger.error("LoRA training failed: %s", e)

    background_tasks.add_task(lambda: asyncio.run(train_bg()))

    return {"model_id": model_id, "status": "training", "message": "Training started (~15-20 min)."}


@app.get("/lora/models")
async def list_lora_models(account_id: str = "default"):
    """List all trained LoRA models."""
    from services.lora.manager import LoRAManager
    manager = LoRAManager()
    return manager.list_models(account_id)


@app.delete("/lora/models/{model_id}")
async def delete_lora_model(model_id: str):
    """Delete a LoRA model."""
    from services.lora.manager import LoRAManager
    manager = LoRAManager()
    if manager.delete_model(model_id):
        return {"status": "deleted"}
    raise HTTPException(status_code=404, detail="Model not found")


# ── Frontend Demo API ────────────────────────────────────────────────

# -- Request / Response Models --

class BrandAnalyzeRequest(BaseModel):
    url: str

    class Config:
        schema_extra = {"example": {"url": "www.chanel.com"}}


class ScenarioAnalyzeRequest(BaseModel):
    scenario: str
    mode: str = "personnage_et_produit"
    industry: str = "auto"
    brand_name: Optional[str] = None
    duration: int = 30
    platforms: List[str] = []
    brand_colors: List[str] = []
    brand_mood: Optional[str] = None
    brand_keywords: List[str] = []

    @validator("mode")
    def validate_mode(cls, v):
        # Map frontend shorthand to backend mode names
        _mode_aliases = {
            "mannequin": "personnage_et_produit",
            "product": "produit_uniquement",
            "personnage": "personnage_et_produit",
            "produit": "produit_uniquement",
        }
        v = _mode_aliases.get(v, v)
        allowed = {"personnage_et_produit", "produit_uniquement"}
        if v not in allowed:
            raise ValueError(f"mode must be one of {allowed}")
        return v

    class Config:
        schema_extra = {
            "example": {
                "scenario": "A model presents a luxury serum in a golden-lit studio.",
                "mode": "personnage_et_produit",
                "industry": "auto",
                "brand_name": "Chanel",
                "duration": 30,
            }
        }


_PLATFORM_ASPECT_MAP: dict[str, str] = {
    "instagram reels": "9:16",
    "instagram stories": "9:16",
    "tiktok": "9:16",
    "youtube": "16:9",
    "tv 16:9": "16:9",
    "linkedin": "1:1",
    "facebook": "1:1",
}

_ASPECT_RESOLUTION: dict[str, str] = {
    "9:16": "1080:1920",
    "16:9": "1920:1080",
    "1:1": "1080:1080",
}


def _resolve_aspect_ratio(platforms: list[str], explicit: str = "") -> str:
    """Derive aspect ratio from selected platforms, or fallback to explicit."""
    if platforms:
        # Prefer vertical if any vertical platform is selected
        for p in platforms:
            ar = _PLATFORM_ASPECT_MAP.get(p.lower())
            if ar:
                return ar
    return explicit or "16:9"


class GenerateRequest(BaseModel):
    brand_name: str
    scenario: str
    scenes: list = []
    lora_model_id: Optional[str] = None
    aspect_ratio: str = "16:9"
    style: Optional[str] = None
    platforms: List[str] = []
    duration: int = 30
    # Product metadata from the frontend "Brand Setup" step
    product_name: Optional[str] = None
    product_category: Optional[str] = None
    # Reference images as base64 data URLs (data:image/png;base64,...) or bare base64.
    product_images: List[str] = []
    brand_logo: Optional[str] = None
    # Brand visual DNA (from /api/analyze-brand result, passed through by frontend)
    brand_colors: List[str] = []
    brand_mood: Optional[str] = None
    brand_prompt_prefix: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "brand_name": "Chanel",
                "scenario": "A model presents a luxury serum.",
                "scenes": [],
                "lora_model_id": "lora_001",
            }
        }


class LoRATrainDemoRequest(BaseModel):
    model_name: str
    trigger_word: Optional[str] = None
    training_images: list = []

    class Config:
        schema_extra = {
            "example": {
                "model_name": "Sophie Martin",
                "trigger_word": "SOPHIE",
            }
        }


# -- In-memory stores for demo API --

_demo_jobs: dict[str, dict[str, Any]] = {}
_demo_lora_models: dict[str, dict[str, Any]] = {
    "lora_001": {
        "model_id": "lora_001",
        "name": "Sophie Martin",
        "status": "ready",
        "created_at": "2026-03-15",
        "preview_url": None,
        "trigger_word": "SOPHIE",
    },
    "lora_002": {
        "model_id": "lora_002",
        "name": "Emma Laurent",
        "status": "ready",
        "created_at": "2026-03-20",
        "preview_url": None,
        "trigger_word": "EMMA",
    },
}


def _extract_brand_name(url: str) -> str:
    """Extract a brand name from a URL domain."""
    cleaned = url.strip()
    if not cleaned.startswith(("http://", "https://")):
        cleaned = "https://" + cleaned
    parsed = urlparse(cleaned)
    hostname = parsed.hostname or ""
    # Remove www. prefix and TLD
    parts = hostname.replace("www.", "").split(".")
    brand = parts[0] if parts else "Brand"
    return brand.capitalize()


def _generate_mock_scenes(scenario: str, mode: str) -> tuple[list[dict[str, Any]], float]:
    """Generate 4-6 realistic mock scenes based on scenario text."""
    camera_movements = ["dolly_in", "pan_left", "static", "crane_up", "tracking", "slow_zoom"]
    transitions = ["fade_from_black", "cut", "dissolve", "cross_fade", "wipe", "fade_to_white"]

    personnage_descriptions = [
        "Close-up of model applying the product, soft Rembrandt lighting",
        "Medium shot of talent walking toward camera, backlit golden hour",
        "Over-the-shoulder shot revealing product in mirror reflection",
        "Profile silhouette of model against gradient background",
        "Slow-motion hair movement, rim-lit with warm tones",
        "Hands delicately holding product, macro detail shot",
    ]

    product_descriptions = [
        "Hero shot of product rotating on reflective surface",
        "Extreme close-up of product texture with anamorphic flare",
        "Product emerging from silk fabric, top-down angle",
        "Splash of liquid gold around the product, high-speed capture",
        "Product placed in botanical arrangement, natural light",
        "Final pack shot with logo resolve, clean white backdrop",
    ]

    num_scenes = random.randint(4, 6)
    scenes = []
    total_duration = 0.0

    for i in range(num_scenes):
        if mode == "produit_uniquement":
            desc = random.choice(product_descriptions)
            scene_type = "produit"
        else:
            # Alternate between personnage and produit
            if i % 2 == 0:
                desc = random.choice(personnage_descriptions)
                scene_type = "personnage"
            else:
                desc = random.choice(product_descriptions)
                scene_type = "produit"

        duration = round(random.uniform(2.5, 5.0), 1)
        total_duration += duration

        scenes.append({
            "scene_number": i + 1,
            "type": scene_type,
            "description": desc,
            "duration_seconds": duration,
            "camera_movement": random.choice(camera_movements),
            "transition": transitions[0] if i == 0 else random.choice(transitions[1:]),
        })

    return scenes, round(total_duration, 1)


# -- Endpoints --

@app.post("/api/analyze-brand")
async def analyze_brand(request: BrandAnalyzeRequest):
    """Analyze a brand's visual identity via web scraping + Instagram + GPT-4o."""
    from services.brand_analyzer import analyze_brand as _analyze

    result = _analyze(url=request.url, openai_api_key=settings.openai_api_key)
    return result


@app.post("/api/analyze-scenario")
async def analyze_scenario(request: ScenarioAnalyzeRequest):
    """Decompose a scenario into scenes using GPT-4o + knowledge engine + RAG."""
    import json as json_mod

    # 1. Detect industry if "auto"
    industry = request.industry
    if industry == "auto":
        try:
            from knowledge.industry_detector import IndustryDetector
            detector = IndustryDetector()
            match = detector.detect(request.scenario)
            industry = match.industry
            logger.info("Auto-detected industry: %s (confidence: %.2f)", industry, match.confidence)
        except Exception as e:
            logger.warning("Industry detection failed: %s — defaulting to luxury", e)
            industry = "luxury"

    # 2. Load industry patterns for context
    try:
        from knowledge.knowledge_engine import KnowledgeEngine
        ke = KnowledgeEngine()
        patterns = ke.get_industry_patterns(industry)
        pattern_context = (
            f"Industry: {industry}. "
            f"Visual signature: {patterns.get('visual_signature', {})}. "
            f"Movement style: {patterns.get('movement_style', {})}. "
            f"Banned elements: {patterns.get('banned_elements', [])}."
        )
    except Exception:
        pattern_context = f"Industry: {industry}."

    # 3. Load brand profile if available
    brand_context = ""
    if request.brand_name:
        try:
            from load_dataset import DatasetLoader
            ds = DatasetLoader()
            profile = ds.get_brand_profile(request.brand_name)
            if profile:
                brand_context = (
                    f"Brand: {profile.get('brand_name')}. "
                    f"Essence: {profile.get('brand_essence', '')}. "
                    f"Prompt prefix: {profile.get('prompt_prefix', '')}."
                )
        except Exception:
            pass

    # 4. Load few-shot example scenarios from dataset (RAG)
    rag_examples = ""
    try:
        from load_dataset import DatasetLoader
        ds = DatasetLoader()
        examples = ds.get_similar_scenarios(industry, mode=request.mode, n=3)
        if examples:
            parts = []
            for ex in examples[:3]:
                parts.append(
                    f"- Brand: {ex.get('brand', 'N/A')}, "
                    f"Scenario: {ex.get('scenario_text', ex.get('scenario', ''))[:200]}"
                )
            rag_examples = "EXAMPLE SCENARIOS FROM THIS INDUSTRY:\n" + "\n".join(parts)
    except Exception:
        pass

    # 5. Build system prompt with knowledge context
    from services.scenario.prompts import (
        SYSTEM_PROMPT_MIXED,
        SYSTEM_PROMPT_PRODUCT_ONLY,
        build_scenario_user_prompt,
    )
    base_prompt = (
        SYSTEM_PROMPT_MIXED if request.mode == "personnage_et_produit"
        else SYSTEM_PROMPT_PRODUCT_ONLY
    )
    system_prompt = (
        f"{base_prompt}\n\n"
        f"INDUSTRY KNOWLEDGE:\n{pattern_context}\n\n"
        f"{brand_context}\n\n"
        f"{rag_examples}"
    )

    # Build the runtime user prompt that injects brand/duration/platform/aspect
    user_prompt = build_scenario_user_prompt(
        request.scenario,
        brand_name=request.brand_name,
        industry=industry,
        duration=request.duration,
        platforms=request.platforms,
        brand_colors=request.brand_colors,
        brand_mood=request.brand_mood,
        brand_keywords=request.brand_keywords,
    )

    logger.info(
        "[analyze-scenario] mode=%s industry=%s brand=%s duration=%ds platforms=%s "
        "colors=%s mood=%s",
        request.mode, industry, request.brand_name, request.duration,
        request.platforms, request.brand_colors, request.brand_mood,
    )
    logger.debug("[analyze-scenario] system_prompt=\n%s", system_prompt)
    logger.debug("[analyze-scenario] user_prompt=\n%s", user_prompt)

    # 6. Call the scenario model. Prefer the fine-tuned model if FINETUNED_MODEL_ID
    # is set in .env (written by run_finetuning.py on success); fall back to
    # gpt-4o transparently on any error (model not found, rate limit, etc.).
    try:
        from openai import OpenAI
        client = OpenAI(api_key=settings.openai_api_key)

        primary_model = FINETUNED_MODEL_ID or SCENARIO_FALLBACK_MODEL
        models_to_try: list[str] = [primary_model]
        if FINETUNED_MODEL_ID and SCENARIO_FALLBACK_MODEL not in models_to_try:
            models_to_try.append(SCENARIO_FALLBACK_MODEL)

        resp = None
        last_err: Exception | None = None
        used_model: str | None = None
        for candidate in models_to_try:
            try:
                logger.info("[analyze-scenario] calling model=%s", candidate)
                resp = client.chat.completions.create(
                    model=candidate,
                    temperature=0.3,
                    max_tokens=8192,
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                )
                used_model = candidate
                break
            except Exception as inner_err:
                last_err = inner_err
                logger.warning(
                    "[analyze-scenario] model %s failed: %s — trying next",
                    candidate, inner_err,
                )
        if resp is None:
            raise last_err or RuntimeError("No scenario model responded")

        raw_content = resp.choices[0].message.content or "{}"
        parsed = json_mod.loads(raw_content)
        logger.info(
            "[analyze-scenario] %s returned %d scenes (total_scenes=%s, estimated_duration=%s)",
            used_model,
            len(parsed.get("scenes", [])),
            parsed.get("total_scenes", "?"),
            parsed.get("estimated_duration", "?"),
        )

        # ── URGENT DEBUG: dump every scene returned by GPT-4o ────────
        for scene in parsed.get("scenes", []):
            print(f"\n--- SCENE {scene.get('scene_number', scene.get('index', '?'))} ---", flush=True)
            print(f"Type: {scene.get('scene_type')}", flush=True)
            print(f"Camera: {scene.get('camera_movement')}", flush=True)
            print(f"Duration: {scene.get('duration_seconds')}s", flush=True)
            print(f"prompt_image: {(scene.get('prompt_image') or 'EMPTY')[:200]}", flush=True)
            print(f"prompt_video: {(scene.get('prompt_video') or 'EMPTY')[:200]}", flush=True)
            print(f"---", flush=True)

        # Hard guard: if GPT-4o returned fewer than 3 scenes, log and let downstream handle it
        if len(parsed.get("scenes", [])) < 3:
            logger.warning(
                "[analyze-scenario] GPT-4o returned only %d scenes — below minimum of 4",
                len(parsed.get("scenes", [])),
            )
    except Exception as e:
        logger.warning("GPT-4o scenario analysis failed: %s — using mock fallback", e)
        scenes, total_duration = _generate_mock_scenes(request.scenario, request.mode)
        return {
            "scenes": scenes,
            "total_duration": total_duration,
            "industry_detected": industry,
            "mode": request.mode,
            "enriched": False,
        }

    # 7. Normalize scenes to frontend format
    raw_scenes = parsed.get("scenes", [])
    if not raw_scenes:
        logger.warning("GPT-4o returned 0 scenes — falling back to mock")
        scenes, total_duration = _generate_mock_scenes(request.scenario, request.mode)
        return {
            "scenes": scenes,
            "total_duration": total_duration,
            "industry_detected": industry,
            "mode": request.mode,
            "enriched": False,
        }

    scenes = []
    for i, s in enumerate(raw_scenes):
        duration = s.get("duration_seconds", 3.5)
        # Clamp duration to 2-5 second range
        duration = max(2.0, min(5.0, float(duration)))
        scenes.append({
            "scene_number": s.get("scene_number", i + 1),
            "type": s.get("scene_type", s.get("type", "produit")),
            "description": s.get("prompt_image", s.get("description", "")),
            "duration_seconds": duration,
            "camera_movement": s.get("camera_movement", "static"),
            "transition": s.get("transition", "cut"),
            "prompt_image": s.get("prompt_image", ""),
            "prompt_video": s.get("prompt_video", ""),
            "needs_mannequin": s.get("needs_mannequin", False),
            "original_text": s.get("original_text", ""),
        })

    # 8. Enrich all scenes through intelligence module
    try:
        from intelligence.prompt_enricher import PromptEnricher
        enricher = PromptEnricher()
        scenes = enricher.enrich_all_scenes(
            scenes, industry=industry, brand_name=request.brand_name
        )
        enriched = True
    except Exception as e:
        logger.warning("Scene enrichment failed: %s", e)
        enriched = False

    total_duration = sum(s.get("duration_seconds", 3.0) for s in scenes)

    return {
        "scenes": scenes,
        "total_duration": round(total_duration, 1),
        "industry_detected": industry,
        "mode": request.mode,
        "mood": parsed.get("mood", ""),
        "color_palette": parsed.get("color_palette", []),
        "enriched": enriched,
    }


@app.post("/api/generate")
async def generate_video(request: GenerateRequest, background_tasks: BackgroundTasks):
    """Start REAL video generation pipeline.

    1. Convert scene dicts → ScenePipeline objects
    2. Generate images with Gemini
    3. Animate with Kling AI
    4. Assemble with FFmpeg
    """
    import os, base64, io
    from PIL import Image as PILImage
    job_id = str(uuid_mod.uuid4())[:12]
    job_dir = Path(f"/tmp/astreli_jobs/{job_id}")
    job_dir.mkdir(parents=True, exist_ok=True)
    (job_dir / "images").mkdir(exist_ok=True)
    (job_dir / "videos").mkdir(exist_ok=True)
    (job_dir / "refs").mkdir(exist_ok=True)

    # ── Decode reference images (product photos + logo) ─────────────
    reference_pil_images: list = []
    for idx, data_url in enumerate(request.product_images or []):
        try:
            payload = data_url.split(",", 1)[1] if data_url.startswith("data:") else data_url
            img_bytes = base64.b64decode(payload)
            img = PILImage.open(io.BytesIO(img_bytes)).convert("RGB")
            reference_pil_images.append(img)
            # Persist for debugging / inspection
            img.save(job_dir / "refs" / f"product_{idx+1}.png")
            logger.info("Job %s: decoded product reference %d (%dx%d)", job_id, idx + 1, img.width, img.height)
        except Exception as e:
            logger.warning("Job %s: failed to decode product image %d: %s", job_id, idx + 1, e)

    if request.brand_logo:
        try:
            payload = request.brand_logo.split(",", 1)[1] if request.brand_logo.startswith("data:") else request.brand_logo
            logo_bytes = base64.b64decode(payload)
            logo_img = PILImage.open(io.BytesIO(logo_bytes)).convert("RGB")
            reference_pil_images.append(logo_img)
            logo_img.save(job_dir / "refs" / "logo.png")
            logger.info("Job %s: decoded brand logo (%dx%d)", job_id, logo_img.width, logo_img.height)
        except Exception as e:
            logger.warning("Job %s: failed to decode brand logo: %s", job_id, e)

    logger.info("Job %s: %d reference images loaded", job_id, len(reference_pil_images))

    # Ensure FFmpeg is findable
    ffmpeg_dirs = ["/opt/homebrew/bin", "/usr/local/bin", "/usr/bin"]
    for d in ffmpeg_dirs:
        if d not in os.environ.get("PATH", ""):
            os.environ["PATH"] = d + ":" + os.environ.get("PATH", "")

    # ── Resolve aspect ratio from platforms ─────────────────────────
    aspect_ratio = _resolve_aspect_ratio(request.platforms, request.aspect_ratio)
    resolution = _ASPECT_RESOLUTION.get(aspect_ratio, "1920x1080")
    logger.info("Job %s: aspect=%s resolution=%s platforms=%s", job_id, aspect_ratio, resolution, request.platforms)

    _demo_jobs[job_id] = {
        "job_id": job_id,
        "status": "queued",
        "progress": 0.0,
        "phase": "queued",
        "message": "Job queued...",
        "result": None,
        "scenes": [{"id": i + 1, "status": "pending"} for i, _ in enumerate(request.scenes)],
    }

    # ── Camera movement → video prompt mapping ──────────────────────
    _CAMERA_PROMPT: dict[str, str] = {
        "static": "Static locked camera, no movement, rock-solid stable",
        "dolly_in": "Smooth slow dolly in toward subject, very gradual approach",
        "dolly_out": "Slow dolly out away from subject, gradually revealing environment",
        "zoom_in": "Gradual zoom in, tightening frame on subject",
        "zoom_out": "Slow zoom out, widening frame to reveal scene",
        "slow_zoom": "Very slow imperceptible zoom, cinematic drift",
        "orbit": "Smooth 180-degree orbit around subject, slow controlled rotation",
        "pan_left": "Gentle pan from right to left, smoothly revealing scene",
        "pan_right": "Gentle pan from left to right, smoothly revealing scene",
        "crane_up": "Slow crane shot rising upward, revealing the environment from above",
        "crane_down": "Slow crane shot descending, approaching subject from above",
        "tracking": "Camera tracking alongside subject, smooth lateral movement",
    }

    async def _run_real_pipeline():
        from models.enums import SceneType, CameraMovement, TransitionType

        # ── Convert frontend scenes to ScenePipeline objects ─────────
        def _to_scene_type(t: str) -> SceneType:
            return {"personnage": SceneType.PERSONNAGE, "produit": SceneType.PRODUIT,
                    "transition": SceneType.TRANSITION}.get(t, SceneType.PRODUIT)

        def _to_camera(c: str) -> CameraMovement:
            try:
                return CameraMovement(c)
            except ValueError:
                return CameraMovement.STATIC

        def _to_transition(t: str) -> TransitionType:
            try:
                return TransitionType(t)
            except ValueError:
                return TransitionType.CUT

        from models.scene import ScenePipeline

        # ── Build brand visual prefix (Problem 2) ───────────────────
        brand_visual_prefix = ""
        if request.brand_prompt_prefix:
            brand_visual_prefix = request.brand_prompt_prefix.strip() + ". "
        if request.brand_colors:
            color_str = ", ".join(request.brand_colors[:5])
            brand_visual_prefix += f"Color palette: {color_str}. "
        if request.brand_mood:
            brand_visual_prefix += f"Mood: {request.brand_mood}. "
        logger.info("Job %s: brand_visual_prefix=%s", job_id, brand_visual_prefix[:200])

        pipeline_scenes: list[ScenePipeline] = []
        for i, s in enumerate(request.scenes):
            sd = s if isinstance(s, dict) else s.dict() if hasattr(s, 'dict') else dict(s)

            raw_camera = sd.get("camera_movement", "static")
            raw_transition = sd.get("transition", "cut")
            scene_duration = float(sd.get("duration_seconds", sd.get("duration", 3.5)))

            # ── Build cinematic VIDEO prompt via Kling-optimized builder ──
            # The builder knows how to talk to Kling: scene content first,
            # then camera directive + details, then subject physics auto-
            # detected from keywords, then mood, then technical tail.
            from knowledge.prompt_templates.kling_video_prompts import (
                build_kling_video_prompt,
                detect_subject_animations,
                mood_for_industry,
            )

            raw_video_prompt = (sd.get("prompt_video") or "").strip()
            raw_image_for_fallback = (sd.get("prompt_image") or sd.get("description") or "").strip()
            subject_line = raw_video_prompt or raw_image_for_fallback

            auto_animations = detect_subject_animations(
                " ".join([subject_line, raw_image_for_fallback]).strip(),
                max_animations=3,
            )
            resolved_mood = (
                request.brand_mood.lower()
                if request.brand_mood
                else mood_for_industry(request.product_category)
            )

            cinematic_video_prompt = build_kling_video_prompt(
                scene_description=subject_line,
                camera_movement=raw_camera,
                subject_animations=auto_animations,
                mood=resolved_mood,
                duration_seconds=scene_duration,
            )

            # ── Build cinematic IMAGE prompt (Problems 2, 7) ─────────
            raw_image_prompt = sd.get("prompt_image", sd.get("description", ""))
            image_parts = []
            if brand_visual_prefix:
                image_parts.append(brand_visual_prefix.strip())
            image_parts.append(raw_image_prompt.strip())
            # Cinematic image quality suffix
            image_parts.extend([
                "Shot on 85mm f/1.4 lens, shallow depth of field with creamy bokeh",
                "Warm 3500K color temperature, Rembrandt lighting",
                "Slight film grain, Kodak Portra 400 tones",
                "Ultra sharp, 8K resolution, photorealistic",
                "Professional advertising photograph, broadcast quality",
            ])
            cinematic_image_prompt = ". ".join(p.rstrip(".") for p in image_parts if p)

            ps = ScenePipeline(
                index=i + 1,
                scene_type=_to_scene_type(sd.get("type", "produit")),
                prompt_image=raw_image_prompt,
                prompt_video=raw_video_prompt,
                original_text=sd.get("original_text", sd.get("description", "")),
                duration_seconds=scene_duration,
                camera_movement=_to_camera(raw_camera),
                transition=_to_transition(raw_transition),
                needs_mannequin=sd.get("needs_mannequin", False),
                enriched_prompt_image=cinematic_image_prompt,
                enriched_prompt_video=cinematic_video_prompt,
                metadata={
                    "aspect_ratio": aspect_ratio,
                    "raw_transition": raw_transition,
                },
            )
            pipeline_scenes.append(ps)

            # Log the full enriched prompts so quality can be verified
            logger.info(
                "Job %s: SCENE %d ENRICHED IMAGE PROMPT (%d chars):\n  %s",
                job_id, i + 1, len(cinematic_image_prompt), cinematic_image_prompt[:500],
            )
            logger.info(
                "Job %s: SCENE %d ENRICHED VIDEO PROMPT (%d chars):\n  %s",
                job_id, i + 1, len(cinematic_video_prompt), cinematic_video_prompt[:500],
            )

        if not pipeline_scenes:
            _demo_jobs[job_id]["status"] = "failed"
            _demo_jobs[job_id]["message"] = "No scenes to generate"
            return

        total_scenes = len(pipeline_scenes)
        gen_scenes = [s for s in pipeline_scenes if s.scene_type != SceneType.TRANSITION]

        def _update(status: str, progress: float, message: str, phase: str = ""):
            _demo_jobs[job_id].update({
                "status": status,
                "progress": round(progress, 3),
                "message": message,
                "phase": phase or status,
            })

        # ── STEP 1: Image Generation (Gemini) ───────────────────────
        _update("generating_images", 0.05, "Starting image generation...", "generating_images")
        logger.info("Job %s: generating %d images with Gemini (aspect=%s)", job_id, len(gen_scenes), aspect_ratio)

        from services.image_generation.product_generator import ProductGenerator
        from services.image_generation.scene_generator import SceneGenerator

        product_gen = ProductGenerator()
        scene_gen = SceneGenerator()

        for i, scene in enumerate(pipeline_scenes):
            scene_progress = 0.05 + (0.45 * (i / total_scenes))
            _update(
                "generating_images", scene_progress,
                f"Generating image {i+1}/{total_scenes}...",
                "generating_images",
            )
            _demo_jobs[job_id]["scenes"] = [
                {"id": j + 1, "status": "completed" if j < i else ("generating" if j == i else "pending")}
                for j in range(total_scenes)
            ]

            if scene.scene_type == SceneType.TRANSITION:
                logger.info("Job %s: scene %d is transition — skipping image", job_id, scene.index)
                continue

            output_path = job_dir / "images" / f"scene_{scene.index:02d}_final.png"
            prompt = scene.enriched_prompt_image or scene.prompt_image

            # If references exist, prepend an explicit instruction so Gemini
            # anchors the generated scene to the uploaded product.
            if reference_pil_images:
                prompt = (
                    "Generate a scene featuring THIS EXACT product (see reference image(s) above). "
                    "Preserve the product's shape, label, colors, proportions and materials precisely. "
                    "Place it in the following scene: " + prompt
                )

            for attempt in range(2):  # retry once on failure
                try:
                    if scene.scene_type == SceneType.PERSONNAGE:
                        await scene_gen.generate(
                            prompt=prompt,
                            output_path=output_path,
                            reference_images=reference_pil_images or None,
                            aspect_ratio=aspect_ratio,
                        )
                    else:
                        await product_gen.generate(
                            prompt=prompt,
                            output_path=output_path,
                            reference_images=reference_pil_images or None,
                            aspect_ratio=aspect_ratio,
                        )
                    scene.final_image_path = output_path
                    scene.image_generated = True
                    logger.info("Job %s: scene %d image generated (%s)", job_id, scene.index, output_path)
                    break
                except Exception as e:
                    logger.warning("Job %s: scene %d image attempt %d failed: %s", job_id, scene.index, attempt + 1, e)
                    if attempt == 1:
                        scene.mark_failed(f"Image generation: {e}")

        images_ok = sum(1 for s in pipeline_scenes if s.image_generated)
        logger.info("Job %s: %d/%d images generated", job_id, images_ok, len(gen_scenes))

        if images_ok == 0:
            _update("failed", 0.5, "All image generations failed", "failed")
            _demo_jobs[job_id]["result"] = {"error": "All image generations failed"}
            return

        # ── STEP 2: Video Animation (Fal.ai / Kling) ────────────────
        _update("generating_videos", 0.50, "Starting video animation...", "generating_videos")
        logger.info("Job %s: animating %d scenes via Fal.ai", job_id, images_ok)

        from services.video_generation.animator import VideoAnimator
        animator = VideoAnimator()

        for i, scene in enumerate(pipeline_scenes):
            if not scene.image_generated or scene.failed:
                continue

            scene_progress = 0.50 + (0.35 * (i / total_scenes))
            _update(
                "generating_videos", scene_progress,
                f"Animating scene {scene.index}/{total_scenes}...",
                "generating_videos",
            )

            for attempt in range(2):  # retry once on failure
                try:
                    await animator.animate_scene(scene, job_dir)
                    logger.info("Job %s: scene %d animated", job_id, scene.index)
                    break
                except Exception as e:
                    logger.warning("Job %s: scene %d animation attempt %d failed: %s", job_id, scene.index, attempt + 1, e)
                    if attempt == 1:
                        scene.mark_failed(f"Video animation: {e}")

        videos_ok = sum(1 for s in pipeline_scenes if s.video_generated)
        logger.info("Job %s: %d/%d videos animated", job_id, videos_ok, images_ok)

        # ── STEP 3: FFmpeg Assembly with xfade transitions ───────────
        _update("assembling", 0.88, "Assembling final video...", "assembling")
        logger.info("Job %s: assembling final video", job_id)

        final_path = job_dir / "final_video.mp4"
        clips_with_video = [s for s in pipeline_scenes if s.video_generated and s.video_path and s.video_path.exists()]

        if clips_with_video:
            try:
                _assemble_with_transitions(clips_with_video, final_path, resolution)
                logger.info("Job %s: final video assembled with transitions: %s", job_id, final_path)
            except Exception as e:
                logger.warning("Job %s: xfade assembly failed: %s — trying simple concat", job_id, e)
                import shutil
                shutil.copy2(str(clips_with_video[0].video_path), str(final_path))
        else:
            # No videos — create a slideshow from images
            image_scenes = [s for s in pipeline_scenes if s.image_generated and s.final_image_path]
            if image_scenes:
                try:
                    _create_slideshow(image_scenes, final_path, resolution)
                    logger.info("Job %s: slideshow created from %d images", job_id, len(image_scenes))
                except Exception as e:
                    logger.error("Job %s: slideshow creation failed: %s", job_id, e)
                    _update("failed", 0.95, f"Assembly failed: {e}", "failed")
                    return

        if not final_path.exists():
            _update("failed", 0.95, "No output video produced", "failed")
            return

        # ── DONE ─────────────────────────────────────────────────────
        file_size = final_path.stat().st_size
        total_duration = sum(s.duration_seconds for s in pipeline_scenes)

        _demo_jobs[job_id] = {
            "job_id": job_id,
            "status": "completed",
            "progress": 1.0,
            "phase": "completed",
            "message": "Generation complete",
            "scenes": [
                {"id": s.index, "status": "completed" if (s.video_generated or s.image_generated) else "failed"}
                for s in pipeline_scenes
            ],
            "result": {
                "video_url": f"/api/videos/{job_id}/final.mp4",
                "thumbnail_url": None,
                "duration_seconds": round(total_duration, 1),
                "resolution": resolution.replace(":", "x"),
                "aspect_ratio": aspect_ratio,
                "brand_name": request.brand_name,
                "scenes_generated": images_ok,
                "scenes_animated": videos_ok,
                "file_size_mb": round(file_size / (1024 * 1024), 2),
                "created_at": datetime.utcnow().isoformat(),
            },
        }
        logger.info(
            "Job %s COMPLETE: %d scenes, %d images, %d videos, %.1f MB, %s",
            job_id, total_scenes, images_ok, videos_ok, file_size / (1024 * 1024), aspect_ratio,
        )

    background_tasks.add_task(_run_real_pipeline)

    return {"job_id": job_id, "status": "queued"}


def _create_slideshow(scenes: list, output_path: Path, resolution: str = "1920x1080") -> None:
    """Create a slideshow video from scene images using FFmpeg."""
    import subprocess
    concat_dir = output_path.parent / "slideshow_temp"
    concat_dir.mkdir(exist_ok=True)

    concat_file = concat_dir / "list.txt"
    with open(concat_file, "w") as f:
        for s in scenes:
            dur = s.duration_seconds
            f.write(f"file '{s.final_image_path}'\n")
            f.write(f"duration {dur}\n")
        f.write(f"file '{scenes[-1].final_image_path}'\n")

    cmd = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-vf", f"scale={resolution}:force_original_aspect_ratio=decrease,pad={resolution}:(ow-iw)/2:(oh-ih)/2,fps=24",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        str(output_path),
    ]
    subprocess.run(cmd, check=True, capture_output=True, text=True)

    import shutil
    shutil.rmtree(concat_dir, ignore_errors=True)


def _assemble_with_transitions(scenes: list, output_path: Path, resolution: str = "1920x1080") -> None:
    """Assemble video clips with xfade transitions between them (Problem 5).

    Uses the scene's transition metadata to select the FFmpeg xfade type.
    """
    import subprocess

    if len(scenes) == 1:
        # Single clip — just re-encode at the correct resolution
        cmd = [
            "ffmpeg", "-y", "-i", str(scenes[0].video_path),
            "-vf", f"scale={resolution}:force_original_aspect_ratio=decrease,pad={resolution}:(ow-iw)/2:(oh-ih)/2,fps=24",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(output_path),
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        return

    _XFADE_MAP = {
        "fade": ("fade", 0.5),
        "dissolve": ("dissolve", 0.8),
        "cross_fade": ("dissolve", 0.6),
        "wipe": ("wipeleft", 0.5),
        "fade_from_black": ("fade", 0.5),
        "fade_to_white": ("fade", 0.5),
        "cut": ("fade", 0.15),  # near-instant fade (0 breaks FFmpeg)
    }

    # Step 1: Normalize all clips to same resolution/fps
    concat_dir = output_path.parent / "xfade_temp"
    concat_dir.mkdir(exist_ok=True)

    norm_paths: list[tuple[Path, float]] = []
    for i, scene in enumerate(scenes):
        norm_path = concat_dir / f"norm_{i:03d}.mp4"
        cmd = [
            "ffmpeg", "-y", "-i", str(scene.video_path),
            "-vf", f"scale={resolution}:force_original_aspect_ratio=decrease,pad={resolution}:(ow-iw)/2:(oh-ih)/2,fps=24",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-an",
            str(norm_path),
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
        norm_paths.append((norm_path, scene.duration_seconds))

    # Step 2: Build xfade filter chain
    # For N clips, we need N-1 xfade filters chained together
    inputs = []
    for p, _ in norm_paths:
        inputs.extend(["-i", str(p)])

    # Probe actual durations with ffprobe (more reliable than scene metadata)
    actual_durations = []
    for p, fallback_dur in norm_paths:
        try:
            probe = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration",
                 "-of", "default=noprint_wrappers=1:nokey=1", str(p)],
                capture_output=True, text=True,
            )
            actual_durations.append(float(probe.stdout.strip()))
        except (ValueError, Exception):
            actual_durations.append(fallback_dur)

    n = len(norm_paths)
    if n == 2:
        # Simple 2-clip case
        raw_transition = scenes[1].metadata.get("raw_transition", "fade")
        xfade_spec = _XFADE_MAP.get(raw_transition, ("fade", 0.5))

        trans_name, trans_dur = xfade_spec
        offset = max(0, actual_durations[0] - trans_dur)
        cmd = ["ffmpeg", "-y"] + inputs + [
            "-filter_complex",
            f"[0:v][1:v]xfade=transition={trans_name}:duration={trans_dur}:offset={offset:.3f},format=yuv420p",
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(output_path),
        ]
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    else:
        # N-clip xfade chain: [0][1]xfade->t0; [t0][2]xfade->t1; ...
        # For chained xfade, the offset is the point in the CURRENT output
        # where the next transition starts. After each xfade, the output
        # duration = sum(clip_durations_so_far) - sum(transition_durations_so_far).
        filter_parts = []
        trans_specs: list[tuple[str, float]] = []
        for i in range(1, n):
            raw_transition = scenes[i].metadata.get("raw_transition", "fade")
            xfade_spec = _XFADE_MAP.get(raw_transition, ("fade", 0.5))
            trans_specs.append(xfade_spec)

        for i in range(1, n):
            trans_name, trans_dur = trans_specs[i - 1]

            if i == 1:
                src_a = "[0:v]"
                src_b = "[1:v]"
            else:
                src_a = f"[v{i-1}]"
                src_b = f"[{i}:v]"

            # Offset = total output duration up to this point minus transition overlap
            # The output of chained xfades up to clip i has duration:
            #   sum(actual_durations[0..i-1]) - sum(trans_durs[0..i-2])
            # The next xfade starts at: that duration - trans_dur_i
            output_so_far = sum(actual_durations[:i]) - sum(td for _, td in trans_specs[:i-1])
            offset = max(0, output_so_far - trans_dur)

            out_label = f"[v{i}]" if i < n - 1 else ""
            filter_parts.append(
                f"{src_a}{src_b}xfade=transition={trans_name}:duration={trans_dur}:offset={offset:.3f}{',format=yuv420p' if i == n - 1 else ''}{out_label}"
            )

        filter_complex = ";".join(filter_parts)
        cmd = ["ffmpeg", "-y"] + inputs + [
            "-filter_complex", filter_complex,
            "-c:v", "libx264", "-preset", "fast", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(output_path),
        ]
        logger.info("FFmpeg xfade cmd: %s", " ".join(cmd[:10]) + " ...")
        subprocess.run(cmd, check=True, capture_output=True, text=True)

    # Cleanup
    import shutil
    shutil.rmtree(concat_dir, ignore_errors=True)


@app.get("/api/status/{job_id}")
async def job_status(job_id: str):
    """Check generation job progress."""
    job = _demo_jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")
    return job


@app.get("/api/result/{job_id}")
async def job_result(job_id: str):
    """Get generation job result."""
    job = _demo_jobs.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail=f"Job {job_id} not found")

    if job.get("status") != "completed":
        return {"status": job.get("status"), "progress": job.get("progress"), "message": "Not yet complete"}

    return job.get("result")


@app.get("/api/videos/{job_id}/final.mp4")
async def serve_video(job_id: str):
    """Serve the generated video file."""
    video_path = Path(f"/tmp/astreli_jobs/{job_id}/final_video.mp4")
    if not video_path.exists():
        raise HTTPException(status_code=404, detail="Video not found")
    return FileResponse(
        path=str(video_path),
        media_type="video/mp4",
        filename=f"astreli_{job_id}.mp4",
    )


@app.get("/api/videos/{job_id}/scene_{scene_index}.png")
async def serve_scene_image(job_id: str, scene_index: int):
    """Serve a generated scene image (for thumbnails)."""
    img_path = Path(f"/tmp/astreli_jobs/{job_id}/images/scene_{scene_index:02d}_final.png")
    if not img_path.exists():
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(path=str(img_path), media_type="image/png")


@app.get("/api/lora/models")
async def demo_list_lora_models():
    """List available LoRA models (mock)."""
    return list(_demo_lora_models.values())


@app.post("/api/lora/train")
async def demo_train_lora(request: LoRATrainDemoRequest, background_tasks: BackgroundTasks):
    """Start mock LoRA training."""
    model_id = f"lora_{str(uuid_mod.uuid4())[:6]}"
    trigger_word = request.trigger_word or request.model_name.split()[0].upper()

    _demo_lora_models[model_id] = {
        "model_id": model_id,
        "name": request.model_name,
        "status": "training",
        "created_at": datetime.utcnow().strftime("%Y-%m-%d"),
        "preview_url": None,
        "trigger_word": trigger_word,
    }

    async def _run_mock_training():
        await asyncio.sleep(20)
        if model_id in _demo_lora_models:
            _demo_lora_models[model_id]["status"] = "ready"

    background_tasks.add_task(_run_mock_training)

    return {"model_id": model_id, "status": "training"}


@app.delete("/api/lora/models/{model_id}")
async def demo_delete_lora_model(model_id: str):
    """Delete a mock LoRA model."""
    if model_id not in _demo_lora_models:
        raise HTTPException(status_code=404, detail="Model not found")
    del _demo_lora_models[model_id]
    return {"status": "deleted"}


# ── Health ───────────────────────────────────────────────────────────

@app.get("/health")
async def health_check():
    """Check all dependencies."""
    import shutil

    checks = {
        "openai_api_key": bool(settings.openai_api_key),
        "gemini_api_key": bool(settings.gemini_api_key),
        "fal_key": bool(settings.fal_key),
        "replicate_api_token": bool(settings.replicate_api_token),
        "ffmpeg": shutil.which("ffmpeg") is not None,
    }
    all_ok = all(v for k, v in checks.items() if k != "replicate_api_token")
    return {
        "status": "healthy" if all_ok else "degraded",
        "checks": checks,
        "version": "3.0.0",
    }


# ── Run ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
