from PyQt6.QtCore import QObject

from services.system_metrics_service import SystemMetricsService


class DashboardController(QObject):
    """
    Coordinates dashboard services and updates the DashboardWidget.
    """

    def __init__(self, dashboard_widget, parent=None):
        super().__init__(parent)

        self.dashboard = dashboard_widget
        self.metrics = SystemMetricsService()

        self.metrics.metricsUpdated.connect(
            self._on_metrics_updated
        )

    # --------------------------------------------------

    def start(self):
        self.metrics.start()

    def stop(self):
        self.metrics.stop()

    # --------------------------------------------------

    def _on_metrics_updated(self, data: dict):

        self.dashboard.set_cpu(
            data.get("cpu", "--")
        )

        self.dashboard.set_ram(
            data.get("ram", "--")
        )

        self.dashboard.set_disk(
            data.get("disk", "--")
        )

        self.dashboard.set_network(
            data.get("network", "--")
        )

        self.dashboard.set_battery(
            data.get("battery", "--")
        )

        self.dashboard.set_uptime(
            data.get("uptime", "--")
        )