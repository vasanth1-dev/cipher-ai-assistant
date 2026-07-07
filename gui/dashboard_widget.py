from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from gui.widgets.dashboard_card import DashboardCard
from gui.widgets.metric_card import MetricCard


class DashboardWidget(QWidget):

    def __init__(self):
        super().__init__()

        self._build_ui()

    # --------------------------------------------------

    def _build_ui(self):

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(18)

        # --------------------------------------------------
        # Header
        # --------------------------------------------------

        title = QLabel("🏠 Dashboard")
        title.setStyleSheet("""
        font-size:24px;
        font-weight:bold;
        color:white;
        """)

        subtitle = QLabel(
            "Welcome back, Vasanth"
        )

        subtitle.setStyleSheet("""
        color:#9CA3AF;
        font-size:11pt;
        """)

        root.addWidget(title)
        root.addWidget(subtitle)

        # --------------------------------------------------
        # Metrics
        # --------------------------------------------------

        metrics = QGridLayout()
        metrics.setSpacing(12)

        self.cpu = MetricCard("CPU", "--", "🖥")
        self.ram = MetricCard("RAM", "--", "🧠")
        self.disk = MetricCard("Disk", "--", "💾")
        self.network = MetricCard("Network", "--", "🌐")
        self.battery = MetricCard("Battery", "--", "🔋")
        self.uptime = MetricCard("Uptime", "--", "⏱")

        metrics.addWidget(self.cpu, 0, 0)
        metrics.addWidget(self.ram, 0, 1)
        metrics.addWidget(self.disk, 0, 2)

        metrics.addWidget(self.network, 1, 0)
        metrics.addWidget(self.battery, 1, 1)
        metrics.addWidget(self.uptime, 1, 2)

        root.addLayout(metrics)

        # --------------------------------------------------
        # Status
        # --------------------------------------------------

        status = QHBoxLayout()
        status.setSpacing(12)

        self.ai_card = DashboardCard(
            "AI Status",
            "Online",
            "Ollama Connected",
        )

        self.voice_card = DashboardCard(
            "Voice",
            "Idle",
            "Waiting...",
        )

        status.addWidget(self.ai_card)
        status.addWidget(self.voice_card)

        root.addLayout(status)

        # --------------------------------------------------
        # Quick Actions
        # --------------------------------------------------

        quick = QLabel("Quick Actions")
        quick.setStyleSheet("""
        font-size:16pt;
        font-weight:bold;
        color:white;
        """)

        root.addWidget(quick)

        actions = QHBoxLayout()

        self.terminal_btn = QPushButton("🖥 Terminal")
        self.browser_btn = QPushButton("🌍 Browser")
        self.files_btn = QPushButton("📁 Files")
        self.settings_btn = QPushButton("⚙ Settings")

        buttons = (
            self.terminal_btn,
            self.browser_btn,
            self.files_btn,
            self.settings_btn,
        )

        for btn in buttons:

            btn.setMinimumHeight(45)

            btn.setStyleSheet("""
            QPushButton{
                background:#2563EB;
                color:white;
                border:none;
                border-radius:10px;
                padding:12px;
            }

            QPushButton:hover{
                background:#3B82F6;
            }
            """)

            actions.addWidget(btn)

        root.addLayout(actions)

        root.addStretch()

    # --------------------------------------------------
    # Metrics
    # --------------------------------------------------

    def set_cpu(self, value):
        self.cpu.set_value(value)

    def set_ram(self, value):
        self.ram.set_value(value)

    def set_disk(self, value):
        self.disk.set_value(value)

    def set_network(self, value):
        self.network.set_value(value)

    def set_battery(self, value):
        self.battery.set_value(value)

    def set_uptime(self, value):
        self.uptime.set_value(value)

    # --------------------------------------------------
    # Status
    # --------------------------------------------------

    def set_ai_status(
        self,
        value,
        subtitle="",
    ):

        self.ai_card.set_value(value)

        if subtitle:
            self.ai_card.set_subtitle(subtitle)

    def set_voice_status(
        self,
        value,
        subtitle="",
    ):

        self.voice_card.set_value(value)

        if subtitle:
            self.voice_card.set_subtitle(subtitle)