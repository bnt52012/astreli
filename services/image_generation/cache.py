"""
Scene image caching with prompt hash.
"""
from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ImageCache:
    """Cache generated images by prompt hash to avoid redundant API calls."""

    def __init__(self, cache_dir: Path | None = None, enabled: bool = True) -> None:
        self.enabled = enabled
        self.cache_dir = cache_dir or Path("/tmp/adgenai_cache/images")
        if self.enabled:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._index: dict[str, str] = {}
        self._load_index()

    def compute_key(self, prompt: str) -> str:
        """Compute a deterministic cache key from prompt text."""
        return hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16]

    def get(self, key: str) -> Path | None:
        """Look up cached image. Returns path if hit, None if miss."""
        if not self.enabled:
            return None
        path_str = self._index.get(key)
        if path_str and Path(path_str).exists():
            logger.debug("Cache hit: %s", key)
            return Path(path_str)
        return None

    def put(self, key: str, image_path: Path) -> None:
        """Store image path in cache index."""
        if not self.enabled:
            return
        self._index[key] = str(image_path)
        self._save_index()
        logger.debug("Cached: %s -> %s", key, image_path)

    def clear(self) -> None:
        """Clear all cache entries."""
        self._index.clear()
        self._save_index()

    def _load_index(self) -> None:
        index_file = self.cache_dir / "cache_index.json"
        if index_file.exists():
            try:
                self._index = json.loads(index_file.read_text())
            except Exception:
                self._index = {}

    def _save_index(self) -> None:
        index_file = self.cache_dir / "cache_index.json"
        try:
            index_file.write_text(json.dumps(self._index, indent=2))
        except Exception as e:
            logger.warning("Failed to save cache index: %s", e)
