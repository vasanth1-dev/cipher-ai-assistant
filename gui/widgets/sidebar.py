from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)
from gui.widgets.conversation_list import(
    ConversationList,
)
from gui.theme import (
    SURFACE,
    PRIMARY,
    PRIMARY_HOVER,
    TEXT,
    TEXT_MUTED,
    SMALL_SIZE,
    CARD_PADDING,
    SIDEBAR_WIDTH,
    SPACING_SMALL,
    SPACING_LARGE,
    TITLE_SIZE,

)


class NavButton(QPushButton):

    def __init__(self, text: str):
        super().__init__(text)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(48)
        self.setCheckable(True)
        self.setMinimumWidth(180)

        self.setStyleSheet(f"""
        QPushButton{{
            background:transparent;
            color:{TEXT_MUTED};
            border:none;
            border-radius:10px;
            text-align:left;
            padding:12px 18px;
            font-size:11pt;
        }}

        QPushButton:hover{{
            background:{PRIMARY_HOVER};
            color:{TEXT};
        }}

        QPushButton:checked{{
            background:{PRIMARY};
            color:{TEXT};
            font-weight:bold;
        }}
        """)
        


class Sidebar(QFrame):

    pageChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("Sidebar")
        self.setFixedWidth(
            SIDEBAR_WIDTH
        )

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
        layout.setSpacing(
            SPACING_SMALL
        )

        logo = QLabel(
    "🤖 Cipher\nUbuntu AI Assistant"
        )
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet(f"""
        font-size:{TITLE_SIZE}px;
        font-weight:bold;
        padding:12px;
        color:{TEXT}
        """)

        layout.addWidget(logo)
        layout.addSpacing(
            SPACING_LARGE
        )

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
            btn = NavButton(text)
            btn.setToolTip(text)
            btn.clicked.connect(
                lambda checked=False, k=key: self.select(k)
            )

            layout.addWidget(btn)
            self.buttons[key] = btn

      


        separator = QFrame()

        separator.setFrameShape(
            QFrame.Shape.HLine
        )

        separator.setStyleSheet(f"""
        background:{PRIMARY};
        max-height:1px;
        border:none;
        """)

        layout.addWidget(separator)

        self.conversation_list = ConversationList()

        layout.addWidget(
            self.conversation_list,
            1,
        )

        layout.addStretch()

        # ---------------------------------------

        # Status

        # ---------------------------------------

        status_layout = QHBoxLayout()

        status_title = QLabel("Status")

        status_title.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:{SMALL_SIZE}pt;
        """)

        self.status_value = QLabel("🟢 Online")

        self.status_value.setStyleSheet(f"""
        color:{TEXT};
        font-weight:bold;
        font-size:10pt;
        """)

        status_layout.addWidget(status_title)

        status_layout.addStretch()

        status_layout.addWidget(
            self.status_value
        )

        layout.addLayout(status_layout)

        model_layout = QHBoxLayout()

        model_title = QLabel("Model")

        model_title.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:10pt;
        """)

        self.model_value = QLabel("qwen2.5")

        self.model_value.setStyleSheet(f"""
        color:{TEXT};
        font-weight:bold;
        font-size:10pt;
        """)

        model_layout.addWidget(model_title)

        model_layout.addStretch()

        model_layout.addWidget(
            self.model_value
        )

        layout.addLayout(model_layout)

        separator = QFrame()

        separator.setFrameShape(
            QFrame.Shape.HLine
        )

        separator.setStyleSheet(f"""
        background:{PRIMARY};
        max-height:1px;
        border:none;
        """)
                                   

        version = QLabel(
            "Cipher v2.0-dev\nBuild 001"
        )
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version.setStyleSheet(f"""
        color:{TEXT_MUTED};
        padding:10px;
        font-size:{SMALL_SIZE}pt
        """)

        layout.addWidget(version)

        self.select("dashboard")

    def select(self, page):

        for btn in self.buttons.values():
            btn.setChecked(False)

        if page in self.buttons:
            self.buttons[page].setChecked(True)

        self.pageChanged.emit(page)


    def set_status(self, text):
        self.status_value.setText(text)

    def set_model(self, text):
        self.model_value.setText(text)