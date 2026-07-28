from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
    QLabel,
)

from gui.theme import (
    SPACING,
    TEXT,
    TEXT_MUTED,
    scale,
)

from gui.widgets.dashboard.action_card import ActionCard


class QuickActions(QWidget):
    """
    Dashboard Quick Actions
    """

    chatClicked = pyqtSignal()
    filesClicked = pyqtSignal()
    memoryClicked = pyqtSignal()
    systemClicked = pyqtSignal()
    settingsClicked = pyqtSignal()

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
        root.setContentsMargins(0, 0, 0, 0)

        title = QLabel("Quick Actions")

        title.setStyleSheet(f"""
            color:{TEXT};
            font-size:20px;
            font-weight:800;
        """)

        subtitle = QLabel(
            "Frequently used actions"
        )

        subtitle.setStyleSheet(f"""
            color:{TEXT_MUTED};
            font-size:11pt;
        """)

        root.addWidget(title)
        root.addWidget(subtitle)

        layout = QHBoxLayout()

        layout.setSpacing(18)
        layout.setContentsMargins(0, 10, 0, 0)

        self.chat = ActionCard("💬", "Chat")
        self.files = ActionCard("📁", "Files")
        self.memory = ActionCard("🧠", "Memory")
        self.system = ActionCard("🖥", "System")
        self.settings = ActionCard("⚙", "Settings")

        for card in (
            self.chat,
            self.files,
            self.memory,
            self.system,
            self.settings,
        ):
            card.setSizePolicy(
                card.sizePolicy().horizontalPolicy(),
                card.sizePolicy().verticalPolicy(),
            )
            layout.addWidget(card)

        layout.addStretch(1)

        root.addLayout(layout)

        self.chat.clicked.connect(self.chatClicked.emit)
        self.files.clicked.connect(self.filesClicked.emit)
        self.memory.clicked.connect(self.memoryClicked.emit)
        self.system.clicked.connect(self.systemClicked.emit)
        self.settings.clicked.connect(self.settingsClicked.emit)

    def set_enabled(
        self,
        enabled: bool,
    ) -> None:

        self.chat.setEnabled(enabled)
        self.files.setEnabled(enabled)
        self.memory.setEnabled(enabled)
        self.system.setEnabled(enabled)
        self.settings.setEnabled(enabled)