"""
LoRA model management service for AdGenAI.

Provides CRUD operations and inference for LoRA SDXL models stored on
Replicate. Used by the image generation pipeline to run mannequin
predictions during Pass 2 of the fusion workflow.
"""

from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field
from typing import Any

import replicate

from backend.config import settings
from backend.pipeline.exceptions import (
    ConfigError,
    LoRAGenerationError,
    LoRANotFoundError,
)

logger = logging.getLogger(__name__)


@dataclass
class LoRAMetadata:
    """Metadata for a trained LoRA model."""

    model_id: str
    version: str | None = None
    trigger_word: str = "MANNEQUIN"
    created_at: float = field(default_factory=time.time)
    training_images_count: int = 0


class LoRAManager:
    """Manages LoRA model lifecycle and inference on Replicate.

    Responsibilities:
        - Validate that a LoRA model exists and is accessible.
        - Run predictions (Pass 2 mannequin generation).
        - List available model versions.
        - Delete obsolete models.
    """

    def __init__(self) -> None:
        if not settings.replicate_api_token:
            raise ConfigError(
                "Replicate API token is required for LoRA management. "
                "Set ADGENAI_REPLICATE_API_TOKEN.",
            )
        self._client = replicate.Client(api_token=settings.replicate_api_token)
        self._metadata_cache: dict[str, LoRAMetadata] = {}

    # ── Validation ───────────────────────────────────────────

    async def validate_lora(self, model_id: str) -> bool:
        """Check whether a LoRA model is accessible on Replicate.

        Args:
            model_id: Replicate model identifier (e.g. ``owner/model-name``).

        Returns:
            True if the model exists and has at least one version.

        Raises:
            LoRANotFoundError: If the model is not found or inaccessible.
        """
        try:
            model = await asyncio.to_thread(self._client.models.get, model_id)
            versions = await asyncio.to_thread(lambda: list(model.versions.list()))
            if not versions:
                raise LoRANotFoundError(model_id)
            logger.info("Validated LoRA model %s (%d versions).", model_id, len(versions))
            return True
        except LoRANotFoundError:
            raise
        except Exception as exc:
            raise LoRANotFoundError(model_id) from exc

    # ── Inference ────────────────────────────────────────────

    async def generate_with_lora(
        self,
        model_id: str,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        """Run a prediction on a LoRA model and return the output image URL.

        Args:
            model_id: Replicate model identifier.
            prompt: Generation prompt (should include trigger word).
            **kwargs: Additional prediction input parameters
                (e.g. ``negative_prompt``, ``width``, ``height``,
                ``num_inference_steps``, ``guidance_scale``).

        Returns:
            URL of the generated image.

        Raises:
            LoRAGenerationError: If the prediction fails.
        """
        logger.info("Generating with LoRA %s: prompt=%r", model_id, prompt[:100])

        input_params: dict[str, Any] = {
            "prompt": prompt,
            "width": kwargs.get("width", 1024),
            "height": kwargs.get("height", 1024),
            "num_inference_steps": kwargs.get("num_inference_steps", 30),
            "guidance_scale": kwargs.get("guidance_scale", 7.5),
        }

        if "negative_prompt" in kwargs:
            input_params["negative_prompt"] = kwargs["negative_prompt"]

        if "seed" in kwargs:
            input_params["seed"] = kwargs["seed"]

        try:
            output = await asyncio.to_thread(
                self._client.run,
                model_id,
                input=input_params,
            )

            # Replicate returns a list of output URLs or a single FileOutput
            if isinstance(output, list):
                image_url = str(output[0])
            else:
                image_url = str(output)

            logger.info("LoRA prediction complete: %s", image_url[:120])
            return image_url

        except replicate.exceptions.ReplicateError as exc:
            raise LoRAGenerationError(
                f"LoRA prediction failed for {model_id}: {exc}",
                lora_model_id=model_id,
                details={"prompt_preview": prompt[:200]},
            ) from exc
        except Exception as exc:
            raise LoRAGenerationError(
                f"Unexpected error during LoRA prediction: {exc}",
                lora_model_id=model_id,
            ) from exc

    # ── Version Management ───────────────────────────────────

    async def list_versions(self, model_id: str) -> list[dict]:
        """List available versions for a LoRA model.

        Args:
            model_id: Replicate model identifier.

        Returns:
            List of version dicts with ``id``, ``created_at``, and ``cog_version``.
        """
        try:
            model = await asyncio.to_thread(self._client.models.get, model_id)
            versions = await asyncio.to_thread(lambda: list(model.versions.list()))

            result = [
                {
                    "id": str(v.id),
                    "created_at": str(getattr(v, "created_at", "")),
                    "cog_version": getattr(v, "cog_version", ""),
                }
                for v in versions
            ]
            logger.info("Listed %d versions for %s.", len(result), model_id)
            return result

        except Exception as exc:
            logger.error("Failed to list versions for %s: %s", model_id, exc)
            return []

    # ── Deletion ─────────────────────────────────────────────

    async def delete_model(self, model_id: str) -> bool:
        """Delete a LoRA model from Replicate.

        Args:
            model_id: Replicate model identifier.

        Returns:
            True if deletion succeeded, False otherwise.
        """
        logger.warning("Deleting LoRA model %s", model_id)
        try:
            model = await asyncio.to_thread(self._client.models.get, model_id)
            await asyncio.to_thread(model.delete)
            self._metadata_cache.pop(model_id, None)
            logger.info("Deleted LoRA model %s.", model_id)
            return True
        except Exception as exc:
            logger.error("Failed to delete LoRA model %s: %s", model_id, exc)
            return False

    # ── Metadata ─────────────────────────────────────────────

    def register_metadata(self, metadata: LoRAMetadata) -> None:
        """Cache metadata for a trained LoRA model.

        Args:
            metadata: Populated ``LoRAMetadata`` instance.
        """
        self._metadata_cache[metadata.model_id] = metadata
        logger.debug("Registered metadata for %s.", metadata.model_id)

    def get_metadata(self, model_id: str) -> LoRAMetadata | None:
        """Retrieve cached metadata for a model.

        Args:
            model_id: Replicate model identifier.

        Returns:
            Cached ``LoRAMetadata`` or None if not registered.
        """
        return self._metadata_cache.get(model_id)
