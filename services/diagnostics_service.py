"""
Cipher v2
Diagnostics Service

Collects runtime diagnostic information from the major Cipher
components and exposes it through a single interface.

Responsibilities
----------------
- Runtime diagnostics
- Service diagnostics
- Plugin diagnostics
- Session diagnostics
- Health summary
"""

from __future__ import annotations

from typing import Any

from core.logger import logger


class DiagnosticsService:
    """
    Aggregates runtime diagnostic information.
    """

    def __init__(
        self,
        *,
        application_state=None,
        session_manager=None,
        service_manager=None,
        plugin_manager=None,
        health_monitor=None,
        performance_monitor=None,
    ):
        self.application_state = application_state
        self.session_manager = session_manager
        self.service_manager = service_manager
        self.plugin_manager = plugin_manager
        self.health_monitor = health_monitor
        self.performance_monitor = performance_monitor

    # --------------------------------------------------
    # Diagnostics
    # --------------------------------------------------

    def collect(self) -> dict[str, Any]:
        """
        Collect diagnostics from all available components.
        """
        report = {
            "application": self._application(),
            "session": self._session(),
            "services": self._services(),
            "plugins": self._plugins(),
            "health": self._health(),
            "performance": self._performance(),
        }

        logger.debug("Diagnostics report generated.")

        return report

    # --------------------------------------------------
    # Sections
    # --------------------------------------------------

    def _application(self) -> dict[str, Any]:
        if self.application_state is None:
            return {}

        if hasattr(self.application_state, "status"):
            return self.application_state.status()

        if hasattr(self.application_state, "snapshot"):
            return self.application_state.snapshot()

        return {}

    def _session(self) -> dict[str, Any]:
        if self.session_manager is None:
            return {}

        if hasattr(self.session_manager, "info"):
            return self.session_manager.info()

        return {}

    def _services(self) -> list[dict[str, Any]]:
        if self.service_manager is None:
            return []

        if hasattr(self.service_manager, "status"):
            return self.service_manager.status()

        return []

    def _plugins(self) -> list[dict[str, Any]]:
        if self.plugin_manager is None:
            return []

        if hasattr(self.plugin_manager, "status"):
            return self.plugin_manager.status()

        return []

    def _health(self) -> dict[str, Any]:
        if self.health_monitor is None:
            return {}

        if hasattr(self.health_monitor, "summary"):
            return self.health_monitor.summary()

        return {}

    def _performance(self) -> dict[str, Any]:
        if self.performance_monitor is None:
            return {}

        if hasattr(self.performance_monitor, "statistics"):
            return self.performance_monitor.statistics()

        return {}