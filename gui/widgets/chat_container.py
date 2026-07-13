from PyQt6.QtCore import (
    Qt,
    QTimer,
)
from PyQt6.QtWidgets import (
    QLabel,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from gui.widgets.message_bubble import MessageBubble


class ChatContainer(QScrollArea):
    """
    Cipher Chat Container

    Responsibilities
    ----------------
    • Store chat bubbles
    • Manage streaming
    • Manage typing indicator
    • Auto scroll
    """

    def __init__(self):
        super().__init__()

        self._last_bubble = None
        self._typing_label = None

        self._build_ui()

    # --------------------------------------------------
    # UI
    # --------------------------------------------------

    def _build_ui(self):

        self.setWidgetResizable(True)

        self.setFrameShape(
            QScrollArea.Shape.NoFrame
        )

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.container = QWidget()

        self.layout = QVBoxLayout(
            self.container
        )

        self.layout.setContentsMargins(
            12,
            12,
            12,
            90,
        )

        self.layout.setSpacing(18)

        self.layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        self.layout.addStretch()

        self.setWidget(
            self.container
        )

    # --------------------------------------------------
    # Messages
    # --------------------------------------------------

    def add_message(
        self,
        sender: str,
        message: str,
    ):

        self.hide_typing_indicator()

        bubble = MessageBubble(
            sender,
            message,
        )

        self.layout.insertWidget(
            self.layout.count() - 1,
            bubble,
        )

        self._last_bubble = bubble

        self.scroll_to_bottom()

        return bubble

    # --------------------------------------------------

    def append_to_last_message(
        self,
        text: str,
    ):

        if self._last_bubble is None:
            return

        self._last_bubble.append_text(
            text,
        )

        self.scroll_to_bottom()

    # --------------------------------------------------
    # Typing Indicator
    # --------------------------------------------------

    def show_typing_indicator(self):

        if self._typing_label is not None:
            return

        self._typing_label = QLabel(
            "Cipher is thinking..."
        )

        self._typing_label.setStyleSheet("""
        QLabel{
            color:#9CA3AF;
            font-size:10pt;
            padding:8px 12px;
        }
        """)

        self.layout.insertWidget(
            self.layout.count() - 1,
            self._typing_label,
        )

        self.scroll_to_bottom()

    # --------------------------------------------------

    def hide_typing_indicator(self):

        if self._typing_label is None:
            return

        self.layout.removeWidget(
            self._typing_label
        )

        self._typing_label.deleteLater()

        self._typing_label = None

    # --------------------------------------------------
    # Clear
    # --------------------------------------------------

    def clear_messages(self):

        self.hide_typing_indicator()

        while self.layout.count() > 1:

            item = self.layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        self._last_bubble = None

    # --------------------------------------------------
    # Scroll
    # --------------------------------------------------

    def scroll_to_bottom(self):

        QTimer.singleShot(

            0,

            lambda:
            self.verticalScrollBar().setValue(

                self.verticalScrollBar().maximum()

            ),

        )