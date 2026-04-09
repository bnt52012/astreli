"""
AdGenAI Pipeline Configuration & Validation.

Reads env vars, validates prerequisites (API keys, ffmpeg, LoRA),
provides typed settings used everywhere.
"""
from __future__ import annotations

import logging
import os
import shutil
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv

from pipeline.exceptions import APIKeyMissingError, ConfigError, FFmpegNotFoundError

# Load .env from project root so os.getenv() picks up API keys
_project_root = Path(__file__).resolve().parent.parent
load_dotenv(_project_root / ".env")

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PipelineDefaults:
    """Immutable pipeline-wide defaults."""
    # GPT-4o
    openai_model: str = "gpt-4o"
    openai_max_tokens: int = 8192
    openai_temperature: float = 0.3
    # Gemini (Nano Banana 2)
    gemini_model: str = "gemini-2.5-flash-image"
    gemini_image_size: str = "1024x1024"
    # Fal.ai (Kling via Fal) — pay-as-you-go, no direct Kling JWT needed
    fal_model_product: str = "fal-ai/kling-video/v2.5-turbo/pro/image-to-video"
    fal_model_human: str = "fal-ai/kling-video/o1/pro/image-to-video"
    fal_timeout: int = 600
    # Replicate / LoRA
    replicate_sdxl_model: str = "stability-ai/sdxl"
    replicate_inpaint_model: str = "stability-ai/stable-diffusion-xl-inpainting"
    # FFmpeg
    ffmpeg_crf: int = 18
    ffmpeg_preset: str = "slow"
    ffmpeg_fps: int = 24
    ffmpeg_resolution: str = "1920x1080"
    # Quality
    quality_threshold: float = 7.0
    max_quality_retries: int = 3
    # Durations
    min_scene_duration: float = 2.0
    max_scene_duration: float = 8.0
    # Output
    default_aspect_ratio: str = "16:9"


PIPELINE_DEFAULTS = PipelineDefaults()


@dataclass
class Settings:
    """Runtime settings populated from env + validation."""
    gemini_api_key: str = ""
    openai_api_key: str = ""
    fal_key: str = ""
    replicate_api_token: str = ""
    output_dir: Path = field(default_factory=lambda: Path("/tmp/adgenai_output"))
    cache_dir: Path = field(default_factory=lambda: Path("/tmp/adgenai_cache"))
    temp_dir: Path = field(default_factory=lambda: Path("/tmp/adgenai_tmp"))
    defaults: PipelineDefaults = field(default_factory=PipelineDefaults)

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
            openai_api_key=os.getenv("OPENAI_API_KEY", ""),
            fal_key=os.getenv("FAL_KEY", ""),
            replicate_api_token=os.getenv("REPLICATE_API_TOKEN", ""),
            output_dir=Path(os.getenv("ADGENAI_OUTPUT_DIR", "/tmp/adgenai_output")),
            cache_dir=Path(os.getenv("ADGENAI_CACHE_DIR", "/tmp/adgenai_cache")),
            temp_dir=Path(os.getenv("ADGENAI_TEMP_DIR", "/tmp/adgenai_tmp")),
        )

    def validate_core(self) -> None:
        """Validate API keys and ffmpeg."""
        missing = []
        if not self.gemini_api_key:
            missing.append("GEMINI_API_KEY")
        if not self.openai_api_key:
            missing.append("OPENAI_API_KEY")
        if not self.fal_key:
            missing.append("FAL_KEY")
        if missing:
            raise APIKeyMissingError(", ".join(missing))
        if not shutil.which("ffmpeg"):
            raise FFmpegNotFoundError()
        for d in (self.output_dir, self.cache_dir, self.temp_dir):
            d.mkdir(parents=True, exist_ok=True)
        logger.info("Core validation passed.")

    def validate_lora(self, lora_model_id: str) -> None:
        """Validate Replicate token when LoRA is selected."""
        if not self.replicate_api_token:
            raise APIKeyMissingError("REPLICATE_API_TOKEN (required for LoRA mode)")
        if not lora_model_id:
            raise ConfigError("LoRA model ID is empty.")
        logger.info("LoRA validation passed for model: %s", lora_model_id)

    def ensure_dirs(self, project_id: str) -> Path:
        """Create and return a project-specific output directory."""
        project_dir = self.output_dir / project_id
        project_dir.mkdir(parents=True, exist_ok=True)
        for sub in ("images", "videos", "assembly"):
            (project_dir / sub).mkdir(exist_ok=True)
        return project_dir


settings = Settings.from_env()
