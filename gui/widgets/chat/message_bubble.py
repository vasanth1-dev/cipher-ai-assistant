from PyQt6.QtCore import (
    Qt,
    QTimer,
    pyqtSignal,
    QPropertyAnimation,
    QPoint,
)
from PyQt6.QtWidgets import QInputDialog
from PyQt6.QtWidgets import QGraphicsOpacityEffect
from datetime import datetime

from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from gui.theme import (
    PRIMARY,
    SURFACE_LIGHT,
    TEXT,
    TEXT_MUTED,
)


class MessageBubble(QWidget):

    deleted = pyqtSignal(QWidget)
    edited = pyqtSignal(QWidget, str)


    """
    Reusable chat message bubble.
    """

    def __init__(
        self,
        text: str,
        is_user: bool = False,
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.is_user = is_user

        self.timestamp = datetime.now().strftime("%I:%M %p")

        self._build_ui(text)

    # --------------------------------------------------

    def _build_ui(
        self,
        text: str,
    ) -> None:

        root = QHBoxLayout(self)

        root.setContentsMargins(12, 6, 12, 6)
        root.setSpacing(0)

        bubble = QFrame()

        bubble.setObjectName("MessageBubble")

        if self.is_user:

            bubble.setStyleSheet(f"""
            QFrame#MessageBubble {{
                background: {PRIMARY};
                border-radius: 18px;
                border: 1px solid rgba(255,255,255,0.08);
            }}

            QLabel#MessageTime {{
                font-size: 9pt;
                color: #94A3B8;
            }}
            """)

        else:

            bubble.setStyleSheet(f"""
            QFrame#MessageBubble {{
                background: {SURFACE_LIGHT};
                border-radius: 18px;
                border: 1px solid rgba(255,255,255,0.08);
            }}

            QLabel#MessageTime {{
                font-size: 9pt;
                color: #94A3B8;
            }}
            """)

        layout = QVBoxLayout(bubble)

        layout.setContentsMargins(
            18,
            14,
            18,
            14,
        )

        layout.setSpacing(8)

        sender = QLabel(
            "👤 You" if self.is_user else "🤖 Cipher"
        )

        sender.setStyleSheet(f"""
            color: {TEXT_MUTED};
            font-size: 9pt;
            font-weight: 600;
        """)

        self.copy_button = QPushButton("📋")

        self.copy_button.setFixedSize(28, 28)

        self.copy_button.setToolTip("Copy message")

        self.copy_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.copy_button.setStyleSheet("""
        QPushButton{
            background:transparent;
            border:none;
            font-size:12pt;
        }
        QPushButton:hover{
            background:rgba(255,255,255,0.08);
            border-radius:6px;
        }
        """)

        self.copy_button.clicked.connect(
            self.copy_message
        )

        self.message = QLabel(text)

        self.time_label = QLabel(self.timestamp)

        self.time_label.setObjectName("MessageTime")

        self.message.setWordWrap(True)

        self.message.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        self.message.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )

        self.message.customContextMenuRequested.connect(
            self._show_context_menu
        )

        self.message.setStyleSheet(f"""
            color: {TEXT};
            font-size: 11pt;
            line-height: 1.45;
            background: transparent;
        """)

        header = QHBoxLayout()
        header.setContentsMargins(0, 0, 0, 0)
        header.setSpacing(8)

        header.addWidget(sender)
        header.addStretch()
        header.addWidget(self.copy_button)

        layout.addLayout(header)
        layout.addWidget(self.message)
        layout.addWidget(self.time_label)

        bubble.setMinimumWidth(140)
        bubble.setMaximumWidth(700)

        self.opacity = QGraphicsOpacityEffect()

        bubble.setGraphicsEffect(self.opacity)

        self.animation = QPropertyAnimation(
            self.opacity,
            b"opacity",
        )

        self.animation.setDuration(180)

        self.animation.setStartValue(0.0)

        self.animation.setEndValue(1.0)

        self.animation.start()

        if self.is_user:

            root.addStretch()
            root.addWidget(bubble)
            root.addSpacing(8)

        else:

            root.addSpacing(8)
            root.addWidget(bubble)
            root.addStretch()

    # --------------------------------------------------

    def set_text(
        self,
        text: str,
    ) -> None:

        self.message.setText(text)

        self.adjustSize()

    def set_message(
        self,
        text: str,
    ) -> None:

        self.set_text(text)

    def text(self) -> str:

        return self.message.text()

    def copy_message(self) -> None:

        QApplication.clipboard().setText(
            self.message.text()
        )

        self.copy_button.setText("✓")
        self.copy_button.setEnabled(False)

        QTimer.singleShot(
            1000,
            self._reset_copy_button,
        )

    def _show_context_menu(
        self,
        pos: QPoint,
    ) -> None:

        menu = QMenu(self)

        copy_action = QAction(
            "📋 Copy",
            self,
        )

        copy_action.triggered.connect(
            self.copy_message
        )

        delete_action = QAction(
            "🗑 Delete",
            self,
        )

        delete_action.triggered.connect(
            lambda: self.deleted.emit(self)
        )

        menu.addAction(copy_action)

        if self.is_user:

            edit_action = QAction(
                "✏ Edit",
                self,
            )

            edit_action.triggered.connect(
                self.edit_message
            )

            menu.addAction(edit_action)

        menu.addSeparator()

        menu.addAction(delete_action)

        menu.exec(
            self.message.mapToGlobal(pos)
        )

    def _reset_copy_button(self) -> None:

        self.copy_button.setText("📋")
        self.copy_button.setEnabled(True)

    def edit_message(self) -> None:

        text, ok = QInputDialog.getText(
            self,
            "Edit Message",
            "Message:",
            text=self.message.text(),
        )

        if not ok:
            return

        text = text.strip()

        if not text:
            return

        self.message.setText(text)

        self.edited.emit(
            self,
            text,
        )