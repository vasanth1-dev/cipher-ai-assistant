from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)

from gui.theme import (
    SURFACE,
    BORDER,
    TEXT,
    TEXT_MUTED,
    CARD_RADIUS,
    CARD_PADDING,
)


class SystemCard(QFrame):

    def __init__(
        self,
        icon: str,
        title: str,
        value: str = "Loading...",
        parent: QFrame | None = None,
    ) -> None:
        super().__init__(parent)

        self.setStyleSheet(f"""
        QFrame {{
            background:{SURFACE};
            border:1px solid {BORDER};
            border-radius:{CARD_RADIUS}px;
        }}
        """)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
        )

        self.title = QLabel(f"{icon} {title}")

        self.title.setStyleSheet(f"""
            color:{TEXT};
            font-size:12pt;
            font-weight:600;
        """)

        self.value = QLabel(value)

        self.value.setStyleSheet(f"""
            color:{TEXT_MUTED};
            font-size:11pt;
        """)

        layout.addWidget(self.title)
        layout.addWidget(self.value)

    # -----------------------------------------

    def set_value(
        self, 
        value: str,
    ) -> None:

        self.value.setText(value)