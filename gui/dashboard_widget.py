from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)
from gui.theme import (
    TEXT,
    TEXT_MUTED,
    CARD_PADDING,
    SPACING,
    BUTTON_HEIGHT,
    TITLE_SIZE,
    HEADER_SIZE,
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
        root.setSpacing(
            CARD_PADDING
        )

        # --------------------------------------------------
        # Header
        # --------------------------------------------------

        title = QLabel("System Overview")
        title.setStyleSheet(f"""
        font-size:{TITLE_SIZE + 2}px;
        font-weight:bold;
        color:{TEXT};
        """)

        subtitle = QLabel(
            "Ubuntu Desktop AI Assistant"
        )

        subtitle.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:11pt;
        """)

        root.addWidget(title)
        root.addWidget(subtitle)

        # --------------------------------------------------
        # Metrics
        # --------------------------------------------------

        metrics = QGridLayout()
        metrics.setSpacing(
            SPACING
        )

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

        line = QLabel()

        line.setFixedHeight(1)

        line.setStyleSheet("""
        background:#334155;
        margin-top:6px;
        margin-bottom:6px;
        """)

        root.addWidget(line)

        # --------------------------------------------------
        # Status
        # --------------------------------------------------

        status = QHBoxLayout()
        status.setSpacing(
            SPACING
        )

        self.ai_card = DashboardCard(
            "AI Status",
            "🟢 Online",
            "Model Ready",
        )

        self.voice_card = DashboardCard(
            "Voice",
            "🎤 Ready",
            "Waiting for command...",
        )

        status.addWidget(self.ai_card)
        status.addWidget(self.voice_card)

        root.addLayout(status)

        # --------------------------------------------------
        # Quick Actions
        # --------------------------------------------------

        quick = QLabel("Quick Actions")
        quick.setStyleSheet(f"""
        font-size:{HEADER_SIZE}pt;
        font-weight:bold;
        color:{TEXT};
        """)

        root.addWidget(quick)

        actions = QHBoxLayout()

        self.terminal_btn = QPushButton("Terminal")
        self.browser_btn = QPushButton("Browser")
        self.files_btn = QPushButton("Files")
        self.settings_btn = QPushButton("Settings")

        self.terminal_btn.setToolTip(
            "Open Terminal"
        )

        self.browser_btn.setToolTip(
            "Open Browser"
        )

        self.files_btn.setToolTip(
            "Open Files"
        )

        self.settings_btn.setToolTip(
            "Open Settings"
        )

        buttons = (
            self.terminal_btn,
            self.browser_btn,
            self.files_btn,
            self.settings_btn,
        )

        for btn in buttons:

            btn.setMinimumHeight(
                BUTTON_HEIGHT
            )

            btn.setCursor(
                Qt.CursorShape.PointingHandCursor
            )

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
        
    def set_ai_online(self):

        self.ai_card.set_value(
            "🟢 Online"
        )

        self.ai_card.set_subtitle(
            "Model Ready"
        )


    def set_ai_offline(self):

        self.ai_card.set_value(
            "🔴 Offline"
        )

        self.ai_card.set_subtitle(
            "Disconnected"
        )


    def set_voice_ready(self):

        self.voice_card.set_value(
            "🎤 Ready"
        )

        self.voice_card.set_subtitle(
            "Waiting for command"
        )


    def set_voice_listening(self):

        self.voice_card.set_value(
            "🎧 Listening"
        )

        self.voice_card.set_subtitle(
            "Speech detected"
        )

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
        online: bool,
        model: str = "",
    ):

        if online:

            self.ai_card.set_value("🟢 Online")

            if model:
                self.ai_card.set_subtitle(model)
            else:
                self.ai_card.set_subtitle("Model Ready")

        else:

            self.ai_card.set_value("🔴 Offline")
            self.ai_card.set_subtitle("Disconnected")

    def set_voice_status(
        self,
        status,
        subtitle="",
    ):

        icons = {

            "Ready": "🎤",
            "Listening": "🎧",
            "Thinking": "🧠",
            "Speaking": "🔊",

        }

        icon = icons.get(
            status,
            "🎤",
        )

        self.voice_card.set_value(
            f"{icon} {status}"
        )

        if subtitle:

            self.voice_card.set_subtitle(
                subtitle
            )

    def enable_actions(
        self,
        enabled=True,
    ):

        buttons = (

            self.terminal_btn,
            self.browser_btn,
            self.files_btn,
            self.settings_btn,

        )

        for button in buttons:

            button.setEnabled(enabled)