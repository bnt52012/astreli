"""
Scene data model for the AdGenAI pipeline v3.0.

Each scene represents one visual segment of the final ad video,
carrying its classification, prompts, generation state, and output paths
through the entire pipeline lifecycle.

v3.0 changes:
- 3-pass fusion tracking (base scene → LoRA mannequin → inpainting)
- LoRA model reference instead of Gemini Pro chat session
- Gemini model updated to gemini-3.1-flash-image-preview
- Scene archetype tracking for knowledge engine
"""

from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field

from backend.models.enums import (
    CameraMovement,
    EmotionalTone,
    FusionPass,
    SceneArchetype,
    SceneType,
    TransitionType,
)

# ── Model Mappings ────────────────────────────────────────────

GEMINI_MODEL = "gemini-3.1-flash-image-preview"
"""Nano Banana 2 — used for ALL image generation (scene bases + product shots)."""

KLING_MODEL_MAP: dict[SceneType, str] = {
    SceneType.PERSONNAGE: "kling-v1",     # Video-01: optimized for human motion
    SceneType.PRODUIT: "kling-v1-6",      # V3: optimized for product animation
    SceneType.TRANSITION: "",              # No video generation for transitions
}


# ── Scene Analysis (from GPT-4o) ─────────────────────────────


class SceneAnalysis(BaseModel):
    """Output from GPT-4o scenario decomposition for a single scene.

    This is the raw analysis before any enrichment or optimization.
    The client's intent is preserved exactly as GPT-4o interpreted it.
    """

    id: int = Field(description="Unique scene index starting at 1")
    type: SceneType = Field(description="Scene classification: personnage/produit/transition")
    goal: str = Field(description="One-sentence narrative purpose of this scene")
    description: str = Field(description="Full scene description as the client envisioned it")
    image_prompt: str = Field(description="Detailed image generation prompt (English)")
    video_prompt: str = Field(description="Video animation/motion prompt (English)")
    camera_movement: str = Field(
        default="static",
        description="Camera movement: static/pan_left/pan_right/zoom_in/zoom_out/tracking/orbit",
    )
    lighting: str = Field(default="", description="Lighting setup description")
    duration: float = Field(
        ge=2.0, le=8.0, default=5.0,
        description="Scene duration in seconds (2.0-8.0, client-specified, never overridden)",
    )
    transition: TransitionType = Field(
        default=TransitionType.FADE,
        description="Transition type TO this scene from the previous one",
    )
    needs_mannequin: bool = Field(
        default=False,
        description="Whether the mannequin/model appears (even partially)",
    )
    needs_product: bool = Field(
        default=False,
        description="Whether the product appears in this scene",
    )
    needs_decor_ref: bool = Field(
        default=False,
        description="Whether decor reference images should be included",
    )
    references_scene: int | None = Field(
        default=None,
        description="If this scene references another scene's location/setup",
    )
    text_overlay: str | None = Field(
        default=None,
        description="Text to display on screen (brand name, slogan, CTA)",
    )


class SceneContext(BaseModel):
    """Contextual intelligence extracted by the scene_understanding module.

    Computed AFTER GPT-4o analysis. Used to silently improve prompt quality
    without changing the client's creative intent.
    """

    emotional_tone: EmotionalTone = EmotionalTone.ELEGANT
    detected_camera_work: CameraMovement = CameraMovement.STATIC
    scene_archetype: SceneArchetype = SceneArchetype.PRODUCT_HERO
    ad_category_hint: str = "general"
    requires_face_consistency: bool = False
    requires_product_in_frame: bool = False
    has_wardrobe_change: bool = False
    character_id: str | None = None  # For multi-mannequin campaigns
    linked_scene_ids: list[int] = Field(default_factory=list)
    enrichment_keywords: list[str] = Field(default_factory=list)
    lighting_suggestion: str = ""
    lens_suggestion: str = ""
    composition_suggestion: str = ""

    # Pose analysis for LoRA matching (extracted from Pass 1 base image)
    detected_head_angle: str = ""       # "facing left", "3/4 right", "forward"
    detected_body_pose: str = ""        # "standing", "sitting", "walking"
    detected_lighting_direction: str = ""  # "light from left", "above", "behind"


# ── Scene Pipeline State ─────────────────────────────────────


class ScenePipeline(BaseModel):
    """Full scene state as it moves through the pipeline.

    Tracks the scene from analysis through enrichment, 3-pass image generation,
    video generation, and quality checks. Each stage writes its outputs
    here so the orchestrator can route decisions.

    For PERSONNAGE scenes (3-pass fusion):
        scene_base_path → mannequin_path → fusion_path → image_path
    For PRODUIT scenes (1-pass):
        image_path (set directly)
    """

    # From GPT-4o
    analysis: SceneAnalysis

    # From intelligence layer
    context: SceneContext = Field(default_factory=SceneContext)

    # From prompt enrichment (knowledge engine)
    enriched_image_prompt: str = ""
    enriched_video_prompt: str = ""

    # From brand analyzer
    brand_prompt_prefix: str = ""

    # ── 3-Pass Fusion State (personnage scenes only) ──────────

    # Pass 1: Nano Banana 2 scene base (with generic figure placeholder)
    scene_base_path: str | None = None
    scene_base_prompt: str = ""

    # Pass 2: LoRA SDXL mannequin generation
    mannequin_path: str | None = None
    mannequin_prompt: str = ""
    lora_model_id: str | None = None     # Replicate model ID
    lora_prediction_id: str | None = None

    # Pass 3: Inpainting fusion result
    fusion_path: str | None = None
    fusion_mask_path: str | None = None
    fusion_quality_score: float | None = None
    current_fusion_pass: FusionPass | None = None

    # ── Image Generation Output ───────────────────────────────

    image_path: str | None = None        # Final image for video animation
    image_url: str | None = None
    image_generation_model: str | None = None
    image_generation_time_ms: int | None = None

    # ── Quality Check ─────────────────────────────────────────

    quality_score: float | None = None
    quality_issues: list[str] = Field(default_factory=list)
    regeneration_count: int = 0

    # ── Video Generation Output ───────────────────────────────

    video_job_id: str | None = None
    video_path: str | None = None
    video_url: str | None = None
    video_generation_model: str | None = None
    video_generation_time_ms: int | None = None

    # ── Pipeline Tracking ─────────────────────────────────────

    retry_count: int = 0
    status: str = "pending"
    error: str | None = None
    used_fallback: bool = False
    cache_hit: bool = False

    @property
    def kling_model(self) -> str:
        """Auto-mapped Kling model based on scene type."""
        return KLING_MODEL_MAP.get(self.analysis.type, "")

    @property
    def is_personnage(self) -> bool:
        """Whether this is a personnage scene (requires 3-pass fusion)."""
        return self.analysis.type == SceneType.PERSONNAGE

    @property
    def is_produit(self) -> bool:
        """Whether this is a product-only scene (one-shot Nano Banana)."""
        return self.analysis.type == SceneType.PRODUIT

    @property
    def is_transition(self) -> bool:
        """Whether this is a transition scene (skip generation)."""
        return self.analysis.type == SceneType.TRANSITION

    @property
    def is_ready_for_video(self) -> bool:
        """Whether this scene has a generated image ready for video animation."""
        return self.image_path is not None and self.status == "image_ready"

    @property
    def is_complete(self) -> bool:
        """Whether this scene has completed all generation stages."""
        return self.video_path is not None and self.status == "video_ready"

    @property
    def final_image_prompt(self) -> str:
        """The fully enriched image prompt ready for Gemini.

        Combines brand prefix + enriched prompt. Falls back to raw
        analysis prompt if enrichment hasn't run yet.
        """
        base = self.enriched_image_prompt or self.analysis.image_prompt
        if self.brand_prompt_prefix:
            return f"{self.brand_prompt_prefix}. {base}"
        return base

    @property
    def final_video_prompt(self) -> str:
        """The fully enriched video prompt ready for Kling."""
        return self.enriched_video_prompt or self.analysis.video_prompt
