"""
Cipher v2
Application State

Centralized runtime state shared across the application.

This class stores application-wide runtime information that is
needed by the GUI, services, plugins, and AI components.

Unlike ContextManager, which stores dynamic user/context data,
ApplicationState stores the operational state of Cipher itself.
"""

from __future__ import annotations

from threading import RLock
from typing import Any

from core.logger import logger


class ApplicationState:
    """
    Thread-safe application state container.
    """

    def __init__(
       self,
    ) -> None:
        self._lock = RLock()

        self._state: dict[str, Any] = {
            "initialized": False,
            "ready": False,
            "listening": False,
            "speaking": False,
            "processing": False,
            "online": False,
            "wake_word_enabled": True,
            "gui_visible": True,
            "microphone_muted": False,
            "active_plugin": None,
            "last_command": None,
            "last_response": None,
        }

    # --------------------------------------------------
    # Generic API
    # --------------------------------------------------

    def set(self, key: str, value: Any) -> None:
        """
        Set a runtime state value.
        """
        with self._lock:
            self._state[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a runtime state value.
        """
        with self._lock:
            return self._state.get(key, default)

    def update(self, values: dict[str, Any]) -> None:
        """
        Update multiple state values.
        """
        with self._lock:
            self._state.update(values)

    def snapshot(self) -> dict[str, Any]:
        """
        Return a copy of the current state.
        """
        with self._lock:
            return dict(self._state)

    def clear(self) -> None:
        """
        Reset the application state to defaults.
        """
        with self._lock:
            defaults = self.__class__()._state
            self._state.clear()
            self._state.update(defaults)

        logger.info("Application state reset.")

    # --------------------------------------------------
    # Convenience Properties
    # --------------------------------------------------

    @property
    def initialized(self) -> bool:
        return self.get("initialized", False)

    @initialized.setter
    def initialized(self, value: bool):
        self.set("initialized", bool(value))

    @property
    def ready(self) -> bool:
        return self.get("ready", False)

    @ready.setter
    def ready(self, value: bool):
        self.set("ready", bool(value))

    @property
    def listening(self) -> bool:
        return self.get("listening", False)

    @listening.setter
    def listening(self, value: bool):
        self.set("listening", bool(value))

    @property
    def speaking(self) -> bool:
        return self.get("speaking", False)

    @speaking.setter
    def speaking(self, value: bool):
        self.set("speaking", bool(value))

    @property
    def processing(self) -> bool:
        return self.get("processing", False)

    @processing.setter
    def processing(self, value: bool):
        self.set("processing", bool(value))

    @property
    def online(self) -> bool:
        return self.get("online", False)

    @online.setter
    def online(self, value: bool):
        self.set("online", bool(value))

    # --------------------------------------------------
    # Diagnostics
    # --------------------------------------------------

    def status(self) -> dict[str, Any]:
        """
        Return a summary of the current application state.
        """
        return {
            "initialized": self.initialized,
            "ready": self.ready,
            "listening": self.listening,
            "speaking": self.speaking,
            "processing": self.processing,
            "online": self.online,
            "active_plugin": self.get("active_plugin"),
            "wake_word_enabled": self.get("wake_word_enabled"),
            "microphone_muted": self.get("microphone_muted"),
        }