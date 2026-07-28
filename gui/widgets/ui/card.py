from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
    QLayout,
)

from gui.theme import (
    get_card_style,
    CARD_PADDING,
    SPACING,
    TEXT,
    TEXT_MUTED,
    TITLE_SIZE,
    scale,
)


class Card(QFrame):
    """
    Reusable UI Card.

    Can be used for:
    - Dashboard
    - Memory
    - Files
    - Settings
    - System
    """

    def __init__(
        self,
        title: str = "",
        subtitle: str = "",
        parent: QFrame | None = None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("Card")
        self.setStyleSheet(get_card_style())

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(
            scale(CARD_PADDING),
            scale(CARD_PADDING),
            scale(CARD_PADDING),
            scale(CARD_PADDING),
        )
        self.layout.setSpacing(
            scale(SPACING)
        )

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(f"""
            color:{TEXT};
            font-size:{TITLE_SIZE}px;
            font-weight:600;
        """)

        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setStyleSheet(f"""
            color:{TEXT_MUTED};
            font-size:{scale(9)}pt;
            line-height:1.3;
        """)

        if title:
            self.layout.addWidget(self.title_label)

        if subtitle:
            self.layout.addWidget(self.subtitle_label)

        self.body = QVBoxLayout()
        self.body.setSpacing(
            scale(SPACING)
        )
        self.body.setContentsMargins(
            0, 
            scale(8), 
            0, 
            0
        )

        self.layout.addLayout(self.body)

    # -----------------------------

    def add_widget(
        self, 
        widget: QWidget,
    ) -> None:
        """
        Add a widget to the card body.
        """
        self.body.addWidget(widget)

    def add_layout(
        self, 
        layout: QLayout,
    ) -> None:
        """
        Add a layout to the card body.
        """
        self.body.addLayout(layout)

    def set_title(
        self, 
        text: str,
    ) -> None:
        self.title_label.setText(text)

    def set_subtitle(
        self, 
        text: str,
    ) -> None:
        self.subtitle_label.setText(text)