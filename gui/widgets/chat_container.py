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

from gui.theme import (
    SPACING,
    SPACING_SMALL,
    CARD_PADDING,
)
from gui.widgets.chat.message_bubble import MessageBubble


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

    def __init__(
       self,
       parent: QWidget | None = None,
    ) -> None:
        
        super().__init__(parent)

        self._scroll_timer = QTimer(self)

        self._scroll_timer.setSingleShot(True)

        self._scroll_timer.timeout.connect(
            self._perform_scroll
        )

        self._last_bubble = None
        self._typing_label = None

        self._build_ui()

    # --------------------------------------------------
    # UI
    # --------------------------------------------------

    def _build_ui(
        self,
    ) -> None:

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
            SPACING,
            SPACING,
            SPACING,
            90,
        )

        self.layout.setSpacing(
            CARD_PADDING
        )

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
    ) -> MessageBubble:
        
        sender = str(sender).strip()
        message = str(message)

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

        return bubble

    # --------------------------------------------------

    def append_to_last_message(
        self,
        text: str,
    ) -> None:
        
        text = str(text)

        if not text:
            return

        if self._last_bubble is None:
            return

        self._last_bubble.append_text(
            text,
        )

    # --------------------------------------------------
    # Typing Indicator
    # --------------------------------------------------

    def show_typing_indicator(
        self,
    ) -> None:

        if self._typing_label is not None:
            return

        self._typing_label = QLabel(
            "Cipher is thinking..."
        )

        self._typing_label.setStyleSheet(f"""
        QLabel{{
            color:#9CA3AF;
            font-size:10pt;
            padding:{SPACING_SMALL}px {SPACING}px;
        }}
        """)

        self.layout.insertWidget(
            self.layout.count() - 1,
            self._typing_label,
        )

        self.scroll_to_bottom()

    # --------------------------------------------------

    def hide_typing_indicator(
        self,
    ) -> None:

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

    def clear_messages(
        self,
    ) -> None:

        self.hide_typing_indicator()

        while self.layout.count():

            item = self.layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        self.layout.addStretch()

        self._last_bubble = None

    # --------------------------------------------------
    # Scroll
    # --------------------------------------------------

    def scroll_to_bottom(
        self,
    ) -> None:

        self._scroll_timer.start(0)

    def _perform_scroll(
        self,
    ) -> None:

        bar = self.verticalScrollBar()

        bar.setValue(
            bar.maximum()
        )