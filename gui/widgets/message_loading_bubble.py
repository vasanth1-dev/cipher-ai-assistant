from __future__ import annotations

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
)


class MessageLoadingBubble(QFrame):
    """
    Animated assistant loading bubble.

    Used while the LLM is generating a response.
    """

    _FRAMES = (
        "Thinking",
        "Thinking.",
        "Thinking..",
        "Thinking...",
    )

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("messageLoadingBubble")

        self.setSizePolicy(
            QSizePolicy.Policy.Maximum,
            QSizePolicy.Policy.Fixed,
        )

        self.setStyleSheet(
            """
            QFrame#messageLoadingBubble{
                background:#202124;
                border:1px solid #34363A;
                border-radius:16px;
            }

            QLabel{
                color:white;
                background:transparent;
            }
            """
        )

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 12, 16, 12)
        layout.setSpacing(8)

        self.icon = QLabel("🤖")

        icon_font = QFont()
        icon_font.setPointSize(14)
        self.icon.setFont(icon_font)

        self.label = QLabel(self._FRAMES[0])

        text_font = QFont()
        text_font.setPointSize(11)
        self.label.setFont(text_font)

        layout.addWidget(self.icon)
        layout.addWidget(self.label)

        self._frame = 0

        self._timer = QTimer(self)
        self._timer.setInterval(450)
        self._timer.timeout.connect(self._next_frame)

    # ---------------------------------------------------------

    def start(self):
        self._frame = 0
        self.label.setText(self._FRAMES[self._frame])
        self.show()
        self._timer.start()

    def stop(self):
        self._timer.stop()
        self.hide()

    # ---------------------------------------------------------

    def _next_frame(self):
        self._frame += 1
        self._frame %= len(self._FRAMES)

        self.label.setText(self._FRAMES[self._frame])

    # ---------------------------------------------------------

    def isRunning(self) -> bool:
        return self._timer.isActive()