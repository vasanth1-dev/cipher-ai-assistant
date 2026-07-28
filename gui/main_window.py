from pathlib import Path
import subprocess

from PyQt6.QtWidgets import (
    QFrame,
    QScrollArea,
)

from PyQt6.QtGui import (
    QGuiApplication,
    QIcon,
)
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu

from PyQt6.QtWidgets import (
    QFrame,
    QFileDialog,
    QHBoxLayout,
    QInputDialog,
    QMainWindow,
    QMessageBox,
    QScrollArea,
    QStackedWidget,
    QStatusBar,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
)
from core.listener import (
    pause_listening,
    resume_listening,
)

from gui.theme import (
    BACKGROUND,
    TEXT,
    INPUT_DIALOG_STYLE,
    MESSAGE_BOX_STYLE,
)

from core.logger import logger
from gui.widgets.dashboard_widget import DashboardWidget
from gui.widgets.chat.chat_widget import ChatWidget
from gui.widgets.memory.memory_widget import MemoryWidget
from gui.files_widget import FilesWidget
from gui.widgets.system_widget import SystemWidget
from gui.settings_widget import SettingsWidget
from gui.system_tray import CipherTray
from gui.widgets.header import Header
from gui.widgets.sidebar import Sidebar
from core.conversation.conversation_service import (
    conversation_service,
)


class MainWindow(QMainWindow):


    DASHBOARD_PAGE = 0
    CHAT_PAGE = 1
    MEMORY_PAGE = 2
    FILES_PAGE = 3
    SYSTEM_PAGE = 4
    SETTINGS_PAGE = 5

    PAGE_INDEX = {
        "dashboard": DASHBOARD_PAGE,
        "chat": CHAT_PAGE,
        "memory": MEMORY_PAGE,
        "files": FILES_PAGE,
        "system": SYSTEM_PAGE,
        "settings": SETTINGS_PAGE,
}

    def __init__(
       self,
    ) -> None:
        super().__init__()

        self.listening = True

        self.setWindowTitle(
            "Cipher v2 - Ubuntu AI Assistant"
        )

        screen = QGuiApplication.primaryScreen()
        geometry = screen.availableGeometry()

        self.resize(
            int(geometry.width() * 0.85),
            int(geometry.height() * 0.85),
        )

        self.move(
            (geometry.width() - self.width()) // 2,
            (geometry.height() - self.height()) // 2,
        )

        self.setMinimumSize(1000, 650)

        icon = Path(__file__).parent / "resources" / "cipher.png"

        if icon.exists():
            self.setWindowIcon(QIcon(str(icon)))

        self._apply_theme()

        self._build_ui()

        self._connect_signals()

        self.set_status("🟢 Ready")

        self.set_online()

        self.tray = CipherTray(self)

        self.tray.pauseRequested.connect(
            self.on_stop_clicked
        )

        self.tray.resumeRequested.connect(
            self.on_mic_clicked
        )

        tray_menu = QMenu()

        show_action = QAction("Show Cipher", self)
        hide_action = QAction("Hide Cipher", self)
        exit_action = QAction("Exit", self)

        show_action.triggered.connect(self.showNormal)
        hide_action.triggered.connect(self.hide)
        exit_action.triggered.connect(self.exit_application)

        tray_menu.addAction(show_action)
        tray_menu.addAction(hide_action)
        tray_menu.addSeparator()
        tray_menu.addAction(exit_action)

        self.tray.setContextMenu(tray_menu)

        self.tray.settingsRequested.connect(
            lambda: self.on_page_changed("settings")
        )

        self._force_exit = False

        self.tray.show()

        self.tray.activated.connect(self.on_tray_activated)

    def on_conversation_search(self, text: str):
        """
        Live conversation search.
        """

        self.sidebar.conversation_list.filter_conversations(text)

        if text.strip():
            self.set_status(f"Searching: {text}")
        else:
            self.set_status("Ready")

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
        root.setContentsMargins(10, 10, 10, 10)
        root.setSpacing(10)

        # ---------------- Sidebar ----------------

        self.sidebar = Sidebar()

        self.sidebar.conversation_list.load(
            conversation_service.get_all()
        )

        # ---------------- Right Panel ----------------

        right = QVBoxLayout()
        right.setSpacing(15)

        self.header = Header()

        # ---------------- Pages ----------------

        self.stack = QStackedWidget()

        self._build_pages()

        right.addWidget(self.header, 0)
        right.addWidget(self.stack, 1)

        root.addWidget(self.sidebar, 1)
        root.addLayout(right, 4)

    # ---------------- Status Bar ----------------

        self._create_statusbar()

    def _build_pages(self):

        # ---------------- Dashboard ----------------

        self.dashboard = DashboardWidget()

        dashboard_scroll = QScrollArea()

        dashboard_scroll.setWidgetResizable(True)

        dashboard_scroll.setFrameShape(
            QFrame.Shape.NoFrame
        )

        dashboard_scroll.setWidget(
            self.dashboard
        )

        self.stack.addWidget(
            dashboard_scroll
        )

        # ---------------- Chat ----------------

        self.chat = ChatWidget()

        self.stack.addWidget(
            self.chat
        )

        # ---------------- Memory ----------------

        self.memory = MemoryWidget()

        self.stack.addWidget(
            self.memory
        )

        # ---------------- Files ----------------

        self.files = FilesWidget()

        self.stack.addWidget(
            self.files
        )

        # ---------------- System ----------------

        self.system = SystemWidget()

        self.stack.addWidget(
            self.system
        )

        # ---------------- Settings ----------------

        self.settings = SettingsWidget()

        self.stack.addWidget(
            self.settings
        )
    
    def _create_statusbar(self):

        self.statusbar = QStatusBar()

        self.statusbar.setFixedHeight(
            24
        )

        self.setStatusBar(
            self.statusbar
        )

   
    # --------------------------------------------------

    def _connect_signals(self):

        self._connect_sidebar_signals()

        self._connect_dashboard_signals()

        self._connect_header_signals()

        self._connect_conversation_signals()

        # ChatWidget

        # ---------------- Chat ----------------

        self.chat.messageSent.connect(
            self.on_send_clicked
        )

        self.chat.micClicked.connect(
            self.on_mic_clicked
        )

        self.chat.header.newChatClicked.connect(
            self.create_new_chat
        )

        self.chat.header.clearChatClicked.connect(
            self.clear_chat
        )

        self.chat.header.exportChatClicked.connect(
            self.export_chat
        )

        self.stack.setCurrentIndex(
            self.DASHBOARD_PAGE
        )

    
    def _connect_dashboard_signals(self):

        actions = self.dashboard.quick_actions

        actions.chatClicked.connect(
            lambda: self.on_page_changed("chat")
        )

        actions.filesClicked.connect(
            lambda: self.on_page_changed("files")
        )

        actions.memoryClicked.connect(
            lambda: self.on_page_changed("memory")
        )

        actions.systemClicked.connect(
            lambda: self.on_page_changed("system")
        )

        actions.settingsClicked.connect(
            lambda: self.on_page_changed("settings")
        )

    def _connect_header_signals(self):

        self.header.settingsClicked.connect(
            lambda: self.on_page_changed(
                "settings"
            )
        )

    def _connect_conversation_signals(self):

        conversation_list = self.sidebar.conversation_list

        conversation_list.conversationSelected.connect(
            self.load_conversation
        )

        conversation_list.renameRequested.connect(
            self.rename_conversation
        )

        conversation_list.deleteRequested.connect(
            self.delete_conversation
        )

        conversation_list.pinRequested.connect(
            self.pin_conversation
        )

        conversation_list.searchChanged.connect(
            self.on_conversation_search
        )


    def _connect_sidebar_signals(self):
        """
        Connect all sidebar related signals.
        """

        # Navigation
        self.sidebar.pageChanged.connect(
            self.on_page_changed
        )

        # New Chat
        self.sidebar.conversation_list.newChatClicked.connect(
            self.create_new_chat
        )

    # --------------------------------------------------
    def on_prompt_selected(self, prompt):

        self.chat.set_input_text(prompt)

        self.chat.focus_input()

    def on_page_changed(self, page: str):
        """
        Centralized page navigation.
        """

        page = page.lower().strip()

        index = self.PAGE_INDEX.get(page)

        if index is None:
            logger.warning(f"Unknown page requested: {page}")
            return

        # Switch page
        self.stack.setCurrentIndex(index)

        # Chat specific behaviour
        if page == "chat":
            self.chat.focus_input()

        self._update_status(
            f"Opened {page.title()}",
            f"Page changed -> {page}",
        )
    # --------------------------------------------------

    def on_send_clicked(self, text):

        # ChatManager already adds the user message.
        # Prevent duplicate "You" bubbles.
        pass

    # --------------------------------------------------

    def on_mic_clicked(self):

        if self.listening:

            pause_listening()

            self.listening = False

            self.set_status("⏸ Listening Paused")

            self.header.set_ready()

            self.tray.set_listening(False)

        else:

            resume_listening()

            self.listening = True

            self.set_status("🎤 Listening")

            self.header.set_listening()

            self.tray.set_listening(True)


    def on_stop_clicked(self):

        from core.listener import pause_listening
        from core.speaker import speaker

        pause_listening()

        speaker.stop()

        self.set_status(
            "⏹ Listening paused."
        )

        self.header.set_ready()

        self.dashboard.set_voice(
            "Paused",
            "Microphone paused",
        )

        self.tray.set_listening(False)

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

        conversation = self._find_conversation(conversation_id)

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

        conversation = self._find_conversation(conversation_id)

        if conversation is None:
            return

        dialog = QInputDialog(self)

        dialog.setWindowTitle("Rename Conversation")
        dialog.setLabelText("New title:")
        dialog.setTextValue(conversation.title)

        dialog.setStyleSheet(
            INPUT_DIALOG_STYLE
        )

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

        conversation = self._find_conversation(conversation_id)

        if conversation is None:
            return

        msg = QMessageBox(self)

        msg.setWindowTitle("Delete Conversation")
        msg.setText(f"Delete '{conversation.title}'?")

        msg.setStandardButtons(
            QMessageBox.StandardButton.Yes |
            QMessageBox.StandardButton.No
        )

        msg.setStyleSheet(
            MESSAGE_BOX_STYLE
        )

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

        logger.info(
            "Conversation deleted."
        )

    def pin_conversation(self, conversation_id):

        conversation = self._find_conversation(conversation_id)

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

    def _find_conversation(self, conversation_id):

        return next(
            (
                conversation
                for conversation in conversation_service.get_all()
                if conversation.id == conversation_id
            ),
            None,
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

    def export_chat(self) -> None:

        history = self.chat.get_chat_history()

        if not history:
            self.set_status("No messages to export.")
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Chat",
            "cipher_chat.txt",
            "Text Files (*.txt)",
        )

        if not filename:
            return

        with open(filename, "w", encoding="utf-8") as file:

            for message in history:

                file.write(
                    f"[{message['sender']}] {message['text']}\n\n"
                )

        self.set_status("Chat exported successfully.")

    def _update_status(
        self,
        status: str,
        log: str | None = None,
    ):

        self.set_status(status)

        if log:

            logger.info(log)

    # --------------------------------------------------

    def set_status(self, text):

        self.statusbar.showMessage(text)

    # --------------------------------------------------
    def create_new_chat(self):
        """
        Create a new conversation and switch the UI
        to the chat page.
        """

        # Create conversation
        conversation = conversation_service.new_chat()

        # Make it the active conversation
        conversation_service.set_current(conversation.id)

        # Refresh sidebar
        self.sidebar.conversation_list.add_conversation(
            conversation.id,
            conversation.title,
        )

        # Clear current chat
        self.chat.clear_chat()

        # Navigate to chat page
        self.on_page_changed("chat")

        # Prepare input
        self.chat.clear_input()
        self.chat.focus_input()

        # Update status
        self.set_status("💬 New conversation created.")

        
    def set_online(self):

        self.header.set_online()

        self._set_dashboard_ready()

    def _set_dashboard_ready(self):

        self.dashboard.set_model(
            "qwen2.5"
        )

        self.dashboard.set_voice(
            "Ready",
            "Waiting for command",
        )

    # --------------------------------------------------

    def set_offline(self):

        self.header.status.set_offline()

        self.dashboard.set_model("Offline")



    def open_terminal(self):

        self._launch(
            ["gnome-terminal"],
            "Terminal",
        )


    def open_browser(self):

        self._launch(
            ["firefox"],
            "Browser",
        )


    def open_files(self):
        
        self._launch(
            ["nautilus"],
            "Files",
        )



    def open_settings(self):


        self._launch(
            ["gnome-control-center"],
            "Settings",
        )


    def _launch(self, command, name):

        try:
            subprocess.Popen(command)

        except Exception as e:

            logger.exception(e)

            self.set_status(
                f"Failed to open {name}."
            )

    def closeEvent(self, event):

        if self._force_exit:

            super().closeEvent(event)

            return

        settings = self.settings_service.load()

        if settings.get("tray", True) and self.tray.isVisible():

            self.hide()

            self.tray.showMessage(
                "Cipher",
                "Cipher is still running in the system tray.",
            )

            event.ignore()

            return

        super().closeEvent(event)

    def exit_application(self):

        self._force_exit = True

        self.tray.hide()

        self.close()

    def on_tray_activated(self, reason):

        if reason != QSystemTrayIcon.ActivationReason.DoubleClick:
            return

        self.showNormal()

        self.raise_()

        self.activateWindow()