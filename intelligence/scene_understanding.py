"""
Scene Understanding — deep comprehension of client's scenario.

Does NOT make creative decisions. Deeply UNDERSTANDS what the client wrote
to route it correctly through the pipeline.

Examples:
  "she walks toward camera" -> tracking shot + forward motion
  "close-up on her wrist"  -> macro framing
  "same location but sunset" -> reference previous scene + modify lighting
  "she holds the bottle"   -> mannequin + product = PATH A
  "the bottle rotates"     -> product only = PATH B + orbit camera
"""
from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class SceneContext:
    """Extracted technical understanding of a scene."""
    implied_camera_movement: str = "static"
    implied_framing: str = "medium"
    implied_lighting_direction: str = "front"
    implied_subject_motion: str = "static"
    implied_speed: str = "normal"
    references_previous_scene: bool = False
    previous_scene_ref_type: str = ""  # "same_location", "same_outfit", etc.
    has_product_interaction: bool = False
    has_multiple_subjects: bool = False
    wardrobe_change: bool = False
    time_of_day: str = ""
    environment_type: str = ""
    mood_keywords: list[str] = field(default_factory=list)
    detected_action: str = ""
    kling_hints: dict[str, Any] = field(default_factory=dict)
    gemini_hints: dict[str, Any] = field(default_factory=dict)


class SceneUnderstanding:
    """Deeply understands scene descriptions for correct pipeline routing."""

    # Camera movement indicators
    _TRACKING_KEYWORDS = [
        "walks toward", "walking toward", "approaches", "approaching",
        "moves toward", "coming closer", "advancing", "striding",
        "walks away", "walking away", "retreats", "departing",
        "camera follows", "follows her", "follows him", "follows them",
    ]
    _PAN_KEYWORDS = [
        "across the", "sweeping view", "panoramic", "panning",
        "looks across", "scanning", "from left to right", "from right to left",
    ]
    _ZOOM_IN_KEYWORDS = [
        "close-up", "closeup", "close up", "macro", "detail",
        "zooming in", "focus on", "tight on", "reveals detail",
    ]
    _ZOOM_OUT_KEYWORDS = [
        "wide shot", "pulls back", "zooming out", "reveal",
        "establishes", "establishing", "full view", "wide angle",
    ]
    _ORBIT_KEYWORDS = [
        "rotates", "rotation", "spins", "spinning", "orbits",
        "360", "around", "circling", "revolving",
    ]

    # Framing indicators
    _CLOSE_FRAMING = [
        "close-up", "closeup", "macro", "detail", "tight shot",
        "extreme close", "her eyes", "his eyes", "the label",
        "her lips", "her hands", "his hands", "fingertips",
        "wrist", "neckline", "texture of", "engraving",
    ]
    _WIDE_FRAMING = [
        "wide shot", "establishing", "landscape", "panorama",
        "full view", "aerial", "drone", "bird's eye", "skyline",
        "full body", "head to toe", "entire scene",
    ]

    # Lighting direction
    _BACKLIT = ["backlit", "backlighting", "silhouette", "rim light", "contre-jour"]
    _SIDE_LIT = ["side light", "side-lit", "dramatic shadow", "chiaroscuro"]
    _TOP_LIT = ["overhead", "top light", "top-down", "zenith"]

    # Subject motion
    _WALKING = ["walks", "walking", "strides", "striding", "strolling", "saunters"]
    _TURNING = ["turns", "turning", "spins", "looks back", "glances", "head turn"]
    _REACHING = ["reaches", "reaching", "picks up", "grabs", "touches", "holds"]
    _STILL = ["poses", "posing", "standing still", "static", "motionless", "frozen"]

    # Time of day
    _GOLDEN_HOUR = ["golden hour", "sunset", "sunrise", "dusk", "dawn", "magic hour"]
    _NIGHT = ["night", "nighttime", "midnight", "moonlight", "starlight", "neon"]
    _OVERCAST = ["overcast", "cloudy", "grey sky", "diffused", "soft day"]

    # Environment
    _STUDIO = ["studio", "backdrop", "seamless", "white background", "black background"]
    _OUTDOOR = ["outdoor", "outside", "field", "beach", "mountain", "city", "street", "garden"]
    _INTERIOR = ["interior", "room", "apartment", "atelier", "boutique", "hotel", "restaurant"]

    def analyze(self, scene_text: str, scene_index: int = 0, previous_context: SceneContext | None = None) -> SceneContext:
        """Analyze a scene description to extract technical understanding."""
        text = scene_text.lower()
        ctx = SceneContext()

        # Camera movement
        ctx.implied_camera_movement = self._detect_camera(text)

        # Framing
        ctx.implied_framing = self._detect_framing(text)

        # Lighting
        ctx.implied_lighting_direction = self._detect_lighting(text)

        # Subject motion
        ctx.implied_subject_motion = self._detect_motion(text)

        # Speed
        if any(w in text for w in ["slow motion", "slowly", "gently", "gracefully", "deliberately"]):
            ctx.implied_speed = "slow"
        elif any(w in text for w in ["fast", "quickly", "rapid", "energetic", "dynamic", "burst"]):
            ctx.implied_speed = "fast"

        # Product interaction
        ctx.has_product_interaction = any(
            w in text for w in [
                "holds", "holding", "picks up", "applies", "sprays",
                "pours", "opens", "unwraps", "lifts", "displays",
                "bottle", "product", "package", "box",
            ]
        )

        # Multiple subjects
        ctx.has_multiple_subjects = any(
            w in text for w in [
                "they", "them", "both", "couple", "group", "two",
                "together", "each other", "models", "friends",
            ]
        )

        # References to previous scene
        if any(w in text for w in ["same location", "same place", "same spot", "same set"]):
            ctx.references_previous_scene = True
            ctx.previous_scene_ref_type = "same_location"
        elif any(w in text for w in ["same outfit", "same dress", "same look"]):
            ctx.references_previous_scene = True
            ctx.previous_scene_ref_type = "same_outfit"
        elif any(w in text for w in ["later", "then", "next", "continues", "continuation"]):
            ctx.references_previous_scene = True
            ctx.previous_scene_ref_type = "temporal_continuation"

        # Wardrobe change
        ctx.wardrobe_change = any(
            w in text for w in [
                "changes into", "new outfit", "different dress",
                "now wearing", "changed clothes", "another look",
            ]
        )

        # Time of day
        if any(w in text for w in self._GOLDEN_HOUR):
            ctx.time_of_day = "golden_hour"
        elif any(w in text for w in self._NIGHT):
            ctx.time_of_day = "night"
        elif any(w in text for w in self._OVERCAST):
            ctx.time_of_day = "overcast"
        elif "morning" in text:
            ctx.time_of_day = "morning"
        elif "noon" in text or "midday" in text:
            ctx.time_of_day = "noon"

        # Environment
        if any(w in text for w in self._STUDIO):
            ctx.environment_type = "studio"
        elif any(w in text for w in self._OUTDOOR):
            ctx.environment_type = "outdoor"
        elif any(w in text for w in self._INTERIOR):
            ctx.environment_type = "interior"

        # Mood keywords
        mood_map = {
            "dramatic": ["dramatic", "intense", "powerful", "bold", "striking"],
            "romantic": ["romantic", "tender", "intimate", "love", "passion", "sensual"],
            "energetic": ["energetic", "dynamic", "vibrant", "exciting", "explosive"],
            "serene": ["serene", "calm", "peaceful", "tranquil", "zen", "quiet"],
            "mysterious": ["mysterious", "enigmatic", "dark", "shadow", "hidden"],
            "luxurious": ["luxurious", "opulent", "rich", "elegant", "refined"],
            "playful": ["playful", "fun", "joyful", "cheerful", "lighthearted"],
            "edgy": ["edgy", "raw", "gritty", "urban", "street"],
        }
        for mood, keywords in mood_map.items():
            if any(w in text for w in keywords):
                ctx.mood_keywords.append(mood)

        # Detected action summary
        ctx.detected_action = self._summarize_action(text)

        # Build Kling-specific hints
        ctx.kling_hints = self._build_kling_hints(ctx, text)

        # Build Gemini-specific hints
        ctx.gemini_hints = self._build_gemini_hints(ctx, text)

        logger.debug(
            "Scene %d understanding: camera=%s, framing=%s, motion=%s, mood=%s",
            scene_index, ctx.implied_camera_movement, ctx.implied_framing,
            ctx.implied_subject_motion, ctx.mood_keywords,
        )
        return ctx

    def analyze_all(self, scene_texts: list[str]) -> list[SceneContext]:
        """Analyze all scenes with inter-scene awareness."""
        contexts: list[SceneContext] = []
        prev: SceneContext | None = None
        for i, text in enumerate(scene_texts):
            ctx = self.analyze(text, i, prev)
            contexts.append(ctx)
            prev = ctx
        return contexts

    def _detect_camera(self, text: str) -> str:
        if any(w in text for w in self._TRACKING_KEYWORDS):
            return "tracking"
        if any(w in text for w in self._ORBIT_KEYWORDS):
            return "orbit"
        if any(w in text for w in self._ZOOM_IN_KEYWORDS):
            return "zoom_in"
        if any(w in text for w in self._ZOOM_OUT_KEYWORDS):
            return "zoom_out"
        if any(w in text for w in self._PAN_KEYWORDS):
            return "pan_right"
        return "static"

    def _detect_framing(self, text: str) -> str:
        if any(w in text for w in self._CLOSE_FRAMING):
            return "close_up"
        if any(w in text for w in self._WIDE_FRAMING):
            return "wide"
        return "medium"

    def _detect_lighting(self, text: str) -> str:
        if any(w in text for w in self._BACKLIT):
            return "backlit"
        if any(w in text for w in self._SIDE_LIT):
            return "side"
        if any(w in text for w in self._TOP_LIT):
            return "top"
        return "front"

    def _detect_motion(self, text: str) -> str:
        if any(w in text for w in self._WALKING):
            return "walking"
        if any(w in text for w in self._TURNING):
            return "turning"
        if any(w in text for w in self._REACHING):
            return "reaching"
        if any(w in text for w in self._STILL):
            return "static"
        return "subtle"

    def _summarize_action(self, text: str) -> str:
        actions = []
        if "walk" in text:
            actions.append("walking")
        if "hold" in text or "pick" in text:
            actions.append("interacting_with_object")
        if "turn" in text or "look" in text:
            actions.append("head_movement")
        if "danc" in text:
            actions.append("dancing")
        if "run" in text:
            actions.append("running")
        if "sit" in text:
            actions.append("sitting")
        if "stand" in text:
            actions.append("standing")
        return ", ".join(actions) if actions else "static_pose"

    def _build_kling_hints(self, ctx: SceneContext, text: str) -> dict[str, Any]:
        hints: dict[str, Any] = {}
        # Map motion to Kling prompt additions
        if ctx.implied_subject_motion == "walking":
            hints["motion_prompt"] = "natural walking movement, subtle body sway"
        elif ctx.implied_subject_motion == "turning":
            hints["motion_prompt"] = "gentle head and body turn"
        elif ctx.implied_subject_motion == "reaching":
            hints["motion_prompt"] = "smooth reaching gesture, deliberate hand movement"

        if ctx.implied_speed == "slow":
            hints["speed_modifier"] = "in slow motion, ethereal movement"
        elif ctx.implied_speed == "fast":
            hints["speed_modifier"] = "dynamic fast movement, energetic pacing"

        if ctx.implied_camera_movement == "tracking":
            hints["camera_prompt"] = "smooth tracking shot following subject"
        elif ctx.implied_camera_movement == "orbit":
            hints["camera_prompt"] = "slow orbit camera movement around subject"
        elif ctx.implied_camera_movement == "zoom_in":
            hints["camera_prompt"] = "smooth push-in toward subject"

        if "wind" in text:
            hints["atmosphere"] = "wind blowing through hair and fabric"
        if "rain" in text:
            hints["atmosphere"] = "rain droplets, wet surfaces"
        if "particle" in text or "dust" in text:
            hints["atmosphere"] = "floating particles in light beams"

        return hints

    def _build_gemini_hints(self, ctx: SceneContext, text: str) -> dict[str, Any]:
        hints: dict[str, Any] = {}
        hints["framing"] = ctx.implied_framing
        hints["lighting_direction"] = ctx.implied_lighting_direction

        if ctx.time_of_day:
            hints["time_of_day"] = ctx.time_of_day
        if ctx.environment_type:
            hints["environment"] = ctx.environment_type
        if ctx.mood_keywords:
            hints["mood"] = ctx.mood_keywords

        return hints
