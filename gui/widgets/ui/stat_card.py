from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel

from gui.theme import (
    TEXT,
    TEXT_MUTED,
    scale,
)

from gui.widgets.ui.card import Card


class StatCard(Card):
    """
    Reusable statistic card.

    Example:
        🤖
        AI Model
        qwen2.5
        Offline Language Model
    """

    def __init__(
        self,
        icon: str = "📊",
        title: str = "",
        value: str = "",
        description: str = "",
        parent : Card | None = None,
    ) -> None:
        super().__init__(parent=parent)

        self.setFixedHeight(
            scale(170)
        )
        self.setMaximumHeight(
            scale(190)
        )

        self.icon_label = QLabel(icon)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.icon_label.setStyleSheet(f"""
            font-size:{scale(30)}px;
            color:{TEXT};
        """)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(f"""
            color:{TEXT_MUTED};
            font-size:{scale(11)}pt;
            font-weight:600;
        """)

        self.value_label = QLabel(value)
        self.value_label.setStyleSheet(f"""
            color:{TEXT};
            font-size:{scale(22)}px;
            font-weight:800;
        """)

        self.description_label = QLabel(description)
        self.description_label.setWordWrap(True)
        self.description_label.setStyleSheet(f"""
            color:{TEXT_MUTED};
            font-size:{scale(10)}pt;
            line-height:1.4;
        """)

        self.add_widget(self.icon_label)
        self.add_widget(self.title_label)
        self.add_widget(self.value_label)
        self.add_widget(self.description_label)

    # -------------------------------------------------

    def set_icon(self, icon: str) -> None:
        self.icon_label.setText(icon)

    def set_title(self, title: str) -> None:
        self.title_label.setText(title)

    def set_value(self, value: str) -> None:
        self.value_label.setText(value)

    def set_description(self, description: str) -> None:
        self.description_label.setText(description)

    # -------------------------------------------------

    def icon(self) -> str:
        return self.icon_label.text()

    def title(self) -> str:
        return self.title_label.text()

    def value(self) -> str:
        return self.value_label.text()

    def description(self) -> str:
        return self.description_label.text()