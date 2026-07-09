from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)


class MessageErrorBubble(QFrame):
    """
    Error bubble displayed when an assistant response fails.

    This widget is presentation-only. It emits a retry signal
    but performs no retry logic itself.
    """

    retryRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("messageErrorBubble")

        self.setSizePolicy(
            QSizePolicy.Policy.Maximum,
            QSizePolicy.Policy.Fixed,
        )

        self.setStyleSheet(
            """
            QFrame#messageErrorBubble{
                background:#2B1E1E;
                border:1px solid #C24141;
                border-radius:16px;
            }

            QLabel#icon{
                font-size:18px;
                background:transparent;
            }

            QLabel#title{
                color:white;
                font-size:13px;
                font-weight:700;
                background:transparent;
            }

            QLabel#message{
                color:#E5E7EB;
                font-size:12px;
                background:transparent;
            }

            QPushButton{
                background:#C24141;
                color:white;
                border:none;
                border-radius:8px;
                padding:6px 14px;
                font-size:12px;
                font-weight:600;
            }

            QPushButton:hover{
                background:#DC4C4C;
            }

            QPushButton:pressed{
                background:#A83232;
            }
            """
        )

        root = QHBoxLayout(self)
        root.setContentsMargins(14, 12, 14, 12)
        root.setSpacing(12)

        self.icon = QLabel("⚠")
        self.icon.setObjectName("icon")
        self.icon.setAlignment(Qt.AlignmentFlag.AlignTop)

        content = QVBoxLayout()
        content.setSpacing(6)

        self.title = QLabel("Something went wrong")
        self.title.setObjectName("title")

        self.message = QLabel(
            "The assistant couldn't generate a response."
        )
        self.message.setObjectName("message")
        self.message.setWordWrap(True)

        self.retry_button = QPushButton("Retry")
        self.retry_button.clicked.connect(self.retryRequested.emit)

        content.addWidget(self.title)
        content.addWidget(self.message)
        content.addWidget(
            self.retry_button,
            alignment=Qt.AlignmentFlag.AlignLeft,
        )

        root.addWidget(self.icon)
        root.addLayout(content)

    # ---------------------------------------------------------

    def setTitle(self, text: str):
        self.title.setText(text)

    def setMessage(self, text: str):
        self.message.setText(text)

    def setRetryVisible(self, visible: bool):
        self.retry_button.setVisible(visible)