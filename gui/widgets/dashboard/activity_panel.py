from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QListWidget,
    QVBoxLayout,
)

from gui.theme import (
    get_card_style,
    LIST_WIDGET_STYLE,
    TEXT,
    TEXT_MUTED,
)


class ActivityPanel(QFrame):
    """
    Dashboard recent activity panel.
    """

    def __init__(
        self, 
        parent: QFrame | None = None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("Card")
        self.setStyleSheet(get_card_style())

        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        title = QLabel("Recent Activity")

        title.setStyleSheet(f"""
            color:{TEXT};
            font-size:20px;
            font-weight:800;
        """)

        subtitle = QLabel(
            "Latest assistant events"
        )

        subtitle.setStyleSheet(f"""
            color:{TEXT_MUTED};
            font-size:11pt;
        """)

        self.list = QListWidget()

        self.list.setStyleSheet(LIST_WIDGET_STYLE)

        self.list.setSpacing(6)

        self.list.setAlternatingRowColors(False)

        self.list.setUniformItemSizes(True)

        layout.addWidget(title)
        layout.addWidget(subtitle)
        layout.addWidget(self.list)

    # -------------------------------------------------

    def add_activity(
        self,
        text: str,
    ) -> None:

        self.list.insertItem(
            0,
            f"✔  {text}",
        )

        while self.list.count() > 50:

            self.list.takeItem(
                self.list.count() - 1
            )

    def clear(
        self,
    ) -> None:

        self.list.clear()