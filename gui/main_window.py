from pathlib import Path

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)

from gui.dashboard_widget import DashboardWidget
from gui.widgets.chat_panel import ChatPanel
from gui.widgets.header import Header
from gui.widgets.input_panel import InputPanel
from gui.widgets.sidebar import Sidebar


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cipher AI Assistant")
        self.resize(1280, 760)

        icon = Path(__file__).parent / "resources" / "cipher.png"
        if icon.exists():
            self.setWindowIcon(QIcon(str(icon)))

        self._apply_theme()
        self._build_ui()
        self._connect_signals()

        self.set_status("🟢 Ready")
        self.set_online()

    # --------------------------------------------------

    def _apply_theme(self):

        self.setStyleSheet("""
        QMainWindow{
            background:#111827;
        }

        QWidget{
            color:white;
            font-family:Segoe UI;
            font-size:11pt;
        }
        """)

    # --------------------------------------------------

    def _build_ui(self):

        central = QWidget()
        self.setCentralWidget(central)

        root = QHBoxLayout(central)
        root.setContentsMargins(15, 15, 15, 15)
        root.setSpacing(15)

        self.sidebar = Sidebar()

        right = QVBoxLayout()
        right.setSpacing(15)

        self.header = Header()

        self.stack = QStackedWidget()

        # Dashboard Page
        self.dashboard = DashboardWidget()

        # Chat Page
        chat_page = QWidget()
        chat_layout = QVBoxLayout(chat_page)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        chat_layout.setSpacing(15)

        self.chat = ChatPanel()
        self.input_panel = InputPanel()

        chat_layout.addWidget(self.chat)
        chat_layout.addWidget(self.input_panel)

        self.stack.addWidget(self.dashboard)   # index 0
        self.stack.addWidget(chat_page)        # index 1

        right.addWidget(self.header)
        right.addWidget(self.stack)

        root.addWidget(self.sidebar)
        root.addLayout(right)

        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)

    # --------------------------------------------------

    def _connect_signals(self):

        self.sidebar.pageChanged.connect(
            self.on_page_changed
        )

        self.input_panel.sendClicked.connect(
            self.on_send_clicked
        )

        self.input_panel.micClicked.connect(
            self.on_mic_clicked
        )

    # --------------------------------------------------

    def on_page_changed(self, page):

        if page == "dashboard":
            self.stack.setCurrentIndex(0)

        elif page == "chat":
            self.stack.setCurrentIndex(1)

        self.set_status(f"Opened: {page.title()}")

    # --------------------------------------------------

    def on_send_clicked(self, text):

        self.add_message("You", text)

    # --------------------------------------------------

    def on_mic_clicked(self):

        self.set_status("🎤 Listening...")

        self.header.status.set_listening()

    # --------------------------------------------------

    def add_message(self, sender, text):

        sender = sender.lower()

        if sender == "you":
            self.chat.add_user_message(text)

        elif sender == "system":
            self.chat.add_system_message(text)

        else:
            self.chat.add_assistant_message(text)

    # --------------------------------------------------

    def clear_chat(self):

        self.chat.clear_chat()

    # --------------------------------------------------

    def set_status(self, text):

        self.statusbar.showMessage(text)

    # --------------------------------------------------

    def set_online(self):

        self.header.status.set_online()

    # --------------------------------------------------

    def set_offline(self):

        self.header.status.set_offline()