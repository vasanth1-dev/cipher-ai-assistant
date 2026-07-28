"""
Cipher v2
Context Manager

Maintains shared runtime context that can be accessed by the AI,
plugins, services, and GUI.

Examples of managed context
---------------------------
- Active application
- Active window
- Current working directory
- Selected files
- Clipboard summary
- User session state
- Temporary variables
"""

from __future__ import annotations

from threading import RLock
from typing import Any

from core.logger import logger


class ContextManager:
    """
    Shared runtime context store.

    This class intentionally stores only runtime state.
    Persistent user preferences should be managed elsewhere.
    """

    def __init__(
       self,
    ) -> None:
        self._context: dict[str, Any] = {}
        self._lock = RLock()

    # --------------------------------------------------
    # Basic Operations
    # --------------------------------------------------

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store a context value.
        """
        with self._lock:
            self._context[key] = value

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve a context value.
        """
        with self._lock:
            return self._context.get(key, default)

    def has(self, key: str) -> bool:
        """
        Return True if a key exists.
        """
        with self._lock:
            return key in self._context

    def remove(self, key: str) -> bool:
        """
        Remove a context value.
        """
        with self._lock:
            if key not in self._context:
                return False

            del self._context[key]
            return True

    # --------------------------------------------------
    # Bulk Operations
    # --------------------------------------------------

    def update(
        self,
        values: dict[str, Any],
    ) -> None:
        """
        Update multiple context values.
        """
        with self._lock:
            self._context.update(values)

    def snapshot(self) -> dict[str, Any]:
        """
        Return a shallow copy of the current context.
        """
        with self._lock:
            return dict(self._context)

    def keys(self) -> list[str]:
        """
        Return all context keys.
        """
        with self._lock:
            return sorted(self._context.keys())

    # --------------------------------------------------
    # Session
    # --------------------------------------------------

    def clear(self) -> None:
        """
        Remove all runtime context.
        """
        with self._lock:
            self._context.clear()

        logger.info("Runtime context cleared.")

    def size(self) -> int:
        """
        Return the number of stored context entries.
        """
        with self._lock:
            return len(self._context)

    # --------------------------------------------------
    # Convenience Helpers
    # --------------------------------------------------

    def set_active_application(self, application: str) -> None:
        self.set("active_application", application)

    def active_application(self) -> str | None:
        return self.get("active_application")

    def set_current_directory(self, directory: str) -> None:
        self.set("current_directory", directory)

    def current_directory(self) -> str | None:
        return self.get("current_directory")

    def set_selected_files(
        self,
        files: list[str],
    ) -> None:
        self.set("selected_files", list(files))

    def selected_files(self) -> list[str]:
        return self.get("selected_files", [])