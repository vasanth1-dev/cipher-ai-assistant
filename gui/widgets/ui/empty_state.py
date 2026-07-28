from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from gui.theme import (
    get_button_style,
    TEXT,
    TEXT_MUTED,
    SPACING,
)


class EmptyState(QWidget):
    """
    Reusable empty state widget.

    Examples:
        • No conversations
        • No memories
        • No files
        • No reminders
        • No plugins
    """

    def __init__(
        self,
        icon: str = "📄",
        title: str = "Nothing here",
        message: str = "",
        button_text: str = "",
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(SPACING)

        self.icon_label = QLabel(icon)
        self.icon_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.icon_label.setStyleSheet("""
            font-size:48px;
        """)

        self.title_label = QLabel(title)
        self.title_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.title_label.setStyleSheet(f"""
            color:{TEXT};
            font-size:18px;
            font-weight:700;
        """)

        self.message_label = QLabel(message)
        self.message_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )
        self.message_label.setWordWrap(True)
        self.message_label.setStyleSheet(f"""
            color:{TEXT_MUTED};
            font-size:10pt;
        """)

        self.button = QPushButton(button_text)
        self.button.setStyleSheet(get_button_style())

        if not button_text:
            self.button.hide()

        layout.addStretch()
        layout.addWidget(self.icon_label)
        layout.addWidget(self.title_label)
        layout.addWidget(self.message_label)
        layout.addWidget(
            self.button,
            alignment=Qt.AlignmentFlag.AlignCenter,
        )
        layout.addStretch()

    # -------------------------------------------------

    def set_icon(self, icon: str) -> None:
        self.icon_label.setText(icon)

    def set_title(self, title: str) -> None:
        self.title_label.setText(title)

    def set_message(self, message: str) -> None:
        self.message_label.setText(message)

    def set_button_text(self, text: str) -> None:
        self.button.setText(text)

        if text:
            self.button.show()
        else:
            self.button.hide()

    # -------------------------------------------------

    def button_widget(self) -> QPushButton:
        return self.button