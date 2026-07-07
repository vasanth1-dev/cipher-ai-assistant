from PyQt6.QtCore import QObject, QTimer

from services.system_monitor import system_monitor


class DashboardUpdater(QObject):

    def __init__(self, dashboard):
        super().__init__()

        self.dashboard = dashboard

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
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

        try:
            self._update_cpu()
            self._update_ram()
            self._update_disk()
            self._update_network()
            self._update_battery()
            self._update_uptime()

        except Exception as e:
            print("Dashboard Update Error:", e)

    # --------------------------------------------------
    # CPU
    # --------------------------------------------------

    def _update_cpu(self):

        data = system_monitor.cpu()

        self.dashboard.set_cpu(
            f"{data['percent']:.0f}%"
        )

    # --------------------------------------------------
    # RAM
    # --------------------------------------------------

    def _update_ram(self):

        data = system_monitor.ram()

        self.dashboard.set_ram(
            f"{data['percent']:.0f}%"
        )

    # --------------------------------------------------
    # Disk
    # --------------------------------------------------

    def _update_disk(self):

        data = system_monitor.disk()

        self.dashboard.set_disk(
            f"{data['percent']:.0f}%"
        )

    # --------------------------------------------------
    # Network
    # --------------------------------------------------

    def _update_network(self):

        data = system_monitor.network()

        self.dashboard.set_network(
            f"↑{data['sent_mb']:.0f} ↓{data['received_mb']:.0f}"
        )

    # --------------------------------------------------
    # Battery
    # --------------------------------------------------

    def _update_battery(self):

        data = system_monitor.battery()

        if not data["available"]:

            self.dashboard.set_battery("--")

            return

        self.dashboard.set_battery(
            f"{data['percent']:.0f}%"
        )

    # --------------------------------------------------
    # Uptime
    # --------------------------------------------------

    def _update_uptime(self):

        data = system_monitor.uptime()

        self.dashboard.set_uptime(
            data["text"]
        )

    # --------------------------------------------------
    # AI Status
    # --------------------------------------------------

    def set_ai_online(self):

        self.dashboard.set_ai_status(
            "Online",
            "Ollama Connected",
        )

    def set_ai_offline(self):

        self.dashboard.set_ai_status(
            "Offline",
            "Ollama Disconnected",
        )

    # --------------------------------------------------
    # Voice Status
    # --------------------------------------------------

    def set_voice_idle(self):

        self.dashboard.set_voice_status(
            "Idle",
            "Waiting for command",
        )

    def set_voice_listening(self):

        self.dashboard.set_voice_status(
            "Listening",
            "Microphone Active",
        )

    def set_voice_speaking(self):

        self.dashboard.set_voice_status(
            "Speaking",
            "Generating response",
        )