"""
Kling AI prompt engineering best practices.

These tips are consumed by intelligence/prompt_enricher.py as a lightweight
"checklist" reference and are also useful as docstrings / UI tooltips.
"""
from __future__ import annotations


KLING_TIPS: dict[str, list[str]] = {
    "general": [
        "Describe what MOVES, not just what EXISTS in the scene",
        "Specify speed: 'very slow', 'gradual', 'subtle' for luxury content",
        "Mention physics: 'natural fluid dynamics', 'realistic cloth simulation'",
        "Include lighting changes: 'light shifts across surface', 'caustics dance'",
        "Reference depth: 'foreground sharp, background soft bokeh'",
        "Avoid abstract concepts — describe concrete visual motion",
        "Shorter prompts (under 300 chars) often work better than very long ones",
        "Include the subject in motion description: 'the glass slowly rotates' not just 'slow rotation'",
    ],
    "product_shots": [
        "Always mention the material: 'crystal glass', 'brushed gold', 'matte ceramic'",
        "Describe light interaction: 'light catches the facets', 'warm glow through amber liquid'",
        "For rotation: specify degrees '45-degree orbit' not just 'orbit'",
        "Include environment micro-motion: 'background softly out of focus with gentle bokeh shift'",
    ],
    "human_shots": [
        "Describe specific body movement: 'she turns her head 30 degrees to the right'",
        "Include micro-expressions: 'subtle smile forms', 'eyes shift focus'",
        "Hair and fabric respond to movement: 'hair sways with the turn'",
        "Breathing creates subtle chest/shoulder movement even in 'static' shots",
    ],
}


# Anti-patterns to flag in logs. If a prompt matches any of these, it's
# probably going to produce weak output.
KLING_ANTIPATTERNS: list[tuple[str, str]] = [
    ("cinematic shot", "too vague — describe the camera movement concretely"),
    ("beautiful", "Kling ignores purely subjective adjectives"),
    ("high quality", "covered by the technical tail — remove from the body"),
    ("make it look good", "describe the actual visual outcome instead"),
]


def flag_antipatterns(prompt: str) -> list[str]:
    """Return a list of warnings if the prompt contains known anti-patterns."""
    if not prompt:
        return []
    lowered = prompt.lower()
    return [
        f"'{token}' → {advice}"
        for token, advice in KLING_ANTIPATTERNS
        if token in lowered
    ]


__all__ = ["KLING_TIPS", "KLING_ANTIPATTERNS", "flag_antipatterns"]
