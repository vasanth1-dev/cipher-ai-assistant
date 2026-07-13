from __future__ import annotations

import time

from PyQt6.QtCore import QObject, QTimer, pyqtSignal

try:
    import psutil
except ImportError:
    psutil = None


class DashboardService(QObject):
    """
    Dashboard Service

    Responsibilities
    ----------------
    • CPU usage
    • RAM usage
    • Disk usage
    • Network status
    • Battery percentage
    • System uptime

    Emits a metrics dictionary every refresh interval.
    """

    metricsUpdated = pyqtSignal(dict)

    def __init__(self, interval: int = 1000):
        super().__init__()

        self._boot_time = time.time()

        if psutil:
            try:
                self._boot_time = psutil.boot_time()
            except Exception:
                pass

        self._timer = QTimer(self)
        self._timer.setInterval(interval)
        self._timer.timeout.connect(self._update_metrics)

    # --------------------------------------------------

    def start(self):
        if not self._timer.isActive():
            self._timer.start()
            self._update_metrics()

    def stop(self):
        self._timer.stop()

    # --------------------------------------------------

    def _update_metrics(self):
        self.metricsUpdated.emit(self._collect())

    # --------------------------------------------------

    def _collect(self) -> dict:

        if psutil is None:
            return {
                "cpu": "--",
                "ram": "--",
                "disk": "--",
                "network": "Unknown",
                "battery": "--",
                "uptime": "--",
            }

        # CPU
        try:
            cpu = f"{psutil.cpu_percent(interval=None):.0f}%"
        except Exception:
            cpu = "--"

        # RAM
        try:
            ram = f"{psutil.virtual_memory().percent:.0f}%"
        except Exception:
            ram = "--"

        # Disk
        try:
            disk = f"{psutil.disk_usage('/').percent:.0f}%"
        except Exception:
            disk = "--"

        # Network
        try:
            counters = psutil.net_io_counters()
            network = (
                "Online"
                if counters.bytes_sent + counters.bytes_recv > 0
                else "Idle"
            )
        except Exception:
            network = "Unknown"

        # Battery
        try:
            battery = psutil.sensors_battery()

            if battery is None:
                battery_text = "N/A"
            elif battery.power_plugged:
                battery_text = f"{battery.percent:.0f}% ⚡"
            else:
                battery_text = f"{battery.percent:.0f}%"

        except Exception:
            battery_text = "--"

        # Uptime
        try:
            seconds = int(time.time() - self._boot_time)

            days, seconds = divmod(seconds, 86400)
            hours, seconds = divmod(seconds, 3600)
            minutes, _ = divmod(seconds, 60)

            if days:
                uptime = f"{days}d {hours}h"
            elif hours:
                uptime = f"{hours}h {minutes}m"
            else:
                uptime = f"{minutes}m"

        except Exception:
            uptime = "--"

        return {
            "cpu": cpu,
            "ram": ram,
            "disk": disk,
            "network": network,
            "battery": battery_text,
            "uptime": uptime,
        }