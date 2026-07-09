from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)


class ChatEmptyState(QFrame):
    """
    Welcome screen shown before the first message.
    Hidden automatically once the first chat message appears.
    """

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("chatEmptyState")

        self.setStyleSheet(
            """
            QFrame#chatEmptyState{
                background:transparent;
                border:none;
            }

            QLabel{
                color:white;
                background:transparent;
            }

            QLabel#title{
                font-size:30px;
                font-weight:700;
            }

            QLabel#subtitle{
                color:#A8ADB4;
                font-size:15px;
            }

            QLabel#hint{
                color:#7E848D;
                font-size:13px;
            }

            QFrame#card{
                background:#202124;
                border:1px solid #34363B;
                border-radius:18px;
            }
            """
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(40, 40, 40, 40)
        root.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 36, 40, 36)
        card_layout.setSpacing(16)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        icon = QLabel("🧠")
        icon_font = QFont()
        icon_font.setPointSize(42)
        icon.setFont(icon_font)
        icon.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Welcome to Cipher")
        title.setObjectName("title")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        subtitle = QLabel(
            "Your professional desktop AI assistant."
        )
        subtitle.setObjectName("subtitle")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

        hint = QLabel(
            "Ask anything, generate code, summarize documents,\n"
            "or control your computer using natural language."
        )
        hint.setObjectName("hint")
        hint.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hint.setWordWrap(True)

        examples = QLabel(
            "Try:\n\n"
            "• Explain Python decorators\n"
            "• Write a Flask API\n"
            "• Summarize this article\n"
            "• Create a SQL query\n"
            "• Help debug my code"
        )
        examples.setAlignment(Qt.AlignmentFlag.AlignLeft)

        examples.setStyleSheet(
            """
            QLabel{
                color:#D8D8D8;
                background:#292B30;
                border-radius:12px;
                padding:16px;
                font-size:13px;
            }
            """
        )

        card_layout.addWidget(icon)
        card_layout.addWidget(title)
        card_layout.addWidget(subtitle)
        card_layout.addSpacing(10)
        card_layout.addWidget(hint)
        card_layout.addSpacing(12)
        card_layout.addWidget(examples)

        root.addWidget(card)

    # --------------------------------------------------

    def show_state(self):
        self.show()

    def hide_state(self):
        self.hide()