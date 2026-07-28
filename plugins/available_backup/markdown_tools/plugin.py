"""
Cipher v2
Markdown Tools Plugin

Utilities for working with Markdown documents.

Features
--------
- Markdown validation
- Markdown to HTML conversion
- HTML to Markdown conversion
- Table of contents generation
- Basic document statistics
"""

from __future__ import annotations

import re

from core.logger import logger
from plugins.base_plugin import Plugin

try:
    import markdown
except ImportError:
    markdown = None

try:
    from markdownify import markdownify
except ImportError:
    markdownify = None


class MarkdownToolsPlugin(Plugin):
    """
    Markdown utilities plugin.
    """

    name = "markdown_tools"
    version = "1.0.0"
    description = "Utilities for Markdown documents."

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "markdown",
            "md file",
            "convert markdown",
            "markdown to html",
            "html to markdown",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        Markdown operations are expected to be invoked through
        Cipher's structured document/developer intent pipeline.
        """

        return {
            "success": True,
            "message": (
                "Markdown Tools plugin is available. "
                "Waiting for structured Markdown commands."
            ),
        }

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    @staticmethod
    def validate(text: str) -> tuple[bool, str]:
        if not text.strip():
            return False, "Markdown document is empty."

        return True, "Valid Markdown"

    # --------------------------------------------------
    # Conversion
    # --------------------------------------------------

    @staticmethod
    def markdown_to_html(text: str) -> str:
        if markdown is None:
            raise RuntimeError(
                "markdown is not installed. "
                "Install with: pip install markdown"
            )

        return markdown.markdown(text)

    @staticmethod
    def html_to_markdown(text: str) -> str:
        if markdownify is None:
            raise RuntimeError(
                "markdownify is not installed. "
                "Install with: pip install markdownify"
            )

        return markdownify(text)

    # --------------------------------------------------
    # TOC
    # --------------------------------------------------

    @staticmethod
    def table_of_contents(text: str) -> list[dict]:
        toc = []

        for line in text.splitlines():
            match = re.match(r"^(#{1,6})\s+(.*)", line)

            if not match:
                continue

            hashes, title = match.groups()

            toc.append(
                {
                    "level": len(hashes),
                    "title": title.strip(),
                }
            )

        return toc

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    @staticmethod
    def statistics(text: str) -> dict:
        headings = len(re.findall(r"^#{1,6}\s", text, re.MULTILINE))
        links = len(re.findall(r"\[.*?\]\(.*?\)", text))
        images = len(re.findall(r"!\[.*?\]\(.*?\)", text))

        return {
            "lines": len(text.splitlines()),
            "words": len(text.split()),
            "characters": len(text),
            "headings": headings,
            "links": links,
            "images": images,
        }

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)