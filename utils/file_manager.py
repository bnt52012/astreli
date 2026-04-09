"""
File management — temp dirs, cleanup, project structure.
"""
from __future__ import annotations

import logging
import shutil
import tempfile
import uuid
from pathlib import Path

logger = logging.getLogger(__name__)


class FileManager:
    """Manages temporary and output directories for pipeline runs."""

    def __init__(self, base_dir: Path | None = None) -> None:
        self.base_dir = base_dir or Path(tempfile.gettempdir()) / "adgenai"
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._temp_dirs: list[Path] = []

    def create_project_dir(self, project_id: str | None = None) -> Path:
        pid = project_id or str(uuid.uuid4())[:8]
        project_dir = self.base_dir / pid
        project_dir.mkdir(parents=True, exist_ok=True)
        for sub in ("images", "videos", "assembly", "reports"):
            (project_dir / sub).mkdir(exist_ok=True)
        self._temp_dirs.append(project_dir)
        logger.info("Created project dir: %s", project_dir)
        return project_dir

    def create_temp_dir(self, prefix: str = "adgenai_") -> Path:
        tmp = Path(tempfile.mkdtemp(prefix=prefix, dir=self.base_dir))
        self._temp_dirs.append(tmp)
        return tmp

    def cleanup(self, keep_output: bool = True) -> None:
        for d in self._temp_dirs:
            if d.exists() and not keep_output:
                shutil.rmtree(d, ignore_errors=True)
                logger.info("Cleaned up: %s", d)

    @staticmethod
    def ensure_dir(path: Path) -> Path:
        path.mkdir(parents=True, exist_ok=True)
        return path

    @staticmethod
    def safe_filename(name: str) -> str:
        """Sanitize filename."""
        return "".join(c if c.isalnum() or c in "._-" else "_" for c in name)

    @staticmethod
    def validate_files_exist(paths: list[str]) -> list[str]:
        """Validate that all paths exist, return list of valid ones."""
        valid = []
        for p in paths:
            if Path(p).exists():
                valid.append(p)
            else:
                logger.warning("File not found: %s", p)
        return valid
