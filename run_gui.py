import sys
import threading

from PyQt6.QtWidgets import QApplication

from core.assistant import Cipher
from gui.chat_widget import ChatManager
from gui.main_window import MainWindow
from gui.tray import CipherTray


class CipherGUI:

    def __init__(self):

        self.app = QApplication(sys.argv)

        self.window = MainWindow()
        self.chat = ChatManager()
        self.tray = CipherTray(self.window)

        self.assistant = Cipher()

        self._connect_gui()
        self._connect_assistant()

    # --------------------------------------------------

    def _connect_gui(self):

        self.window.input_panel.sendClicked.connect(
            self.chat.send
        )

        self.window.input_panel.micClicked.connect(
            self._mic_clicked
        )

        self.chat.message_received.connect(
            self.window.add_message
        )

        self.chat.status_changed.connect(
            self.window.set_status
        )

        self.chat.thinking_started.connect(
            self.window.header.status.set_listening
        )

        self.chat.thinking_finished.connect(
            self.window.header.status.set_online
        )

    # --------------------------------------------------

    def _connect_assistant(self):

        self.chat.set_response_callback(
            self._process_message
        )

        self.assistant.on_message = (
            self.chat.message_received.emit
        )

    # --------------------------------------------------

    def _process_message(self, text: str):

        self.assistant.process(text)

        return ""

    # --------------------------------------------------

    def _mic_clicked(self):

        self.window.set_status("🎤 Listening...")

    # --------------------------------------------------

    def start_voice(self):

        threading.Thread(
            target=self.assistant.run,
            daemon=True,
        ).start()

    # --------------------------------------------------

    def run(self):

        self.window.show()

        self.window.set_online()

        self.start_voice()

        sys.exit(self.app.exec())


def main():

    CipherGUI().run()


if __name__ == "__main__":

    main()