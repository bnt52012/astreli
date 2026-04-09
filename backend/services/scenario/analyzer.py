"""
GPT-4o Scenario Analyzer — Step 1 of the AdGenAI Pipeline.

The client writes an ad scenario in natural language.
GPT-4o acts as a faithful analyst: splits into scenes, classifies each,
generates detailed image & video prompts.

GPT-4o NEVER overrides creative decisions. It faithfully decomposes
the scenario into structured data for the pipeline.
"""

from __future__ import annotations

import logging
import uuid
from typing import Any

from openai import AsyncOpenAI, APIConnectionError, APITimeoutError, RateLimitError

from backend.config import settings
from backend.models.enums import PipelineMode
from backend.models.scene import SceneAnalysis
from backend.pipeline.exceptions import (
    AuthenticationError,
    RateLimitError as AdGenRateLimitError,
    ScenarioAnalysisError,
)
from backend.services.scenario.prompts import get_system_prompt
from backend.services.scenario.scene_parser import parse_gpt4o_response

logger = logging.getLogger(__name__)


class ScenarioAnalyzer:
    """Analyzes ad scenarios using GPT-4o.

    Decomposes natural language scenarios into structured scene data
    with separate system prompts for each pipeline mode.

    Attributes:
        client: OpenAI async client instance.
    """

    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)

    async def analyze(
        self,
        scenario: str,
        mode: PipelineMode,
        project_id: str,
        brand_name: str | None = None,
        brand_tone: str | None = None,
    ) -> tuple[dict[str, Any], list[SceneAnalysis]]:
        """Analyze a scenario and decompose it into scenes.

        Args:
            scenario: The client's ad scenario in natural language.
            mode: Pipeline mode (determines system prompt).
            project_id: Project identifier for tracing.
            brand_name: Optional brand name for context.
            brand_tone: Optional brand tone description.

        Returns:
            Tuple of (metadata dict with concept/tone/style, list of SceneAnalysis).

        Raises:
            ScenarioAnalysisError: If analysis fails.
            AuthenticationError: If OpenAI API key is invalid.
            AdGenRateLimitError: If rate limited by OpenAI.
        """
        request_id = uuid.uuid4().hex[:12]
        system_prompt = get_system_prompt(mode.value)

        # Build user message
        user_parts = [f"SCENARIO:\n{scenario}"]
        if brand_name:
            user_parts.append(f"\nBRAND: {brand_name}")
        if brand_tone:
            user_parts.append(f"\nBRAND TONE: {brand_tone}")

        user_message = "\n".join(user_parts)

        logger.info(
            "[ANALYSIS] Starting scenario analysis (mode=%s, project=%s, req=%s)",
            mode.value,
            project_id,
            request_id,
        )

        try:
            response = await self.client.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message},
                ],
                temperature=0.7,
                max_tokens=4096,
                response_format={"type": "json_object"},
            )

            raw_content = response.choices[0].message.content
            if not raw_content:
                raise ScenarioAnalysisError(
                    "GPT-4o returned empty response",
                    details={"request_id": request_id},
                )

            # Parse and validate the response
            metadata, scenes = parse_gpt4o_response(raw_content, mode)

            # Log usage for cost tracking
            usage = response.usage
            if usage:
                logger.info(
                    "[ANALYSIS] Tokens used: %d input + %d output = %d total (req=%s)",
                    usage.prompt_tokens,
                    usage.completion_tokens,
                    usage.total_tokens,
                    request_id,
                )

            logger.info(
                "[ANALYSIS] Scenario decomposed: %d scenes (%s) (req=%s)",
                len(scenes),
                ", ".join(s.type.value for s in scenes),
                request_id,
            )

            return metadata, scenes

        except RateLimitError as e:
            logger.error("[ANALYSIS] OpenAI rate limit hit (req=%s)", request_id)
            raise AdGenRateLimitError("openai") from e

        except APIConnectionError as e:
            logger.error("[ANALYSIS] OpenAI connection error (req=%s): %s", request_id, e)
            raise ScenarioAnalysisError(
                f"Failed to connect to OpenAI API: {e}",
                details={"request_id": request_id},
            ) from e

        except APITimeoutError as e:
            logger.error("[ANALYSIS] OpenAI timeout (req=%s)", request_id)
            raise ScenarioAnalysisError(
                "OpenAI API request timed out",
                details={"request_id": request_id},
            ) from e

        except ScenarioAnalysisError:
            raise

        except Exception as e:
            # Check for auth errors
            error_str = str(e).lower()
            if "401" in error_str or "invalid api key" in error_str:
                raise AuthenticationError("openai") from e

            logger.exception(
                "[ANALYSIS] Unexpected error during scenario analysis (req=%s)",
                request_id,
            )
            raise ScenarioAnalysisError(
                f"Scenario analysis failed: {e}",
                details={"request_id": request_id},
            ) from e
