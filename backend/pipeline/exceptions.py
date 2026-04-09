"""
Custom exception hierarchy for AdGenAI pipeline.

Provides granular error classification so callers can handle specific
failure modes (API rate limits, invalid config, generation failures,
FFmpeg errors) independently and produce actionable error reports.
"""

from __future__ import annotations

from typing import Any


class AdGenError(Exception):
    """Base exception for all AdGenAI pipeline errors.

    Attributes:
        message: Human-readable error description.
        details: Structured data for logging / error reports.
        request_id: Optional API request ID for tracing.
        recoverable: Whether the pipeline can continue past this error.
    """

    def __init__(
        self,
        message: str,
        *,
        details: dict[str, Any] | None = None,
        request_id: str | None = None,
        recoverable: bool = False,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.details = details or {}
        self.request_id = request_id
        self.recoverable = recoverable

    def to_dict(self) -> dict[str, Any]:
        """Serialize for JSON error reports."""
        return {
            "error_type": self.__class__.__name__,
            "message": self.message,
            "details": self.details,
            "request_id": self.request_id,
            "recoverable": self.recoverable,
        }


# ── Configuration Errors ──────────────────────────────────────


class ConfigError(AdGenError):
    """Raised when pipeline configuration is invalid or incomplete.

    Examples:
        - Missing API key environment variable
        - ffmpeg not found in PATH
        - Invalid image resolution format
        - Mannequin reference files don't exist on disk
    """

    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, details=details, recoverable=False)


class MissingAPIKeyError(ConfigError):
    """Raised when a required API key is not set."""

    def __init__(self, key_name: str, env_var: str) -> None:
        super().__init__(
            f"Missing required API key: {key_name}. "
            f"Set the {env_var} environment variable.",
            details={"key_name": key_name, "env_var": env_var},
        )


class FFmpegNotFoundError(ConfigError):
    """Raised when ffmpeg binary is not available."""

    def __init__(self) -> None:
        super().__init__(
            "ffmpeg not found in PATH. Install ffmpeg to use the assembly pipeline.",
            details={"dependency": "ffmpeg"},
        )


class InvalidReferenceError(ConfigError):
    """Raised when reference image files are missing or invalid."""

    def __init__(self, missing_paths: list[str]) -> None:
        super().__init__(
            f"{len(missing_paths)} reference image(s) not found on disk.",
            details={"missing_paths": missing_paths},
        )


# ── Pipeline Errors ───────────────────────────────────────────


class PipelineError(AdGenError):
    """Raised for pipeline orchestration failures.

    Examples:
        - Scenario analysis returned invalid JSON
        - No scenes produced after analysis
        - All scenes failed generation (nothing to assemble)
    """

    def __init__(
        self,
        message: str,
        *,
        step: str | None = None,
        scene_index: int | None = None,
        details: dict[str, Any] | None = None,
        recoverable: bool = False,
    ) -> None:
        _details = details or {}
        if step:
            _details["step"] = step
        if scene_index is not None:
            _details["scene_index"] = scene_index
        super().__init__(message, details=_details, recoverable=recoverable)
        self.step = step
        self.scene_index = scene_index


class ScenarioAnalysisError(PipelineError):
    """Raised when GPT-4o scenario analysis fails."""

    def __init__(self, message: str, *, details: dict[str, Any] | None = None) -> None:
        super().__init__(message, step="scenario_analysis", details=details)


class NoScenesError(PipelineError):
    """Raised when no valid scenes could be produced."""

    def __init__(self, reason: str = "No scenes completed generation") -> None:
        super().__init__(reason, step="validation")


# ── Generation Errors ─────────────────────────────────────────


class GenerationError(AdGenError):
    """Raised when AI content generation fails.

    Covers both image generation (Gemini) and video generation (Kling).
    """

    def __init__(
        self,
        message: str,
        *,
        provider: str = "unknown",
        model: str | None = None,
        scene_index: int | None = None,
        details: dict[str, Any] | None = None,
        request_id: str | None = None,
        recoverable: bool = True,
    ) -> None:
        _details = details or {}
        _details["provider"] = provider
        if model:
            _details["model"] = model
        if scene_index is not None:
            _details["scene_index"] = scene_index
        super().__init__(
            message, details=_details, request_id=request_id, recoverable=recoverable,
        )
        self.provider = provider
        self.model = model
        self.scene_index = scene_index


class ImageGenerationError(GenerationError):
    """Raised when Gemini image generation fails for a scene."""

    def __init__(
        self,
        message: str,
        *,
        model: str | None = None,
        scene_index: int | None = None,
        details: dict[str, Any] | None = None,
        request_id: str | None = None,
    ) -> None:
        super().__init__(
            message,
            provider="gemini",
            model=model,
            scene_index=scene_index,
            details=details,
            request_id=request_id,
            recoverable=True,
        )


class LoRAGenerationError(GenerationError):
    """Raised when LoRA SDXL mannequin generation fails on Replicate."""

    def __init__(
        self,
        message: str,
        *,
        lora_model_id: str | None = None,
        prediction_id: str | None = None,
        scene_index: int | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        _details = details or {}
        if lora_model_id:
            _details["lora_model_id"] = lora_model_id
        if prediction_id:
            _details["prediction_id"] = prediction_id
        super().__init__(
            message,
            provider="replicate",
            scene_index=scene_index,
            details=_details,
            recoverable=True,
        )


class FusionError(GenerationError):
    """Raised when the inpainting fusion step fails."""

    def __init__(
        self,
        message: str,
        *,
        scene_index: int | None = None,
        fusion_pass: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        _details = details or {}
        if fusion_pass:
            _details["fusion_pass"] = fusion_pass
        super().__init__(
            message,
            provider="replicate",
            scene_index=scene_index,
            details=_details,
            recoverable=True,
        )


class LoRANotFoundError(ConfigError):
    """Raised when the selected LoRA model is not accessible on Replicate."""

    def __init__(self, lora_model_id: str) -> None:
        super().__init__(
            f"LoRA model not found or inaccessible: {lora_model_id}",
            details={"lora_model_id": lora_model_id},
        )


class VideoGenerationError(GenerationError):
    """Raised when Kling video generation fails for a scene."""

    def __init__(
        self,
        message: str,
        *,
        model: str | None = None,
        scene_index: int | None = None,
        task_id: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        _details = details or {}
        if task_id:
            _details["task_id"] = task_id
        super().__init__(
            message,
            provider="kling",
            model=model,
            scene_index=scene_index,
            details=_details,
            recoverable=True,
        )


class VideoDownloadError(GenerationError):
    """Raised when a generated video cannot be downloaded or is corrupted."""

    def __init__(
        self,
        message: str,
        *,
        video_url: str | None = None,
        file_size: int | None = None,
    ) -> None:
        super().__init__(
            message,
            provider="kling",
            details={"video_url": video_url, "file_size": file_size},
            recoverable=True,
        )


class PollingTimeoutError(GenerationError):
    """Raised when async task polling exceeds the timeout window."""

    def __init__(self, task_id: str, timeout_seconds: int) -> None:
        super().__init__(
            f"Polling timeout after {timeout_seconds}s for task {task_id}",
            provider="kling",
            details={"task_id": task_id, "timeout_seconds": timeout_seconds},
            recoverable=True,
        )


class RateLimitError(GenerationError):
    """Raised when an API returns 429 Too Many Requests."""

    def __init__(
        self,
        provider: str,
        retry_after: float | None = None,
    ) -> None:
        super().__init__(
            f"Rate limited by {provider}" + (f" (retry after {retry_after}s)" if retry_after else ""),
            provider=provider,
            details={"retry_after": retry_after},
            recoverable=True,
        )


class AuthenticationError(GenerationError):
    """Raised when an API returns 401/403 — invalid or expired key."""

    def __init__(self, provider: str) -> None:
        super().__init__(
            f"Authentication failed for {provider}. Check your API key.",
            provider=provider,
            recoverable=False,
        )


# ── Assembly Errors ───────────────────────────────────────────


class AssemblyError(AdGenError):
    """Raised when FFmpeg video assembly fails.

    Examples:
        - FFmpeg process returns non-zero exit code
        - Missing video clip files
        - Invalid filter graph
        - Output file not created
    """

    def __init__(
        self,
        message: str,
        *,
        ffmpeg_stderr: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        _details = details or {}
        if ffmpeg_stderr:
            # Truncate very long FFmpeg output
            _details["ffmpeg_stderr"] = ffmpeg_stderr[:2000]
        super().__init__(message, details=_details, recoverable=False)
        self.ffmpeg_stderr = ffmpeg_stderr


class MissingClipError(AssemblyError):
    """Raised when a video clip file is missing during assembly."""

    def __init__(self, scene_index: int, expected_path: str) -> None:
        super().__init__(
            f"Video clip missing for scene {scene_index}: {expected_path}",
            details={"scene_index": scene_index, "expected_path": expected_path},
        )


# ── Quality Errors ────────────────────────────────────────────


class QualityCheckError(AdGenError):
    """Raised when generated content fails quality verification."""

    def __init__(
        self,
        message: str,
        *,
        scene_index: int | None = None,
        quality_score: float | None = None,
        issues: list[str] | None = None,
    ) -> None:
        super().__init__(
            message,
            details={
                "scene_index": scene_index,
                "quality_score": quality_score,
                "issues": issues or [],
            },
            recoverable=True,
        )
