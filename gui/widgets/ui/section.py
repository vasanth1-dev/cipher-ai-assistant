from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
    QLayout,
)

from gui.theme import (
    SPACING,
    TEXT,
    TEXT_MUTED,
)


class Section(QWidget):
    """
    Reusable dashboard/page section.

    Example:

        Quick Actions
        Open applications quickly.

        [content]
    """

    def __init__(
        self,
        title: str,
        subtitle: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(SPACING)

        self.title_label = QLabel(title)
        self.title_label.setStyleSheet(f"""
            color:{TEXT};
            font-size:16px;
            font-weight:700;
        """)

        self.subtitle_label = QLabel(subtitle)
        self.subtitle_label.setStyleSheet(f"""
            color:{TEXT_MUTED};
            font-size:10pt;
        """)

        self.layout.addWidget(self.title_label)

        if subtitle:
            self.layout.addWidget(self.subtitle_label)

    # --------------------------------------------------

    def add_widget(
        self, 
        widget: QWidget,
    ) -> None:
        self.layout.addWidget(widget)

    def add_layout(
        self, 
        layout: QLayout,
    ) -> None:
        self.layout.addLayout(layout)

    # --------------------------------------------------

    def set_title(self, text: str) -> None:
        self.title_label.setText(text)

    def set_subtitle(self, text: str) -> None:

        self.subtitle_label.setText(text)

        if text:
            self.subtitle_label.show()
        else:
            self.subtitle_label.hide()