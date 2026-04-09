"""
Progress tracking and callback system for the AdGenAI pipeline.

Provides a structured way to report pipeline progress to external
consumers (WebSocket, database, logging) without coupling the
pipeline internals to any specific notification mechanism.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Awaitable, Callable

from backend.models.enums import JobStatus

logger = logging.getLogger(__name__)

# Type alias for progress callbacks
ProgressCallback = Callable[["ProgressUpdate"], Awaitable[None]]


@dataclass
class SceneProgress:
    """Progress state for an individual scene."""

    scene_index: int
    scene_type: str
    status: str = "pending"
    step: str = ""
    image_ready: bool = False
    video_ready: bool = False
    quality_checked: bool = False
    error: str | None = None
    elapsed_ms: int = 0


@dataclass
class ProgressUpdate:
    """A single progress update emitted by the pipeline.

    Contains everything a frontend needs to display real-time status.
    """

    project_id: str
    status: JobStatus
    progress: float  # 0.0 to 1.0
    step: str  # Human-readable current step
    message: str  # Detailed status message
    scenes: list[SceneProgress] = field(default_factory=list)
    elapsed_seconds: float = 0.0
    estimated_remaining_seconds: float | None = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class ProgressTracker:
    """Tracks and emits pipeline progress updates.

    Usage:
        tracker = ProgressTracker(project_id, callback=my_callback)
        await tracker.start()
        await tracker.update_step("analyzing", 0.1, "Analyzing scenario...")
        await tracker.update_scene(1, status="generating_image")
        await tracker.complete()
    """

    # Step weights for progress calculation
    STEP_WEIGHTS = {
        "initialization": 0.02,
        "scenario_analysis": 0.10,
        "prompt_enrichment": 0.08,
        "brand_analysis": 0.03,
        "image_generation": 0.30,
        "quality_check": 0.07,
        "video_generation": 0.30,
        "assembly": 0.10,
    }

    def __init__(
        self,
        project_id: str,
        total_scenes: int = 0,
        callback: ProgressCallback | None = None,
    ) -> None:
        self.project_id = project_id
        self.total_scenes = total_scenes
        self._callback = callback
        self._start_time: float = 0.0
        self._current_step = "initialization"
        self._current_progress = 0.0
        self._scenes: dict[int, SceneProgress] = {}
        self._status = JobStatus.PENDING

    async def _emit(self, message: str) -> None:
        """Emit a progress update to the registered callback."""
        if not self._callback:
            return

        elapsed = time.time() - self._start_time if self._start_time else 0.0

        update = ProgressUpdate(
            project_id=self.project_id,
            status=self._status,
            progress=self._current_progress,
            step=self._current_step,
            message=message,
            scenes=list(self._scenes.values()),
            elapsed_seconds=round(elapsed, 1),
        )

        try:
            await self._callback(update)
        except Exception as e:
            logger.warning("[PROGRESS] Callback error: %s", e)

    async def start(self) -> None:
        """Mark pipeline as started."""
        self._start_time = time.time()
        self._status = JobStatus.PENDING
        self._current_progress = 0.0
        await self._emit("Pipeline started")

    async def update_step(
        self,
        step: str,
        progress: float,
        message: str,
        status: JobStatus | None = None,
    ) -> None:
        """Update the current pipeline step and progress.

        Args:
            step: Step identifier (matches STEP_WEIGHTS keys).
            progress: Overall progress 0.0-1.0.
            message: Human-readable status message.
            status: Optional JobStatus override.
        """
        self._current_step = step
        self._current_progress = min(progress, 1.0)
        if status:
            self._status = status
        await self._emit(message)

    async def update_scene(
        self,
        scene_index: int,
        *,
        scene_type: str = "",
        status: str = "",
        step: str = "",
        image_ready: bool | None = None,
        video_ready: bool | None = None,
        quality_checked: bool | None = None,
        error: str | None = None,
    ) -> None:
        """Update progress for an individual scene."""
        if scene_index not in self._scenes:
            self._scenes[scene_index] = SceneProgress(
                scene_index=scene_index,
                scene_type=scene_type,
            )

        scene = self._scenes[scene_index]
        if status:
            scene.status = status
        if step:
            scene.step = step
        if scene_type:
            scene.scene_type = scene_type
        if image_ready is not None:
            scene.image_ready = image_ready
        if video_ready is not None:
            scene.video_ready = video_ready
        if quality_checked is not None:
            scene.quality_checked = quality_checked
        if error is not None:
            scene.error = error

        scene.elapsed_ms = int((time.time() - self._start_time) * 1000)

    async def complete(self, video_url: str | None = None) -> None:
        """Mark pipeline as successfully completed."""
        self._status = JobStatus.COMPLETED
        self._current_progress = 1.0
        self._current_step = "completed"
        await self._emit(
            f"Pipeline completed successfully"
            + (f" - {video_url}" if video_url else "")
        )

    async def fail(self, error: str) -> None:
        """Mark pipeline as failed."""
        self._status = JobStatus.FAILED
        self._current_step = "failed"
        await self._emit(f"Pipeline failed: {error}")
