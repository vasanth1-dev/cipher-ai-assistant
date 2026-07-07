from PyQt6.QtCore import QObject, QTimer

from services.system_monitor import system_monitor


class DashboardUpdater(QObject):
    """
    Updates the DashboardWidget periodically with
    live system information.
    """

    def __init__(self, dashboard):
        super().__init__()

        self.dashboard = dashboard

        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # 1 second
        self.timer.timeout.connect(self.update)

    # --------------------------------------------------

    def start(self):

        self.update()
        self.timer.start()

    # --------------------------------------------------

    def stop(self):

        self.timer.stop()

    # --------------------------------------------------

    def update(self):

        self._update_cpu()
        self._update_ram()
        self._update_disk()
        self._update_network()

    # --------------------------------------------------

    def _update_cpu(self):

        data = system_monitor.cpu()

        self.dashboard.set_cpu(
            f"{data['percent']:.0f}%"
        )

    # --------------------------------------------------

    def _update_ram(self):

        data = system_monitor.ram()

        self.dashboard.set_ram(
            f"{data['percent']:.0f}%"
        )

    # --------------------------------------------------

    def _update_disk(self):

        data = system_monitor.disk()

        self.dashboard.set_disk(
            f"{data['percent']:.0f}%"
        )

    # --------------------------------------------------

    def _update_network(self):

        data = system_monitor.network()

        sent = data["sent_mb"]
        received = data["received_mb"]

        self.dashboard.set_network(
            f"↑{sent:.0f} ↓{received:.0f}"
        )

    # --------------------------------------------------

    def set_ai_online(self):

        self.dashboard.set_ai_status(
            "Online",
            "AI model connected",
        )

    def set_ai_offline(self):

        self.dashboard.set_ai_status(
            "Offline",
            "AI model unavailable",
        )

    # --------------------------------------------------

    def set_voice_idle(self):

        self.dashboard.set_voice_status(
            "Idle",
            "Waiting for command",
        )

    def set_voice_listening(self):

        self.dashboard.set_voice_status(
            "Listening",
            "Microphone active",
        )

    def set_voice_speaking(self):

        self.dashboard.set_voice_status(
            "Speaking",
            "Generating speech",
        )