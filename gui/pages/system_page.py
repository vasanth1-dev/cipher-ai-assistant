from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGridLayout,
)

from gui.theme import (
    BACKGROUND,
    CARD_PADDING,
    SPACING,
)

from gui.widgets.ui.page_header import PageHeader
from gui.widgets.ui.section import Section
from gui.widgets.ui.stat_card import StatCard


class SystemPage(QWidget):
    """
    Cipher v2 - System Monitor
    """

     def __init__(
       self,
    ) -> None:
        super().__init__()
        self._build_ui()

    def _build_ui(
        self,
    ) -> None:

        self.setStyleSheet(f"""
        QWidget {{
            background:{BACKGROUND};
        }}
        """)

        root = QVBoxLayout(self)

        root.setContentsMargins(
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
        )

        root.setSpacing(SPACING)

        header = PageHeader(
            "🖥 System Monitor",
            "Live system information"
        )

        root.addWidget(header)

        section = Section("System Statistics")

        root.addWidget(section)

        grid = QGridLayout()

        grid.setSpacing(SPACING)

        self.cpu = StatCard("CPU", "--")
        self.ram = StatCard("RAM", "--")
        self.disk = StatCard("Disk", "--")
        self.network = StatCard("Network", "--")
        self.battery = StatCard("Battery", "--")
        self.uptime = StatCard("Uptime", "--")

        grid.addWidget(self.cpu, 0, 0)
        grid.addWidget(self.ram, 0, 1)
        grid.addWidget(self.disk, 0, 2)

        grid.addWidget(self.network, 1, 0)
        grid.addWidget(self.battery, 1, 1)
        grid.addWidget(self.uptime, 1, 2)

        grid.setColumnStretch(0, 1)
        grid.setColumnStretch(1, 1)
        grid.setColumnStretch(2, 1)

        root.addLayout(grid)

        root.addStretch()

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def set_cpu(
        self, 
        value: str,
    ) -> None:
        self.cpu.set_value(value)

    def set_ram(
        self, 
        value: str,
    ) -> None:
        self.ram.set_value(value)

    def set_disk(
        self, 
        value: str,
    ) -> None:
        self.disk.set_value(value)

    def set_network(
        self, 
        value: str,
    ) -> None:
        self.network.set_value(value)

    def set_battery(
        self, 
        value: str,
    ) -> None:
        self.battery.set_value(value)

    def set_uptime(
        self, 
        value: str,
    ) -> None:
        self.uptime.set_value(value)