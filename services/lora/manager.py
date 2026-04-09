"""
LoRA Model Manager — CRUD operations for trained LoRA models.
"""
from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from pipeline.config import settings
from pipeline.exceptions import LoRANotAccessibleError
from utils.http_client import create_session

logger = logging.getLogger(__name__)

# Simple file-based storage (replace with DB in production)
_LORA_STORE_PATH = Path("/tmp/adgenai_lora_models.json")


class LoRAManager:
    """Manages LoRA model lifecycle."""

    def __init__(self) -> None:
        self.session = create_session(timeout=30)
        self.api_base = "https://api.replicate.com/v1"
        self._models: dict[str, dict[str, Any]] = {}
        self._load_store()

    def list_models(self, account_id: str = "default") -> list[dict[str, Any]]:
        """List all LoRA models for an account."""
        return [
            m for m in self._models.values()
            if m.get("account_id") == account_id
        ]

    def get_model(self, model_id: str) -> dict[str, Any] | None:
        """Get a specific LoRA model by ID."""
        return self._models.get(model_id)

    def save_model(
        self,
        model_id: str,
        name: str,
        trigger_word: str,
        replicate_version: str,
        account_id: str = "default",
    ) -> dict[str, Any]:
        """Save a trained LoRA model record."""
        import datetime
        record = {
            "model_id": model_id,
            "name": name,
            "trigger_word": trigger_word,
            "replicate_version": replicate_version,
            "account_id": account_id,
            "status": "ready",
            "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        self._models[model_id] = record
        self._save_store()
        logger.info("Saved LoRA model: %s (%s)", name, model_id)
        return record

    def delete_model(self, model_id: str) -> bool:
        """Delete a LoRA model record."""
        if model_id in self._models:
            del self._models[model_id]
            self._save_store()
            logger.info("Deleted LoRA model: %s", model_id)
            return True
        return False

    def validate_accessible(self, model_id: str) -> bool:
        """Check if a LoRA model is still accessible on Replicate.

        Raises:
            LoRANotAccessibleError if not accessible.
        """
        if not settings.replicate_api_token:
            raise LoRANotAccessibleError(model_id, "No Replicate API token")

        headers = {"Authorization": f"Bearer {settings.replicate_api_token}"}

        try:
            # Try to get the model version
            resp = self.session.get(
                f"{self.api_base}/predictions",
                headers=headers,
                timeout=10,
            )
            if resp.status_code == 401:
                raise LoRANotAccessibleError(model_id, "Invalid API token")

            logger.info("LoRA model %s is accessible.", model_id)
            return True

        except LoRANotAccessibleError:
            raise
        except Exception as e:
            raise LoRANotAccessibleError(model_id, str(e))

    def select_for_pipeline(self, model_id: str) -> dict[str, Any]:
        """Select a LoRA model for a pipeline run.

        Returns:
            Model record with replicate_version and trigger_word.

        Raises:
            ValueError if model not found.
        """
        model = self.get_model(model_id)
        if not model:
            raise ValueError(f"LoRA model not found: {model_id}")
        if model.get("status") != "ready":
            raise ValueError(f"LoRA model not ready: {model_id} (status: {model.get('status')})")
        return model

    def _load_store(self) -> None:
        if _LORA_STORE_PATH.exists():
            try:
                self._models = json.loads(_LORA_STORE_PATH.read_text())
            except Exception:
                self._models = {}

    def _save_store(self) -> None:
        try:
            _LORA_STORE_PATH.parent.mkdir(parents=True, exist_ok=True)
            _LORA_STORE_PATH.write_text(json.dumps(self._models, indent=2))
        except Exception as e:
            logger.warning("Failed to save LoRA store: %s", e)
