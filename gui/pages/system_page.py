from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
    QLabel,
    QFrame,
)

from gui.theme import (
    BACKGROUND,
    SURFACE,
    BORDER,
    TEXT,
    TEXT_MUTED,
)


class SystemCard(QFrame):

    def __init__(self, title: str):
        super().__init__()

        self.setStyleSheet(f"""
        QFrame{{
            background:{SURFACE};
            border:1px solid {BORDER};
            border-radius:12px;
        }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(8)

        self.title = QLabel(title)
        self.title.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:10pt;
        """)

        self.value = QLabel("--")
        self.value.setStyleSheet(f"""
        color:{TEXT};
        font-size:22px;
        font-weight:bold;
        """)

        layout.addWidget(self.title)
        layout.addWidget(self.value)
        layout.addStretch()

    def set_value(self, value):
        self.value.setText(str(value))


class SystemPage(QWidget):

    def __init__(self):
        super().__init__()

        self._build_ui()

    def _build_ui(self):

        self.setStyleSheet(f"""
        QWidget{{
            background:{BACKGROUND};
            color:{TEXT};
        }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(20)

        title = QLabel("🖥 System Monitor")
        title.setStyleSheet("""
        font-size:24px;
        font-weight:bold;
        """)

        subtitle = QLabel("Live system information")

        subtitle.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:10pt;
        """)

        root.addWidget(title)
        root.addWidget(subtitle)

        grid = QGridLayout()
        grid.setSpacing(15)

        self.cpu = SystemCard("CPU")
        self.ram = SystemCard("RAM")
        self.disk = SystemCard("Disk")
        self.network = SystemCard("Network")
        self.battery = SystemCard("Battery")
        self.uptime = SystemCard("Uptime")

        grid.addWidget(self.cpu, 0, 0)
        grid.addWidget(self.ram, 0, 1)
        grid.addWidget(self.disk, 0, 2)

        grid.addWidget(self.network, 1, 0)
        grid.addWidget(self.battery, 1, 1)
        grid.addWidget(self.uptime, 1, 2)

        root.addLayout(grid)
        root.addStretch()

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