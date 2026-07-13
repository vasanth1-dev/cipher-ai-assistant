from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from gui.widgets.chat_container import ChatContainer


class ChatPanel(QWidget):
    """
    Cipher Professional Chat Panel

    Responsibilities
    ----------------
    • Conversation Management
    • Streaming
    • Typing Indicator
    • Auto Scroll
    """

    def __init__(self):
        super().__init__()

        self.container = ChatContainer()

        self._streaming = False
        self._auto_scroll = True

        self._build_ui()

    # --------------------------------------------------
    # UI
    # --------------------------------------------------

    def _build_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(8)

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        layout.addWidget(
            self.container,
            1,
        )

    # --------------------------------------------------
    # Messages
    # --------------------------------------------------

    def add_user_message(
        self,
        text: str,
    ):

        self.container.add_message(
            "You",
            text,
        )

        self._schedule_scroll()

    def add_assistant_message(
        self,
        text: str,
    ):

        self.container.add_message(
            "Cipher",
            text,
        )

        self._schedule_scroll()

    def add_system_message(
        self,
        text: str,
    ):

        self.container.add_message(
            "System",
            text,
        )

        self._schedule_scroll()

    # --------------------------------------------------
    # Typing Indicator
    # --------------------------------------------------

    def show_typing(self):

        if self._streaming:
            return

        self.container.show_typing_indicator()

    def hide_typing(self):

        self.container.hide_typing_indicator()

    # --------------------------------------------------
    # Streaming
    # --------------------------------------------------

    def start_stream(self):

        if self._streaming:
            return

        self.hide_typing()

        self._streaming = True

        self.container.add_message(
            "Cipher",
            "",
        )

        self._schedule_scroll()

    def append_stream(
        self,
        text: str,
    ):

        if not self._streaming:

            self.start_stream()

        self.container.append_to_last_message(
            text,
        )

        self._schedule_scroll()

    def finish_stream(self):

        self._streaming = False

        self._schedule_scroll()

    # --------------------------------------------------

    def clear_chat(self):

        self._streaming = False

        self.hide_typing()

        self.container.clear_messages()

    # --------------------------------------------------
    # Scroll
    # --------------------------------------------------

    def enable_auto_scroll(
        self,
        enabled=True,
    ):

        self._auto_scroll = enabled

    def _schedule_scroll(self):

        if not self._auto_scroll:
            return

        QTimer.singleShot(
            0,
            self._scroll_bottom,
        )

    def _scroll_bottom(self):

        self.container.scroll_to_bottom()