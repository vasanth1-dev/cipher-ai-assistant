from __future__ import annotations

from typing import Dict, List, Optional

from core.logger import logger
from plugins.plugin_service import PluginService


class PluginServiceRegistry:
    """
    Registry for services exposed to plugins.

    Services provide stable interfaces between Cipher's
    internal components and plugins.

    Example services:
        - ai
        - speech
        - tts
        - memory
        - clipboard
        - settings
        - notification
    """

    def __init__(self):

        self._services: Dict[str, PluginService] = {}

    # --------------------------------------------------
    # Register
    # --------------------------------------------------

    def register(
        self,
        service: PluginService,
    ) -> None:

        name = service.name.lower().strip()

        if name in self._services:

            logger.warning(
                f"Plugin service already registered: {name}"
            )
            return

        self._services[name] = service

        logger.info(
            f"Registered plugin service: {name}"
        )

    # --------------------------------------------------
    # Unregister
    # --------------------------------------------------

    def unregister(
        self,
        name: str,
    ) -> bool:

        name = name.lower().strip()

        service = self._services.pop(name, None)

        if service is None:
            return False

        logger.info(
            f"Unregistered plugin service: {name}"
        )

        return True

    # --------------------------------------------------
    # Lookup
    # --------------------------------------------------

    def get(
        self,
        name: str,
    ) -> Optional[PluginService]:

        return self._services.get(
            name.lower().strip()
        )

    def exists(
        self,
        name: str,
    ) -> bool:

        return (
            name.lower().strip()
            in self._services
        )

    # --------------------------------------------------
    # Lifecycle
    # --------------------------------------------------

    def start_all(self) -> None:

        for service in self._services.values():

            try:

                service.start()

            except Exception:

                logger.exception(
                    f"Failed starting service: {service.name}"
                )

    def stop_all(self) -> None:

        for service in self._services.values():

            try:

                service.stop()

            except Exception:

                logger.exception(
                    f"Failed stopping service: {service.name}"
                )

    # --------------------------------------------------
    # Lists
    # --------------------------------------------------

    def services(self) -> List[PluginService]:

        return sorted(
            self._services.values(),
            key=lambda service: service.name,
        )

    def names(self) -> List[str]:

        return sorted(
            self._services.keys()
        )

    # --------------------------------------------------
    # Maintenance
    # --------------------------------------------------

    def clear(self) -> None:

        self.stop_all()

        self._services.clear()

    # --------------------------------------------------
    # Count
    # --------------------------------------------------

    @property
    def count(self) -> int:

        return len(self._services)


# Global service registry
plugin_service_registry = PluginServiceRegistry()