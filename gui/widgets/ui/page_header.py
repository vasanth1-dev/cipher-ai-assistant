from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
)

from gui.theme import (
    TEXT,
    TEXT_MUTED,
    SPACING,
)


class PageHeader(QFrame):
    """
    Reusable page header.

    Example:
        Dashboard
        Manage your AI assistant
    """

    def __init__(
        self,
        title: str = "",
        subtitle: str = "",
        parent: QFrame | None = None,
    ) -> None:
        super().__init__(parent)

        self.setFrameShape(QFrame.Shape.NoFrame)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(SPACING)

        self.title = QLabel(title)
        self.title.setStyleSheet(f"""
            color:{TEXT};
            font-size:24px;
            font-weight:700;
        """)

        self.subtitle = QLabel(subtitle)
        self.subtitle.setStyleSheet(f"""
            color:{TEXT_MUTED};
            font-size:11pt;
        """)

        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)

    # ---------------------------------

    def set_title(
        self,
        text: str,
    ) -> None:
        self.title.setText(text)

    def set_subtitle(
        self,
        text: str,
    ) -> None:
        self.subtitle.setText(text)

    def title_text(self) -> str:
        return self.title.text()

    def subtitle_text(self) -> str:
        return self.subtitle.text()