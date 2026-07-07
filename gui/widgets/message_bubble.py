from html import escape

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
)


class MessageBubble(QFrame):

    def __init__(self, sender: str, message: str):
        super().__init__()

        self.sender = sender
        self.message = message

        self._build_ui()

    # --------------------------------------------------

    def _build_ui(self):

        self.setObjectName("MessageBubble")

        self.setStyleSheet("""
        QFrame#MessageBubble{
            border-radius:14px;
            background:#334155;
        }

        QLabel{
            color:white;
            background:transparent;
        }

        QPushButton{
            background:#1E293B;
            color:white;
            border:none;
            border-radius:8px;
            padding:4px 10px;
        }

        QPushButton:hover{
            background:#2563EB;
        }
        """)

        if self.sender.lower() == "you":
            background = "#2563EB"
        elif self.sender.lower() == "system":
            background = "#14532D"
        else:
            background = "#334155"

        self.setStyleSheet(f"""
        QFrame#MessageBubble{{
            background:{background};
            border-radius:14px;
        }}

        QLabel{{
            color:white;
            background:transparent;
        }}

        QPushButton{{
            background:#1E293B;
            color:white;
            border:none;
            border-radius:8px;
            padding:4px 10px;
        }}

        QPushButton:hover{{
            background:#2563EB;
        }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(14, 12, 14, 12)
        root.setSpacing(8)

        header = QHBoxLayout()

        self.sender_label = QLabel(self.sender)
        self.sender_label.setStyleSheet("""
        font-size:11pt;
        font-weight:bold;
        """)

        header.addWidget(self.sender_label)
        header.addStretch()

        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.copy_message)

        header.addWidget(self.copy_button)

        root.addLayout(header)

        self.message_label = QLabel()

        self.message_label.setWordWrap(True)
        self.message_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.message_label.setText(
            escape(self.message).replace("\n", "<br>")
        )

        root.addWidget(self.message_label)

    # --------------------------------------------------

    def set_message(self, text: str):

        self.message = text

        self.message_label.setText(
            escape(text).replace("\n", "<br>")
        )

    # --------------------------------------------------

    def append_text(self, text: str):

        self.message += text

        self.set_message(self.message)

    # --------------------------------------------------

    def copy_message(self):

        from PyQt6.QtWidgets import QApplication

        QApplication.clipboard().setText(self.message)