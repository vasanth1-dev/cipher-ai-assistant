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
        root.setSpacing(15)

        # -------------------------
        # Header
        # -------------------------

        title = QLabel("🏠 Dashboard")
        title.setStyleSheet("""
        font-size:22px;
        font-weight:bold;
        color:white;
        """)

        subtitle = QLabel(
            "Welcome to Cipher Professional Desktop Assistant"
        )

        subtitle.setStyleSheet("""
        color:#9CA3AF;
        font-size:11pt;
        """)

        root.addWidget(title)
        root.addWidget(subtitle)

        # -------------------------
        # Metrics
        # -------------------------

        metrics = QGridLayout()
        metrics.setSpacing(12)

        self.cpu = MetricCard("CPU", "--", "🖥")
        self.ram = MetricCard("RAM", "--", "🧠")
        self.disk = MetricCard("Disk", "--", "💾")
        self.network = MetricCard("Network", "--", "🌐")

        metrics.addWidget(self.cpu, 0, 0)
        metrics.addWidget(self.ram, 0, 1)
        metrics.addWidget(self.disk, 1, 0)
        metrics.addWidget(self.network, 1, 1)

        root.addLayout(metrics)

        # -------------------------
        # Status Cards
        # -------------------------

        cards = QHBoxLayout()
        cards.setSpacing(12)

        self.ai_card = DashboardCard(
            "AI Status",
            "Ready",
            "Ollama Connected",
        )

        self.voice_card = DashboardCard(
            "Voice",
            "Idle",
            "Waiting for command",
        )

        cards.addWidget(self.ai_card)
        cards.addWidget(self.voice_card)

        root.addLayout(cards)

        # -------------------------
        # Quick Actions
        # -------------------------

        quick = QLabel("Quick Actions")
        quick.setStyleSheet("""
        font-size:15pt;
        font-weight:bold;
        """)

        root.addWidget(quick)

        actions = QHBoxLayout()

        self.terminal_btn = QPushButton("Terminal")
        self.browser_btn = QPushButton("Browser")
        self.files_btn = QPushButton("Files")
        self.settings_btn = QPushButton("Settings")

        for btn in (
            self.terminal_btn,
            self.browser_btn,
            self.files_btn,
            self.settings_btn,
        ):
            btn.setMinimumHeight(42)

            btn.setStyleSheet("""
            QPushButton{
                background:#2563EB;
                color:white;
                border:none;
                border-radius:10px;
                padding:10px 18px;
            }

            QPushButton:hover{
                background:#3B82F6;
            }
            """)

            actions.addWidget(btn)

        root.addLayout(actions)
        root.addStretch()

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def set_cpu(self, value):
        self.cpu.set_value(value)

    def set_ram(self, value):
        self.ram.set_value(value)

    def set_disk(self, value):
        self.disk.set_value(value)

    def set_network(self, value):
        self.network.set_value(value)

    def set_ai_status(self, value, subtitle=""):
        self.ai_card.set_value(value)
        if subtitle:
            self.ai_card.set_subtitle(subtitle)

    def set_voice_status(self, value, subtitle=""):
        self.voice_card.set_value(value)
        if subtitle:
            self.voice_card.set_subtitle(subtitle)