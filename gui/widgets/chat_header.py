from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QFont, QPainter
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class StatusDot(QWidget):
    """
    Small colored status indicator.
    """

    def __init__(self, color: str = "#22C55E", diameter: int = 10, parent=None):
        super().__init__(parent)

        self._color = QColor(color)
        self._diameter = diameter

        self.setFixedSize(diameter, diameter)

    def setColor(self, color: str):
        self._color = QColor(color)
        self.update()

    def paintEvent(self, event):
        del event

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setBrush(self._color)
        painter.setPen(Qt.PenStyle.NoPen)

        painter.drawEllipse(
            0,
            0,
            self._diameter,
            self._diameter,
        )


class Avatar(QWidget):
    """
    Simple circular avatar displaying the first letter.
    """

    def __init__(self, letter="C", parent=None):
        super().__init__(parent)

        self.letter = letter.upper()

        self.setFixedSize(42, 42)

    def paintEvent(self, event):
        del event

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#3B82F6"))

        painter.drawEllipse(self.rect())

        painter.setPen(QColor("white"))

        font = painter.font()
        font.setBold(True)
        font.setPointSize(15)

        painter.setFont(font)

        painter.drawText(
            self.rect(),
            Qt.AlignmentFlag.AlignCenter,
            self.letter,
        )


class ChatHeader(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("chatHeader")

        self.setStyleSheet(
            """
            QFrame#chatHeader{
                background:#202124;
                border:1px solid #34363A;
                border-radius:14px;
            }

            QLabel{
                color:white;
                background:transparent;
            }

            QLabel#title{
                font-size:16px;
                font-weight:700;
            }

            QLabel#subtitle{
                color:#A8ADB4;
                font-size:12px;
            }

            QLabel#model{
                color:#60A5FA;
                font-size:12px;
                font-weight:600;
                padding:4px 10px;
                border:1px solid #355D96;
                border-radius:8px;
                background:#1B2737;
            }
            """
        )

        self.avatar = Avatar("C")

        self.title = QLabel("Cipher")
        self.title.setObjectName("title")

        self.subtitle = QLabel("Ready")
        self.subtitle.setObjectName("subtitle")

        self.status_dot = StatusDot("#22C55E")

        self.model = QLabel("Model: Unknown")
        self.model.setObjectName("model")

        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)
        title_layout.setContentsMargins(0, 0, 0, 0)

        status_row = QHBoxLayout()
        status_row.setSpacing(6)
        status_row.setContentsMargins(0, 0, 0, 0)

        status_row.addWidget(self.status_dot)
        status_row.addWidget(self.subtitle)
        status_row.addStretch()

        title_layout.addWidget(self.title)
        title_layout.addLayout(status_row)

        self.right_container = QWidget()
        self.right_layout = QHBoxLayout(self.right_container)

        self.right_layout.setContentsMargins(0, 0, 0, 0)
        self.right_layout.setSpacing(8)

        root = QHBoxLayout(self)

        root.setContentsMargins(16, 12, 16, 12)
        root.setSpacing(12)

        root.addWidget(self.avatar)
        root.addLayout(title_layout)

        root.addStretch()

        root.addWidget(self.model)
        root.addWidget(self.right_container)

        self.right_container.setSizePolicy(
            QSizePolicy.Policy.Maximum,
            QSizePolicy.Policy.Preferred,
        )

    # ---------------------------------------------------------

    def setAssistantName(self, name: str):
        self.title.setText(name)

        if name:
            self.avatar.letter = name[0].upper()
            self.avatar.update()

    def setStatus(self, text: str, color: str = "#22C55E"):
        self.subtitle.setText(text)
        self.status_dot.setColor(color)

    def setModel(self, model: str):
        self.model.setText(f"Model: {model}")

    def addRightWidget(self, widget):
        self.right_layout.addWidget(widget)