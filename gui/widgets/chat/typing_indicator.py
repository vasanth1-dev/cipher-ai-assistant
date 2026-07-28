from PyQt6.QtCore import (
    QTimer,
)
from PyQt6.QtWidgets import (
    QLabel,
    QWidget,
    QHBoxLayout,
)

from gui.theme import (
    TEXT_MUTED,
)


class TypingIndicator(QWidget):
    """
    Animated typing indicator.
    """

    def __init__(
        self, 
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.dots = 0

        self.label = QLabel("🤖 Cipher is thinking")

        self.label.setStyleSheet(f"""
            color: {TEXT_MUTED};
            font-size: 10pt;
            font-style: italic;
            font-weight: 500;
            padding: 4px 0px;
        """)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            12,
            4,
            12,
            4,
        )

        layout.setSpacing(8)

        layout.addWidget(self.label)
        layout.addStretch()

        self.timer = QTimer(self)

        self.timer.timeout.connect(
            self._animate
        )

        self.hide()

    # --------------------------------------------------

    def _animate(
        self,
    ) -> None:

        self.dots = (self.dots + 1) % 4

        self.label.setText(
            "🤖 Cipher is thinking" +
            "." * self.dots
        )

    # --------------------------------------------------

    def start(
        self,
    ) -> None:

        if self.timer.isActive():
            return

        self.dots = 0

        self.label.setText(
            "🤖 Cipher is thinking"
        )

        self.show()

        self.timer.start(400)

    # --------------------------------------------------

    def stop(
        self,
    ) -> None:

        if self.timer.isActive():
            self.timer.stop()

        self.hide()