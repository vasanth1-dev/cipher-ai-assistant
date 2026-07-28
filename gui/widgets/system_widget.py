import platform
import socket

import psutil


from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QWidget,
    QGridLayout,
    QLabel,
)

from gui.widgets.system.system_card import SystemCard


class SystemWidget(QWidget):

    def __init__(
       self,
    ) -> None:
        super().__init__()

        layout = QGridLayout(self)

        layout.setContentsMargins(20, 20, 20, 20)
        layout.setHorizontalSpacing(20)
        layout.setVerticalSpacing(20)

        title = QLabel("🖥 System Information")

        title.setStyleSheet("""
            font-size:22px;
            font-weight:bold;
        """)

        layout.addWidget(title, 0, 0, 1, 2)

        self.cpu = SystemCard(
            "💻",
            "CPU",
        )

        self.ram = SystemCard(
            "🧠",
            "Memory",
        )

        self.storage = SystemCard(
            "💾",
            "Storage",
        )

        self.network = SystemCard(
            "🌐",
            "Network",
        )

        self.battery = SystemCard(
            "🔋",
            "Battery",
        )

        self.python = SystemCard(
            "🐍",
            "Python",
        )

        self.os = SystemCard(
            "🐧",
            "Ubuntu",
        )

        self.hostname = SystemCard(
            "🖥",
            "Hostname",
        )

        layout.addWidget(self.cpu, 1, 0)
        layout.addWidget(self.ram, 1, 1)

        layout.addWidget(self.storage, 2, 0)
        layout.addWidget(self.network, 2, 1)

        layout.addWidget(self.battery, 3, 0)
        layout.addWidget(self.python, 3, 1)

        layout.addWidget(self.os, 4, 0)
        layout.addWidget(self.hostname, 4, 1)

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self.refresh
        )

        self.refresh()

        self.timer.start(2000)

    def refresh(self):

        # CPU
        self.cpu.set_value(
            f"{psutil.cpu_percent()} %"
        )

        # Memory
        memory = psutil.virtual_memory()

        self.ram.set_value(
            f"{memory.used // (1024**3)} GB / "
            f"{memory.total // (1024**3)} GB"
        )

        # Storage
        disk = psutil.disk_usage("/")

        self.storage.set_value(
            f"{disk.used // (1024**3)} GB / "
            f"{disk.total // (1024**3)} GB"
        )

        # Battery
        battery = psutil.sensors_battery()

        if battery:

            self.battery.set_value(
                f"{battery.percent}%"
            )

        else:

            self.battery.set_value(
                "Not Available"
            )

        # Network
        self.network.set_value(
            socket.gethostname()
        )

        # Python
        self.python.set_value(
            platform.python_version()
        )

        # Ubuntu / OS
        self.os.set_value(
            platform.platform()
        )

        # Hostname
        self.hostname.set_value(
            socket.gethostname()
        )