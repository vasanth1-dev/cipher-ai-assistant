from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QLabel


class ChatStatusBadge(QLabel):
    """
    Small rounded status badge.

    Examples:
        Ready
        Listening
        Thinking
        Generating
        Offline
        Error
    """

    STATUS_COLORS = {
        "ready": ("#16A34A", "#DCFCE7", "#14532D"),
        "listening": ("#2563EB", "#DBEAFE", "#1E3A8A"),
        "thinking": ("#D97706", "#FEF3C7", "#78350F"),
        "generating": ("#7C3AED", "#EDE9FE", "#4C1D95"),
        "offline": ("#6B7280", "#E5E7EB", "#374151"),
        "error": ("#DC2626", "#FEE2E2", "#7F1D1D"),
    }

    def __init__(self, status: str = "ready", parent=None):
        super().__init__(parent)

        self.setMinimumHeight(28)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._status = ""
        self.setStatus(status)

    # ------------------------------------------------------------------

    def status(self) -> str:
        return self._status

    # ------------------------------------------------------------------

    def setStatus(self, status: str):
        status = status.lower().strip()

        if status not in self.STATUS_COLORS:
            status = "ready"

        self._status = status

        border, background, text = self.STATUS_COLORS[status]

        self.setText(status.capitalize())

        self.setStyleSheet(
            f"""
            QLabel {{
                background:{background};
                color:{text};
                border:1px solid {border};
                border-radius:14px;
                padding-left:12px;
                padding-right:12px;
                font-size:12px;
                font-weight:600;
            }}
            """
        )