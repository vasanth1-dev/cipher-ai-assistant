"""
Cipher v2
JSON Tools Plugin

Provides JSON formatting, validation, and minification utilities.

Features
--------
- Validate JSON
- Pretty-print JSON
- Minify JSON
- Sort object keys
"""

from __future__ import annotations

import json

from core.logger import logger
from plugins.base.plugin import Plugin


class JSONToolsPlugin(Plugin):
    """
    JSON utilities plugin.
    """

    name = "json_tools"
    version = "1.0.0"
    description = "Utilities for working with JSON."

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "json",
            "format json",
            "validate json",
            "pretty json",
            "minify json",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        JSON operations are expected to be invoked through
        Cipher's structured intent pipeline.
        """

        return {
            "success": True,
            "message": (
                "JSON Tools plugin is available. "
                "Waiting for structured JSON commands."
            ),
        }

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    @staticmethod
    def validate(text: str) -> tuple[bool, str]:
        try:
            json.loads(text)
            return True, "Valid JSON"
        except json.JSONDecodeError as exc:
            return False, str(exc)

    # --------------------------------------------------
    # Formatting
    # --------------------------------------------------

    @staticmethod
    def pretty(text: str, indent: int = 4, sort_keys: bool = False) -> str:
        data = json.loads(text)

        return json.dumps(
            data,
            indent=indent,
            sort_keys=sort_keys,
            ensure_ascii=False,
        )

    @staticmethod
    def minify(text: str) -> str:
        data = json.loads(text)

        return json.dumps(
            data,
            separators=(",", ":"),
            ensure_ascii=False,
        )

    @staticmethod
    def normalize(text: str) -> str:
        data = json.loads(text)

        return json.dumps(
            data,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
        )

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)