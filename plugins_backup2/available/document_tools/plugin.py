"""
Cipher v2
Document Tools Plugin

Provides common document processing utilities.

Features
--------
- Read text documents
- Write text documents
- Detect document type
- Basic document statistics
- Search within documents
"""

from __future__ import annotations

from pathlib import Path

from core.logger import logger
from plugins.base_plugin import BasePlugin


class DocumentToolsPlugin(BasePlugin):
    """
    Document processing plugin.
    """

    name = "document_tools"
    version = "1.0.0"
    description = "Utilities for working with text documents."

    SUPPORTED_EXTENSIONS = {
        ".txt",
        ".md",
        ".log",
        ".csv",
        ".json",
        ".xml",
        ".yaml",
        ".yml",
    }

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "document",
            "text file",
            "open document",
            "read document",
            "search document",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        Document operations are expected to be routed through
        Cipher's structured document-intent pipeline.
        """

        return {
            "success": True,
            "message": (
                "Document Tools plugin is available. "
                "Waiting for structured document commands."
            ),
        }

    # --------------------------------------------------
    # Read / Write
    # --------------------------------------------------

    @staticmethod
    def read(path: Path, encoding: str = "utf-8") -> str:
        path = Path(path)

        return path.read_text(
            encoding=encoding,
        )

    @staticmethod
    def write(
        path: Path,
        text: str,
        encoding: str = "utf-8",
    ) -> None:
        path = Path(path)

        path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        path.write_text(
            text,
            encoding=encoding,
        )

    # --------------------------------------------------
    # Statistics
    # --------------------------------------------------

    @staticmethod
    def statistics(text: str) -> dict:
        lines = text.splitlines()

        return {
            "lines": len(lines),
            "words": len(text.split()),
            "characters": len(text),
            "non_empty_lines": sum(
                1 for line in lines if line.strip()
            ),
        }

    # --------------------------------------------------
    # Search
    # --------------------------------------------------

    @staticmethod
    def search(text: str, query: str) -> list[int]:
        """
        Return line numbers containing the query.
        """
        matches = []

        query = query.lower()

        for index, line in enumerate(
            text.splitlines(),
            start=1,
        ):
            if query in line.lower():
                matches.append(index)

        return matches

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @classmethod
    def is_supported(cls, path: Path) -> bool:
        return (
            Path(path).suffix.lower()
            in cls.SUPPORTED_EXTENSIONS
        )

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)