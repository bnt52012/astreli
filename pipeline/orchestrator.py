"""
Pipeline Orchestrator — The Heart of AdGenAI v3.0.

Coordinates the complete 4-step advertising video generation pipeline:

  Step 0: Mode detection + validation
  Step 1: GPT-4o scenario analysis -> scene decomposition
  Step 1.5: Intelligence layer -> scene understanding + prompt enrichment
  Step 2: Dual image generation engine
         PATH A: personnage -> 3-pass fusion (Gemini + LoRA + inpainting)
         PATH B: produit -> Gemini one-shot
  Step 2.5: Quality check with auto-regeneration (max 3 retries)
  Step 3: Dual Kling video animation (Video-01 human / V3 product), concurrent
  Step 4: FFmpeg final assembly (transitions, music, logo)

Each scene is wrapped in try/except — pipeline continues with whatever succeeds.
Reports generated on both success and failure.
"""
from __future__ import annotations

import asyncio
import json
import logging
import time
import uuid
from pathlib import Path
from typing import Any, Callable

from models.enums import CameraMovement, PipelineMode, SceneType, TransitionType
from models.scene import ScenePipeline
from pipeline.config import settings, PIPELINE_DEFAULTS
from pipeline.exceptions import (
    AssemblyError,
    ConfigError,
    NoScenesError,
    PipelineError,
)
from pipeline.mode_detector import ModeDetector

logger = logging.getLogger(__name__)

# Type alias for progress callback
ProgressCallback = Callable[[dict[str, Any]], None] | None


class PipelineOrchestrator:
    """Main pipeline orchestrator for AdGenAI v3.0."""

    def __init__(self, on_progress: ProgressCallback = None) -> None:
        self._on_progress = on_progress

    def _emit_progress(self, data: dict[str, Any]) -> None:
        if self._on_progress:
            try:
                self._on_progress(data)
            except Exception:
                pass

    async def run(
        self,
        project_id: str | None = None,
        scenario: str = "",
        lora_model_id: str | None = None,
        lora_trigger_word: str = "MANNEQUIN",
        product_photos: list[str] | None = None,
        decor_photos: list[str] | None = None,
        logo_path: str | None = None,
        music_path: str | None = None,
        brand_name: str | None = None,
        aspect_ratio: str = "16:9",
    ) -> dict[str, Any]:
        """Execute the complete pipeline from scenario to final video.

        Args:
            project_id: Unique project identifier (auto-generated if None).
            scenario: Client's advertising scenario (SACRED — never modified).
            lora_model_id: Replicate LoRA model ID (None = product-only mode).
            lora_trigger_word: Trigger word for the LoRA model.
            product_photos: Paths to product reference images.
            decor_photos: Paths to decor/environment reference images.
            logo_path: Path to brand logo for overlay.
            music_path: Path to background music.
            brand_name: Brand name for context.
            aspect_ratio: Primary aspect ratio (16:9, 9:16, 1:1).

        Returns:
            Pipeline result dict with video path, scene data, costs, timing.
        """
        pid = project_id or str(uuid.uuid4())[:8]
        start_time = time.time()
        scenes: list[ScenePipeline] = []
        errors: list[str] = []

        # ── Setup ────────────────────────────────────────────────────
        project_dir = settings.ensure_dirs(pid)
        self._emit_progress({"step": "init", "progress": 0.0, "message": "Initializing..."})

        # ── STEP 0: Mode Detection + Validation ─────────────────────
        mode = ModeDetector.detect(lora_model_id)
        logger.info("[PIPELINE] Project %s | Mode: %s", pid, mode.value)

        try:
            settings.validate_core()
            if mode == PipelineMode.PERSONNAGE_ET_PRODUIT:
                settings.validate_lora(lora_model_id or "")
        except ConfigError as e:
            logger.error("[PIPELINE] Validation failed: %s", e)
            return self._build_error_report(pid, str(e), scenes, start_time)

        # ── STEP 1: Scenario Analysis (GPT-4o) ─────────────────────
        self._emit_progress({"step": "analysis", "progress": 0.05, "message": "Analyzing scenario with GPT-4o..."})

        try:
            from services.scenario.analyzer import ScenarioAnalyzer

            analyzer = ScenarioAnalyzer()

            # Brand context
            brand_context = ""
            if brand_name:
                from intelligence.brand_analyzer import BrandAnalyzer
                brand_analyzer = BrandAnalyzer()
                brand_context = brand_analyzer.analyze(
                    logo_path=logo_path,
                    reference_images=(product_photos or []) + (decor_photos or []),
                    brand_name=brand_name,
                )

            analysis = analyzer.analyze(scenario, mode, brand_context)
            scene_dicts = analysis.get("scenes", [])

            if not scene_dicts:
                raise NoScenesError()

            # Convert to ScenePipeline objects
            for sd in scene_dicts:
                scene = ScenePipeline(
                    index=sd["scene_number"],
                    scene_type=SceneType(sd["scene_type"]),
                    prompt_image=sd["prompt_image"],
                    prompt_video=sd["prompt_video"],
                    duration_seconds=sd["duration_seconds"],
                    camera_movement=CameraMovement(sd["camera_movement"]),
                    transition=TransitionType(sd["transition"]),
                    needs_mannequin=sd["needs_mannequin"],
                    needs_decor_ref=sd["needs_decor_ref"],
                    original_text=sd.get("original_text", ""),
                    metadata={"aspect_ratio": aspect_ratio},
                )
                scenes.append(scene)

            logger.info("[PIPELINE] %d scenes analyzed.", len(scenes))

        except Exception as e:
            logger.error("[PIPELINE] Scenario analysis failed: %s", e)
            return self._build_error_report(pid, f"Scenario analysis: {e}", scenes, start_time)

        # ── STEP 1.5: Intelligence Layer ────────────────────────────
        self._emit_progress({"step": "enrichment", "progress": 0.15, "message": "Enriching prompts..."})

        try:
            from intelligence.scene_understanding import SceneUnderstanding
            from intelligence.prompt_enricher import PromptEnricher
            from knowledge.industry_detector import IndustryDetector

            # Detect industry
            detector = IndustryDetector()
            industry_match = detector.detect(scenario)
            industry = industry_match.industry

            # Scene understanding
            understanding = SceneUnderstanding()
            enricher = PromptEnricher()

            for scene in scenes:
                if scene.scene_type == SceneType.TRANSITION:
                    continue

                # Deep scene understanding
                ctx = understanding.analyze(
                    scene.prompt_image + " " + scene.original_text,
                    scene.index,
                )

                # Enrich image prompt
                scene.enriched_prompt_image = enricher.enrich_image_prompt(
                    original_prompt=scene.prompt_image,
                    scene_context=ctx,
                    industry=industry,
                    brand_prefix=brand_context,
                    scene_type="lifestyle" if scene.is_personnage else "product_hero",
                )

                # Enrich video prompt
                scene.enriched_prompt_video = enricher.enrich_video_prompt(
                    original_prompt=scene.prompt_video,
                    scene_context=ctx,
                    industry=industry,
                )

            logger.info("[PIPELINE] Prompts enriched for industry: %s", industry)

        except Exception as e:
            logger.warning("[PIPELINE] Enrichment failed (continuing with raw prompts): %s", e)
            errors.append(f"Enrichment: {e}")

        # ── STEP 2: Image Generation (Dual Engine) ──────────────────
        self._emit_progress({"step": "images", "progress": 0.20, "message": "Generating images..."})

        try:
            from services.image_generation.engine import ImageGenerationEngine

            image_engine = ImageGenerationEngine(
                lora_model_id=lora_model_id,
                lora_trigger_word=lora_trigger_word,
                cache_dir=settings.cache_dir,
            )

            for i, scene in enumerate(scenes):
                if scene.scene_type == SceneType.TRANSITION:
                    continue

                try:
                    self._emit_progress({
                        "step": "images",
                        "progress": 0.20 + (0.25 * (i / len(scenes))),
                        "message": f"Generating image for scene {scene.index}...",
                    })

                    await image_engine.generate_scene_image(
                        scene=scene,
                        output_dir=project_dir,
                        product_photos=product_photos,
                        decor_photos=decor_photos,
                    )

                    # Quality check for personnage scenes (fusion)
                    if scene.is_personnage and scene.fused_image_path:
                        await self._quality_check_with_retry(
                            scene, image_engine, project_dir,
                            product_photos, decor_photos,
                        )

                except Exception as e:
                    logger.error("[PIPELINE] Scene %d image failed: %s", scene.index, e)
                    scene.mark_failed(f"Image: {e}")
                    errors.append(f"Scene {scene.index} image: {e}")

        except Exception as e:
            logger.error("[PIPELINE] Image engine init failed: %s", e)
            errors.append(f"Image engine: {e}")

        images_done = sum(1 for s in scenes if s.image_generated)
        logger.info("[PIPELINE] Images: %d/%d succeeded.", images_done, len(scenes))

        if images_done == 0:
            return self._build_error_report(pid, "No images generated", scenes, start_time, errors)

        # ── STEP 3: Video Animation (Dual Kling) ────────────────────
        self._emit_progress({"step": "videos", "progress": 0.50, "message": "Animating scenes..."})

        try:
            from services.video_generation.animator import VideoAnimator

            animator = VideoAnimator()
            await animator.animate_all(scenes, project_dir)

        except Exception as e:
            logger.error("[PIPELINE] Video animation error: %s", e)
            errors.append(f"Video animation: {e}")

        videos_done = sum(1 for s in scenes if s.video_generated)
        logger.info("[PIPELINE] Videos: %d/%d succeeded.", videos_done, len(scenes))

        if videos_done == 0:
            return self._build_error_report(pid, "No videos generated", scenes, start_time, errors)

        # ── STEP 4: Final Assembly (FFmpeg) ─────────────────────────
        self._emit_progress({"step": "assembly", "progress": 0.85, "message": "Assembling final video..."})

        final_video_path = project_dir / "assembly" / "final_ad.mp4"

        try:
            from services.assembly.assembler import VideoAssembler

            assembler = VideoAssembler()
            final_video_path = assembler.assemble(
                scenes=scenes,
                output_path=final_video_path,
                music_path=music_path,
                logo_path=logo_path,
            )
            logger.info("[PIPELINE] Final video: %s", final_video_path)

        except Exception as e:
            logger.error("[PIPELINE] Assembly failed: %s", e)
            errors.append(f"Assembly: {e}")
            return self._build_error_report(pid, f"Assembly: {e}", scenes, start_time, errors)

        # ── Success ──────────────────────────────────────────────────
        elapsed = time.time() - start_time
        self._emit_progress({"step": "complete", "progress": 1.0, "message": "Complete!"})

        report = self._build_success_report(
            pid, mode, scenes, final_video_path, elapsed, errors
        )

        # Save report
        report_path = project_dir / "reports" / "pipeline_report.json"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(json.dumps(report, indent=2, default=str))

        logger.info("[PIPELINE] Completed in %.1fs: %s", elapsed, final_video_path)
        return report

    async def _quality_check_with_retry(
        self,
        scene: ScenePipeline,
        image_engine: Any,
        project_dir: Path,
        product_photos: list[str] | None,
        decor_photos: list[str] | None,
    ) -> None:
        """Quality check a fused image with auto-retry."""
        try:
            from intelligence.quality_checker import QualityChecker
            checker = QualityChecker()

            for attempt in range(PIPELINE_DEFAULTS.max_quality_retries):
                image_path = scene.fused_image_path or scene.final_image_path
                if not image_path:
                    break

                score, passes = await checker.check_and_retry(
                    image_path, scene.scene_type.value, is_fusion=True
                )
                scene.quality_score = score

                if passes:
                    logger.info("Scene %d quality OK: %.1f/10", scene.index, score)
                    break

                if attempt < PIPELINE_DEFAULTS.max_quality_retries - 1:
                    logger.info(
                        "Scene %d quality %.1f/10 — regenerating (attempt %d/%d)...",
                        scene.index, score, attempt + 2, PIPELINE_DEFAULTS.max_quality_retries,
                    )
                    scene.fusion_attempts += 1
                    try:
                        await image_engine.generate_scene_image(
                            scene=scene,
                            output_dir=project_dir,
                            product_photos=product_photos,
                            decor_photos=decor_photos,
                        )
                    except Exception as e:
                        logger.warning("Regeneration failed: %s", e)
                        break
                else:
                    logger.warning(
                        "Scene %d quality %.1f/10 after %d attempts — accepting.",
                        scene.index, score, PIPELINE_DEFAULTS.max_quality_retries,
                    )

        except Exception as e:
            logger.warning("Quality check failed: %s", e)

    def _build_success_report(
        self,
        project_id: str,
        mode: PipelineMode,
        scenes: list[ScenePipeline],
        video_path: Path,
        elapsed: float,
        errors: list[str],
    ) -> dict[str, Any]:
        """Build pipeline success report."""
        return {
            "status": "completed",
            "project_id": project_id,
            "mode": mode.value,
            "output_video": str(video_path),
            "total_duration_seconds": elapsed,
            "scenes_total": len(scenes),
            "scenes_succeeded": sum(1 for s in scenes if s.video_generated),
            "scenes_failed": sum(1 for s in scenes if s.failed),
            "personnage_scenes": sum(1 for s in scenes if s.is_personnage),
            "produit_scenes": sum(1 for s in scenes if s.is_produit),
            "transition_scenes": sum(1 for s in scenes if s.is_transition),
            "total_cost": sum(s.total_cost for s in scenes),
            "scene_details": [s.to_dict() for s in scenes],
            "errors": errors,
        }

    def _build_error_report(
        self,
        project_id: str,
        reason: str,
        scenes: list[ScenePipeline],
        start_time: float,
        errors: list[str] | None = None,
    ) -> dict[str, Any]:
        """Build pipeline error report."""
        elapsed = time.time() - start_time
        report = {
            "status": "failed",
            "project_id": project_id,
            "failure_reason": reason,
            "total_duration_seconds": elapsed,
            "scenes_total": len(scenes),
            "scenes_succeeded": sum(1 for s in scenes if s.video_generated),
            "scenes_failed": sum(1 for s in scenes if s.failed),
            "scene_details": [s.to_dict() for s in scenes],
            "errors": errors or [reason],
        }

        # Save error report
        try:
            project_dir = settings.output_dir / project_id / "reports"
            project_dir.mkdir(parents=True, exist_ok=True)
            (project_dir / "error_report.json").write_text(
                json.dumps(report, indent=2, default=str)
            )
        except Exception:
            pass

        return report

    async def estimate_cost(
        self,
        scenario: str,
        lora_model_id: str | None = None,
    ) -> dict[str, Any]:
        """Estimate pipeline cost WITHOUT running it.

        Runs only Step 1 (scenario analysis) to get scene count,
        then calculates expected costs.
        """
        from services.scenario.analyzer import ScenarioAnalyzer
        from utils.cost_calculator import CostCalculator

        mode = ModeDetector.detect(lora_model_id)
        analyzer = ScenarioAnalyzer()
        analysis = analyzer.analyze(scenario, mode)

        scene_dicts = analysis.get("scenes", [])
        personnage = sum(1 for s in scene_dicts if s["scene_type"] == "personnage")
        produit = sum(1 for s in scene_dicts if s["scene_type"] == "produit")
        transition = sum(1 for s in scene_dicts if s["scene_type"] == "transition")

        calculator = CostCalculator()
        costs = calculator.estimate_pipeline(
            total_scenes=len(scene_dicts),
            personnage_scenes=personnage,
            produit_scenes=produit,
            transition_scenes=transition,
        )

        return {
            "mode": mode.value,
            "total_scenes": len(scene_dicts),
            "personnage_scenes": personnage,
            "produit_scenes": produit,
            "transition_scenes": transition,
            "estimated_duration": analysis.get("estimated_duration", 0),
            "costs": costs,
        }
