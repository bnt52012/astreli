"""
Pipeline orchestration layer for AdGenAI.

Coordinates the full advertising video generation pipeline:
  Step 0: Mode detection (mannequin reference photos present?)
  Step 1: GPT-4o scenario analysis and scene decomposition
  Step 1.5: Intelligence layer - prompt enrichment + brand analysis
  Step 2: Dual Gemini image generation (Pro chat / Flash one-shot)
  Step 3: Dual Kling video animation (Video-01 / V3)
  Step 4: FFmpeg final assembly with transitions, audio, logo
"""

from backend.pipeline.exceptions import (
    AdGenError,
    AssemblyError,
    ConfigError,
    GenerationError,
    PipelineError,
)
from backend.pipeline.mode_detector import ModeDetector
from backend.pipeline.orchestrator import PipelineOrchestrator

__all__ = [
    "PipelineOrchestrator",
    "ModeDetector",
    "AdGenError",
    "ConfigError",
    "PipelineError",
    "GenerationError",
    "AssemblyError",
]
