import sys
import threading

from PyQt6.QtWidgets import QApplication

from core.assistant import Cipher
from gui.chat_widget import ChatManager
from gui.main_window import MainWindow
from gui.dashboard_updater import DashboardUpdater
from gui.tray import CipherTray

class CipherApp:

    def __init__(self):

        self.app = QApplication(sys.argv)

        self.window = MainWindow()

        self.tray = CipherTray(
            self.window
        )

        self.dashboard_updater = DashboardUpdater(
            self.window.dashboard
        )
        self.chat = ChatManager()
        self.assistant = Cipher()

        self._connect_backend()
        self._connect_gui()

    # --------------------------------------------------

    def _connect_backend(self):

        # Assistant -> GUI
        self.assistant.on_message = (
            self.chat.message_received.emit
        )

        self.assistant.on_status = (
            self.chat.status
        )

        # ChatManager -> Assistant
        self.chat.set_response_callback(
            self.assistant.process
        )

    # --------------------------------------------------

    def _connect_gui(self):

        # Input Panel
        self.window.input_panel.sendClicked.connect(
            self.chat.send
        )

        # Messages
        self.chat.message_received.connect(
            self.window.add_message
        )

        # Status
        self.chat.status_changed.connect(
            self.window.set_status
        )

        self.chat.thinking_started.connect(
            self.window.header.status.set_listening
        )

        self.chat.thinking_finished.connect(
            self.window.set_online
        )

        # Microphone button
        self.window.input_panel.micClicked.connect(
            self._start_voice_once
        )

    # --------------------------------------------------

    def _start_voice_once(self):

        if getattr(self, "_voice_started", False):
            return

        self._voice_started = True

        threading.Thread(
            target=self.assistant.run,
            daemon=True,
        ).start()

    # --------------------------------------------------

    def run(self):

        self.window.show()

        self.window.set_online()

        self.dashboard_updater.set_ai_online()

        self.dashboard_updater.start()

        self._start_voice_once()

        sys.exit(
            self.app.exec()
        )