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
    QInputDialog,
    QMessageBox,
)
from gui.theme import (
    BACKGROUND,
    TEXT,
    PRIMARY,
    PRIMARY_HOVER,
    BORDER,
    SURFACE,
)

from gui.dashboard_widget import DashboardWidget
from gui.widgets.chat_panel import ChatPanel
from gui.widgets.header import Header
from gui.widgets.input_panel import InputPanel
from gui.widgets.sidebar import Sidebar
from core.conversation.conversation_service import (
    conversation_service,
)


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

        self.sidebar.conversation_list.load(
            conversation_service.get_all()
        )

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

        self.sidebar.conversation_list.newChatClicked.connect(
            self.create_new_chat
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

        self.chat.promptSelected.connect(
            self.on_prompt_selected
        )

        self.sidebar.conversation_list.conversationSelected.connect(
            self.load_conversation
        )

        self.sidebar.conversation_list.renameRequested.connect(
            self.rename_conversation
        )

        self.sidebar.conversation_list.deleteRequested.connect(
            self.delete_conversation
        )

        self.sidebar.conversation_list.pinRequested.connect (
            self.pin_conversation
        )

        self.stack.setCurrentIndex(0)

    # --------------------------------------------------
    def on_prompt_selected(self, prompt):

        self.input_panel.input.setText(prompt)

        self.input_panel.focus_input()

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

    def load_conversation(self, conversation_id):

        conversations = conversation_service.get_all()

        conversation = next(
            (
                c
                for c in conversations
                if c.id == conversation_id
            ),
            None,
        )

        if conversation is None:
            return

        conversation_service.set_current(
            conversation_id
        )

        self.chat.load_conversation(
            conversation
        )

        self.set_status(
            f"Loaded: {conversation.title}"
        )

    def rename_conversation(self, conversation_id):

        conversation = next(
            (
                c
                for c in conversation_service.get_all()
                if c.id == conversation_id
            ),
            None,
        )

        if conversation is None:
            return

        dialog = QInputDialog(self)

        dialog.setWindowTitle("Rename Conversation")
        dialog.setLabelText("New title:")
        dialog.setTextValue(conversation.title)

        dialog.setStyleSheet(f"""
        QInputDialog {{
            background: {BACKGROUND};
        }}

        QLabel {{
            color: {TEXT};
        }}

        QLineEdit {{
            background: {SURFACE};
            color: {TEXT};
            border: 1px solid {BORDER};
            border-radius: 6px;
            padding: 6px;
        }}

        QPushButton {{
            background: {PRIMARY};
            color: white;
            padding: 6px 12px;
            border-radius: 6px;
        }}

        QPushButton:hover {{
            background: {PRIMARY_HOVER};
        }}
        """)

        ok = dialog.exec()

        title = dialog.textValue()

        if not ok:
            return

        title = title.strip()

        if not title:
            return

        conversation_service.rename(
            conversation_id,
            title,
        )

        self.sidebar.conversation_list.update_title(
            conversation_id,
            title,
        )

        self.set_status(
            f"Renamed to '{title}'"
        )

    def delete_conversation(self, conversation_id):

        conversation = next(
            (
                c
                for c in conversation_service.get_all()
                if c.id == conversation_id
            ),
            None,
        )

        if conversation is None:
            return

        msg = QMessageBox(self)

        msg.setWindowTitle("Delete Conversation")
        msg.setText(f"Delete '{conversation.title}'?")

        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        msg.setStyleSheet(f"""
        QMessageBox {{
            background-color: {BACKGROUND}
        }}

        QLabel {{
            color: {TEXT};
            font-size: 11pt;
        }}

        QPushButton {{
            background-color: {PRIMARY};
            color: white;
            border: none;
            border-radius: 6px;
            padding: 6px 16px;
            min-width: 80px;
        }}

        QPushButton {{
            background-color: {PRIMARY_HOVER};
        }}

        QPushButton:pressed {{
            background-color: {PRIMARY_HOVER}
        }}
        """)

        reply = msg.exec()

        if reply != QMessageBox.StandardButton.Yes:
            return

        conversation_service.delete(
            conversation_id
        )

        self.sidebar.conversation_list.remove_conversation(
            conversation_id
        )

        if conversation_service.get_current() is None:

            self.chat.clear_chat()

        self.set_status(
            "Conversation deleted."
        )

    def pin_conversation(self, conversation_id):

        conversation = next(
            (
                c
                for c in conversation_service.get_all()
                if c.id == conversation_id
            ),
            None,
        )

        if conversation is None:
            return

        if conversation.pinned:

            conversation_service.unpin(
                conversation_id
            )

            self.set_status(
                "Conversation unpinned."
            )

        else:

            conversation_service.pin(
                conversation_id
            )

            self.set_status(
                "Conversation pinned."
            )

        self.sidebar.conversation_list.load(
            conversation_service.get_all()
        )

    def refresh_current_conversation_title(self):

        conversation = conversation_service.get_current()

        if conversation is None:
            return

        self.sidebar.conversation_list.update_title(
            conversation.id,
            conversation.title,
        )

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
    def create_new_chat(self):

        conversation = conversation_service.new_chat()

        self.sidebar.conversation_list.add_conversation(
            conversation.id,
            conversation.title,
        )

        self.chat.clear_chat()

        self.set_status("New conversation created.")

        
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