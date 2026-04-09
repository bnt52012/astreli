"""
AdGenAI Configuration — Single source of truth for all settings.

All settings are loaded from environment variables with the ADGENAI_ prefix,
or from a .env file in the project root.

Example .env:
    ADGENAI_OPENAI_API_KEY=sk-...
    ADGENAI_GEMINI_API_KEY=AI...
    ADGENAI_KLING_API_KEY=ak-...
    ADGENAI_KLING_API_SECRET=sk-...
"""
from __future__ import annotations

from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # ── API Keys ──────────────────────────────────────────────
    openai_api_key: str = ""
    gemini_api_key: str = ""
    kling_api_key: str = ""
    kling_api_secret: str = ""
    replicate_api_token: str = ""

    # ── Storage ───────────────────────────────────────────────
    upload_dir: Path = Path("storage/uploads")
    output_dir: Path = Path("storage/outputs")
    temp_dir: Path = Path("storage/temp")
    cache_dir: Path = Path("storage/cache")

    # ── Models ────────────────────────────────────────────────
    openai_model: str = "gpt-4o"
    gemini_image_model: str = "gemini-3.1-flash-image-preview"  # Nano Banana 2

    # ── Replicate (LoRA + Inpainting) ─────────────────────────
    replicate_sdxl_inpaint_model: str = "stability-ai/sdxl:inpainting"
    replicate_poll_interval: int = 5  # seconds
    replicate_max_timeout: int = 300  # seconds

    # ── Kling ─────────────────────────────────────────────────
    kling_base_url: str = "https://api.klingai.com"
    kling_poll_interval: int = 10  # seconds
    kling_max_poll: int = 120  # max polls before timeout
    kling_max_concurrent: int = 5  # max parallel polling tasks

    # ── FFmpeg ────────────────────────────────────────────────
    ffmpeg_path: str = "ffmpeg"
    output_resolution: str = "1920x1080"
    output_codec: str = "libx264"
    output_preset: str = "slow"
    output_crf: int = 18

    # ── Pipeline Defaults ────────────────────────────────────
    cache_enabled: bool = True
    quality_check_enabled: bool = True
    max_regeneration_attempts: int = 2
    max_scenes: int = 20

    # ── Server ────────────────────────────────────────────────
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list[str] = ["http://localhost:3000"]
    max_upload_size_mb: int = 100
    redis_url: str = "redis://localhost:6379/0"
    database_url: str = "sqlite+aiosqlite:///./adgenai.db"

    # ── Logging ───────────────────────────────────────────────
    log_level: str = "INFO"
    log_json: bool = False  # True for production (structured JSON logs)
    log_file: str | None = None  # Optional log file path

    model_config = {"env_file": ".env", "env_prefix": "ADGENAI_"}


settings = Settings()

# Ensure directories exist
for d in (settings.upload_dir, settings.output_dir, settings.temp_dir, settings.cache_dir):
    d.mkdir(parents=True, exist_ok=True)
