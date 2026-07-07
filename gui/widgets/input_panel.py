from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)


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

    def __init__(self):
        super().__init__()

        self.setObjectName("InputPanel")

        self.setStyleSheet("""
        QFrame#InputPanel{
            background:#1F2937;
            border-radius:14px;
        }

        QLineEdit{
            background:#111827;
            color:white;
            border:1px solid #374151;
            border-radius:10px;
            padding:12px;
            font-size:11pt;
        }

        QLineEdit:focus{
            border:2px solid #2563EB;
        }

        QPushButton{
            background:#2563EB;
            color:white;
            border:none;
            border-radius:10px;
            padding:10px 18px;
            font-weight:bold;
        }

        QPushButton:hover{
            background:#3B82F6;
        }

        QPushButton:pressed{
            background:#1D4ED8;
        }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Ask Cipher anything...")
        self.input.returnPressed.connect(self._send)

        self.mic_button = QPushButton("🎤")
        self.mic_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mic_button.setFixedSize(52, 46)
        self.mic_button.clicked.connect(self.micClicked.emit)

        self.send_button = QPushButton("Send")
        self.send_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_button.setFixedWidth(100)
        self.send_button.clicked.connect(self._send)

        layout.addWidget(self.input)
        layout.addWidget(self.mic_button)
        layout.addWidget(self.send_button)

    def _send(self):
        text = self.input.text().strip()

        if not text:
            return

        self.sendClicked.emit(text)
        self.input.clear()

    def text(self) -> str:
        return self.input.text()

    def clear(self):
        self.input.clear()

    def set_placeholder(self, text: str):
        self.input.setPlaceholderText(text)

    def set_enabled(self, enabled: bool):
        self.input.setEnabled(enabled)
        self.send_button.setEnabled(enabled)
        self.mic_button.setEnabled(enabled)

    def focus_input(self):
        self.input.setFocus()