from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QLineEdit,
)

from gui.theme import (
    SURFACE,
    BORDER,
    PRIMARY,
    PRIMARY_HOVER,
    TEXT,
    TEXT_MUTED,
    CARD_RADIUS,
    BUTTON_HEIGHT,
)


class ChatHeader(QFrame):
    """
    Professional chat header.
    """

    newChatClicked = pyqtSignal()
    clearChatClicked = pyqtSignal()
    exportChatClicked = pyqtSignal()
    searchTextChanged = pyqtSignal(str)

    def __init__(
        self, 
        parent: QFrame |None = None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("ChatHeader")

        self.setStyleSheet(f"""
        QFrame#ChatHeader {{
            background:{SURFACE};
            border:1px solid {BORDER};
            border-radius:{CARD_RADIUS}px;
        }}

        QPushButton {{
            background:{PRIMARY};
            color:white;
            border:none;
            border-radius:8px;
            padding:6px 14px;
            min-height:{BUTTON_HEIGHT}px;
        }}

        QPushButton:hover {{
            background:{PRIMARY_HOVER};
        }}
        """)

        self._build_ui()

    # --------------------------------------------------

    def _build_ui(
        self,
    ) -> None:

        root = QHBoxLayout(self)

        root.setContentsMargins(
            20,
            16,
            20,
            16,
        )

        root.setSpacing(16)

        # ---------------- Left ----------------

        left = QVBoxLayout()

        left.setSpacing(4)

        self.title = QLabel("💬 Chat")

        self.title.setStyleSheet(f"""
            color: {TEXT};
            font-size: 20pt;
            font-weight: 700;
        """)

        self.subtitle = QLabel(
            "🟢 Online  •  qwen2.5"
        )

        self.subtitle.setStyleSheet(f"""
            color: {TEXT_MUTED};
            font-size: 10pt;
        """)

        left.addWidget(self.title)
        left.addWidget(self.subtitle)

        root.addLayout(left)

        root.addStretch()

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "🔍 Search messages..."
        )

        self.search.setMinimumWidth(220)

        self.search.textChanged.connect(
            self.searchTextChanged.emit
        )

        root.addWidget(self.search)

        # ---------------- Right ----------------

        self.new_chat = QPushButton("✨ New Chat")

        self.export_chat = QPushButton("💾 Export")

        self.clear_chat = QPushButton("🗑 Clear")

        self.new_chat.setMinimumWidth(120)
        self.export_chat.setMinimumWidth(110)
        self.clear_chat.setMinimumWidth(100)

        self.new_chat.clicked.connect(
            self.newChatClicked.emit
        )

        self.export_chat.clicked.connect(
            self.exportChatClicked.emit
        )

        self.clear_chat.clicked.connect(
            self.clearChatClicked.emit
        )

        root.addWidget(self.new_chat)
        root.addWidget(self.export_chat)
        root.addWidget(self.clear_chat)

    # --------------------------------------------------

    def set_model(
        self,
        model: str,
    ) -> None:

        self.subtitle.setText(
            f"🟢 Online   •   {model}"
        )

    def set_status(
        self,
        status: str,
        model: str = "qwen2.5",
    ) -> None:

        self.subtitle.setText(
            f"{status}   •   {model}"
        )