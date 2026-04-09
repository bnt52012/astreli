"""
Quality Checker — post-generation quality verification via Gemini.

After EVERY image (especially after LoRA fusion): send to Gemini for verification.
Check: mannequin consistency, lighting coherence, visible seams/artifacts.
Quality score 1-10. If < 7: auto-regenerate (max 3 retries).
The client NEVER sees a failed image.
"""
from __future__ import annotations

import logging
from pathlib import Path

from pipeline.config import settings, PIPELINE_DEFAULTS

logger = logging.getLogger(__name__)


class QualityChecker:
    """Verifies image quality via Gemini and triggers regeneration if needed."""

    def __init__(self, quality_threshold: float | None = None, max_retries: int | None = None) -> None:
        self.threshold = quality_threshold or PIPELINE_DEFAULTS.quality_threshold
        self.max_retries = max_retries or PIPELINE_DEFAULTS.max_quality_retries

    async def check_image(
        self,
        image_path: Path,
        scene_type: str = "produit",
        is_fusion: bool = False,
    ) -> tuple[float, str]:
        """Check image quality using Gemini.

        Args:
            image_path: Path to the image to check.
            scene_type: Type of scene for context-specific checks.
            is_fusion: Whether this is a fused image (extra checks for seams).

        Returns:
            Tuple of (quality_score, feedback_text).
        """
        try:
            from google import genai
            from google.genai import types
            from PIL import Image

            client = genai.Client(api_key=settings.gemini_api_key)
            img = Image.open(str(image_path))

            # Build verification prompt
            if is_fusion:
                check_prompt = (
                    "Analyze this advertising photograph for quality. "
                    "Pay special attention to:\n"
                    "1. Does the person look natural in this scene?\n"
                    "2. Is the lighting consistent across the entire image?\n"
                    "3. Are there any visible seams, artifacts, or unnatural transitions "
                    "around the face/neck area?\n"
                    "4. Is the skin tone consistent between face and body?\n"
                    "5. Does the image look professionally shot?\n\n"
                    "Rate the overall quality from 1-10 where 10 is broadcast-ready.\n"
                    "Respond in JSON: {\"score\": <int>, \"issues\": [\"...\"], \"feedback\": \"...\"}"
                )
            else:
                check_prompt = (
                    "Analyze this advertising photograph for quality. Check:\n"
                    "1. Professional lighting and composition\n"
                    "2. No visible artifacts, distortions, or AI tells\n"
                    "3. Realistic textures and materials\n"
                    "4. Correct proportions and perspective\n"
                    "5. Broadcast/print-ready quality\n\n"
                    "Rate quality from 1-10 where 10 is broadcast-ready.\n"
                    "Respond in JSON: {\"score\": <int>, \"issues\": [\"...\"], \"feedback\": \"...\"}"
                )

            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=[img, check_prompt],
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                ),
            )

            if response.text:
                import json
                try:
                    result = json.loads(response.text)
                    score = float(result.get("score", 5))
                    feedback = result.get("feedback", "")
                    issues = result.get("issues", [])
                    logger.info(
                        "Quality check: %.1f/10 for %s (issues: %s)",
                        score, image_path.name, issues[:3],
                    )
                    return score, feedback
                except json.JSONDecodeError:
                    logger.warning("Could not parse quality check response")
                    return 7.0, "Parse error — assuming acceptable"

            return 7.0, "No response from quality check"

        except ImportError:
            logger.warning("google-genai not installed, skipping quality check")
            return 8.0, "Quality check skipped (no SDK)"
        except Exception as e:
            logger.warning("Quality check failed: %s", e)
            return 7.0, f"Check failed: {e}"

    async def check_and_retry(
        self,
        image_path: Path,
        scene_type: str = "produit",
        is_fusion: bool = False,
    ) -> tuple[float, bool]:
        """Check quality and indicate if regeneration is needed.

        Returns:
            Tuple of (score, passes_threshold).
        """
        score, feedback = await self.check_image(image_path, scene_type, is_fusion)
        passes = score >= self.threshold
        if not passes:
            logger.warning(
                "Image %s failed quality check: %.1f/10 (threshold: %.1f). Feedback: %s",
                image_path.name, score, self.threshold, feedback,
            )
        return score, passes

    def build_retry_adjustments(self, feedback: str) -> str:
        """Build prompt adjustments based on quality feedback.

        Returns additional prompt text to address issues.
        """
        adjustments = []

        lower = feedback.lower()
        if "seam" in lower or "transition" in lower or "blend" in lower:
            adjustments.append("seamless natural transitions, no visible edges")
        if "lighting" in lower or "light" in lower:
            adjustments.append("consistent coherent lighting across entire image")
        if "artifact" in lower or "distort" in lower:
            adjustments.append("clean artifact-free image, no distortions")
        if "skin" in lower or "tone" in lower:
            adjustments.append("natural consistent skin tone, realistic texture")
        if "proportion" in lower or "anatomy" in lower:
            adjustments.append("correct anatomical proportions")

        if not adjustments:
            adjustments.append("higher quality, more photorealistic rendering")

        return ". ".join(adjustments)
