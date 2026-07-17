from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)
from PyQt6.QtCore import pyqtSignal
from gui.widgets.chat_container import ChatContainer
from gui.widgets.welcome_widget import WelcomeWidget
from gui.theme import(
    SPACING_SMALL,
)

class ChatPanel(QWidget):
    
    promptSelected = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.welcome = WelcomeWidget()

        self.welcome.promptSelected.connect(
            self.promptSelected.emit
        )

        self.container = ChatContainer()

        self.container.hide()

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

        layout.setSpacing(
            SPACING_SMALL
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Expanding,
        )

        layout.addWidget(
            self.welcome,
            1,
        )

        layout.addWidget(
            self.container,
            1,
        )

    # --------------------------------------------------
    # Messages
    # --------------------------------------------------
    def _show_chat(self):

        if self.welcome.isVisible():
            self.welcome.hide()
            self.container.show()


    def add_user_message(
        self,
        text: str,
    ):
        
        self._show_chat()

        self.container.add_message(
            "You",
            text,
        )

        self._schedule_scroll()

    def add_assistant_message(
        self,
        text: str,
    ):
        
        self._show_chat()

        self.container.add_message(
            "Cipher",
            text,
        )

        self._schedule_scroll()

    def add_system_message(
        self,
        text: str,
    ):
        
        self._show_chat()

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

        self.container.hide()

        self.welcome.show()


    # --------------------------------------------------
    # Load Conversation
    # --------------------------------------------------

    def load_conversation(self, conversation):

        self.clear_chat()

        if not conversation.messages:
            return

        self._show_chat()

        for message in conversation.messages:

            sender = message.get("sender", "")

            text = message.get("text", "")

            if sender == "You":

                self.add_user_message(text)

            elif sender == "Cipher":

                self.add_assistant_message(text)

            else:

                self.add_system_message(text)

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