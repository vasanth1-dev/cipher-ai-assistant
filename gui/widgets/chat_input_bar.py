from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QKeyEvent
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)


class ChatTextEdit(QTextEdit):
    """
    Chat input with:
    - Enter = Send
    - Shift+Enter = New line
    """

    sendRequested = pyqtSignal()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if (
            event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter)
            and not (event.modifiers() & Qt.KeyboardModifier.ShiftModifier)
        ):
            event.accept()
            self.sendRequested.emit()
            return

        super().keyPressEvent(event)


class ChatInputBar(QFrame):

    sendClicked = pyqtSignal(str)

    def __init__(
        self, 
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setObjectName("chatInputBar")

        self.setStyleSheet(
            """
            QFrame#chatInputBar{
                background:#202124;
                border:1px solid #35363A;
                border-radius:16px;
            }

            QTextEdit{
                background:transparent;
                color:white;
                border:none;
                font-size:14px;
                padding:8px;
            }

            QPushButton{
                background:#3B82F6;
                color:white;
                border:none;
                border-radius:10px;
                padding:8px 18px;
                font-weight:bold;
            }

            QPushButton:hover{
                background:#4F93FF;
            }

            QPushButton:disabled{
                background:#4A4A4A;
                color:#A0A0A0;
            }
            """
        )

        self.editor = ChatTextEdit()

        self.editor.setPlaceholderText(
            "Message Cipher..."
        )

        self.editor.setMinimumHeight(48)
        self.editor.setMaximumHeight(150)

        font = QFont()
        font.setPointSize(11)
        self.editor.setFont(font)

        self.send_button = QPushButton("Send")
        self.send_button.setFixedHeight(40)
        self.send_button.setFixedWidth(90)

        self.editor.sendRequested.connect(self._emit_message)
        self.send_button.clicked.connect(self._emit_message)

        row = QHBoxLayout()
        row.setContentsMargins(10, 8, 10, 8)
        row.setSpacing(10)

        row.addWidget(self.editor, 1)
        row.addWidget(self.send_button)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.addLayout(row)

    # --------------------------------------------------
    # API
    # --------------------------------------------------

    def text(self) -> str:
        return self.editor.toPlainText()

    def setText(
        self, 
        text: str,
    ) -> None:
        self.editor.setPlainText(text)

    def clear(
        self,
    ) -> None:
        self.editor.clear()

    def focus(
        self,
    ) -> None:
        self.editor.setFocus()

    def setSending(
        self, 
        sending: bool,
    ) -> None:
        self.send_button.setDisabled(sending)
        self.editor.setReadOnly(sending)

    # --------------------------------------------------

    def _emit_message(
        self,
    ) -> None:
        text = self.text().strip()

        if not text:
            return

        self.sendClicked.emit(text)
        self.clear()