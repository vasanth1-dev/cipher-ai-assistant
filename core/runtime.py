"""
Cipher v2
Runtime

Central runtime container.

This module exposes a single object that owns the major runtime
components after bootstrapping. It acts as the application's
dependency container.

It intentionally does not create components itself; that remains
the responsibility of ApplicationBootstrap.
"""

from __future__ import annotations

from typing import Any


class Runtime:
    """
    Holds references to the application's runtime objects.
    """

    def __init__(self):
        self._objects: dict[str, Any] = {}

    # --------------------------------------------------
    # Registration
    # --------------------------------------------------

    def register(self, name: str, instance: Any) -> None:
        self._objects[name] = instance

    def register_many(self, **objects: Any) -> None:
        for name, instance in objects.items():
            self.register(name, instance)

    # --------------------------------------------------
    # Lookup
    # --------------------------------------------------

    def get(self, name: str, default: Any = None) -> Any:
        return self._objects.get(name, default)

    def require(self, name: str) -> Any:
        if name not in self._objects:
            raise KeyError(
                f"Runtime component '{name}' is not registered."
            )

        return self._objects[name]

    def contains(self, name: str) -> bool:
        return name in self._objects

    # --------------------------------------------------
    # Information
    # --------------------------------------------------

    def names(self) -> list[str]:
        return sorted(self._objects.keys())

    def snapshot(self) -> dict[str, str]:
        return {
            key: value.__class__.__name__
            for key, value in self._objects.items()
        }

    # --------------------------------------------------
    # Convenience Properties
    # --------------------------------------------------

    @property
    def plugin_manager(self):
        return self.get("plugin_manager")

    @property
    def service_manager(self):
        return self.get("service_manager")

    @property
    def event_bus(self):
        return self.get("event_bus")

    @property
    def command_pipeline(self):
        return self.get("command_pipeline")

    @property
    def application_state(self):
        return self.get("application_state")

    @property
    def context_manager(self):
        return self.get("context_manager")

    @property
    def conversation_manager(self):
        return self.get("conversation_manager")

    @property
    def session_manager(self):
        return self.get("session_manager")