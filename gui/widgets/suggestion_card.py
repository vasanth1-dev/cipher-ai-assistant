from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)

from gui.theme import (
    SURFACE,
    PRIMARY_HOVER,
    TEXT,
    TEXT_MUTED,
    CARD_PADDING,
    RADIUS_LARGE,
    TEXT_SIZE,
    SMALL_SIZE,
)


class SuggestionCard(QFrame):

    clicked = pyqtSignal(str)

    def __init__(
        self,
        icon: str,
        title: str,
        prompt: str,
    ):
        super().__init__()

        self.prompt = prompt

        self.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.setStyleSheet(f"""
        QFrame{{
            background:{SURFACE};
            border-radius:{RADIUS_LARGE}px;
        }}

        QFrame:hover{{
            background:{PRIMARY_HOVER};
        }}

        QLabel{{
            background:transparent;
            color:{TEXT};
        }}
        """)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
        )

        layout.setSpacing(8)

        self.icon_label = QLabel(icon)

        self.icon_label.setStyleSheet(f"""
        font-size:22px;
        """)

        self.title_label = QLabel(title)

        self.title_label.setStyleSheet(f"""
        font-size:{TEXT_SIZE}pt;
        font-weight:bold;
        color:{TEXT};
        """)

        self.subtitle_label = QLabel(prompt)

        self.subtitle_label.setWordWrap(True)

        self.subtitle_label.setStyleSheet(f"""
        font-size:{SMALL_SIZE}pt;
        color:{TEXT_MUTED};
        """)

        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.subtitle_label)

    def mousePressEvent(self, event):

        self.clicked.emit(self.prompt)

        super().mousePressEvent(event)