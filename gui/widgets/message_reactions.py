from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QPushButton,
)


class ReactionButton(QPushButton):
    """
    Small reaction button used for assistant responses.
    """

    def __init__(self, icon: str, tooltip: str, parent=None):
        super().__init__(icon, parent)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip(tooltip)

        self.setCheckable(True)
        self.setFixedSize(30, 30)

        self.setStyleSheet(
            """
            QPushButton{
                background:transparent;
                border:none;
                border-radius:15px;
                font-size:14px;
                color:#B8BDC7;
            }

            QPushButton:hover{
                background:#2B2D31;
                color:white;
            }

            QPushButton:checked{
                background:#3B82F6;
                color:white;
            }
            """
        )


class MessageReactions(QFrame):
    """
    Reusable reaction widget.

    Only emits signals. It does not store ratings or
    perform any business logic.
    """

    thumbsUpClicked = pyqtSignal()
    thumbsDownClicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("messageReactions")

        self.setStyleSheet(
            """
            QFrame#messageReactions{
                background:transparent;
                border:none;
            }
            """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 4, 0, 0)
        layout.setSpacing(4)

        self.up_button = ReactionButton(
            "👍",
            "Helpful",
        )

        self.down_button = ReactionButton(
            "👎",
            "Not Helpful",
        )

        layout.addWidget(self.up_button)
        layout.addWidget(self.down_button)
        layout.addStretch()

        self.up_button.clicked.connect(self._thumbs_up)
        self.down_button.clicked.connect(self._thumbs_down)

    # ---------------------------------------------------------

    def _thumbs_up(self):
        if self.up_button.isChecked():
            self.down_button.setChecked(False)

        self.thumbsUpClicked.emit()

    def _thumbs_down(self):
        if self.down_button.isChecked():
            self.up_button.setChecked(False)

        self.thumbsDownClicked.emit()

    # ---------------------------------------------------------

    def clearSelection(self):
        self.up_button.setChecked(False)
        self.down_button.setChecked(False)

    def setEnabledButtons(self, enabled: bool):
        self.up_button.setEnabled(enabled)
        self.down_button.setEnabled(enabled)