"""
Pydantic schemas for the AdGenAI API layer.

These schemas define request/response contracts for the REST API.
Internal pipeline logic uses the dataclasses in models/scene.py instead.

Enums are imported from models/enums.py — the single source of truth.
"""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from backend.models.enums import (
    JobStatus,
    PipelineMode,
    QualityLevel,
    SceneType,
    TargetPlatform,
    TransitionType,
)


# ── Scene (API view) ─────────────────────────────────────────


class SceneAnalysisResponse(BaseModel):
    """Read-only API representation of a scene analysis."""

    id: int
    type: SceneType
    goal: str
    description: str
    image_prompt: str
    video_prompt: str
    camera_movement: str
    lighting: str = ""
    duration: float = Field(ge=2.0, le=10.0, default=5.0)
    transition: TransitionType = TransitionType.FADE
    needs_mannequin: bool = False
    needs_product: bool = False
    needs_decor_ref: bool = False


class ScenePipelineResponse(BaseModel):
    """Read-only API representation of a scene's pipeline state."""

    analysis: SceneAnalysisResponse
    enriched_image_prompt: str = ""
    enriched_video_prompt: str = ""
    image_path: Optional[str] = None
    video_path: Optional[str] = None
    image_generation_model: Optional[str] = None
    video_generation_model: Optional[str] = None
    quality_score: Optional[float] = None
    cache_hit: bool = False
    used_fallback: bool = False
    regeneration_count: int = 0
    status: str = "pending"
    error: Optional[str] = None


# ── Scenario Analysis Output ──────────────────────────────────


class ScenarioAnalysisResult(BaseModel):
    """Structured result from GPT-4o scenario analysis."""

    project_id: str
    concept: str
    tone: str
    visual_style: str
    target_audience: str
    narrative_arc: str
    scenes: list[SceneAnalysisResponse]


# ── Project Requests ──────────────────────────────────────────


class ProjectCreate(BaseModel):
    """Request body for creating a new ad generation project."""

    scenario: str = Field(min_length=10, description="Natural language scenario (sacred — never modified)")
    brand_name: Optional[str] = None
    brand_colors: Optional[list[str]] = None
    brand_tone: Optional[str] = None
    music_url: Optional[str] = None
    target_platforms: Optional[list[TargetPlatform]] = None
    quality_level: QualityLevel = QualityLevel.PREMIUM


class CostEstimateRequest(BaseModel):
    """Request body for cost estimation (runs analysis only)."""

    scenario: str = Field(min_length=10)
    brand_name: Optional[str] = None
    brand_tone: Optional[str] = None
    quality_check_enabled: bool = True


# ── Project Responses ─────────────────────────────────────────


class ProjectResponse(BaseModel):
    """Standard project status response."""

    id: str
    status: JobStatus
    mode: Optional[PipelineMode] = None
    created_at: datetime
    updated_at: datetime
    scenes_count: int = 0
    progress: float = 0.0
    video_url: Optional[str] = None
    error: Optional[str] = None


class CostEstimateResponse(BaseModel):
    """Cost estimation response with scene breakdown."""

    scenes_count: int
    scenes: list[dict]
    cost: dict
    metadata: dict


class HealthResponse(BaseModel):
    """Health check response."""

    status: str
    service: str
    checks: dict[str, bool | str]


# ── Pipeline State (internal, but serializable for WebSocket) ─


class PipelineState(BaseModel):
    """Full internal state of a running pipeline — serialized for WebSocket."""

    project_id: str
    mode: PipelineMode
    analysis: Optional[ScenarioAnalysisResult] = None
    scenes: list[ScenePipelineResponse] = []
    status: JobStatus = JobStatus.PENDING
    final_video_path: Optional[str] = None
    final_video_url: Optional[str] = None
    progress: float = 0.0
    error: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # File references
    mannequin_images: list[str] = []
    product_images: list[str] = []
    decor_images: list[str] = []
    logo_path: Optional[str] = None
    music_path: Optional[str] = None
