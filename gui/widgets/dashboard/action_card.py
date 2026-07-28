from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)
from PyQt6.QtGui import QMouseEvent
from gui.theme import (
    SURFACE,
    SURFACE_LIGHT,
    BORDER,
    PRIMARY,
    TEXT,
    TEXT_MUTED,
    CARD_RADIUS,
    CARD_PADDING,
    CLICK_CURSOR,
)


class ActionCard(QFrame):
    """
    Reusable Dashboard Action Card.

    Example
    -------
        💬
        Chat
    """

    clicked = pyqtSignal()

    def __init__(
        self,
        icon: str,
        title: str,
        parent: QFrame | None = None,
    ) -> None:
        super().__init__(parent)

        self.setCursor(
            getattr(
                Qt.CursorShape,
                CLICK_CURSOR,
            )
        )

        self.setObjectName("ActionCard")

        self.setStyleSheet(f"""
        QFrame#ActionCard {{
            background:{SURFACE};
            border:1px solid {BORDER};
            border-radius:{CARD_RADIUS}px;
        }}

        QFrame#ActionCard:hover {{
            background:{SURFACE_LIGHT};
            border:2px solid {PRIMARY};
        }}
        """)

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
        )

        self.layout.setSpacing(14)

        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.icon = QLabel(icon)

        self.icon.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.icon.setStyleSheet(f"""
            color:{TEXT};
            font-size:38px;
            font-weight:700;
        """)

        self.title = QLabel(title)

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.title.setStyleSheet(f"""
            color:{TEXT_MUTED};
            font-size:11pt;
            font-weight:700;
        """)

        self.layout.addWidget(self.icon)

        self.layout.addWidget(self.title)

        self.setMinimumSize(
            145,
            130,
        )

    # -------------------------------------------------

    def mousePressEvent(
        self,
        event: QMouseEvent,
    ) -> None:

        self.clicked.emit()

        super().mousePressEvent(event)

    def mouseReleaseEvent(
        self, 
        event: QMouseEvent,
    ) -> None:

        super().mouseReleaseEvent(event)