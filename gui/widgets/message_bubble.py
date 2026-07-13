from datetime import datetime

from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtGui import QDesktopServices
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)

from gui.renderers.renderer_manager import (
    renderer_manager,
)

from gui.theme import (
    ASSISTANT_BUBBLE,
    PRIMARY,
    SURFACE,
    SYSTEM_BUBBLE,
    TEXT,
    USER_BUBBLE,
)


class MessageBubble(QFrame):

    MAX_WIDTH = 850

    def __init__(
        self,
        sender: str,
        message: str,
    ):
        super().__init__()

        self.sender = sender
        self.message = message
        self.timestamp = datetime.now()

        self._build_ui()

    # --------------------------------------------------

    def _build_ui(self):

        self.setObjectName("MessageBubble")

        self.setMaximumWidth(
            self.MAX_WIDTH
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Maximum,
            QSizePolicy.Policy.Minimum,
        )

        if self.sender.lower() == "you":
            background = USER_BUBBLE

        elif self.sender.lower() == "system":
            background = SYSTEM_BUBBLE

        else:
            background = ASSISTANT_BUBBLE

        self.setStyleSheet(f"""
        QFrame#MessageBubble{{
            background:{background};
            border-radius:14px;
        }}

        QLabel{{
            color:{TEXT};
            background:transparent;
            font-size:11pt;
        }}

        QPushButton{{
            background:{SURFACE};
            color:white;
            border:none;
            border-radius:8px;
            padding:5px 12px;
        }}

        QPushButton:hover{{
            background:{PRIMARY};
        }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(
            18,
            14,
            18,
            14,
        )
        root.setSpacing(10)

        # ---------------- Header ----------------

        header = QHBoxLayout()

        self.sender_label = QLabel(
            self.sender
        )

        self.sender_label.setStyleSheet("""
        font-weight:bold;
        font-size:11pt;
        """)

        header.addWidget(
            self.sender_label
        )

        self.time_label = QLabel(
            self.timestamp.strftime("%H:%M")
        )

        self.time_label.setStyleSheet("""
        color:#9CA3AF;
        font-size:9pt;
        """)

        header.addWidget(
            self.time_label
        )

        header.addStretch()

        self.copy_button = QPushButton(
            "Copy"
        )

        self.copy_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.copy_button.clicked.connect(
            self.copy_message
        )

        header.addWidget(
            self.copy_button
        )

        root.addLayout(
            header
        )

        # ---------------- Message ----------------

        self.message_label = QLabel()

        self.message_label.setWordWrap(
            True
        )

        self.message_label.setTextFormat(
            Qt.TextFormat.RichText
        )

        self.message_label.setOpenExternalLinks(
            False
        )

        self.message_label.linkActivated.connect(
            self.open_link
        )

        self.message_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextBrowserInteraction
        )

        self.message_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft
            |
            Qt.AlignmentFlag.AlignTop
        )

        self.message_label.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Preferred,
        )

        root.addWidget(
            self.message_label
        )

        self.set_message(
            self.message
        )

    # --------------------------------------------------

    def set_message(
        self,
        text,
    ):

        self.message = text

        rendered = renderer_manager.render(
            text
        )

        self.message_label.setText(
            rendered
        )

    # --------------------------------------------------

    def append_text(
        self,
        text,
    ):

        self.set_message(
            self.message + text
        )

    # --------------------------------------------------

    def open_link(
        self,
        url,
    ):

        QDesktopServices.openUrl(
            QUrl(url)
        )

    # --------------------------------------------------

    def copy_message(self):

        QApplication.clipboard().setText(
            self.message
        )

        self.copy_button.setText(
            "Copied "
        )

        self.copy_button.setEnabled(
            False
        )

        QTimer.singleShot (
            1500,
            self._reset_copy_button,
        )

    def _reset_copy_button(self):

        self.copy_button.setText(
            "Copy"
        )

        self.copy_button.setEnabled(
            True
        )