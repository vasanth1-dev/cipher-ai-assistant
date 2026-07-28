from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
)

from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QPushButton,
)

from gui.widgets.chat.chat_text_edit import ChatTextEdit
from gui.theme import (
    SURFACE,
    BORDER,
    PRIMARY,
    PRIMARY_HOVER,
    TEXT,
    CARD_RADIUS,
    CARD_PADDING,
    BUTTON_HEIGHT,
)


class ChatInput(QFrame):
    """
    Professional chat input panel.
    """

    sendClicked = pyqtSignal(str)
    micClicked = pyqtSignal()
    attachmentClicked = pyqtSignal()

    def __init__(
        self, 
        parent: QFrame | None = None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("ChatInput")

        self.setStyleSheet(f"""
        QFrame#ChatInput {{
            background:{SURFACE};
            border:1px solid {BORDER};
            border-radius:{CARD_RADIUS}px;
        }}

        QTextEdit {{
            background:transparent;
            border:none;
            color:{TEXT};
            font-size:11pt;
            padding:8px;
        }}

        QTextEdit:focus {{
            border:none;
        }}

        QPushButton {{
            background:{PRIMARY};
            color:white;
            border:none;
            border-radius:8px;
            min-height:{BUTTON_HEIGHT}px;
            min-width:44px;
            padding:6px 12px;
        }}

        QPushButton:hover {{
            background:{PRIMARY_HOVER};
        }}
        """)

        self._build_ui()

    # --------------------------------------------------

    def _build_ui(
        self,
    ) -> None:

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
        )

        layout.setSpacing(10)

        self.attach_button = QPushButton("📎")

        self.mic_button = QPushButton("🎤")

        self.editor = ChatTextEdit()

        self.editor.sendRequested.connect(
            self._send
        )

        self.editor.setPlaceholderText(
            "Message Cipher..."
        )

        self.editor.setMinimumHeight(50)
        self.editor.setMaximumHeight(120)

        self.send_button = QPushButton("➤ Send")
        self.stop_button = QPushButton("⏹ Stop")
        self.stop_button.hide()

        layout.addWidget(self.stop_button)

        layout.addWidget(self.attach_button)
        layout.addWidget(self.mic_button)
        layout.addWidget(self.editor, 1)
        layout.addWidget(self.send_button)

        self.send_button.clicked.connect(
            self._send
        )

        self.attach_button.clicked.connect(
            self.attachmentClicked.emit
        )

        self.mic_button.clicked.connect(
            self._on_mic_clicked
        )

    # --------------------------------------------------

    # --------------------------------------------------

    def _send(
        self,
    ) -> None:

        text = self.editor.toPlainText().strip()

        if not text:
            return

        self.sendClicked.emit(text)

        self.editor.clear()

    # --------------------------------------------------

    def text(
        self,
    ) -> str:

        return self.editor.toPlainText()

    def clear(
        self,
    ) -> None:

        self.editor.clear()

    def set_placeholder(
        self,
        text: str,
    ) -> None:

        self.editor.setPlaceholderText(text)

    def set_enabled(
        self,
        enabled: bool,
    ) -> None:

        self.editor.setEnabled(enabled)
        self.send_button.setEnabled(enabled)
        self.attach_button.setEnabled(enabled)
        self.mic_button.setEnabled(enabled)

    def focus_input(
        self,
    ) -> None:
        self.editor.setFocus(Qt.FocusReason.OtherFocusReason)

    def show_stop_button(
        self,
    ) -> None:
        self.send_button.hide()
        self.stop_button.show()


    def hide_stop_button(
        self,
    ) -> None:
        self.stop_button.hide()
        self.send_button.show()

    def _on_mic_clicked(
        self,
    ) -> None:

        print("MIC BUTTON CLICKED")

        self.micClicked.emit()


    def set_text(
        self, 
        text: str,
    ) -> None:
        self.editor.setPlainText(text)
        self.focus_input()