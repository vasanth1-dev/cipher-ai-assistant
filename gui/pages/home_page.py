from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QGridLayout,
)

from gui.theme import (
    BACKGROUND,
    SURFACE,
    BORDER,
    PRIMARY,
    PRIMARY_HOVER,
    TEXT,
    TEXT_MUTED,
)


class HomePage(QWidget):

    def __init__(self):
        super().__init__()

        self._build_ui()

    def _build_ui(self):

        self.setStyleSheet(f"""
        QWidget {{
            background:{BACKGROUND};
            color:{TEXT};
        }}

        QFrame {{
            background:{SURFACE};
            border:1px solid {BORDER};
            border-radius:14px;
        }}

        QPushButton {{
            background:{PRIMARY};
            color:white;
            border:none;
            border-radius:10px;
            padding:12px;
            font-weight:bold;
        }}

        QPushButton:hover {{
            background:{PRIMARY_HOVER};
        }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(20)

        title = QLabel("Welcome to Cipher")
        title.setStyleSheet("""
        font-size:28px;
        font-weight:bold;
        """)

        subtitle = QLabel("Professional AI Assistant")
        subtitle.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:11pt;
        """)

        root.addWidget(title)
        root.addWidget(subtitle)

        grid = QGridLayout()
        grid.setSpacing(15)

        cards = [
            ("💬", "Chat"),
            ("🧠", "Memory"),
            ("⚙", "Settings"),
            ("🔌", "Plugins"),
            ("🖥", "System"),
            ("🎤", "Voice"),
        ]

        for index, (icon, text) in enumerate(cards):

            card = QFrame()

            layout = QVBoxLayout(card)

            icon_label = QLabel(icon)
            icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            icon_label.setStyleSheet("font-size:34px;")

            text_label = QLabel(text)
            text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            text_label.setStyleSheet("""
            font-size:13pt;
            font-weight:bold;
            """)

            layout.addStretch()
            layout.addWidget(icon_label)
            layout.addWidget(text_label)
            layout.addStretch()

            grid.addWidget(card, index // 3, index % 3)

        root.addLayout(grid)

        self.start_button = QPushButton("Start Chatting")

        root.addStretch()
        root.addWidget(self.start_button)