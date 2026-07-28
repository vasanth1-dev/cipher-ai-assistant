"""
Cipher v2
Runtime Registry

Central registry for shared runtime objects.

Purpose
-------
Avoid circular imports by providing a single place where the
running application can register and retrieve shared managers
and services.

Typical entries include:

- service_manager
- plugin_manager
- event_bus
- application_state
- context_manager
- conversation_manager
- session_manager
- command_pipeline
"""

from __future__ import annotations

from threading import RLock
from typing import Any

from core.logger import logger


class RuntimeRegistry:
    """
    Thread-safe runtime object registry.
    """

    def __init__(
       self,
    ) -> None:
        self._lock = RLock()
        self._objects: dict[str, Any] = {}

    # --------------------------------------------------
    # Registration
    # --------------------------------------------------

    def register(
        self,
        name: str,
        instance: Any,
        *,
        replace: bool = False,
    ) -> None:
        """
        Register a runtime object.

        Raises
        ------
        ValueError
            If the name already exists and replace=False.
        """
        name = name.strip()

        if not name:
            raise ValueError("Registry name cannot be empty.")

        with self._lock:
            if name in self._objects and not replace:
                raise ValueError(
                    f"Runtime object '{name}' is already registered."
                )

            self._objects[name] = instance

        logger.debug("Registered runtime object: %s", name)

    # --------------------------------------------------
    # Lookup
    # --------------------------------------------------

    def get(
        self,
        name: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve a registered runtime object.
        """
        with self._lock:
            return self._objects.get(name, default)

    def require(self, name: str) -> Any:
        """
        Retrieve a runtime object or raise KeyError.
        """
        with self._lock:
            if name not in self._objects:
                raise KeyError(
                    f"Runtime object '{name}' is not registered."
                )

            return self._objects[name]

    def contains(self, name: str) -> bool:
        """
        Return True if an object is registered.
        """
        with self._lock:
            return name in self._objects

    # --------------------------------------------------
    # Removal
    # --------------------------------------------------

    def unregister(self, name: str) -> bool:
        """
        Remove a registered object.
        """
        with self._lock:
            return self._objects.pop(name, None) is not None

    def clear(self) -> None:
        """
        Remove all registered objects.
        """
        with self._lock:
            self._objects.clear()

        logger.info("Runtime registry cleared.")

    # --------------------------------------------------
    # Information
    # --------------------------------------------------

    def names(self) -> list[str]:
        """
        Return all registered object names.
        """
        with self._lock:
            return sorted(self._objects.keys())

    def snapshot(self) -> dict[str, str]:
        """
        Return a lightweight registry snapshot.
        """
        with self._lock:
            return {
                name: obj.__class__.__name__
                for name, obj in self._objects.items()
            }

    def size(self) -> int:
        """
        Return the number of registered objects.
        """
        with self._lock:
            return len(self._objects)