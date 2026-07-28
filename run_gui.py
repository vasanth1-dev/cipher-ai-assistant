import sys
import threading

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication

from core.logger import logger
from core.assistant import Cipher

from gui.main_window import MainWindow
from gui.system_tray import CipherTray

from config import USER_NAME


class CipherGUI(QObject):

    # --------------------------------------------------
    # Thread-safe GUI Signals
    # --------------------------------------------------

    assistantMessage = pyqtSignal(str, str)
    assistantStatus = pyqtSignal(str)
    streamStarted = pyqtSignal()
    streamUpdated = pyqtSignal(str)
    streamFinished = pyqtSignal()

    # --------------------------------------------------

    def __init__(
       self,
    ) -> None:

        self.process_threads = []

        super().__init__()

        self.app = QApplication.instance()

        if self.app is None:
            self.app = QApplication(sys.argv)

        self.window = MainWindow()

        self.chat = self.window.chat

        self.tray = CipherTray(self.window)

        self.voice_thread = None

        try:

            self.assistant = Cipher()

        except Exception as e:

            logger.exception(e)

            raise

        # ------------------------------------------

        self._connect_gui()

        self._connect_assistant()

    # --------------------------------------------------
    # GUI Connections
    # --------------------------------------------------

    def _connect_gui(self):

        self.window.chat.messageSent.connect(
            self._process_message
        )

    # --------------------------------------------------
    # Assistant Connections
    # --------------------------------------------------

    def _connect_assistant(self):

        # Thread-safe Qt signals

        self.assistantMessage.connect(
            self._assistant_message
        )

        self.assistantStatus.connect(
            self.window.set_status
        )

        self.streamStarted.connect(
            self.window.chat.start_stream
        )

        self.streamFinished.connect(
            self.window.chat.finish_stream
        )

        # Backend callbacks

        self.assistant.on_message = (
            lambda role, text:
            self.assistantMessage.emit(
                role,
                text,
            )
        )

        self.assistant.on_status = (
            lambda status:
            self.assistantStatus.emit(
                status,
            )
        )

        self.assistant.on_stream_start = (
            lambda:
            self.streamStarted.emit()
        )

        self.streamUpdated.connect(
            self.window.chat.append_stream
        )

        self.assistant.on_stream_update = (
            lambda text:
            self.streamUpdated.emit(text)
        )

        self.assistant.on_stream_finish = (
            lambda:
            self.streamFinished.emit()
        )

        # --------------------------------------------------
    # Thread-safe UI callback
    # --------------------------------------------------

    def _assistant_message(
        self,
        role: str,
        text: str,
    ) -> None:

        if role == "Cipher":

            self.window.chat.hide_typing()

            self.window.chat.add_assistant_message(
                text
            )

        elif role == USER_NAME:

            self.window.chat.add_user_message(
                text
            )

        else:

            self.window.add_message(
                role,
                text,
            )

    # --------------------------------------------------

    def _process_message(
        self,
        text: str,
    ) -> None:

        threading.Thread(
            target=self.assistant.process,
            args=(text,),
            daemon=True,
            name="CipherProcessThread",
        ).start()

    # --------------------------------------------------

    def start_voice(
        self,
    ) -> None:

        if (
            self.voice_thread
            and self.voice_thread.is_alive()
        ):
            return

        self.voice_thread = threading.Thread(
            target=self.assistant.run,
            daemon=True,
            name="CipherVoiceThread",
        )

        self.voice_thread.start()

    # --------------------------------------------------

    def shutdown(
        self,
    ) -> None:

        try:

            self.assistant.stop()

        except Exception as e:

            logger.exception(e)

    # --------------------------------------------------

    def run(
        self,
    ) -> None:

        self.window.show()

        self.window.set_online()

        self.start_voice()

        try:

            sys.exit(
                self.app.exec()
            )

        finally:

            self.shutdown()


# ------------------------------------------------------


def main() -> None:

    CipherGUI().run()


if __name__ == "__main__":

    main()

