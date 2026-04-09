"""Scene dataclass — carries all data for one scene through the pipeline."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from models.enums import CameraMovement, SceneType, TransitionType


@dataclass
class ScenePipeline:
    """Represents a single scene flowing through the pipeline."""

    # Identity
    index: int = 0
    scene_type: SceneType = SceneType.PRODUIT

    # Prompts from GPT-4o
    prompt_image: str = ""
    prompt_video: str = ""
    original_text: str = ""

    # Timing & camera
    duration_seconds: float = 4.0
    camera_movement: CameraMovement = CameraMovement.STATIC
    transition: TransitionType = TransitionType.CUT

    # Flags
    needs_mannequin: bool = False
    needs_decor_ref: bool = False

    # Enriched prompts (after knowledge engine)
    enriched_prompt_image: str = ""
    enriched_prompt_video: str = ""

    # Generated artifacts
    base_image_path: Path | None = None      # Pass 1: Gemini scene
    mannequin_image_path: Path | None = None  # Pass 2: LoRA mannequin
    fused_image_path: Path | None = None      # Pass 3: Inpainted fusion
    final_image_path: Path | None = None      # Final image (fused or direct)
    video_path: Path | None = None            # Animated video clip

    # Quality tracking
    quality_score: float = 0.0
    generation_attempts: int = 0
    fusion_attempts: int = 0

    # Status
    image_generated: bool = False
    video_generated: bool = False
    failed: bool = False
    failure_reason: str = ""

    # Cost tracking
    cost_image: float = 0.0
    cost_video: float = 0.0

    # Metadata
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def is_personnage(self) -> bool:
        return self.scene_type == SceneType.PERSONNAGE

    @property
    def is_produit(self) -> bool:
        return self.scene_type == SceneType.PRODUIT

    @property
    def is_transition(self) -> bool:
        return self.scene_type == SceneType.TRANSITION

    @property
    def total_cost(self) -> float:
        return self.cost_image + self.cost_video

    def mark_failed(self, reason: str) -> None:
        self.failed = True
        self.failure_reason = reason

    def to_dict(self) -> dict[str, Any]:
        return {
            "index": self.index,
            "scene_type": self.scene_type.value,
            "prompt_image": self.prompt_image,
            "prompt_video": self.prompt_video,
            "duration_seconds": self.duration_seconds,
            "camera_movement": self.camera_movement.value,
            "transition": self.transition.value,
            "needs_mannequin": self.needs_mannequin,
            "needs_decor_ref": self.needs_decor_ref,
            "quality_score": self.quality_score,
            "generation_attempts": self.generation_attempts,
            "image_generated": self.image_generated,
            "video_generated": self.video_generated,
            "failed": self.failed,
            "failure_reason": self.failure_reason,
            "cost_image": self.cost_image,
            "cost_video": self.cost_video,
            "final_image_path": str(self.final_image_path) if self.final_image_path else None,
            "video_path": str(self.video_path) if self.video_path else None,
        }
