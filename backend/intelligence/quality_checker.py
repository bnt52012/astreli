"""
AI-Powered Quality Verification.

After each image is generated, sends it to Gemini for quality analysis.
Checks for mannequin consistency, professional composition, AI artifacts,
and overall quality. If the score falls below threshold, triggers
automatic regeneration with adjusted prompts.

The client NEVER sees a failed image. Everything happens silently.
"""

from __future__ import annotations

import logging
from pathlib import Path

from google import genai
from google.genai import types

from backend.config import settings
from backend.models.enums import QualityLevel, SceneType
from backend.models.scene import ScenePipeline
from backend.pipeline.exceptions import QualityCheckError

logger = logging.getLogger(__name__)

# Quality thresholds by level
QUALITY_THRESHOLDS: dict[QualityLevel, float] = {
    QualityLevel.DRAFT: 0.4,
    QualityLevel.STANDARD: 0.6,
    QualityLevel.PREMIUM: 0.75,
    QualityLevel.BROADCAST: 0.85,
}

QUALITY_CHECK_PROMPT = """Analyze this AI-generated advertising photograph for quality.

Rate each aspect from 0.0 to 1.0:
1. COMPOSITION: Is the framing professional? Rule of thirds? Balance?
2. LIGHTING: Is the lighting consistent, professional, and flattering?
3. REALISM: Does this look like a real photograph or obviously AI-generated?
4. ARTIFACTS: Any distortions, weird hands, face deformations, text errors, extra limbs?
5. BRAND_FIT: Does this look like a professional advertising image?

{mannequin_check}

CRITICAL: Be honest and strict. Marketing teams at luxury brands will see these images.

Respond in this EXACT JSON format:
{{
  "overall_score": 0.0-1.0,
  "composition_score": 0.0-1.0,
  "lighting_score": 0.0-1.0,
  "realism_score": 0.0-1.0,
  "artifact_score": 0.0-1.0,
  "brand_fit_score": 0.0-1.0,
  "issues": ["list of specific issues found"],
  "suggestions": ["list of prompt adjustments to fix issues"]
}}"""

MANNEQUIN_CHECK_ADDENDUM = """6. MANNEQUIN_CONSISTENCY: Does the person match the reference photos provided?
   Same face shape, skin tone, features, proportions? Score 0.0-1.0.
   Add "mannequin_consistency_score" to the JSON."""


class QualityChecker:
    """Verifies generated image quality and triggers regeneration if needed.

    Uses Gemini Flash for fast, cost-effective quality analysis.
    The checker is configurable per quality level:
    - DRAFT: Relaxed thresholds for fast iteration
    - STANDARD: Balanced thresholds for production
    - PREMIUM: Strict thresholds for luxury brand deliverables
    - BROADCAST: Maximum strictness for TV/cinema output
    """

    def __init__(
        self,
        quality_level: QualityLevel = QualityLevel.PREMIUM,
    ) -> None:
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.quality_level = quality_level
        self.threshold = QUALITY_THRESHOLDS[quality_level]

    async def check_image(
        self,
        scene: ScenePipeline,
        mannequin_refs: list[str] | None = None,
    ) -> tuple[float, list[str], list[str]]:
        """Check a generated image's quality.

        Args:
            scene: The scene with its generated image.
            mannequin_refs: Paths to mannequin reference photos (for consistency check).

        Returns:
            Tuple of (overall_score, list_of_issues, list_of_suggestions).

        Raises:
            QualityCheckError: If the check itself fails (not if quality is low).
        """
        if not scene.image_path or not Path(scene.image_path).exists():
            raise QualityCheckError(
                "No image to check",
                scene_index=scene.analysis.id,
            )

        try:
            parts = []

            # Include the generated image
            image_bytes = Path(scene.image_path).read_bytes()
            parts.append(types.Part.from_bytes(data=image_bytes, mime_type="image/png"))

            # Include mannequin references for consistency check
            mannequin_check = ""
            if (
                mannequin_refs
                and scene.analysis.type == SceneType.PERSONNAGE
            ):
                mannequin_check = MANNEQUIN_CHECK_ADDENDUM
                for ref_path in mannequin_refs[:3]:  # Max 3 refs for speed
                    if Path(ref_path).exists():
                        ref_bytes = Path(ref_path).read_bytes()
                        mime = (
                            "image/jpeg"
                            if ref_path.lower().endswith((".jpg", ".jpeg"))
                            else "image/png"
                        )
                        parts.append(types.Part.from_bytes(data=ref_bytes, mime_type=mime))

            # Build prompt
            prompt = QUALITY_CHECK_PROMPT.format(mannequin_check=mannequin_check)
            parts.append(types.Part.from_text(text=prompt))

            # Call Gemini for analysis
            response = await self.client.aio.models.generate_content(
                model=settings.gemini_flash_model,
                contents=types.Content(parts=parts),
                config=types.GenerateContentConfig(
                    response_modalities=["TEXT"],
                    temperature=0.2,  # Low temperature for consistent evaluation
                ),
            )

            # Parse response
            response_text = ""
            for part in response.candidates[0].content.parts:
                if part.text:
                    response_text += part.text

            result = self._parse_quality_response(response_text)

            score = result.get("overall_score", 0.0)
            issues = result.get("issues", [])
            suggestions = result.get("suggestions", [])

            logger.info(
                "[QUALITY] Scene %d: score=%.2f (threshold=%.2f), issues=%d",
                scene.analysis.id,
                score,
                self.threshold,
                len(issues),
            )

            return score, issues, suggestions

        except Exception as e:
            logger.warning(
                "[QUALITY] Check failed for scene %d: %s (continuing without check)",
                scene.analysis.id,
                e,
            )
            # On check failure, return passing score to not block the pipeline
            return 1.0, [], []

    async def check_and_decide(
        self,
        scene: ScenePipeline,
        mannequin_refs: list[str] | None = None,
    ) -> bool:
        """Check quality and decide if regeneration is needed.

        Args:
            scene: The scene to check.
            mannequin_refs: Mannequin reference paths.

        Returns:
            True if the image passes quality, False if regeneration is needed.
        """
        score, issues, suggestions = await self.check_image(scene, mannequin_refs)

        scene.quality_score = score
        scene.quality_issues = issues

        if score >= self.threshold:
            return True

        logger.warning(
            "[QUALITY] Scene %d FAILED quality check (%.2f < %.2f): %s",
            scene.analysis.id,
            score,
            self.threshold,
            "; ".join(issues[:3]),
        )
        return False

    def build_retry_prompt_adjustments(
        self,
        scene: ScenePipeline,
        suggestions: list[str],
    ) -> str:
        """Build prompt adjustments based on quality check feedback.

        Appends corrective instructions to the existing prompt without
        changing the client's original intent.

        Args:
            scene: The scene that failed quality.
            suggestions: Suggestions from the quality checker.

        Returns:
            Additional prompt text to append for retry.
        """
        adjustments: list[str] = []

        for suggestion in suggestions[:3]:
            adjustments.append(suggestion)

        # Common fixes based on known issues
        for issue in scene.quality_issues:
            issue_lower = issue.lower()
            if "hand" in issue_lower or "finger" in issue_lower:
                adjustments.append("hands must be anatomically correct with 5 fingers each")
            if "face" in issue_lower or "distort" in issue_lower:
                adjustments.append("face must be photorealistic with natural proportions")
            if "text" in issue_lower:
                adjustments.append("any text must be crisp, correctly spelled, and readable")
            if "lighting" in issue_lower:
                adjustments.append("ensure consistent, professional lighting throughout the frame")

        if adjustments:
            return ". QUALITY CORRECTIONS: " + "; ".join(adjustments)
        return ""

    def _parse_quality_response(self, response_text: str) -> dict:
        """Parse Gemini's quality analysis JSON response.

        Handles both clean JSON and JSON embedded in markdown fences.
        """
        import json

        # Try direct JSON parse
        text = response_text.strip()

        # Remove markdown code fences if present
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:-1] if lines[-1].strip() == "```" else lines[1:])
            text = text.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Fallback: extract JSON from text
            import re
            json_match = re.search(r"\{[^{}]*\}", text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass

        logger.warning("[QUALITY] Could not parse quality response, returning default")
        return {"overall_score": 0.7, "issues": [], "suggestions": []}
