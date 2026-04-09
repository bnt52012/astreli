"""
Structured logging configuration for AdGenAI.

Provides two modes:
- Human-readable console logging with emojis for development
- Structured JSON logging for production deployment (ELK, Datadog, etc.)
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any


# ── Emoji Prefixes for Console Logging ────────────────────────

STEP_EMOJIS = {
    "mode": "\U0001f50d",      # magnifying glass
    "analysis": "\U0001f3ac",  # clapper board
    "enrich": "\u2728",        # sparkles
    "image": "\U0001f5bc\ufe0f",  # framed picture
    "video": "\U0001f3a5",     # movie camera
    "assembly": "\U0001f3ac",  # clapper board
    "quality": "\u2705",       # check mark
    "error": "\u274c",         # cross mark
    "warning": "\u26a0\ufe0f", # warning
    "success": "\U0001f389",   # party popper
    "cache": "\U0001f4be",     # floppy disk
    "fallback": "\U0001f504",  # counterclockwise arrows
    "brand": "\U0001f3a8",     # artist palette
    "cost": "\U0001f4b0",      # money bag
    "health": "\U0001f3e5",    # hospital
}


class StructuredJsonFormatter(logging.Formatter):
    """Formats log records as single-line JSON for machine consumption.

    Output fields:
        timestamp, level, logger, message, module, function, line,
        plus any extras passed via the `extra` dict.
    """

    def format(self, record: logging.LogRecord) -> str:
        log_entry: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Include exception info if present
        if record.exc_info and record.exc_info[1]:
            log_entry["exception"] = {
                "type": record.exc_info[0].__name__ if record.exc_info[0] else "Unknown",
                "message": str(record.exc_info[1]),
            }

        # Include any extra fields
        standard_attrs = {
            "name", "msg", "args", "created", "relativeCreated",
            "exc_info", "exc_text", "stack_info", "lineno", "funcName",
            "filename", "module", "pathname", "thread", "threadName",
            "process", "processName", "levelname", "levelno", "message",
            "msecs", "taskName",
        }
        for key, value in record.__dict__.items():
            if key not in standard_attrs and not key.startswith("_"):
                try:
                    json.dumps(value)
                    log_entry[key] = value
                except (TypeError, ValueError):
                    log_entry[key] = str(value)

        return json.dumps(log_entry, default=str)


class EmojiConsoleFormatter(logging.Formatter):
    """Human-readable console formatter with color and emoji prefixes."""

    COLORS = {
        "DEBUG": "\033[36m",     # Cyan
        "INFO": "\033[32m",      # Green
        "WARNING": "\033[33m",   # Yellow
        "ERROR": "\033[31m",     # Red
        "CRITICAL": "\033[1;31m",  # Bold Red
    }
    RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLORS.get(record.levelname, "")
        timestamp = datetime.fromtimestamp(record.created).strftime("%H:%M:%S")

        # Extract step emoji from message prefix if present
        emoji = ""
        msg = record.getMessage()
        for prefix, icon in STEP_EMOJIS.items():
            if msg.startswith(f"[{prefix.upper()}]"):
                emoji = f"{icon} "
                break

        formatted = (
            f"{color}{timestamp} [{record.levelname:<7}]{self.RESET} "
            f"{emoji}{record.name}: {msg}"
        )

        if record.exc_info and record.exc_info[1]:
            formatted += f"\n{color}  Exception: {record.exc_info[1]}{self.RESET}"

        return formatted


def configure_logging(
    *,
    level: str = "INFO",
    json_mode: bool = False,
    log_file: str | None = None,
) -> None:
    """Configure logging for the entire application.

    Args:
        level: Minimum log level (DEBUG, INFO, WARNING, ERROR).
        json_mode: If True, use structured JSON format for all output.
        log_file: Optional file path for persistent log output.
    """
    root = logging.getLogger()
    root.setLevel(getattr(logging, level.upper(), logging.INFO))

    # Remove existing handlers
    root.handlers.clear()

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(getattr(logging, level.upper(), logging.INFO))

    if json_mode:
        console.setFormatter(StructuredJsonFormatter())
    else:
        console.setFormatter(EmojiConsoleFormatter())

    root.addHandler(console)

    # Optional file handler (always JSON for machine parsing)
    if log_file:
        file_handler = logging.FileHandler(log_file, encoding="utf-8")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(StructuredJsonFormatter())
        root.addHandler(file_handler)

    # Silence noisy third-party loggers
    for name in ("httpx", "httpcore", "urllib3", "openai", "google"):
        logging.getLogger(name).setLevel(logging.WARNING)
