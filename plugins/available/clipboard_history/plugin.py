"""
Cipher v2
Clipboard History Plugin

Provides clipboard history management.

Features
--------
- Maintain clipboard history
- Retrieve recent clipboard items
- Search clipboard history
- Clear clipboard history
- Limit history size
"""

from __future__ import annotations

from collections import deque
from typing import Any

from core.logger import logger
from plugins.base.plugin import Plugin


class ClipboardHistoryPlugin(Plugin):
    """
    Clipboard history plugin.

    Note:
        This plugin provides an in-memory clipboard history manager.
        Clipboard monitoring should be performed by a background service
        that feeds new clipboard contents into this plugin.
    """

    name = "clipboard_history"
    version = "1.0.0"
    description = "Manage clipboard history."

    DEFAULT_HISTORY_SIZE = 100

    def __init__(self):
        super().__init__()

        self._history: deque[str] = deque(
            maxlen=self.DEFAULT_HISTORY_SIZE
        )

    # --------------------------------------------------
    # Plugin API
    # --------------------------------------------------

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "clipboard history",
            "clipboard",
            "copied items",
            "copy history",
            "clipboard manager",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        Clipboard operations are expected to be invoked through
        Cipher's structured intent pipeline.
        """

        return {
            "success": True,
            "message": (
                "Clipboard History plugin is available. "
                "Waiting for structured clipboard history commands."
            ),
        }

    # --------------------------------------------------
    # History
    # --------------------------------------------------

    def add(self, text: str) -> None:
        """
        Add a new clipboard entry.
        """
        if not text:
            return

        if self._history and self._history[-1] == text:
            return

        self._history.append(text)

    def recent(self, limit: int = 10) -> list[str]:
        """
        Return the most recent clipboard items.
        """
        limit = max(1, limit)

        return list(self._history)[-limit:][::-1]

    def search(self, query: str) -> list[str]:
        """
        Search clipboard history.
        """
        query = query.lower()

        return [
            item
            for item in reversed(self._history)
            if query in item.lower()
        ]

    def clear(self) -> None:
        """
        Clear clipboard history.
        """
        self._history.clear()

    def count(self) -> int:
        """
        Number of stored clipboard entries.
        """
        return len(self._history)

    def set_limit(self, size: int) -> None:
        """
        Change history capacity.
        """
        size = max(10, size)

        self._history = deque(
            self._history,
            maxlen=size,
        )

    def snapshot(self) -> dict[str, Any]:
        """
        Return clipboard history metadata.
        """
        return {
            "count": self.count(),
            "capacity": self._history.maxlen,
            "items": self.recent(),
        }

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)