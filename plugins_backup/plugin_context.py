from __future__ import annotations

from typing import Any, Dict, Optional

from core.logger import logger


class PluginContext:
    """
    Shared runtime context passed to plugins.

    The context provides controlled access to core Cipher
    services without plugins importing internal modules
    directly.

    Example services that may be registered later:

    - ai_service
    - speech_service
    - tts_service
    - memory_service
    - settings_service
    - event_bus
    - command_router
    """

    def __init__(
       self,
    ) -> None:

        self._services: Dict[str, Any] = {}
        self._data: Dict[str, Any] = {}

    # --------------------------------------------------
    # Services
    # --------------------------------------------------

    def register_service(
        self,
        name: str,
        service: Any,
    ) -> None:

        self._services[name] = service

        logger.debug(
            f"Plugin service registered: {name}"
        )

    def unregister_service(
        self,
        name: str,
    ) -> None:

        self._services.pop(name, None)

        logger.debug(
            f"Plugin service removed: {name}"
        )

    def get_service(
        self,
        name: str,
        default: Any = None,
    ) -> Any:

        return self._services.get(name, default)

    def has_service(
        self,
        name: str,
    ) -> bool:

        return name in self._services

    # --------------------------------------------------
    # Shared Runtime Data
    # --------------------------------------------------

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:

        self._data[key] = value

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        return self._data.get(key, default)

    def remove(
        self,
        key: str,
    ) -> None:

        self._data.pop(key, None)

    def clear(self) -> None:

        self._data.clear()

    # --------------------------------------------------
    # Information
    # --------------------------------------------------

    @property
    def services(self) -> Dict[str, Any]:

        return dict(self._services)

    @property
    def data(self) -> Dict[str, Any]:

        return dict(self._data)

    def __contains__(
        self,
        name: str,
    ) -> bool:

        return self.has_service(name)

    def __repr__(self) -> str:

        return (
            f"PluginContext("
            f"services={len(self._services)}, "
            f"data={len(self._data)})"
        )