"""
Pipeline Orchestrator — The Heart of AdGenAI.

Coordinates the complete advertising video generation pipeline:

  Step 0: Mode detection + input validation
  Step 1: GPT-4o scenario analysis → scene decomposition
  Step 1.5: Intelligence layer → scene understanding + prompt enrichment + brand analysis
  Step 2: Dual Gemini image generation → Pro (personnage) / Flash (produit)
  Step 2.5: Quality verification → auto-regeneration if below threshold
  Step 3: Dual Kling video animation → Video-01 (human) / V3 (product), concurrent
  Step 4: FFmpeg final assembly → transitions, music, logo

Error handling: each scene wrapped in try/except. Pipeline continues
with whatever scenes succeed. Reports exported on success AND failure.
"""

from __future__ import annotations

import asyncio
import logging
import shutil
from pathlib import Path

from backend.config import settings
from backend.intelligence.audience_adapter import AudienceAdapter
from backend.intelligence.brand_analyzer import BrandAnalyzer
from backend.intelligence.prompt_enricher import PromptEnricher
from backend.intelligence.quality_checker import QualityChecker
from backend.intelligence.scene_understanding import SceneUnderstanding
from backend.models.enums import (
    JobStatus,
    PipelineMode,
    QualityLevel,
    SceneType,
    TargetPlatform,
)
from backend.models.scene import ScenePipeline
from backend.pipeline.config import PIPELINE_DEFAULTS
from backend.pipeline.exceptions import (
    AssemblyError,
    ConfigError,
    FFmpegNotFoundError,
    NoScenesError,
    PipelineError,
)
from backend.pipeline.mode_detector import ModeDetector
from backend.services.assembly.assembler import VideoAssembler
from backend.services.image_generation.engine import DualGeminiEngine
from backend.services.scenario.analyzer import ScenarioAnalyzer
from backend.services.video_generation.animator import VideoAnimator
from backend.utils.cost_calculator import CostCalculator
from backend.utils.file_manager import ProjectFileManager
from backend.utils.progress import ProgressCallback, ProgressTracker

logger = logging.getLogger(__name__)


class PipelineOrchestrator:
    """Main pipeline orchestrator for AdGenAI.

    Coordinates all pipeline steps with progress tracking,
    error handling, and report generation.

    Usage:
        orchestrator = PipelineOrchestrator(on_progress=my_callback)
        result = await orchestrator.run(
            project_id="abc123",
            scenario="A luxury perfume ad...",
            mannequin_images=["/path/to/model.jpg"],
            product_images=["/path/to/bottle.jpg"],
        )
    """

    def __init__(
        self,
        on_progress: ProgressCallback | None = None,
        quality_level: QualityLevel = QualityLevel.PREMIUM,
    ) -> None:
        self._on_progress = on_progress
        self._quality_level = quality_level

        # Services
        self._analyzer = ScenarioAnalyzer()
        self._scene_understanding = SceneUnderstanding()
        self._prompt_enricher = PromptEnricher()
        self._brand_analyzer = BrandAnalyzer()
        self._quality_checker = QualityChecker(quality_level=quality_level)
        self._cost_calculator = CostCalculator()
        self._audience_adapter = AudienceAdapter()

    # ── Health Check ──────────────────────────────────────────

    @staticmethod
    def health_check() -> dict[str, bool | str]:
        """Validate all dependencies without running the pipeline.

        Checks API keys, ffmpeg availability, and storage directories.

        Returns:
            Dict with check results for each dependency.
        """
        results: dict[str, bool | str] = {}
        results["openai_api_key"] = bool(settings.openai_api_key)
        results["gemini_api_key"] = bool(settings.gemini_api_key)
        results["kling_api_key"] = bool(settings.kling_api_key)
        results["ffmpeg"] = shutil.which(settings.ffmpeg_path) is not None
        results["output_dir_writable"] = settings.output_dir.exists()
        return results

    # ── Cost Estimation ───────────────────────────────────────

    async def estimate_cost(
        self,
        scenario: str,
        mode: PipelineMode,
        project_id: str = "estimate",
        brand_name: str | None = None,
        brand_tone: str | None = None,
        quality_check_enabled: bool = True,
    ) -> dict:
        """Estimate pipeline cost by running only scenario analysis.

        Runs GPT-4o analysis to get scene count and types, then
        calculates expected API costs without running generation.

        Args:
            scenario: Client's scenario text.
            mode: Pipeline mode.
            project_id: Project ID for the analysis call.
            brand_name: Optional brand name.
            brand_tone: Optional brand tone.
            quality_check_enabled: Whether quality checks would run.

        Returns:
            Dict with scene breakdown and cost estimate.
        """
        metadata, scenes = await self._analyzer.analyze(
            scenario=scenario, mode=mode, project_id=project_id,
            brand_name=brand_name, brand_tone=brand_tone,
        )
        breakdown = self._cost_calculator.estimate_from_scenes(
            scenes, quality_check_enabled=quality_check_enabled,
        )
        return {
            "metadata": metadata,
            "scenes_count": len(scenes),
            "scenes": [
                {"id": s.id, "type": s.type.value, "duration": s.duration}
                for s in scenes
            ],
            "cost": breakdown.to_dict(),
        }

    # ── Main Pipeline ─────────────────────────────────────────

    async def run(
        self,
        project_id: str,
        scenario: str,
        mannequin_images: list[str] | None = None,
        product_images: list[str] | None = None,
        decor_images: list[str] | None = None,
        logo_path: str | None = None,
        music_path: str | None = None,
        brand_name: str | None = None,
        brand_tone: str | None = None,
        brand_colors: list[str] | None = None,
        target_platforms: list[TargetPlatform] | None = None,
        quality_check_enabled: bool = True,
    ) -> dict:
        """Execute the complete pipeline from scenario to final video.

        Args:
            project_id: Unique project identifier.
            scenario: Client's ad scenario in natural language.
            mannequin_images: Paths to mannequin/model reference photos.
            product_images: Paths to product reference photos.
            decor_images: Paths to decor/environment reference photos.
            logo_path: Path to brand logo PNG.
            music_path: Path to background music file.
            brand_name: Brand name for context.
            brand_tone: Brand tone description.
            brand_colors: Brand color hex codes.
            target_platforms: Output platforms.
            quality_check_enabled: Whether to run quality checks.

        Returns:
            Pipeline result dict with final video path, scene data, and stats.

        Raises:
            PipelineError: On orchestration failures.
            NoScenesError: If no scenes completed generation.
        """
        # Setup project filesystem
        file_mgr = ProjectFileManager(settings.output_dir, project_id)
        file_mgr.setup()

        tracker = ProgressTracker(project_id=project_id, callback=self._on_progress)
        await tracker.start()

        video_animator: VideoAnimator | None = None
        scenes: list[ScenePipeline] = []

        try:
            # ── STEP 0: Mode Detection + Validation ───────────
            await tracker.update_step(
                "initialization", 0.02, "Detecting pipeline mode...",
                status=JobStatus.ANALYZING,
            )

            mode, valid_mannequin = ModeDetector.detect(mannequin_images)
            valid_product = ModeDetector.validate_reference_images(
                product_images, "product",
            )
            valid_decor = ModeDetector.validate_reference_images(
                decor_images, "decor",
            )

            logger.info(
                "[PIPELINE] Mode: %s | Mannequin: %d | Product: %d | Decor: %d",
                mode.value, len(valid_mannequin), len(valid_product), len(valid_decor),
            )

            # ── STEP 1: Scenario Analysis (GPT-4o) ────────────
            await tracker.update_step(
                "scenario_analysis", 0.05,
                "Analyzing scenario with GPT-4o...",
            )

            metadata, scene_analyses = await self._analyzer.analyze(
                scenario=scenario, mode=mode, project_id=project_id,
                brand_name=brand_name, brand_tone=brand_tone,
            )

            scenes = [ScenePipeline(analysis=sa) for sa in scene_analyses]
            tracker.total_scenes = len(scenes)

            # Register scenes for progress tracking
            for s in scenes:
                await tracker.update_scene(
                    s.analysis.id,
                    scene_type=s.analysis.type.value,
                    status="analyzed",
                )

            logger.info(
                "[PIPELINE] %d scenes analyzed: %s",
                len(scenes),
                ", ".join(
                    f"{s.analysis.id}:{s.analysis.type.value}" for s in scenes
                ),
            )

            # ── STEP 1.5: Intelligence Layer ──────────────────
            await tracker.update_step(
                "prompt_enrichment", 0.15,
                "Understanding scenes and enriching prompts...",
                status=JobStatus.ENRICHING,
            )

            # Deep scene understanding (extract implied technical requirements)
            contexts = self._scene_understanding.analyze_all_scenes(scene_analyses)
            for scene, ctx in zip(scenes, contexts):
                scene.context = ctx

            # Auto-detect ad category from scenario
            category = self._prompt_enricher.detect_ad_category(scenario)

            # Brand visual identity analysis
            brand_prefix = self._brand_analyzer.analyze(
                logo_path=logo_path,
                reference_images=valid_product + valid_decor,
                brand_name=brand_name,
                brand_colors_override=brand_colors,
                brand_tone=brand_tone,
            )

            # Invisible prompt enrichment (client's words preserved at start)
            for scene in scenes:
                if scene.analysis.type == SceneType.TRANSITION:
                    continue
                scene.brand_prompt_prefix = brand_prefix
                scene.enriched_image_prompt = (
                    self._prompt_enricher.enrich_image_prompt(
                        scene.analysis, scene.context, category, brand_prefix,
                    )
                )
                scene.enriched_video_prompt = (
                    self._prompt_enricher.enrich_video_prompt(
                        scene.analysis, scene.context,
                    )
                )

            await tracker.update_step(
                "prompt_enrichment", 0.22,
                "Prompts enriched with professional photography directives",
            )

            # ── STEP 2: Image Generation (Dual Gemini) ────────
            await tracker.update_step(
                "image_generation", 0.25,
                "Generating scene images...",
                status=JobStatus.GENERATING_IMAGES,
            )

            image_engine = DualGeminiEngine(
                cache_dir=file_mgr.cache_dir,
                cache_enabled=PIPELINE_DEFAULTS.cache_enabled,
            )

            # Initialize character session for face consistency
            if mode == PipelineMode.PERSONNAGE_ET_PRODUIT and valid_mannequin:
                await image_engine.initialize_character_session(
                    valid_mannequin, valid_decor,
                )

            personnage_scenes = [
                s for s in scenes if s.analysis.type == SceneType.PERSONNAGE
            ]
            produit_scenes = [
                s for s in scenes if s.analysis.type == SceneType.PRODUIT
            ]

            # Personnage: SEQUENTIAL (chat session maintains face memory)
            for scene in personnage_scenes:
                try:
                    await tracker.update_scene(
                        scene.analysis.id, status="generating_image",
                    )
                    await image_engine.generate_scene(
                        scene, mode, file_mgr.images_dir,
                        product_paths=valid_product,
                        decor_paths=valid_decor,
                    )
                    await tracker.update_scene(
                        scene.analysis.id, image_ready=True,
                    )
                except Exception as e:
                    scene.status = "image_failed"
                    scene.error = str(e)
                    logger.error(
                        "[PIPELINE] Image failed scene %d: %s",
                        scene.analysis.id, e,
                    )

            # Produit: PARALLEL (no session dependency)
            if produit_scenes:
                prod_tasks = [
                    image_engine.generate_scene(
                        s, mode, file_mgr.images_dir,
                        product_paths=valid_product,
                        decor_paths=valid_decor,
                    )
                    for s in produit_scenes
                ]
                results = await asyncio.gather(
                    *prod_tasks, return_exceptions=True,
                )
                for scene, result in zip(produit_scenes, results):
                    if isinstance(result, Exception):
                        scene.status = "image_failed"
                        scene.error = str(result)
                        logger.error(
                            "[PIPELINE] Image failed scene %d: %s",
                            scene.analysis.id, result,
                        )
                    else:
                        await tracker.update_scene(
                            scene.analysis.id, image_ready=True,
                        )

            images_done = sum(1 for s in scenes if s.image_path)
            await tracker.update_step(
                "image_generation", 0.45,
                f"Images generated for {images_done}/{len(scenes)} scenes",
            )

            # ── STEP 2.5: Quality Check ───────────────────────
            if quality_check_enabled:
                await tracker.update_step(
                    "quality_check", 0.48,
                    "Verifying image quality...",
                    status=JobStatus.QUALITY_CHECK,
                )

                for scene in scenes:
                    if not scene.is_ready_for_video:
                        continue

                    mannequin_refs = (
                        valid_mannequin
                        if scene.analysis.type == SceneType.PERSONNAGE
                        else None
                    )
                    passes = await self._quality_checker.check_and_decide(
                        scene, mannequin_refs=mannequin_refs,
                    )

                    if (
                        not passes
                        and scene.regeneration_count
                        < PIPELINE_DEFAULTS.max_regeneration_attempts
                    ):
                        logger.info(
                            "[PIPELINE] Regenerating scene %d "
                            "(quality below threshold)",
                            scene.analysis.id,
                        )
                        adjustments = (
                            self._quality_checker.build_retry_prompt_adjustments(
                                scene, [],
                            )
                        )
                        scene.enriched_image_prompt += adjustments
                        scene.regeneration_count += 1

                        try:
                            await image_engine.generate_scene(
                                scene, mode, file_mgr.images_dir,
                                product_paths=valid_product,
                                decor_paths=valid_decor,
                            )
                        except Exception as e:
                            logger.warning(
                                "[PIPELINE] Regeneration failed scene %d: %s",
                                scene.analysis.id, e,
                            )

            # ── STEP 3: Video Generation (Dual Kling) ─────────
            await tracker.update_step(
                "video_generation", 0.55,
                "Generating scene videos (concurrent)...",
                status=JobStatus.GENERATING_VIDEOS,
            )

            video_animator = VideoAnimator()
            await video_animator.generate_all_scenes(
                scenes, mode, file_mgr.videos_dir,
            )

            videos_done = sum(1 for s in scenes if s.is_complete)
            await tracker.update_step(
                "video_generation", 0.82,
                f"Videos generated for {videos_done}/{len(scenes)} scenes",
            )

            # ── STEP 4: Final Assembly (FFmpeg) ───────────────
            await tracker.update_step(
                "assembly", 0.85,
                "Assembling final video...",
                status=JobStatus.ASSEMBLING,
            )

            final_scenes = sorted(
                [s for s in scenes if s.is_complete],
                key=lambda s: s.analysis.id,
            )

            if not final_scenes:
                raise NoScenesError()

            assembler = VideoAssembler(
                ffmpeg_path=settings.ffmpeg_path,
                quality=self._quality_level,
                resolution=settings.output_resolution,
            )

            output_path = file_mgr.final_video_path()
            final_video = await assembler.assemble(
                scenes=final_scenes,
                output_path=output_path,
                music_path=music_path,
                logo_path=logo_path,
            )

            # ── Success ───────────────────────────────────────
            video_url = f"/outputs/{project_id}/final_ad.mp4"
            await tracker.complete(video_url)

            report = self._build_report(
                project_id, mode, metadata, scenes, final_video, video_url,
            )
            file_mgr.save_report(report)
            file_mgr.cleanup_temp()

            logger.info("[PIPELINE] Completed: %s", video_url)
            return report

        except Exception as e:
            await tracker.fail(str(e))

            # Save error report with partial progress
            partial_state = {
                "scenes": [
                    {
                        "id": s.analysis.id,
                        "type": s.analysis.type.value,
                        "status": s.status,
                        "image_path": s.image_path,
                        "video_path": s.video_path,
                        "error": s.error,
                    }
                    for s in scenes
                ]
            }
            file_mgr.save_error_report(e, partial_state)
            logger.exception("[PIPELINE] Failed for project %s", project_id)
            raise

        finally:
            if video_animator:
                await video_animator.close()

    # ── Report Builder ────────────────────────────────────────

    def _build_report(
        self,
        project_id: str,
        mode: PipelineMode,
        metadata: dict,
        scenes: list[ScenePipeline],
        final_video: str,
        video_url: str,
    ) -> dict:
        """Build the pipeline success report with full scene telemetry."""
        return {
            "status": "completed",
            "project_id": project_id,
            "mode": mode.value,
            "metadata": metadata,
            "video_path": final_video,
            "video_url": video_url,
            "scenes": [
                {
                    "id": s.analysis.id,
                    "type": s.analysis.type.value,
                    "status": s.status,
                    "image_path": s.image_path,
                    "video_path": s.video_path,
                    "image_model": s.image_generation_model,
                    "video_model": s.video_generation_model,
                    "image_time_ms": s.image_generation_time_ms,
                    "video_time_ms": s.video_generation_time_ms,
                    "quality_score": s.quality_score,
                    "cache_hit": s.cache_hit,
                    "used_fallback": s.used_fallback,
                    "regenerations": s.regeneration_count,
                    "error": s.error,
                }
                for s in scenes
            ],
            "stats": {
                "total_scenes": len(scenes),
                "completed_scenes": sum(
                    1 for s in scenes if s.is_complete
                ),
                "failed_scenes": sum(
                    1 for s in scenes if "failed" in (s.status or "")
                ),
                "cache_hits": sum(1 for s in scenes if s.cache_hit),
                "fallbacks": sum(1 for s in scenes if s.used_fallback),
                "regenerations": sum(
                    s.regeneration_count for s in scenes
                ),
            },
        }
