"""
Concurrent Kling Task Manager.

Submits ALL video generation tasks concurrently using ThreadPoolExecutor,
then polls all tasks in parallel. Does NOT wait for scene 1 to finish
before submitting scene 2.

Handles:
- Concurrent task submission
- Parallel polling with configurable max workers
- Partial failure handling (continue with successful scenes)
- Priority queue (hero scenes first) — future enhancement
"""

from __future__ import annotations

import asyncio
import logging
from dataclasses import dataclass
from typing import Any

from backend.pipeline.exceptions import PollingTimeoutError, VideoGenerationError

logger = logging.getLogger(__name__)


@dataclass
class KlingTask:
    """Tracks a single Kling video generation task."""

    scene_index: int
    task_id: str
    model: str
    status: str = "submitted"
    video_url: str | None = None
    error: str | None = None
    poll_count: int = 0


class TaskManager:
    """Manages concurrent Kling API task submission and polling.

    Submits all tasks, then polls all in parallel until each completes
    or times out.
    """

    def __init__(
        self,
        poll_interval: int = 10,
        max_timeout: int = 600,
        max_concurrent: int = 4,
    ) -> None:
        self._poll_interval = poll_interval
        self._max_timeout = max_timeout
        self._max_concurrent = max_concurrent
        self._tasks: dict[str, KlingTask] = {}

    def register_task(self, scene_index: int, task_id: str, model: str) -> KlingTask:
        """Register a submitted task for tracking."""
        task = KlingTask(scene_index=scene_index, task_id=task_id, model=model)
        self._tasks[task_id] = task
        logger.info(
            "[TASKS] Registered: scene=%d, task=%s, model=%s",
            scene_index, task_id, model,
        )
        return task

    async def poll_all(
        self,
        poll_fn,
    ) -> list[KlingTask]:
        """Poll all registered tasks concurrently until completion.

        Args:
            poll_fn: Async function(task_id) -> {"status": ..., "video_url": ..., "error": ...}

        Returns:
            List of all KlingTask objects with final status.
        """
        if not self._tasks:
            return []

        # Create semaphore for concurrent polling limit
        semaphore = asyncio.Semaphore(self._max_concurrent)

        async def poll_single(task: KlingTask) -> None:
            async with semaphore:
                await self._poll_task(task, poll_fn)

        # Poll all tasks concurrently
        await asyncio.gather(
            *[poll_single(task) for task in self._tasks.values()],
            return_exceptions=True,
        )

        # Log summary
        completed = sum(1 for t in self._tasks.values() if t.status == "completed")
        failed = sum(1 for t in self._tasks.values() if t.status == "failed")
        logger.info(
            "[TASKS] All polling complete: %d completed, %d failed, %d total",
            completed, failed, len(self._tasks),
        )

        return list(self._tasks.values())

    async def _poll_task(self, task: KlingTask, poll_fn) -> None:
        """Poll a single task until completion or timeout."""
        max_polls = self._max_timeout // self._poll_interval

        for i in range(max_polls):
            task.poll_count = i + 1

            try:
                result = await poll_fn(task.task_id)
                status = result.get("status", "")

                if status == "completed":
                    task.status = "completed"
                    task.video_url = result.get("video_url")
                    logger.info(
                        "[TASKS] Task %s completed (scene=%d, polls=%d)",
                        task.task_id, task.scene_index, i + 1,
                    )
                    return

                if status == "failed":
                    task.status = "failed"
                    task.error = result.get("error", "Unknown error")
                    logger.error(
                        "[TASKS] Task %s failed (scene=%d): %s",
                        task.task_id, task.scene_index, task.error,
                    )
                    return

                # Still processing — continue polling
                if (i + 1) % 6 == 0:  # Log every ~60 seconds
                    logger.info(
                        "[TASKS] Task %s still processing (scene=%d, poll=%d/%d)",
                        task.task_id, task.scene_index, i + 1, max_polls,
                    )

            except Exception as e:
                # Transient error — continue polling (resilient)
                logger.warning(
                    "[TASKS] Poll error for %s (scene=%d, continuing): %s",
                    task.task_id, task.scene_index, e,
                )

            await asyncio.sleep(self._poll_interval)

        # Timeout
        task.status = "failed"
        task.error = f"Polling timeout after {self._max_timeout}s"
        logger.error(
            "[TASKS] Task %s timed out (scene=%d, %d polls)",
            task.task_id, task.scene_index, max_polls,
        )
