"""
Cipher v2
Health Monitor

Monitors the runtime health of Cipher.

Features
--------
- Heartbeat
- Service health
- Plugin health
- Process uptime
- Memory usage
- CPU usage
"""

from __future__ import annotations

import time
from typing import Any

from core.logger import logger

try:
    import psutil
except ImportError:
    psutil = None


class HealthMonitor:
    """
    Runtime health monitor.
    """

    def __init__(
        self,
        *,
        service_manager=None,
        plugin_manager=None,
    ):
        self.service_manager = service_manager
        self.plugin_manager = plugin_manager

        self._started = time.time()
        self._last_heartbeat = self._started

    # --------------------------------------------------
    # Heartbeat
    # --------------------------------------------------

    def heartbeat(self) -> None:
        """
        Record a heartbeat.
        """
        self._last_heartbeat = time.time()

    @property
    def last_heartbeat(self) -> float:
        return self._last_heartbeat

    @property
    def uptime(self) -> float:
        return time.time() - self._started

    # --------------------------------------------------
    # Runtime
    # --------------------------------------------------

    def runtime(self) -> dict[str, Any]:
        """
        Return runtime statistics.
        """
        info = {
            "uptime_seconds": round(self.uptime, 2),
            "last_heartbeat": self.last_heartbeat,
        }

        if psutil is not None:
            self._process = (
                psutil.Process()
                if psutil is not None
                else None
            )

            info.update(
                {
                    "cpu_percent": self.process.cpu_percent(interval=0.0),
                    "memory_mb": round(
                        self.process.memory_info().rss / (1024 * 1024),
                        2,
                    ),
                    "threads": self.process.num_threads(),
                }
            )

        return info

    # --------------------------------------------------
    # Services
    # --------------------------------------------------

    def services(self) -> list[dict[str, Any]]:
        """
        Return service health.
        """
        if self.service_manager is None:
            return []

        try:
            return self.service_manager.status()
        except Exception:
            logger.exception(
                "Failed to retrieve service status."
            )
            return []

    # --------------------------------------------------
    # Plugins
    # --------------------------------------------------

    def plugins(self) -> list[dict[str, Any]]:
        """
        Return plugin information.
        """
        if self.plugin_manager is None:
            return []

        try:
            return self.plugin_manager.status()
        except Exception:
            logger.exception(
                "Failed to retrieve plugin status."
            )
            return []

    # --------------------------------------------------
    # Summary
    # --------------------------------------------------

    def summary(self) -> dict[str, Any]:
        """
        Return an overall health summary.
        """
        return {
            "runtime": self.runtime(),
            "services": self.services(),
            "plugins": self.plugins(),
        }
    
    def start(self) -> None:
        """
        Start the health monitor.
        """
        self._started = time.time()
        self.heartbeat()
        logger.info("Health Monitor started.")

    def stop(self) -> None:
        """
        Stop the health monitor.
        """
        logger.info("Health Monitor stopped.")