"""
Prompt Templates Knowledge Engine
=================================
Comprehensive lookup data for enriching AI image/video generation prompts
with professional photography, cinematography, and advertising knowledge.
"""

from .photography_styles import PHOTOGRAPHY_STYLES
from .lighting_setups import LIGHTING_SETUPS
from .lens_library import LENS_LIBRARY
from .color_palettes import COLOR_PALETTES
from .composition_rules import COMPOSITION_RULES
from .texture_materials import TEXTURE_MATERIALS
from .environment_moods import ENVIRONMENT_MOODS

__all__ = [
    "PHOTOGRAPHY_STYLES",
    "LIGHTING_SETUPS",
    "LENS_LIBRARY",
    "COLOR_PALETTES",
    "COMPOSITION_RULES",
    "TEXTURE_MATERIALS",
    "ENVIRONMENT_MOODS",
]
