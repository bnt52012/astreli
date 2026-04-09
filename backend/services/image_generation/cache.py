"""
Scene-Level Image Cache.

Caches generated images based on a hash of:
- The enriched image prompt
- Reference image hashes
- Generation parameters

If the prompt + refs haven't changed, skip regeneration and reuse
the cached image. This saves API costs during iterative development.
"""

from __future__ import annotations

import hashlib
import json
import logging
from pathlib import Path

from backend.utils.image_utils import compute_image_hash

logger = logging.getLogger(__name__)


class ImageCache:
    """Prompt + reference hash-based image cache.

    Cache structure:
        {cache_dir}/
            {hash}.json      # Metadata (prompt, params, timestamp)
            {hash}.png        # Cached image
    """

    def __init__(self, cache_dir: Path, enabled: bool = True) -> None:
        self._cache_dir = cache_dir
        self._enabled = enabled
        if enabled:
            cache_dir.mkdir(parents=True, exist_ok=True)

    def compute_cache_key(
        self,
        prompt: str,
        reference_paths: list[str] | None = None,
        model: str = "",
    ) -> str:
        """Compute a deterministic cache key for a generation request.

        Args:
            prompt: The enriched image prompt.
            reference_paths: Paths to reference images.
            model: Model name.

        Returns:
            Hex hash string.
        """
        hasher = hashlib.sha256()
        hasher.update(prompt.encode("utf-8"))
        hasher.update(model.encode("utf-8"))

        if reference_paths:
            for path in sorted(reference_paths):
                try:
                    img_hash = compute_image_hash(path)
                    hasher.update(img_hash.encode("utf-8"))
                except Exception:
                    hasher.update(path.encode("utf-8"))

        return hasher.hexdigest()[:24]

    def get(self, cache_key: str) -> str | None:
        """Check if a cached image exists for the given key.

        Args:
            cache_key: Hash key from compute_cache_key().

        Returns:
            Path to cached image, or None if not cached.
        """
        if not self._enabled:
            return None

        image_path = self._cache_dir / f"{cache_key}.png"
        meta_path = self._cache_dir / f"{cache_key}.json"

        if image_path.exists() and meta_path.exists():
            # Validate the cached image is not empty/corrupt
            if image_path.stat().st_size > 100:
                logger.info("[CACHE] Hit for key %s", cache_key)
                return str(image_path)

        return None

    def put(
        self,
        cache_key: str,
        source_image_path: str,
        prompt: str,
        model: str = "",
    ) -> str:
        """Store a generated image in the cache.

        Args:
            cache_key: Hash key.
            source_image_path: Path to the generated image to cache.
            prompt: The prompt used (for metadata).
            model: Model used (for metadata).

        Returns:
            Path to the cached image.
        """
        if not self._enabled:
            return source_image_path

        import shutil
        from datetime import datetime, timezone

        dest_image = self._cache_dir / f"{cache_key}.png"
        dest_meta = self._cache_dir / f"{cache_key}.json"

        # Copy image to cache
        shutil.copy2(source_image_path, dest_image)

        # Save metadata
        meta = {
            "cache_key": cache_key,
            "prompt": prompt[:500],
            "model": model,
            "cached_at": datetime.now(timezone.utc).isoformat(),
            "source_path": source_image_path,
        }
        dest_meta.write_text(json.dumps(meta, indent=2), encoding="utf-8")

        logger.info("[CACHE] Stored key %s", cache_key)
        return str(dest_image)

    def clear(self) -> int:
        """Clear all cached images. Returns number of entries removed."""
        if not self._cache_dir.exists():
            return 0

        count = 0
        for f in self._cache_dir.iterdir():
            if f.suffix in (".png", ".json"):
                f.unlink()
                count += 1

        logger.info("[CACHE] Cleared %d cache entries", count // 2)
        return count // 2
