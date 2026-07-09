"""
Cipher v2
Text Tools Plugin

Provides common text manipulation utilities.

Features
--------
- Uppercase / lowercase conversion
- Title case conversion
- Sentence case conversion
- Word and character counts
- Remove extra whitespace
- Reverse text
- Slug generation
"""

from __future__ import annotations

import re

from core.logger import logger
from plugins.base.plugin import Plugin


class TextToolsPlugin(Plugin):
    """
    Text manipulation plugin.
    """

    name = "text_tools"
    version = "1.0.0"
    description = "Utilities for manipulating text."

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "uppercase",
            "lowercase",
            "title case",
            "sentence case",
            "reverse text",
            "word count",
            "character count",
            "slug",
            "clean text",
            "format text",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        Text manipulation requests are expected to be routed through
        Cipher's structured intent pipeline.
        """

        return {
            "success": True,
            "message": (
                "Text Tools plugin is available. "
                "Waiting for structured text tool commands."
            ),
        }

    # --------------------------------------------------
    # Case Conversion
    # --------------------------------------------------

    @staticmethod
    def uppercase(text: str) -> str:
        return text.upper()

    @staticmethod
    def lowercase(text: str) -> str:
        return text.lower()

    @staticmethod
    def titlecase(text: str) -> str:
        return text.title()

    @staticmethod
    def sentencecase(text: str) -> str:
        text = text.strip()

        if not text:
            return text

        return text[0].upper() + text[1:].lower()

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    @staticmethod
    def word_count(text: str) -> int:
        return len(text.split())

    @staticmethod
    def character_count(text: str, include_spaces: bool = True) -> int:
        if include_spaces:
            return len(text)

        return len(text.replace(" ", ""))

    @staticmethod
    def line_count(text: str) -> int:
        if not text:
            return 0

        return len(text.splitlines())

    # --------------------------------------------------
    # Formatting
    # --------------------------------------------------

    @staticmethod
    def clean_whitespace(text: str) -> str:
        return re.sub(r"\s+", " ", text).strip()

    @staticmethod
    def reverse(text: str) -> str:
        return text[::-1]

    @staticmethod
    def slug(text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[-\s]+", "-", text)
        return text

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)