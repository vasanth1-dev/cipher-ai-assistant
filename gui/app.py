import sys
import threading

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QApplication

from core.assistant import Cipher
from gui.widgets.chat.chat_widget import ChatWidget
from gui.dashboard_updater import DashboardUpdater
from gui.main_window import MainWindow
from gui.system_tray import CipherTray


class CipherApp(QObject):

    assistantMessage = pyqtSignal(str, str)
    assistantStatus = pyqtSignal(str)
    streamStarted = pyqtSignal()
    streamUpdated = pyqtSignal(str)
    streamFinished = pyqtSignal()

    def __init__(
       self,
    ) -> None:

        super().__init__()

        self.app = QApplication.instance() or QApplication(sys.argv)

        self.window = MainWindow()

        self.tray = CipherTray(
            self.window
        )

        self.dashboard_updater = DashboardUpdater(
            self.window.dashboard
        )

        self.chat = self.window.chat

        self.assistant = Cipher()

        self._voice_started = False

        self._connect_backend()
        self._connect_gui()

    # --------------------------------------------------

    def _connect_backend(self):

        # Assistant → ChatWidget
        self.assistant.on_message = (
            lambda role, message:
            self.assistantMessage.emit(
                role,
                message
            )
        )

        self.assistant.on_status = (
            lambda status:
            self.assistantStatus.emit(status)
        )

        self.assistant.on_stream_start = (
            lambda:
            self.streamStarted.emit()
        )

        self.assistant.on_stream_update = (
            lambda text:
            self.streamUpdated.emit(text)
        )

        self.assistant.on_stream_finish = (
            lambda:
            self.streamFinished.emit()
        )

        # ChatWidget → Assistant

        # Thread-safe signal connections

        self.assistantMessage.connect(
            self._assistant_message
        )

        self.assistantStatus.connect(
            self.chat.set_status
        )

        self.streamStarted.connect(
            self.chat.start_stream
        )

        self.streamUpdated.connect(
            self.chat.append_stream
        )

        self.streamFinished.connect(
            self.chat.finish_stream
        )
        import threading

        self.chat.messageSent.connect(
            lambda text: threading.Thread(
                target=self.assistant.process,
                args=(text,),
                daemon=True,
            ).start()
        )

    def _assistant_message(
        self,
        role: str,
        text: str,
    ) -> None:

        if role == "Cipher":

            self.chat.add_assistant_message(
                text
            )

        else:

            self.chat.add_user_message(
                text
            )
    # --------------------------------------------------

    def _connect_gui(self):

        # Input
        self.chat.micClicked.connect(
            self._start_voice_once
        )

    # --------------------------------------------------

    def _start_voice_once(self):

        if getattr(self, "_voice_started", False):
            return

        self._voice_started = True

        self.voice_thread = threading.Thread(
            target=self.assistant.run,
            daemon=True,
            name="VoiceThread",
        )
        self.voice_thread.start()



    # --------------------------------------------------

    def run(self):

        self.window.show()

        self.window.set_online()

        self.dashboard_updater.set_ai_online()
        self.dashboard_updater.start()

        self._start_voice_once()

        exit_code = self.app.exec()

        self.dashboard_updater.stop()

        sys.exit(exit_code)


def main():

    CipherApp().run()


if __name__ == "__main__":

    main()