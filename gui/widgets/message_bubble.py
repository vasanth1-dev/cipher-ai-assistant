from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class MessageBubble(QFrame):

    def __init__(self, sender: str, message: str):
        super().__init__()

        self.sender = sender
        self.message = message

        self._build_ui()

    # --------------------------------------------------

    def _build_ui(self):

        self.setObjectName("MessageBubble")

        if self.sender.lower() == "you":
            background = "#2563EB"
        elif self.sender.lower() == "system":
            background = "#14532D"
        else:
            background = "#334155"

        self.setStyleSheet(f"""
        QFrame#MessageBubble {{
            background: {background};
            border-radius: 14px;
        }}

        QLabel {{
            color: white;
            background: transparent;
            font-size: 11pt;
        }}

        QPushButton {{
            background: #1E293B;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 4px 10px;
        }}

        QPushButton:hover {{
            background: #2563EB;
        }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(14, 12, 14, 12)
        root.setSpacing(8)

        header = QHBoxLayout()

        self.sender_label = QLabel(self.sender)
        self.sender_label.setStyleSheet("""
            font-size: 11pt;
            font-weight: bold;
        """)

        header.addWidget(self.sender_label)
        header.addStretch()

        self.copy_button = QPushButton("Copy")
        self.copy_button.clicked.connect(self.copy_message)

        header.addWidget(self.copy_button)

        root.addLayout(header)

        self.message_label = QLabel()

        # IMPORTANT
        self.message_label.setWordWrap(True)
        self.message_label.setTextFormat(Qt.TextFormat.PlainText)
        self.message_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )
        self.message_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop
        )

        root.addWidget(self.message_label)

        self.set_message(self.message)

    # --------------------------------------------------

    def set_message(self, text: str):

        self.message = text

        # Plain text-ஆ direct display பண்ணு.
        # Spaces, new lines, bullets எல்லாம் preserve ஆகும்.
        self.message_label.setText(text)

    # --------------------------------------------------

    def append_text(self, text: str):

        self.message += text
        self.message_label.setText(self.message)

    # --------------------------------------------------

    def copy_message(self):

        QApplication.clipboard().setText(self.message)