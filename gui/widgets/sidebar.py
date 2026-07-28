from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)

from gui.widgets.conversation_list import ConversationList

from gui.theme import (
    SURFACE,
    TEXT,
    TEXT_MUTED,
    SMALL_SIZE,
    SIDEBAR_WIDTH,
    SPACING_LARGE,
    CARD_PADDING,
    PRIMARY_OVERLAY,
    PRIMARY_OVERLAY_HOVER,
    SPACING_SMALL
)


class NavButton(QPushButton):

    def __init__(self, text: str):
        super().__init__(text)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setCheckable(True)

        self.setMinimumHeight(44)
        self.setMinimumWidth(0)

        self.setStyleSheet(f"""
        QPushButton {{
            background: transparent;
            color: {TEXT_MUTED};
            border: none;
            border-radius: 12px;
            text-align: left;
            padding: 0 16px;
            font-size: 10.5pt;
            font-weight: 500;
        }}

        QPushButton:hover {{
            background:{PRIMARY_OVERLAY};
            color: {TEXT};
        }}

        QPushButton:checked {{
            background:{PRIMARY_OVERLAY_HOVER};
            color: white;
            font-weight: 600;
        }}
        """)


class Sidebar(QFrame):

    pageChanged = pyqtSignal(str)

    def __init__(
       self,
    ) -> None:
        super().__init__()

        self.setObjectName("Sidebar")
        self.setFixedWidth(SIDEBAR_WIDTH)

        self.setStyleSheet(f"""
        QFrame#Sidebar{{
            background:{SURFACE};
            border-radius:16px;
        }}

        QLabel{{
            color:{TEXT};
        }}
        """)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
        )

        layout.setSpacing(SPACING_SMALL)

        logo = QLabel(
            "🤖 Cipher\nUbuntu AI Assistant"
        )

        logo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        logo.setStyleSheet(f"""
        font-size:18px;
        font-weight:700;
        padding:8px;
        color:{TEXT};
        """)

        layout.addWidget(logo)

        layout.addSpacing(
            SPACING_LARGE
        )

        # Conversation Search

        self.buttons = {}

        pages = [
            ("dashboard", "🏠 Dashboard"),
            ("chat", "💬 Chat"),
            ("memory", "🧠 Memory"),
            ("files", "📁 Files"),
            ("system", "🖥 System"),
            ("settings", "⚙ Settings"),
        ]

        for key, text in pages:

            button = NavButton(text)

            button.setToolTip(text)

            button.clicked.connect(
                lambda _, page=key: self.select(page)
            )

            self.buttons[key] = button

            layout.addWidget(button)

        layout.addWidget(
            self._create_separator()
        )

        self.conversation_list = ConversationList()

        layout.addSpacing(
            SPACING_SMALL
        )

        layout.addWidget(
            self.conversation_list,
            1,
        )

        layout.addStretch()

        status_layout, self.status_value = self._create_info_row(
            "Status",
            "Online",
        )

        layout.addLayout(status_layout)

        model_layout, self.model_value = self._create_info_row(
            "Model",
            "qwen2.5",
        )

        layout.addLayout(model_layout)

        layout.addWidget(
            self._create_separator()
        )

        self.version = QLabel(
            "Cipher v2.0\nBuild 1"
        )

        self.version.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.version.setStyleSheet(f"""
        color:{TEXT_MUTED};
        padding:8px;
        font-size:{SMALL_SIZE}pt;
        """)

        layout.addWidget(self.version)

        self.select("dashboard")

    def _create_separator(self) -> QFrame:
        """
        Creates a horizontal separator line.
        """

        separator = QFrame()

        separator.setFrameShape(
            QFrame.Shape.HLine
        )

        separator.setStyleSheet(f"""
        background:rgba(255,255,255,0.08);
        max-height:1px;
        border:none;
        """)

        return separator


    def _create_info_row(
        self,
        title: str,
        value: str,
    ) -> tuple[QHBoxLayout, QLabel]:
        """
        Creates an information row used for
        Status, Model, etc.
        """

        row = QHBoxLayout()

        title_label = QLabel(title)

        title_label.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:{SMALL_SIZE}pt;
        """)

        value_label = QLabel(value)

        value_label.setStyleSheet(f"""
        color:{TEXT};
        font-weight:bold;
        font-size:10pt;
        """)

        row.addWidget(title_label)

        row.addStretch()

        row.addWidget(value_label)

        return row, value_label

    def select(
        self,
        page: str,
        emit_signal: bool = True,
    ) -> None:
        """
        Select the active navigation page.

        Parameters
        ----------
        page:
            Page identifier.

        emit_signal:
            When False, only the UI is updated without
            emitting the pageChanged signal.
        """

        if page not in self.buttons:
            return

        for button in self.buttons.values():
            button.setChecked(False)

        self.buttons[page].setChecked(True)

        if emit_signal:
            self.pageChanged.emit(page)


    def set_status(
        self,
        text: str,
    ) -> None:
        """
        Update sidebar status text.
        """

        self.status_value.setText(text)


    def set_model(
        self,
        text: str,
    ) -> None:
        """
        Update model name.
        """

        self.model_value.setText(text)