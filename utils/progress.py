"""
Progress tracking with callbacks.
"""
from __future__ import annotations

import logging
import time
from dataclasses import dataclass, field
from typing import Any, Callable

logger = logging.getLogger(__name__)


@dataclass
class ProgressStep:
    name: str
    weight: float = 1.0
    started: float = 0.0
    completed: float = 0.0
    status: str = "pending"


@dataclass
class ProgressTracker:
    """Track pipeline progress and emit callbacks."""

    total_steps: int = 4
    callbacks: list[Callable[[dict[str, Any]], None]] = field(default_factory=list)
    _steps: list[ProgressStep] = field(default_factory=list)
    _current_step: int = 0
    _sub_progress: float = 0.0

    def __post_init__(self) -> None:
        weights = [0.1, 0.35, 0.40, 0.15]  # analysis, images, videos, assembly
        names = ["Scenario Analysis", "Image Generation", "Video Animation", "Final Assembly"]
        self._steps = [
            ProgressStep(name=n, weight=w) for n, w in zip(names, weights)
        ]

    def add_callback(self, cb: Callable[[dict[str, Any]], None]) -> None:
        self.callbacks.append(cb)

    def start_step(self, step_index: int) -> None:
        self._current_step = step_index
        self._sub_progress = 0.0
        if step_index < len(self._steps):
            self._steps[step_index].started = time.time()
            self._steps[step_index].status = "running"
        self._emit()

    def update_sub_progress(self, fraction: float) -> None:
        """Update sub-progress within current step (0.0 - 1.0)."""
        self._sub_progress = min(1.0, max(0.0, fraction))
        self._emit()

    def complete_step(self, step_index: int) -> None:
        if step_index < len(self._steps):
            self._steps[step_index].completed = time.time()
            self._steps[step_index].status = "completed"
        self._sub_progress = 1.0
        self._emit()

    def fail_step(self, step_index: int, reason: str = "") -> None:
        if step_index < len(self._steps):
            self._steps[step_index].status = f"failed: {reason}"
        self._emit()

    @property
    def overall_progress(self) -> float:
        """Overall progress 0.0 - 1.0."""
        total = 0.0
        for i, step in enumerate(self._steps):
            if step.status == "completed":
                total += step.weight
            elif step.status == "running":
                total += step.weight * self._sub_progress
        return min(1.0, total)

    def _emit(self) -> None:
        data = {
            "overall_progress": round(self.overall_progress * 100, 1),
            "current_step": self._steps[self._current_step].name if self._current_step < len(self._steps) else "",
            "steps": [
                {"name": s.name, "status": s.status, "weight": s.weight}
                for s in self._steps
            ],
        }
        for cb in self.callbacks:
            try:
                cb(data)
            except Exception:
                pass

    def get_status(self) -> dict[str, Any]:
        return {
            "overall_progress": round(self.overall_progress * 100, 1),
            "current_step": self._steps[self._current_step].name if self._current_step < len(self._steps) else "",
            "steps": [
                {"name": s.name, "status": s.status} for s in self._steps
            ],
        }
