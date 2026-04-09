"""
File and directory management for the AdGenAI pipeline.

Handles temp directory creation, cleanup, file validation,
and structured project directory layouts.
"""

from __future__ import annotations

import json
import logging
import shutil
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


class ProjectFileManager:
    """Manages the file system layout for a pipeline run.

    Creates and tracks all directories needed during generation,
    and handles cleanup on success or failure.

    Directory structure per project:
        {output_dir}/{project_id}/
            images/          # Generated scene images
            videos/          # Generated scene video clips
            cache/           # Prompt+ref hash cache
            temp/            # Intermediate files (cleaned up)
            reports/         # JSON progress and error reports
            final_ad.mp4     # Assembled output
    """

    def __init__(self, base_output_dir: Path, project_id: str) -> None:
        self.project_id = project_id
        self.project_dir = base_output_dir / project_id
        self.images_dir = self.project_dir / "images"
        self.videos_dir = self.project_dir / "videos"
        self.cache_dir = self.project_dir / "cache"
        self.temp_dir = self.project_dir / "temp"
        self.reports_dir = self.project_dir / "reports"

    def setup(self) -> None:
        """Create all project directories."""
        for d in (
            self.project_dir,
            self.images_dir,
            self.videos_dir,
            self.cache_dir,
            self.temp_dir,
            self.reports_dir,
        ):
            d.mkdir(parents=True, exist_ok=True)
        logger.info("[FILE] Project directories created: %s", self.project_dir)

    def cleanup_temp(self) -> None:
        """Remove temporary files (keep images, videos, reports)."""
        if self.temp_dir.exists():
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            logger.info("[FILE] Temp directory cleaned: %s", self.temp_dir)

    def cleanup_all(self) -> None:
        """Remove the entire project directory (for failed runs)."""
        if self.project_dir.exists():
            shutil.rmtree(self.project_dir, ignore_errors=True)
            logger.info("[FILE] Project directory removed: %s", self.project_dir)

    def scene_image_path(self, scene_index: int, scene_type: str) -> Path:
        """Generate a unique path for a scene's image."""
        return self.images_dir / f"scene_{scene_index:03d}_{scene_type}.png"

    def scene_video_path(self, scene_index: int) -> Path:
        """Generate a unique path for a scene's video clip."""
        return self.videos_dir / f"scene_{scene_index:03d}.mp4"

    def final_video_path(self, suffix: str = "") -> Path:
        """Path for the final assembled video."""
        name = f"final_ad{suffix}.mp4"
        return self.project_dir / name

    def report_path(self, report_type: str = "pipeline") -> Path:
        """Path for a JSON report file."""
        return self.reports_dir / f"{report_type}_report.json"

    def save_report(
        self,
        report_data: dict[str, Any],
        report_type: str = "pipeline",
    ) -> Path:
        """Save a JSON report to the reports directory.

        Args:
            report_data: Dictionary to serialize as JSON.
            report_type: Report filename prefix.

        Returns:
            Path to the saved report file.
        """
        report_data["generated_at"] = datetime.now(timezone.utc).isoformat()
        report_data["project_id"] = self.project_id

        path = self.report_path(report_type)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(report_data, indent=2, default=str), encoding="utf-8")
        logger.info("[FILE] Report saved: %s", path)
        return path

    def save_error_report(
        self,
        error: Exception,
        partial_state: dict[str, Any] | None = None,
    ) -> Path:
        """Save an error report with partial progress data.

        Args:
            error: The exception that caused the failure.
            partial_state: Whatever pipeline state was achieved before failure.

        Returns:
            Path to the saved error report.
        """
        report = {
            "status": "failed",
            "error_type": type(error).__name__,
            "error_message": str(error),
            "partial_state": partial_state,
        }

        # Include AdGenError details if available
        if hasattr(error, "to_dict"):
            report["error_details"] = error.to_dict()

        return self.save_report(report, report_type="error")


def validate_file_exists(path: str | Path, label: str = "file") -> Path:
    """Validate that a file exists and return its Path.

    Args:
        path: File path to validate.
        label: Human-readable label for error messages.

    Returns:
        Validated Path object.

    Raises:
        FileNotFoundError: If the file doesn't exist.
    """
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"{label} not found: {p}")
    if not p.is_file():
        raise FileNotFoundError(f"{label} is not a file: {p}")
    return p


def validate_video_file(path: str | Path, min_size_bytes: int = 1024) -> Path:
    """Validate a downloaded video file is not corrupted.

    Args:
        path: Path to the video file.
        min_size_bytes: Minimum acceptable file size (default 1KB).

    Returns:
        Validated Path object.

    Raises:
        ValueError: If the file is too small (likely corrupted).
    """
    p = validate_file_exists(path, "Video file")
    size = p.stat().st_size
    if size < min_size_bytes:
        raise ValueError(
            f"Video file too small ({size} bytes < {min_size_bytes}), "
            f"likely corrupted: {p}"
        )
    return p
