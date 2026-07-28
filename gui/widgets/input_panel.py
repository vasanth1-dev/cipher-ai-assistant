from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
)
from gui.theme import(
    SURFACE,
)

from gui.widgets.ui.icon_button import IconButton
from gui.widgets.ui.search_box import SearchBox

class InputPanel(QFrame):
    """
    Bottom input area used by Cipher.

    Signals
    -------
    sendClicked(str)
        Emitted when the user sends a message.

    micClicked()
        Emitted when the microphone button is pressed.
    """

    sendClicked = pyqtSignal(str)
    micClicked = pyqtSignal()
    stopClicked = pyqtSignal()

    def __init__(
       self,
    ) -> None:
        super().__init__()

        self.setObjectName("InputPanel")

        self.setStyleSheet(f"""
        QFrame#InputPanel {{
            background:{SURFACE};
            border:1px solid rgba(255,255,255,0.08);
            border-radius:18px;
        }}
        """)

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            18,
            14,
            18,
            14,
        )

        layout.setSpacing(12)

        self.input = SearchBox(
            "Message Cipher..."
        )

        self.input.setMinimumHeight(52)

        self.input.returnPressed.connect(
            self._send
        )

        self.mic_button = IconButton(
            "🎤",
            ""
        )

        self.stop_button = IconButton(
            "⏹",
            ""
        )

        self.send_button = IconButton(
            "➤",
            "Send"
        )

        self.mic_button.setFixedSize(56, 56)

        self.stop_button.setFixedSize(56, 56)

        self.send_button.setFixedSize(120, 56)

        self.stop_button.hide()

        self.mic_button.clicked.connect(
            self.micClicked.emit
        )

        self.send_button.clicked.connect(
            self._send
        )

        self.stop_button.clicked.connect(
            self.stopClicked.emit
        )

        layout.addWidget(self.input, 1)
        layout.addWidget(self.mic_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.send_button)

        self.mic_button.setToolTip(
            "Start Voice Input"
        )

        self.stop_button.setToolTip(
            "Stop Speaking"
        )

        self.send_button.setToolTip(
            "Send Message"
        )

        self.input.setFocus()


    def _send(self) -> None:
        text = self.input.text()

        text = text.strip()

        if len(text) == 0:
            self.input.setFocus()
            return

        self.sendClicked.emit(text)
        self.input.clear()
        self.input.setFocus()

    def text(self) -> str:
        return self.input.text()

    def clear(self) -> None:
        self.input.clear()

    def set_placeholder(
        self, 
        text: str
    ) -> None:
        self.input.setPlaceholderText(text)

    def set_enabled(
        self, 
        enabled: bool
    ) -> None:
        self.input.setEnabled(enabled)
        self.send_button.setEnabled(enabled)
        self.mic_button.setEnabled(enabled)
        self.stop_button.setEnabled(enabled)

    def is_busy(self) -> bool:

        return self.stop_button.isVisible()

    def show_stop_button(self) -> None:

        self.stop_button.show()

        self.mic_button.hide()

        self.send_button.setEnabled(False)


    def hide_stop_button(self) -> None:

        self.stop_button.hide()

        self.mic_button.show()

        self.send_button.setEnabled(True)

    def focus_input(self) -> None:
        self.input.setFocus()