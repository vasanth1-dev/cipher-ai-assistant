from __future__ import annotations

import time

from PyQt6.QtCore import QObject, QTimer, pyqtSignal

try:
    import psutil
except ImportError:
    psutil = None


class SystemMetricsService(QObject):
    """
    Collects live system metrics for the Dashboard.

    Signals
    -------
    metricsUpdated(dict)
    """

    metricsUpdated = pyqtSignal(dict)

    def __init__(self, interval: int = 1000, parent=None):
        super().__init__(parent)

        self._boot_time = time.time()

        if psutil:
            try:
                self._boot_time = psutil.boot_time()
            except Exception:
                pass

        self._timer = QTimer(self)
        self._timer.setInterval(interval)
        self._timer.timeout.connect(self._emit_metrics)

    # --------------------------------------------------

    def start(self):
        if not self._timer.isActive():
            self._timer.start()
            self._emit_metrics()

    def stop(self):
        self._timer.stop()

    def set_interval(self, interval: int):
        self._timer.setInterval(interval)

    # --------------------------------------------------

    def _emit_metrics(self):
        self.metricsUpdated.emit(self.collect())

    # --------------------------------------------------

    def collect(self) -> dict:

        if psutil is None:
            return {
                "cpu": "--",
                "ram": "--",
                "disk": "--",
                "network": "Unknown",
                "battery": "--",
                "uptime": "--",
            }

        return {
            "cpu": self._cpu(),
            "ram": self._ram(),
            "disk": self._disk(),
            "network": self._network(),
            "battery": self._battery(),
            "uptime": self._uptime(),
        }

    # --------------------------------------------------

    def _cpu(self):

        try:
            return f"{psutil.cpu_percent(interval=None):.0f}%"
        except Exception:
            return "--"

    def _ram(self):

        try:
            return f"{psutil.virtual_memory().percent:.0f}%"
        except Exception:
            return "--"

    def _disk(self):

        try:
            return f"{psutil.disk_usage('/').percent:.0f}%"
        except Exception:
            return "--"

    def _network(self):

        try:
            counters = psutil.net_io_counters()

            if counters.bytes_recv + counters.bytes_sent > 0:
                return "Online"

            return "Idle"

        except Exception:
            return "Unknown"

    def _battery(self):

        try:
            battery = psutil.sensors_battery()

            if battery is None:
                return "N/A"

            if battery.power_plugged:
                return f"{battery.percent:.0f}% ⚡"

            return f"{battery.percent:.0f}%"

        except Exception:
            return "--"

    def _uptime(self):

        try:
            seconds = int(time.time() - self._boot_time)

            days, seconds = divmod(seconds, 86400)
            hours, seconds = divmod(seconds, 3600)
            minutes, _ = divmod(seconds, 60)

            if days:
                return f"{days}d {hours}h"

            if hours:
                return f"{hours}h {minutes}m"

            return f"{minutes}m"

        except Exception:
            return "--"