import sys
import threading

from PyQt6.QtWidgets import QApplication

from core.assistant import Cipher
from gui.chat_widget import ChatManager
from gui.dashboard_updater import DashboardUpdater
from gui.main_window import MainWindow
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

        self.assistant.on_message = (
            self.chat.message_received.emit
        )

        self.assistant.on_status = (
            self.chat.status
        )

        self.assistant.on_stream_start = (
            self.chat.start_stream
        )

        self.assistant.on_stream_update = (
            self.chat.append_stream
        )

        self.assistant.on_stream_finish = (
            self.chat.finish_stream
        )

        self.chat.set_response_callback(
            self.assistant.process
        )

    # --------------------------------------------------

    def _connect_gui(self):

        # Input
        self.window.input_panel.sendClicked.connect(
            self.chat.send
        )

        self.window.input_panel.micClicked.connect(
            self._start_voice_once
        )

        # Normal messages
        self.chat.message_received.connect(
            self.window.add_message
        )

        # Streaming
        self.chat.stream_started.connect(
            lambda sender: self.window.chat.start_stream()
        )

        self.chat.stream_updated.connect(
            self.window.chat.append_stream
        )

        self.chat.stream_finished.connect(
            self.window.chat.finish_stream
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


def main():

    CipherApp().run()


if __name__ == "__main__":

    main()