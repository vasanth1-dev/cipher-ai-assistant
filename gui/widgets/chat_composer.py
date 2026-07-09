from __future__ import annotations

from PyQt6.QtCore import QObject, pyqtSignal

from gui.widgets.chat_attachment_button import ChatAttachmentButton
from gui.widgets.chat_input_bar import ChatInputBar
from gui.widgets.chat_suggestions import ChatSuggestions


class ChatComposer(QObject):
    """
    Coordinates the chat input widgets.

    Responsibilities
    ----------------
    - Connect suggestion clicks to the input box.
    - Forward send requests.
    - Forward attachment requests.

    This class contains no business logic and no AI logic.
    """

    messageSubmitted = pyqtSignal(str)
    attachmentSelected = pyqtSignal(str)

    def __init__(
        self,
        input_bar: ChatInputBar,
        attachment_button: ChatAttachmentButton,
        suggestions: ChatSuggestions,
        parent=None,
    ):
        super().__init__(parent)

        self.input_bar = input_bar
        self.attachment_button = attachment_button
        self.suggestions = suggestions

        self.input_bar.sendClicked.connect(
            self.messageSubmitted.emit
        )

        self.attachment_button.fileSelected.connect(
            self.attachmentSelected.emit
        )

        self.suggestions.suggestionClicked.connect(
            self._use_suggestion
        )

    # ---------------------------------------------------------

    def _use_suggestion(self, text: str):
        self.input_bar.setText(text)
        self.input_bar.focus()

    # ---------------------------------------------------------

    def clear(self):
        self.input_bar.clear()

    def setSending(self, sending: bool):
        self.input_bar.setSending(sending)

    def text(self) -> str:
        return self.input_bar.text()

    def focus(self):
        self.input_bar.focus()