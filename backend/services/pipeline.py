"""
Pipeline Orchestrator — AdGenAI

Coordinates the full pipeline:
  Step 0: Mode detection (mannequin photos?)
  Step 1: GPT-4o scenario analysis
  Step 1.5: Prompt optimization
  Step 2: Gemini image generation (dual or single engine)
  Step 3: Kling AI video generation (async, parallel)
  Step 4: FFmpeg final assembly
"""
from __future__ import annotations

import asyncio
import logging
from datetime import datetime
from pathlib import Path

from backend.config import settings
from backend.models.schemas import (
    JobStatus,
    PipelineMode,
    PipelineState,
    ScenePipeline,
    SceneType,
)
from backend.services.assembler import FFmpegAssembler
from backend.services.image_generator import ImageGenerator
from backend.services.prompt_optimizer import PromptOptimizer
from backend.services.scenario_analyzer import ScenarioAnalyzer
from backend.services.video_generator import VideoGenerator

logger = logging.getLogger(__name__)


class PipelineOrchestrator:
    def __init__(self, on_progress=None):
        self.analyzer = ScenarioAnalyzer()
        self.optimizer = PromptOptimizer()
        self.image_gen = ImageGenerator()
        self.video_gen = VideoGenerator()
        self.assembler = FFmpegAssembler()
        self._on_progress = on_progress  # callback(state) for WebSocket updates

    async def _notify(self, state: PipelineState):
        state.updated_at = datetime.utcnow()
        if self._on_progress:
            await self._on_progress(state)

    # ── STEP 0: Mode Detection ────────────────────────────────

    def detect_mode(self, mannequin_images: list[str]) -> PipelineMode:
        if mannequin_images:
            logger.info("Mode: CHARACTER_PRODUCT (%d mannequin images)", len(mannequin_images))
            return PipelineMode.CHARACTER_PRODUCT
        logger.info("Mode: PRODUCT_ONLY")
        return PipelineMode.PRODUCT_ONLY

    # ── FULL PIPELINE ─────────────────────────────────────────

    async def run(self, state: PipelineState) -> PipelineState:
        """Execute the complete pipeline from scenario to final video."""
        project_dir = settings.output_dir / state.project_id
        project_dir.mkdir(parents=True, exist_ok=True)
        images_dir = project_dir / "images"
        videos_dir = project_dir / "videos"
        images_dir.mkdir(exist_ok=True)
        videos_dir.mkdir(exist_ok=True)

        try:
            # ── STEP 1: Scenario Analysis ─────────────────────
            state.status = JobStatus.ANALYZING
            state.progress = 0.05
            await self._notify(state)

            analysis = await self.analyzer.analyze(
                scenario=state.analysis.concept if state.analysis else "",
                mode=state.mode,
                project_id=state.project_id,
                brand_name=None,
                brand_tone=None,
            )
            # Re-extract scenario from the state — analysis.concept was a placeholder
            # The actual scenario is passed via the API. We'll fix the call in run_from_scenario.

            state.analysis = analysis
            state.scenes = [ScenePipeline(analysis=s) for s in analysis.scenes]
            state.progress = 0.15
            await self._notify(state)

            # ── STEP 1.5: Prompt Optimization ─────────────────
            optimization_tasks = [
                self.optimizer.optimize_scene(
                    scene,
                    visual_style=analysis.visual_style,
                    brand_tone=analysis.tone,
                )
                for scene in state.scenes
            ]
            await asyncio.gather(*optimization_tasks)
            state.progress = 0.25
            await self._notify(state)

            # ── STEP 2: Image Generation ──────────────────────
            state.status = JobStatus.GENERATING_IMAGES
            await self._notify(state)

            # Initialize character session if needed
            if state.mode == PipelineMode.CHARACTER_PRODUCT and state.mannequin_images:
                await self.image_gen.initialize_character_session(
                    mannequin_images=state.mannequin_images,
                    decor_images=state.decor_images,
                )

            # Generate images — character scenes sequentially (session), products in parallel
            character_scenes = [s for s in state.scenes if s.analysis.type == SceneType.CHARACTER]
            product_scenes = [s for s in state.scenes if s.analysis.type == SceneType.PRODUCT]

            # Character scenes must be sequential to maintain session coherence
            for scene in character_scenes:
                scene.image_path = await self.image_gen.generate_scene_image(
                    scene, state.mode, images_dir,
                    product_images=state.product_images,
                    decor_images=state.decor_images,
                )
                scene.status = "image_ready"

            # Product scenes can run in parallel
            if product_scenes:
                product_tasks = [
                    self.image_gen.generate_scene_image(
                        scene, state.mode, images_dir,
                        product_images=state.product_images,
                        decor_images=state.decor_images,
                    )
                    for scene in product_scenes
                ]
                results = await asyncio.gather(*product_tasks, return_exceptions=True)
                for scene, result in zip(product_scenes, results):
                    if isinstance(result, Exception):
                        scene.error = str(result)
                        scene.status = "image_failed"
                        logger.error("Image failed for scene %d: %s", scene.analysis.id, result)
                    else:
                        scene.image_path = result
                        scene.status = "image_ready"

            state.progress = 0.50
            await self._notify(state)

            # ── STEP 3: Video Generation (parallel) ───────────
            state.status = JobStatus.GENERATING_VIDEOS
            await self._notify(state)

            ready_scenes = [s for s in state.scenes if s.status == "image_ready"]
            video_tasks = [
                self.video_gen.generate_scene_video(scene, state.mode, videos_dir)
                for scene in ready_scenes
            ]
            video_results = await asyncio.gather(*video_tasks, return_exceptions=True)

            for scene, result in zip(ready_scenes, video_results):
                if isinstance(result, Exception):
                    logger.warning("Video failed for scene %d: %s — retrying", scene.analysis.id, result)
                    # One retry
                    try:
                        result = await self.video_gen.generate_scene_video(scene, state.mode, videos_dir)
                        scene.video_path = result
                        scene.status = "video_ready"
                        scene.retry_count = 1
                    except Exception as e2:
                        scene.error = str(e2)
                        scene.status = "video_failed"
                else:
                    scene.video_path = result
                    scene.status = "video_ready"

            state.progress = 0.80
            await self._notify(state)

            # ── STEP 4: Final Assembly ────────────────────────
            state.status = JobStatus.ASSEMBLING
            await self._notify(state)

            final_scenes = [s for s in state.scenes if s.status == "video_ready"]
            if not final_scenes:
                raise RuntimeError("No scenes completed video generation")

            # Sort by scene ID to maintain narrative order
            final_scenes.sort(key=lambda s: s.analysis.id)

            output_path = project_dir / "final_ad.mp4"
            state.final_video_path = await self.assembler.assemble(
                scenes=final_scenes,
                output_path=output_path,
                music_path=state.music_path,
                logo_path=state.logo_path,
            )
            state.final_video_url = f"/outputs/{state.project_id}/final_ad.mp4"

            state.status = JobStatus.COMPLETED
            state.progress = 1.0
            await self._notify(state)

            logger.info("Pipeline completed for project %s", state.project_id)
            return state

        except Exception as e:
            state.status = JobStatus.FAILED
            state.error = str(e)
            await self._notify(state)
            logger.exception("Pipeline failed for project %s: %s", state.project_id, e)
            raise

        finally:
            await self.video_gen.close()

    async def run_from_scenario(
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
    ) -> PipelineState:
        """Convenience method: create state and run full pipeline."""
        mode = self.detect_mode(mannequin_images or [])

        state = PipelineState(
            project_id=project_id,
            mode=mode,
            mannequin_images=mannequin_images or [],
            product_images=product_images or [],
            decor_images=decor_images or [],
            logo_path=logo_path,
            music_path=music_path,
        )

        # Step 1: Analyze scenario
        state.status = JobStatus.ANALYZING
        state.progress = 0.05
        await self._notify(state)

        analysis = await self.analyzer.analyze(
            scenario=scenario,
            mode=mode,
            project_id=project_id,
            brand_name=brand_name,
            brand_tone=brand_tone,
        )
        state.analysis = analysis
        state.scenes = [ScenePipeline(analysis=s) for s in analysis.scenes]

        # Continue with optimization → images → videos → assembly
        return await self._run_from_optimization(state)

    async def _run_from_optimization(self, state: PipelineState) -> PipelineState:
        """Run pipeline from prompt optimization onward (reusable after analysis)."""
        project_dir = settings.output_dir / state.project_id
        project_dir.mkdir(parents=True, exist_ok=True)
        images_dir = project_dir / "images"
        videos_dir = project_dir / "videos"
        images_dir.mkdir(exist_ok=True)
        videos_dir.mkdir(exist_ok=True)

        try:
            # Prompt optimization
            state.progress = 0.15
            await self._notify(state)
            opt_tasks = [
                self.optimizer.optimize_scene(
                    scene,
                    visual_style=state.analysis.visual_style if state.analysis else "",
                    brand_tone=state.analysis.tone if state.analysis else "",
                )
                for scene in state.scenes
            ]
            await asyncio.gather(*opt_tasks)
            state.progress = 0.25
            await self._notify(state)

            # Image generation
            state.status = JobStatus.GENERATING_IMAGES
            await self._notify(state)

            if state.mode == PipelineMode.CHARACTER_PRODUCT and state.mannequin_images:
                await self.image_gen.initialize_character_session(
                    mannequin_images=state.mannequin_images,
                    decor_images=state.decor_images,
                )

            char_scenes = [s for s in state.scenes if s.analysis.type == SceneType.CHARACTER]
            prod_scenes = [s for s in state.scenes if s.analysis.type == SceneType.PRODUCT]

            for scene in char_scenes:
                scene.image_path = await self.image_gen.generate_scene_image(
                    scene, state.mode, images_dir,
                    product_images=state.product_images, decor_images=state.decor_images,
                )
                scene.status = "image_ready"

            if prod_scenes:
                results = await asyncio.gather(*[
                    self.image_gen.generate_scene_image(
                        scene, state.mode, images_dir,
                        product_images=state.product_images, decor_images=state.decor_images,
                    )
                    for scene in prod_scenes
                ], return_exceptions=True)
                for scene, r in zip(prod_scenes, results):
                    if isinstance(r, Exception):
                        scene.error = str(r)
                        scene.status = "image_failed"
                    else:
                        scene.image_path = r
                        scene.status = "image_ready"

            state.progress = 0.50
            await self._notify(state)

            # Video generation
            state.status = JobStatus.GENERATING_VIDEOS
            await self._notify(state)

            ready = [s for s in state.scenes if s.status == "image_ready"]
            vid_results = await asyncio.gather(*[
                self.video_gen.generate_scene_video(s, state.mode, videos_dir)
                for s in ready
            ], return_exceptions=True)

            for scene, r in zip(ready, vid_results):
                if isinstance(r, Exception):
                    try:
                        r = await self.video_gen.generate_scene_video(scene, state.mode, videos_dir)
                        scene.video_path = r
                        scene.status = "video_ready"
                        scene.retry_count = 1
                    except Exception as e2:
                        scene.error = str(e2)
                        scene.status = "video_failed"
                else:
                    scene.video_path = r
                    scene.status = "video_ready"

            state.progress = 0.80
            await self._notify(state)

            # Assembly
            state.status = JobStatus.ASSEMBLING
            await self._notify(state)

            final = sorted(
                [s for s in state.scenes if s.status == "video_ready"],
                key=lambda s: s.analysis.id,
            )
            if not final:
                raise RuntimeError("No scenes completed video generation")

            output_path = settings.output_dir / state.project_id / "final_ad.mp4"
            state.final_video_path = await self.assembler.assemble(
                scenes=final, output_path=output_path,
                music_path=state.music_path, logo_path=state.logo_path,
            )
            state.final_video_url = f"/outputs/{state.project_id}/final_ad.mp4"
            state.status = JobStatus.COMPLETED
            state.progress = 1.0
            await self._notify(state)
            return state

        except Exception as e:
            state.status = JobStatus.FAILED
            state.error = str(e)
            await self._notify(state)
            raise
        finally:
            await self.video_gen.close()
