from PyQt6.QtWidgets import (
    QGridLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from gui.theme import (
    SPACING,
    TEXT,
    TEXT_MUTED,
    scale,
)

from gui.widgets.dashboard.status_tile import StatusTile


class StatusStrip(QWidget):
    """
    Dashboard system overview section.
    """

    def __init__(
        self, 
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self._build_ui()

    # --------------------------------------------------

    def _build_ui(
        self,
    ) -> None:

        root = QVBoxLayout(self)

        root.setSpacing(
            scale(SPACING)
        )

        root.setContentsMargins(
            0,
            8,
            0,
            8,
        )

        title = QLabel("Assistant Status")

        title.setStyleSheet(f"""
            color:{TEXT};
            font-size:20px;
            font-weight:800;
        """)

        subtitle = QLabel(
            "Current assistant and system health"
        )

        subtitle.setStyleSheet(f"""
            color:{TEXT_MUTED};
            font-size:11pt;
        """)

        root.addSpacing(8)

        root.addWidget(title)
        root.addWidget(subtitle)

        grid = QGridLayout()

        grid.setHorizontalSpacing(18)
        grid.setVerticalSpacing(18)

        self.model = StatusTile(
            "🤖",
            "AI Model",
            "qwen2.5",
        )

        self.voice = StatusTile(
            "🎤",
            "Voice",
            "Ready",
        )

        self.memory = StatusTile(
            "🧠",
            "Memory",
            "Active",
        )

        self.ai_status = StatusTile(
            "🤖",
            "AI Status",
            "Ready",
        )

        self.uptime = StatusTile(
            "⏱",
            "Uptime",
            "00:00:00",
        )

        self.conversations = StatusTile(
            "💬",
            "Conversations",
            "0",
        )

        self.cpu = StatusTile(
            "🖥",
            "CPU",
            "-- %",
        )

        self.ram = StatusTile(
            "💾",
            "RAM",
            "-- %",
        )

        self.disk = StatusTile(
            "🗄",
            "Storage",
            "-- %",
        )

        grid.addWidget(self.model, 0, 0)
        grid.addWidget(self.voice, 0, 1)
        grid.addWidget(self.memory, 0, 2)

        grid.addWidget(self.cpu, 1, 0)
        grid.addWidget(self.ram, 1, 1)
        grid.addWidget(self.disk, 1, 2)

        grid.addWidget(self.ai_status, 2, 0)
        grid.addWidget(self.uptime, 2, 1)
        grid.addWidget(self.conversations, 2, 2)

        for column in range(3):
            grid.setColumnStretch(column, 1)

        for row in range(3):
            grid.setRowStretch(row, 1)

        root.addLayout(grid)

    # --------------------------------------------------

    def set_model(
        self, 
        value: str,
    ) -> None:
        self.model.set_value(value)

    def set_voice(
        self, 
        value: str,
    ) -> None:
        self.voice.set_value(value)

    def set_memory(
        self, 
        value: str,
    ) -> None:
        self.memory.set_value(value)

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

    def set_ai_status(
        self, 
        value: str,
    ) -> None:
        self.ai_status.set_value(value)


    def set_uptime(
        self, 
        value: str,
    ) -> None:
        self.uptime.set_value(value)


    def set_conversations(
        self, 
        value: str,
    ) -> None:
        self.conversations.set_value(value)