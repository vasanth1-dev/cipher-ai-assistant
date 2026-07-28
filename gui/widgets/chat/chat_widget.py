from PyQt6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import pyqtSignal

from gui.theme import (
    CARD_PADDING,
    SPACING,
)

from gui.widgets.chat.chat_header import ChatHeader
from gui.widgets.chat.message_list import MessageList
from gui.widgets.chat.typing_indicator import TypingIndicator
from gui.widgets.chat.chat_input import ChatInput


class ChatWidget(QWidget):
    """
    Professional chat page.
    """

    messageSent = pyqtSignal(str)

    micClicked = pyqtSignal()

    def __init__(
        self, 
        parent: QWidget | None = None,
    ) ->None:
        super().__init__(parent)

        self._build_ui()

    # --------------------------------------------------

    def _build_ui(
        self,
    ) -> None:

        self.root = QVBoxLayout(self)

        self.root.setContentsMargins(
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
        )

        self.root.setSpacing(SPACING)

        # Header

        self.header = ChatHeader()

        self.root.addWidget(
            self.header
        )

        # Messages

        self.messages = MessageList()

        self.root.addWidget(
            self.messages,
            1,
        )

        # Typing Indicator

        self.typing = TypingIndicator()

        self.root.addWidget(
            self.typing
        )

        # Input

        self.input = ChatInput()

        self.root.addWidget(
            self.input
        )

        # ---------------- Signals ----------------

        self.input.sendClicked.connect(
            self._handle_send
        )

        self.input.micClicked.connect(
            self.micClicked.emit
        )

        self.header.clearChatClicked.connect(
            self.clear_chat
        )

        self.header.searchTextChanged.connect(
            self.messages.filter_messages
        )

    def load_conversation(
        self, 
        conversation,
    ) -> None:
        """
        Load a saved conversation.
        """

        self.clear_chat()

        if conversation is None:
            return

        for message in conversation.messages:

            sender = message.get("sender", "").lower()
            text = message.get("text", "")

            if sender == "you":
                self.add_user_message(text)

            elif sender == "system":
                self.messages.add_system_message(text)

            else:
                self.add_assistant_message(text)

        self.hide_typing()

    def _handle_send(
        self,
        text: str,
    ) -> None:

        text = text.strip()

        if not text:
            return

        self.add_user_message(text)

        self.show_typing()

        self.set_input_enabled(False)

        self.messageSent.emit(text)

        # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def add_user_message(
        self,
        text: str,
    ) -> None:

        self.messages.add_user_message(text)

    def add_assistant_message(
        self,
        text: str,
    ) -> None:

        self.messages.add_assistant_message(text)

        self.hide_typing()

        self.set_input_enabled(True)

        self.focus_input()

    # --------------------------------------------------

    def show_typing(self) -> None:

        self.typing.start()

        self.messages.scroll_to_bottom()

    def hide_typing(self) -> None:

        self.typing.stop()

        self.messages.scroll_to_bottom()
    # --------------------------------------------------

    def clear_chat(self) -> None:

        self.messages.clear_messages()

        self.messages.clear_stream()

        self.hide_typing()

        self.input.hide_stop_button()

        self.clear_input()

        self.set_input_enabled(True)

    # --------------------------------------------------

    def set_model(
        self,
        model: str,
    ) -> None:

        self.header.set_model(model)

    def set_status(
        self,
        status: str,
        model: str = "qwen2.5",
    ) -> None:

        self.header.set_status(
            status,
            model,
        )

    def focus_input(self) -> None:
        self.input.focus_input()


    def clear_input(self) -> None:
        self.input.clear()


    def set_input_text(self, text: str) -> None:
        self.input.set_text(text)

    # --------------------------------------------------

    def set_input_enabled(
        self,
        enabled: bool,
    ) -> None:

        self.input.set_enabled(enabled)

    # --------------------------------------------------

    def load_demo_chat(self) -> None:

        self.clear_chat()

        self.add_user_message(
            "Hello Cipher"
        )

        self.add_assistant_message(
            "Hello Vasanth! How can I help you today?"
        )

        self.add_user_message(
            "Open Firefox"
        )

        self.add_assistant_message(
            "Firefox has been opened successfully."
        )

    def start_stream(self) -> None:

        self.show_typing()

        self.set_input_enabled(False)

        self.input.show_stop_button()

        self.messages.clear_stream()

    def append_stream(
        self,
        text: str,
    ) -> None:

        self.hide_typing()

        self.messages.update_stream(text)

    def finish_stream(self) -> None:

        self.messages.finish_stream()

        self.hide_typing()

        self.input.hide_stop_button()

        self.set_input_enabled(True)

        self.focus_input()

    def get_chat_history(
        self,
    ) -> list[dict[str, str]]:

        history = []

        for i in range(self.messages.message_layout.count()):

            item = self.messages.message_layout.itemAt(i)

            bubble = item.widget()

            if bubble is None:
                continue

            history.append(
                {
                    "sender": "You" if bubble.is_user else "Cipher",
                    "text": bubble.text(),
                }
            )

        return history