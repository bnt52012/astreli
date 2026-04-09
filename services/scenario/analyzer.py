"""
GPT-4o Scenario Analyzer.

Sends the client's scenario to GPT-4o with the appropriate system prompt
(mixed or product-only) and returns structured scene decomposition.
"""
from __future__ import annotations

import json
import logging
from typing import Any

import requests

from models.enums import PipelineMode
from pipeline.config import PIPELINE_DEFAULTS, settings
from pipeline.exceptions import ScenarioAnalysisError
from services.scenario.prompts import SYSTEM_PROMPT_MIXED, SYSTEM_PROMPT_PRODUCT_ONLY
from services.scenario.scene_parser import SceneParser
from utils.http_client import create_session

logger = logging.getLogger(__name__)


class ScenarioAnalyzer:
    """Decomposes a scenario into scenes using GPT-4o."""

    def __init__(self) -> None:
        self.session = create_session(timeout=120)
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.parser = SceneParser()

    def analyze(
        self,
        scenario: str,
        mode: PipelineMode,
        brand_context: str = "",
    ) -> dict[str, Any]:
        """Analyze the scenario and return structured scenes.

        Args:
            scenario: Client's natural-language scenario.
            mode: Pipeline mode determines which system prompt to use.
            brand_context: Optional brand context from brand_analyzer.

        Returns:
            Parsed and validated scenario response dict.

        Raises:
            ScenarioAnalysisError: On any failure.
        """
        system_prompt = (
            SYSTEM_PROMPT_MIXED
            if mode == PipelineMode.PERSONNAGE_ET_PRODUIT
            else SYSTEM_PROMPT_PRODUCT_ONLY
        )

        user_message = scenario
        if brand_context:
            user_message = f"[BRAND CONTEXT: {brand_context}]\n\n{scenario}"

        payload = {
            "model": PIPELINE_DEFAULTS.openai_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message},
            ],
            "max_tokens": PIPELINE_DEFAULTS.openai_max_tokens,
            "temperature": PIPELINE_DEFAULTS.openai_temperature,
            "response_format": {"type": "json_object"},
        }

        headers = {
            "Authorization": f"Bearer {settings.openai_api_key}",
            "Content-Type": "application/json",
        }

        try:
            logger.info("Sending scenario to GPT-4o (%s mode)...", mode.value)
            resp = self.session.post(
                self.api_url,
                json=payload,
                headers=headers,
                timeout=120,
            )
        except requests.exceptions.ConnectionError as e:
            raise ScenarioAnalysisError(f"Connection error: {e}")
        except requests.exceptions.Timeout:
            raise ScenarioAnalysisError("Request timed out after 120s")

        if resp.status_code == 401:
            raise ScenarioAnalysisError("Invalid OpenAI API key", status_code=401)
        if resp.status_code == 429:
            raise ScenarioAnalysisError("Rate limited by OpenAI", status_code=429)
        if resp.status_code != 200:
            raise ScenarioAnalysisError(
                f"HTTP {resp.status_code}: {resp.text[:500]}",
                status_code=resp.status_code,
            )

        try:
            data = resp.json()
            content = data["choices"][0]["message"]["content"]
            parsed = json.loads(content)
        except (json.JSONDecodeError, KeyError, IndexError) as e:
            raise ScenarioAnalysisError(f"Invalid JSON response from GPT-4o: {e}")

        # Validate and normalize
        validated = self.parser.parse_and_validate(parsed, mode)

        logger.info(
            "Scenario analysis complete: %d scenes, %.1fs estimated duration.",
            validated["total_scenes"],
            validated["estimated_duration"],
        )
        return validated
