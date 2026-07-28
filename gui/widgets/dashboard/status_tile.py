from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)

from gui.theme import (
    SURFACE,
    SURFACE_LIGHT,
    BORDER,
    PRIMARY,
    TEXT,
    TEXT_MUTED,
    CARD_RADIUS,
    CARD_PADDING,
)


class StatusTile(QFrame):
    """
    Reusable dashboard status tile.

    Example
    -------
        🤖
        AI Model
        qwen2.5
    """

    def __init__(
        self,
        icon: str,
        title: str,
        value: str = "--",
        parent: QFrame | None = None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("StatusTile")

        self.setStyleSheet(f"""
        QFrame#StatusTile {{
            background:{SURFACE};
            border:1px solid {BORDER};
            border-radius:{CARD_RADIUS}px;
        }}

        QFrame#StatusTile:hover {{
            background:{SURFACE_LIGHT};
            border:2px solid {PRIMARY};
        }}
        """)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
        )

        layout.setSpacing(12)

        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.setMinimumHeight(155)

        self.icon = QLabel(icon)

        self.icon.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.icon.setStyleSheet(f"""
            color:{TEXT};
            font-size:34px;
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

        self.value = QLabel(value)

        self.value.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.value.setStyleSheet(f"""
            color:{PRIMARY};
            font-size:20px;
            font-weight:800;
        """)

        layout.addWidget(self.icon)
        layout.addWidget(self.title)
        layout.addWidget(self.value)

    # -------------------------------------------------

    def set_value(
        self, value: str,
    ) -> None:

        self.value.setText(value)

    def set_title(
        self, 
        title: str,
    ) -> None:

        self.title.setText(title)

    def set_icon(
        self, 
        icon: str,
    ) -> None:

        self.icon.setText(icon)