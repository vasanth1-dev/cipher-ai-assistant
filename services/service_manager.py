"""
Cipher v2
Service Manager

Central manager for all long-running background services.

Responsibilities
----------------
- Register services
- Start all services
- Stop all services
- Restart individual services
- Query service status
- Prevent duplicate registrations

Each managed service is expected to expose:

    start()
    stop()

Optionally:

    running  -> bool property
"""

from __future__ import annotations

from collections import OrderedDict
from typing import Any

from core.logger import logger


class ServiceManager:
    """
    Central registry for Cipher background services.
    """

    def __init__(
       self,
    ) -> None:
        self._services: OrderedDict[str, Any] = OrderedDict()

    # --------------------------------------------------
    # Registration
    # --------------------------------------------------

    def register(self, name: str, service: Any) -> None:
        """
        Register a background service.

        Raises:
            ValueError
                If the service name already exists.
        """
        name = name.strip()

        if not name:
            raise ValueError("Service name cannot be empty.")

        if name in self._services:
            raise ValueError(
                f"Service '{name}' is already registered."
            )

        self._services[name] = service

        logger.info("Registered service: %s", name)

    def unregister(self, name: str) -> bool:
        """
        Remove a registered service.
        """
        service = self._services.pop(name, None)

        if service is None:
            return False

        logger.info("Unregistered service: %s", name)
        return True

    # --------------------------------------------------
    # Lifecycle
    # --------------------------------------------------

    def start_all(self) -> None:
        """
        Start every registered service.
        """
        for name, service in self._services.items():
            self._safe_start(name, service)

    def stop_all(self) -> None:
        """
        Stop services in reverse registration order.
        """
        for name, service in reversed(self._services.items()):
            self._safe_stop(name, service)

    def restart(self, name: str) -> bool:
        """
        Restart a single service.
        """
        service = self._services.get(name)

        if service is None:
            return False

        self._safe_stop(name, service)
        self._safe_start(name, service)

        return True

    # --------------------------------------------------
    # Access
    # --------------------------------------------------

    def get(self, name: str):
        """
        Retrieve a registered service.
        """
        return self._services.get(name)

    def names(self) -> list[str]:
        """
        Return registered service names.
        """
        return list(self._services.keys())

    def status(self) -> list[dict]:
        """
        Return status information for every service.
        """
        results = []

        for name, service in self._services.items():
            running = False

            if hasattr(service, "running"):
                try:
                    running = bool(service.running)
                except Exception:
                    running = False

            results.append(
                {
                    "name": name,
                    "running": running,
                    "type": service.__class__.__name__,
                }
            )

        return results

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _safe_start(name: str, service: Any):
        try:
            service.start()
            logger.info("Started service: %s", name)

        except Exception:
            logger.exception(
                "Failed to start service: %s",
                name,
            )

    @staticmethod
    def _safe_stop(name: str, service: Any):
        try:
            service.stop()
            logger.info("Stopped service: %s", name)

        except Exception:
            logger.exception(
                "Failed to stop service: %s",
                name,
            )