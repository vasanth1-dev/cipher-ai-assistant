"""
Cipher v2
Code Tools Plugin

Provides common source code utilities.

Features
--------
- Syntax checking (basic)
- Line counting
- Comment removal
- Code statistics
- Language detection (basic)
"""

from __future__ import annotations

import ast
import re
from pathlib import Path

from core.logger import logger
from plugins.base_plugin import Plugin


class CodeToolsPlugin(Plugin):
    """
    Source code utilities plugin.
    """

    name = "code_tools"
    version = "1.0.0"
    description = "Utilities for source code analysis."

    LANGUAGE_MAP = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".java": "Java",
        ".c": "C",
        ".cpp": "C++",
        ".cs": "C#",
        ".go": "Go",
        ".rs": "Rust",
        ".php": "PHP",
        ".html": "HTML",
        ".css": "CSS",
        ".json": "JSON",
        ".xml": "XML",
        ".md": "Markdown",
        ".sh": "Shell",
    }

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "source code",
            "code",
            "syntax",
            "analyze code",
            "code statistics",
            "programming",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        Code analysis requests are intended to be routed through
        Cipher's structured developer-intent pipeline.
        """

        return {
            "success": True,
            "message": (
                "Code Tools plugin is available. "
                "Waiting for structured code analysis commands."
            ),
        }

    # --------------------------------------------------
    # Language Detection
    # --------------------------------------------------

    @classmethod
    def detect_language(cls, path: Path) -> str:
        return cls.LANGUAGE_MAP.get(
            path.suffix.lower(),
            "Unknown",
        )

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    @staticmethod
    def statistics(code: str) -> dict:
        lines = code.splitlines()

        blank = sum(1 for line in lines if not line.strip())

        comment = sum(
            1
            for line in lines
            if line.strip().startswith(("#", "//"))
        )

        return {
            "lines": len(lines),
            "blank_lines": blank,
            "comment_lines": comment,
            "characters": len(code),
        }

    # --------------------------------------------------
    # Python Syntax
    # --------------------------------------------------

    @staticmethod
    def validate_python(code: str) -> tuple[bool, str]:
        try:
            ast.parse(code)
            return True, "Valid Python"
        except SyntaxError as exc:
            return False, str(exc)

    # --------------------------------------------------
    # Comment Removal
    # --------------------------------------------------

    @staticmethod
    def remove_python_comments(code: str) -> str:
        cleaned = []

        for line in code.splitlines():
            cleaned.append(
                re.sub(r"#.*$", "", line)
            )

        return "\n".join(cleaned)

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)