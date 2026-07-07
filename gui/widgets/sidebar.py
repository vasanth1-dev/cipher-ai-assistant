from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class NavButton(QPushButton):

    def __init__(self, text: str):
        super().__init__(text)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(48)
        self.setCheckable(True)

        self.setStyleSheet("""
        QPushButton{
            background:transparent;
            color:#D1D5DB;
            border:none;
            border-radius:10px;
            text-align:left;
            padding:12px 18px;
            font-size:11pt;
        }

        QPushButton:hover{
            background:#2D3748;
            color:white;
        }

        QPushButton:checked{
            background:#2563EB;
            color:white;
            font-weight:bold;
        }
        """)


class Sidebar(QFrame):

    pageChanged = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self.setObjectName("Sidebar")
        self.setFixedWidth(230)

        self.setStyleSheet("""
        QFrame#Sidebar{
            background:#1F2937;
            border-radius:14px;
        }

        QLabel{
            color:white;
        }
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(8)

        logo = QLabel("🤖 Cipher")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setStyleSheet("""
        font-size:22px;
        font-weight:bold;
        padding:10px;
        """)

        layout.addWidget(logo)
        layout.addSpacing(15)

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
            btn.clicked.connect(
                lambda checked=False, k=key: self.select(k)
            )

            layout.addWidget(btn)
            self.buttons[key] = btn

        layout.addStretch()

        version = QLabel("Cipher v2")
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version.setStyleSheet("""
        color:#9CA3AF;
        padding:8px;
        """)

        layout.addWidget(version)

        self.select("dashboard")

    def select(self, page):

        for btn in self.buttons.values():
            btn.setChecked(False)

        if page in self.buttons:
            self.buttons[page].setChecked(True)

        self.pageChanged.emit(page)