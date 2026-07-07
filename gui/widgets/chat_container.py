from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from gui.widgets.message_bubble import MessageBubble


class ChatContainer(QScrollArea):

    def __init__(self):
        super().__init__()

        self._last_bubble = None

        self.setWidgetResizable(True)
        self.setFrameShape(QScrollArea.Shape.NoFrame)
        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        self.container = QWidget()

        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(10, 10, 10, 10)
        self.layout.setSpacing(12)
        self.layout.addStretch()

        self.setWidget(self.container)

    # --------------------------------------------------

    def add_message(self, sender: str, message: str):

        bubble = MessageBubble(sender, message)

        self.layout.insertWidget(
            self.layout.count() - 1,
            bubble,
        )

        self._last_bubble = bubble

        self.scroll_to_bottom()

        return bubble

    # --------------------------------------------------

    def append_to_last_message(self, text: str):

        if self._last_bubble is None:
            return

        self._last_bubble.append_text(text)

        self.scroll_to_bottom()

    # --------------------------------------------------

    def clear_messages(self):

        while self.layout.count() > 1:

            item = self.layout.takeAt(0)

            widget = item.widget()

            if widget is not None:
                widget.deleteLater()

        self._last_bubble = None

    # --------------------------------------------------

    def scroll_to_bottom(self):

        bar = self.verticalScrollBar()

        bar.setValue(bar.maximum())