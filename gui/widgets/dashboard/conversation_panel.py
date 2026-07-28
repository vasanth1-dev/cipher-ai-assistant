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


class ConversationPanel(QFrame):
    """
    Dashboard recent conversations panel.
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

        title = QLabel("Recent Conversations")
        title.setStyleSheet(f"""
            color:{TEXT};
            font-size:20px;
            font-weight:800;
        """)

        subtitle = QLabel(
            "Continue your latest conversations"
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

    def set_conversations(
        self,
        conversations: list[str],
    ) -> None:

        self.list.clear()

        if not conversations:

            self.list.addItem(
                "No recent conversations"
            )

            return

        for conversation in conversations:

            self.list.addItem(
                f"💬  {conversation}"
            )

    def clear(
        self,
    ) -> None:

        self.list.clear()