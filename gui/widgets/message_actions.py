from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QPushButton,
)


class ActionButton(QPushButton):
    """
    Small icon/text button used below or beside a message bubble.
    """

    def __init__(
        self,
        text: str,
        tooltip: str,
        parent=None,
    ):
        super().__init__(text, parent)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(tooltip)

        self.setFixedHeight(28)
        self.setMinimumWidth(36)

        self.setStyleSheet(
            """
            QPushButton{
                background:transparent;
                color:#B8BDC7;
                border:none;
                border-radius:8px;
                padding:4px 8px;
                font-size:12px;
            }

            QPushButton:hover{
                background:#2B2D31;
                color:white;
            }

            QPushButton:pressed{
                background:#35383D;
            }
            """
        )


class MessageActions(QFrame):
    """
    Reusable action bar shown for assistant messages.

    This widget only emits signals.
    Business logic stays outside.
    """

    copyRequested = pyqtSignal()
    regenerateRequested = pyqtSignal()
    retryRequested = pyqtSignal()
    deleteRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("messageActions")

        self.setStyleSheet(
            """
            QFrame#messageActions{
                background:transparent;
                border:none;
            }
            """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 0)
        layout.setSpacing(4)

        self.copy_button = ActionButton(
            "⧉",
            "Copy",
        )

        self.regenerate_button = ActionButton(
            "↻",
            "Regenerate",
        )

        self.retry_button = ActionButton(
            "⟳",
            "Retry",
        )

        self.delete_button = ActionButton(
            "🗑",
            "Delete",
        )

        layout.addWidget(self.copy_button)
        layout.addWidget(self.regenerate_button)
        layout.addWidget(self.retry_button)
        layout.addWidget(self.delete_button)
        layout.addStretch()

        self.copy_button.clicked.connect(
            self.copyRequested.emit
        )

        self.regenerate_button.clicked.connect(
            self.regenerateRequested.emit
        )

        self.retry_button.clicked.connect(
            self.retryRequested.emit
        )

        self.delete_button.clicked.connect(
            self.deleteRequested.emit
        )

    # ---------------------------------------------------------

    def showRetry(self, visible: bool):
        self.retry_button.setVisible(visible)

    def showRegenerate(self, visible: bool):
        self.regenerate_button.setVisible(visible)

    def showDelete(self, visible: bool):
        self.delete_button.setVisible(visible)

    def showCopy(self, visible: bool):
        self.copy_button.setVisible(visible)