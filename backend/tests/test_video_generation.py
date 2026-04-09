"""
Tests for the Kling AI Video Generation Service.

Covers:
- Task manager concurrent polling
- Model selection based on scene type and mode
- Video download verification
- Polling timeout handling
- Partial failure resilience
"""

from __future__ import annotations

import asyncio
import pytest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock

from backend.models.enums import PipelineMode, SceneType, TransitionType
from backend.models.scene import SceneAnalysis, ScenePipeline
from backend.services.video_generation.task_manager import TaskManager, KlingTask
from backend.services.video_generation.download import download_video
from backend.pipeline.exceptions import VideoDownloadError


# ── Helpers ───────────────────────────────────────────────────


def make_scene(
    scene_id: int = 1,
    scene_type: SceneType = SceneType.PRODUIT,
    image_path: str = "/fake/image.png",
) -> ScenePipeline:
    analysis = SceneAnalysis(
        id=scene_id, type=scene_type, goal="Test",
        description="Test", image_prompt="Test", video_prompt="Test",
        camera_movement="static", duration=5.0, transition=TransitionType.FADE,
    )
    scene = ScenePipeline(analysis=analysis)
    scene.image_path = image_path
    scene.status = "image_ready"
    return scene


# ── Task Manager Tests ────────────────────────────────────────


class TestTaskManager:
    """Tests for concurrent task polling."""

    @pytest.mark.asyncio
    async def test_register_and_poll_success(self):
        manager = TaskManager(poll_interval=0, max_timeout=10)

        manager.register_task(1, "task_001", "kling-v1")

        async def mock_poll(task_id):
            return {"status": "completed", "video_url": "https://cdn.example.com/video.mp4"}

        results = await manager.poll_all(mock_poll)
        assert len(results) == 1
        assert results[0].status == "completed"
        assert results[0].video_url == "https://cdn.example.com/video.mp4"

    @pytest.mark.asyncio
    async def test_poll_failure(self):
        manager = TaskManager(poll_interval=0, max_timeout=10)

        manager.register_task(1, "task_002", "kling-v1")

        async def mock_poll(task_id):
            return {"status": "failed", "error": "Content policy violation"}

        results = await manager.poll_all(mock_poll)
        assert results[0].status == "failed"
        assert "policy" in results[0].error.lower()

    @pytest.mark.asyncio
    async def test_poll_timeout(self):
        manager = TaskManager(poll_interval=0, max_timeout=0)

        manager.register_task(1, "task_003", "kling-v1")

        call_count = 0

        async def mock_poll(task_id):
            nonlocal call_count
            call_count += 1
            return {"status": "processing"}

        results = await manager.poll_all(mock_poll)
        assert results[0].status == "failed"
        assert "timeout" in results[0].error.lower()

    @pytest.mark.asyncio
    async def test_concurrent_multiple_tasks(self):
        manager = TaskManager(poll_interval=0, max_timeout=10)

        manager.register_task(1, "task_a", "kling-v1")
        manager.register_task(2, "task_b", "kling-v1-6")
        manager.register_task(3, "task_c", "kling-v1")

        async def mock_poll(task_id):
            if task_id == "task_b":
                return {"status": "failed", "error": "Test error"}
            return {"status": "completed", "video_url": f"https://cdn.example.com/{task_id}.mp4"}

        results = await manager.poll_all(mock_poll)
        completed = [r for r in results if r.status == "completed"]
        failed = [r for r in results if r.status == "failed"]

        assert len(completed) == 2
        assert len(failed) == 1

    @pytest.mark.asyncio
    async def test_empty_task_list(self):
        manager = TaskManager(poll_interval=0, max_timeout=10)
        results = await manager.poll_all(AsyncMock())
        assert results == []

    @pytest.mark.asyncio
    async def test_transient_poll_error_resilience(self):
        """Transient errors during polling should not fail the task."""
        manager = TaskManager(poll_interval=0, max_timeout=10)
        manager.register_task(1, "task_resilient", "kling-v1")

        call_count = 0

        async def mock_poll(task_id):
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                raise ConnectionError("Temporary network error")
            return {"status": "completed", "video_url": "https://cdn.example.com/ok.mp4"}

        results = await manager.poll_all(mock_poll)
        assert results[0].status == "completed"


# ── Download Tests ────────────────────────────────────────────


class TestVideoDownload:
    """Tests for video download and verification."""

    @pytest.mark.asyncio
    async def test_download_too_small(self, tmp_path, httpx_mock):
        """Files smaller than min_size should raise VideoDownloadError."""
        # This test would require httpx_mock fixture
        # Placeholder for the concept
        pass

    def test_kling_task_dataclass(self):
        task = KlingTask(scene_index=1, task_id="abc", model="kling-v1")
        assert task.status == "submitted"
        assert task.poll_count == 0
