from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)
from gui.theme import(
    BACKGROUND,
    SURFACE,
    BORDER,
    PRIMARY,
    PRIMARY_HOVER,
    PRIMARY_PRESSED,
    TEXT,
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
    stopClicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.setObjectName("InputPanel")

        self.setStyleSheet(f"""
        QFrame#InputPanel{{
            background:{SURFACE};
            border-radius:14px;
        }}

        QLineEdit{{
            background:{BACKGROUND};
            color:{TEXT};
            border:1px solid {BORDER};
            border-radius:10px;
            padding:12px;
            font-size:11pt;
        }}

        QLineEdit:focus{{
            border:2px solid {PRIMARY};
        }}

        QPushButton{{
            background:{PRIMARY};
            color:white;
            border:none;
            border-radius:10px;
            padding:10px 18px;
            font-weight:bold;
        }}

        QPushButton:hover{{
            background:{PRIMARY_HOVER};
        }}

        QPushButton:pressed{{
            background:{PRIMARY_PRESSED};
        }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        self.input = QLineEdit()
        self.input.setPlaceholderText("Ask Cipher anything...")
        self.input.returnPressed.connect(self._send)

        self.mic_button = QPushButton("🎙")
        self.mic_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.mic_button.setFixedSize(52, 48)
        self.mic_button.clicked.connect(self.micClicked.emit)

        self.send_button = QPushButton("➤ Send")
        self.send_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.send_button.setFixedWidth(100)
        self.send_button.clicked.connect(self._send)

        self.stop_button = QPushButton("⏹ Stop")

        self.stop_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.stop_button.setFixedSize(52, 48)

        self.stop_button.clicked.connect(
            self.stopClicked.emit
        )

        layout.addWidget(self.input)
        layout.addWidget(self.mic_button)
        layout.addWidget(self.stop_button)
        layout.addWidget(self.send_button)

        self.input.setClearButtonEnabled(True)
        self.input.setMinimumHeight(48)
        self.send_button.setMinimumHeight(48)
        self.mic_button.setMinimumHeight(48)

    def _send(self):
        text = self.input.text().strip()

        if not text:
            return

        self.sendClicked.emit(text)
        self.input.clear()
        self.input.setFocus()

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