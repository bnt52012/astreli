"""Pydantic models for API request/response validation."""
from __future__ import annotations

from typing import Any, Dict, List, Optional

try:
    from pydantic import BaseModel, Field, validator  # v1
except ImportError:
    from pydantic import BaseModel, Field, validator


class PipelineRequest(BaseModel):
    """Client request to run the pipeline."""
    scenario: str = Field(..., min_length=10, description="The advertising scenario in natural language")
    lora_model_id: Optional[str] = Field(None, description="Replicate LoRA model ID (if mannequin mode)")
    mannequin_photos: List[str] = Field(default_factory=list, description="Paths to mannequin reference photos")
    product_photos: List[str] = Field(default_factory=list, description="Paths to product reference photos")
    decor_photos: List[str] = Field(default_factory=list, description="Paths to decor/environment reference photos")
    logo_path: Optional[str] = Field(None, description="Path to brand logo for overlay")
    music_path: Optional[str] = Field(None, description="Path to background music file")
    target_platforms: List[str] = Field(default_factory=lambda: ["youtube"], description="Target platforms")
    aspect_ratio: str = Field("16:9", description="Primary aspect ratio")
    quality: str = Field("standard", description="Quality level: draft, standard, premium")
    brand_name: Optional[str] = Field(None, description="Brand name for context")

    @validator("scenario")
    @classmethod
    def scenario_not_empty(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("Scenario cannot be empty")
        return v.strip()


class SceneAnalysis(BaseModel):
    """A single scene as returned by GPT-4o."""
    scene_number: int
    scene_type: str
    prompt_image: str
    prompt_video: str
    duration_seconds: float = Field(..., ge=2.0, le=8.0)
    camera_movement: str = "static"
    transition: str = "cut"
    needs_mannequin: bool = False
    needs_decor_ref: bool = False
    original_text: str = ""


class ScenarioResponse(BaseModel):
    """Full GPT-4o response."""
    total_scenes: int
    estimated_duration: float
    scenes: List[SceneAnalysis]
    mood: str = ""
    color_palette: List[str] = Field(default_factory=list)


class PipelineStatus(BaseModel):
    """Pipeline progress status."""
    project_id: str
    status: str
    progress: float = 0.0
    current_step: str = ""
    scenes_completed: int = 0
    scenes_total: int = 0
    message: str = ""


class PipelineResult(BaseModel):
    """Final pipeline result."""
    project_id: str
    status: str
    output_video: Optional[str] = None
    scenes_succeeded: int = 0
    scenes_failed: int = 0
    total_scenes: int = 0
    total_cost: float = 0.0
    total_duration: float = 0.0
    scene_details: List[Dict[str, Any]] = Field(default_factory=list)
    errors: List[str] = Field(default_factory=list)


class LoRATrainingRequest(BaseModel):
    """Request to train a LoRA model."""
    name: str = Field(..., min_length=2)
    training_images: List[str] = Field(..., min_items=10, max_items=30)
    trigger_word: str = Field("MANNEQUIN", description="Trigger word for the LoRA")


class LoRAModel(BaseModel):
    """A trained LoRA model record."""
    model_id: str
    name: str
    trigger_word: str
    status: str = "training"
    replicate_model_id: Optional[str] = None
    created_at: Optional[str] = None


class CostEstimate(BaseModel):
    """Pre-run cost estimation."""
    total_estimated_cost: float
    breakdown: Dict[str, float] = Field(default_factory=dict)
    scene_count: int = 0
    personnage_scenes: int = 0
    produit_scenes: int = 0
    transition_scenes: int = 0
    estimated_duration_minutes: float = 0.0
