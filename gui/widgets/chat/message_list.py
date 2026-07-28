from PyQt6.QtCore import (
    Qt,
    QTimer
)
from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import (
    QScrollArea,
    QVBoxLayout,
    QWidget,
    QPushButton,
)


from gui.widgets.chat.message_bubble import MessageBubble


class MessageList(QScrollArea):
    """
    Scrollable chat message container.
    """

    def __init__(
        self, 
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setWidgetResizable(True)
        self.setFrameShape(self.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.container = QWidget()

        self.message_layout = QVBoxLayout(self.container)

        self.message_layout.setContentsMargins(
            16,
            16,
            16,
            120,
        )

        self.message_layout.setSpacing(12)

        self.message_layout.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        self.setWidget(self.container)

        self.scroll_bottom_button = QPushButton("⬇")

        self.scroll_bottom_button.setParent(
            self.viewport()
        )

        self.scroll_bottom_button.setFixedSize(42, 42)

        self.scroll_bottom_button.hide()

        self.scroll_bottom_button.clicked.connect(
            self.scroll_to_bottom
        )

        self._auto_scroll = True

        self.verticalScrollBar().valueChanged.connect(
            self._on_scroll_changed
        )

    # -------------------------------------------------

    def add_user_message(
        self,
        text: str,
    ) -> MessageBubble:

        bubble = MessageBubble(
            text=text,
            is_user=True,
        )

        bubble.deleted.connect(
            self.remove_message
        )

        bubble.edited.connect(
            self.on_message_edited
        )

        self.message_layout.addWidget(bubble)

        self._scroll_bottom()

        return bubble

    # -------------------------------------------------

    def add_assistant_message(
        self,
        text: str,
    ) -> MessageBubble:

        if (
            hasattr(self, "_stream_bubble")
            and self._stream_bubble is not None
        ):

            self._stream_bubble.set_message(text)

            bubble = self._stream_bubble

            del self._stream_bubble

            self._scroll_bottom()

            return bubble

        bubble = MessageBubble(
            text=text,
            is_user=False,
        )

        bubble.deleted.connect(
            self.remove_message
        )

        self.message_layout.addWidget(
            bubble
        )

        self._scroll_bottom()

        return bubble

    
    def add_system_message(
        self,
        text: str,
    ) -> None:

        bubble = MessageBubble(
            text=text,
            is_user=False,
        )

        self.message_layout.addWidget(bubble)

        self._scroll_bottom()

    # -------------------------------------------------

    def clear_messages(
        self,
    ) -> None:

        while self.message_layout.count():

            item = self.message_layout.takeAt(0)

            widget = item.widget()

            if widget:

                widget.deleteLater()

    def remove_message(
        self,
        bubble: MessageBubble,
    ) -> None:

        self.message_layout.removeWidget(
            bubble
        )

        bubble.deleteLater()

    def on_message_edited(
        self,
        bubble: MessageBubble,
        text: str,
    ) -> None:

        bubble.set_message(text)

    def scroll_to_bottom(self) -> None:

        self._scroll_bottom()

    def update_stream(
        self,
        text: str,
    ) -> None:

        if not hasattr(self, "_stream_bubble"):

            self._stream_bubble = self.add_assistant_message("")

        self._stream_bubble.set_message(text)

        self.scroll_to_bottom()

    def finish_stream(self) -> None:

        if hasattr(self, "_stream_bubble"):

            del self._stream_bubble

        self.scroll_to_bottom()

    def clear_stream(self) -> None:
        """
        Clear any active streaming state.
        """

        if hasattr(self, "_stream_bubble"):
            del self._stream_bubble

    # -------------------------------------------------
    def _on_scroll_changed(self, value: int) -> None:

        scrollbar = self.verticalScrollBar()

        self._auto_scroll = (
            scrollbar.maximum() - value <= 20
        )

        if self._auto_scroll:
            self.scroll_bottom_button.hide()
        else:
            self.scroll_bottom_button.show()

    def _scroll_bottom(
        self,
    ) -> None:

        if not self._auto_scroll:
            return

        self.container.adjustSize()

        QTimer.singleShot(
            10,
            lambda: self.verticalScrollBar().setValue(
                self.verticalScrollBar().maximum()
            ),
        )

    def message_count(self) -> int:

        return self.message_layout.count()

    def filter_messages(
        self,
        text: str,
    ) -> None:

        text = text.lower().strip()

        for i in range(self.message_layout.count()):

            item = self.message_layout.itemAt(i)

            bubble = item.widget()

            if bubble is None:
                continue

            if not text:
                bubble.show()
                continue

            bubble.setVisible(
                text in bubble.text().lower()
            )

    def resizeEvent(
        self, 
        event: QResizeEvent,
    ) -> None:

        super().resizeEvent(event)

        self.scroll_bottom_button.move(
            self.viewport().width() - 60,
            self.viewport().height() - 60,
        )