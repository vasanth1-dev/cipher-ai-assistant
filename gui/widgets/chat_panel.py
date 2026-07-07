from PyQt6.QtWidgets import QVBoxLayout, QWidget

from gui.widgets.chat_container import ChatContainer


class ChatPanel(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.container = ChatContainer()

        layout.addWidget(self.container)

    # --------------------------------------------------

    def add_user_message(self, text: str):

        self.container.add_message(
            "You",
            text,
        )

    # --------------------------------------------------

    def add_assistant_message(self, text: str):

        self.container.add_message(
            "Cipher",
            text,
        )

    # --------------------------------------------------

    def add_system_message(self, text: str):

        self.container.add_message(
            "System",
            text,
        )

    # --------------------------------------------------

    def append_to_last_message(self, text: str):

        self.container.append_to_last_message(text)

    # --------------------------------------------------

    def clear_chat(self):

        self.container.clear_messages()