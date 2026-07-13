from pathlib import Path
import subprocess

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QMainWindow,
    QStackedWidget,
    QStatusBar,
    QVBoxLayout,
    QWidget,
)
from gui.theme import (
    BACKGROUND,
    TEXT,
)

from gui.dashboard_widget import DashboardWidget
from gui.widgets.chat_panel import ChatPanel
from gui.widgets.header import Header
from gui.widgets.input_panel import InputPanel
from gui.widgets.sidebar import Sidebar


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("" \
        "Cipher v2 - Ubuntu AI Assistant"
        )
        DEFAULT_WIDTH = 1280
        DEFAULT_HEIGHT = 760

        self.resize(
            DEFAULT_WIDTH,
            DEFAULT_HEIGHT,
        )

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

        self.setStyleSheet(f"""
        QMainWindow{{
            background:{BACKGROUND};
        }}

        QWidget{{
            color:{TEXT};
            font-family:Segoe UI;
            font-size:11pt;
        }}
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

        # ---------------- Dashboard ----------------

        self.dashboard = DashboardWidget()

        # ---------------- Chat ----------------

        chat_page = QWidget()

        chat_layout = QVBoxLayout(chat_page)
        chat_layout.setContentsMargins(0, 0, 0, 0)
        chat_layout.setSpacing(10)

        self.chat = ChatPanel()
        self.input_panel = InputPanel()

        chat_layout.addWidget(self.chat, 1)
        chat_layout.addWidget(self.input_panel, 0)

        self.stack.addWidget(self.dashboard)
        self.stack.addWidget(chat_page)

        right.addWidget(self.header, 0)
        right.addWidget(self.stack, 1)

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

        self.input_panel.stopClicked.connect(
            self.on_stop_clicked
        )

        self.dashboard.terminal_btn.clicked.connect(
            self.open_terminal
        )

        self.dashboard.browser_btn.clicked.connect(
            self.open_browser
        )

        self.dashboard.files_btn.clicked.connect(
            self.open_files
        )

        self.dashboard.settings_btn.clicked.connect(
            self.open_settings
        )

        self.stack.setCurrentIndex(0)

    # --------------------------------------------------

    def on_page_changed(self, page):

        if page == "dashboard":

            self.stack.setCurrentIndex(0)

        elif page == "chat":

            self.stack.setCurrentIndex(1)

        self.set_status(
            f"Opened: {page.title()}"
        )

    # --------------------------------------------------

    def on_send_clicked(self, text):

        # ChatManager already adds the user message.
        # Prevent duplicate "You" bubbles.
        pass

    # --------------------------------------------------

    def on_mic_clicked(self):

        self.set_status("🎤 Listening...")

        self.header.set_listening()


    def on_stop_clicked(self):

        from core.listener import pause_listening
        from core.speaker import speaker

        pause_listening()

        speaker.stop()

        self.set_status(
            "⏹ Listening paused."
        )

        self.header.set_ready()

        self.dashboard.set_voice_status(
            "Paused",
            "Microphone paused",
        )

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
    # Streaming
    # --------------------------------------------------

    def start_stream(self):

        self.chat.start_stream()

    def append_stream(self, text):

        self.chat.append_stream(text)

    def finish_stream(self):

        self.chat.finish_stream()

    # --------------------------------------------------

    def clear_chat(self):

        self.chat.clear_chat()

    # --------------------------------------------------

    def set_status(self, text):

        self.statusbar.showMessage(text)

    # --------------------------------------------------

    def set_online(self):

        self.header.set_online()

        self.dashboard.set_ai_status(
            True,
            "qwen2.5",
        )

        self.dashboard.set_voice_status(
            "Ready",
            "Waiting for command",
        )

    # --------------------------------------------------

    def set_offline(self):

        self.header.status.set_offline()

        self.dashboard.set_ai_status(
            False,
        )

    def closeEvent(self, event):

        from core.speaker import speaker

        speaker.stop()

        event.accept()



    def open_terminal(self):

        subprocess.Popen(["gnome-terminal"])


    def open_browser(self):

        subprocess.Popen(["firefox"])


    def open_files(self):

        subprocess.Popen(["nautilus"])


    def open_settings(self):

        subprocess.Popen(["gnome-control-center"])