"""
Cipher v2
System Monitor Plugin

Provides real-time system monitoring information.

Features
--------
- CPU usage
- Memory usage
- Disk usage
- Network I/O
- Battery status
- System uptime
- Boot time
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

from core.logger import logger
from plugins.base_plugin import BasePlugin

try:
    import psutil
except ImportError:
    psutil = None


class SystemMonitorPlugin(BasePlugin):
    """
    System monitoring plugin.
    """

    name = "system_monitor"
    version = "1.0.0"
    description = "Monitor system resources."

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "system status",
            "system monitor",
            "cpu usage",
            "memory usage",
            "ram usage",
            "disk usage",
            "storage usage",
            "battery",
            "uptime",
            "network usage",
            "resource usage",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        Structured monitoring requests should be routed here by
        Cipher's intent pipeline.
        """

        try:
            return {
                "success": True,
                "system": self.snapshot(),
            }
        except Exception as exc:
            logger.exception(exc)
            return {
                "success": False,
                "message": str(exc),
            }

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _require_library():
        if psutil is None:
            raise RuntimeError(
                "psutil is not installed. "
                "Install it using: pip install psutil"
            )

    # --------------------------------------------------
    # Snapshot
    # --------------------------------------------------

    def snapshot(self) -> dict[str, Any]:
        self._require_library()

        vm = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        net = psutil.net_io_counters()

        battery = None
        if hasattr(psutil, "sensors_battery"):
            battery = psutil.sensors_battery()

        boot_time = datetime.fromtimestamp(psutil.boot_time())

        result = {
            "cpu_percent": psutil.cpu_percent(interval=0.2),
            "cpu_count": psutil.cpu_count(),
            "memory": {
                "total": vm.total,
                "available": vm.available,
                "used": vm.used,
                "percent": vm.percent,
            },
            "disk": {
                "total": disk.total,
                "used": disk.used,
                "free": disk.free,
                "percent": disk.percent,
            },
            "network": {
                "bytes_sent": net.bytes_sent,
                "bytes_received": net.bytes_recv,
                "packets_sent": net.packets_sent,
                "packets_received": net.packets_recv,
            },
            "boot_time": boot_time.isoformat(),
            "uptime_seconds": int(datetime.now().timestamp() - psutil.boot_time()),
        }

        if battery is not None:
            result["battery"] = {
                "percent": battery.percent,
                "plugged": battery.power_plugged,
                "seconds_left": battery.secsleft,
            }

        return result