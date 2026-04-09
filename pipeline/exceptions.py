"""
AdGenAI Custom Exception Hierarchy.

Four core exceptions plus specialised sub-classes for every failure mode
the pipeline can encounter.
"""
from __future__ import annotations


class AdGenError(Exception):
    """Root of the AdGenAI exception tree."""
    def __init__(self, message: str, *, details: dict | None = None) -> None:
        super().__init__(message)
        self.details = details or {}


# ── 4 core exceptions ──────────────────────────────────────────────

class ConfigError(AdGenError):
    """Missing or invalid configuration (API keys, paths, etc.)."""

class PipelineError(AdGenError):
    """Failure in pipeline orchestration logic."""

class GenerationError(AdGenError):
    """Failure during content generation (image / video)."""

class AssemblyError(AdGenError):
    """Failure during FFmpeg assembly."""


# ── Specialised sub-classes ─────────────────────────────────────────

class APIKeyMissingError(ConfigError):
    def __init__(self, key_name: str) -> None:
        super().__init__(
            f"Required API key '{key_name}' is missing from environment.",
            details={"key_name": key_name},
        )

class FFmpegNotFoundError(ConfigError):
    def __init__(self) -> None:
        super().__init__("ffmpeg not found in PATH. Install: https://ffmpeg.org/download.html")

class LoRANotAccessibleError(ConfigError):
    def __init__(self, model_id: str, reason: str = "") -> None:
        super().__init__(
            f"LoRA model '{model_id}' is not accessible on Replicate. {reason}",
            details={"model_id": model_id, "reason": reason},
        )

class ScenarioAnalysisError(PipelineError):
    def __init__(self, reason: str, *, status_code: int | None = None) -> None:
        super().__init__(f"Scenario analysis failed: {reason}", details={"status_code": status_code})

class NoScenesError(PipelineError):
    def __init__(self) -> None:
        super().__init__("Scenario analysis produced zero scenes.")

class ImageGenerationError(GenerationError):
    def __init__(self, scene_index: int, reason: str) -> None:
        super().__init__(f"Image generation failed for scene {scene_index}: {reason}", details={"scene_index": scene_index})

class FusionError(GenerationError):
    def __init__(self, scene_index: int, reason: str) -> None:
        super().__init__(f"Fusion failed for scene {scene_index}: {reason}", details={"scene_index": scene_index})

class VideoGenerationError(GenerationError):
    def __init__(self, scene_index: int, reason: str) -> None:
        super().__init__(f"Video generation failed for scene {scene_index}: {reason}", details={"scene_index": scene_index})

class QualityCheckError(GenerationError):
    def __init__(self, scene_index: int, score: float, max_retries: int) -> None:
        super().__init__(
            f"Scene {scene_index} quality {score}/10 after {max_retries} retries.",
            details={"scene_index": scene_index, "score": score},
        )
