"""
AdGenAI Intelligence Layer.

This module deeply UNDERSTANDS the client's creative vision to execute it
at the highest possible quality. It NEVER overrides creative decisions.

The client's scenario is sacred. The intelligence layer:
- Understands implied technical requirements from natural language
- Enriches prompts with invisible professional photography knowledge
- Analyzes brand assets for visual consistency
- Verifies generated content meets quality standards
- Adapts output for target platforms

Think of it as a world-class film crew: they receive the director's
storyboard and deliver perfection without questioning the vision.
"""

from backend.intelligence.scene_understanding import SceneUnderstanding
from backend.intelligence.prompt_enricher import PromptEnricher
from backend.intelligence.brand_analyzer import BrandAnalyzer
from backend.intelligence.quality_checker import QualityChecker
from backend.intelligence.audience_adapter import AudienceAdapter

__all__ = [
    "SceneUnderstanding",
    "PromptEnricher",
    "BrandAnalyzer",
    "QualityChecker",
    "AudienceAdapter",
]
