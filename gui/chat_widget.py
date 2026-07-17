from PyQt6.QtCore import QObject, QThread, pyqtSignal
from core.conversation.conversation_service import (
    conversation_service,
)

class ChatWorker(QThread):

    finishedProcessing = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, callback, text):
        super().__init__()

        self._callback = callback
        self._text = text

    def run(self):

        try:

            self._callback(self._text)

        except Exception as e:

            self.error.emit(str(e))

        finally:

            self.finishedProcessing.emit()


class ChatManager(QObject):

    # Normal message
    message_received = pyqtSignal(str, str)

    # Streaming
    stream_started = pyqtSignal(str)
    stream_updated = pyqtSignal(str)
    stream_finished = pyqtSignal()

    # Status
    status_changed = pyqtSignal(str)

    conversation_title_changed = pyqtSignal(str, str)

    thinking_started = pyqtSignal()
    thinking_finished = pyqtSignal()

    def __init__(self):
        super().__init__()

        self._worker = None
        self._callback = None

    # --------------------------------------------------

    def set_response_callback(self, callback):

        self._callback = callback

    # --------------------------------------------------

    def send(self, text: str):

        text = text.strip()

        if not text:
            return

        self.user(text)

        if self._callback is None:
            self.system(
                "Assistant callback is not configured."
            )
            return

        self.status("🧠 Thinking...")
        self.thinking_started.emit()

        self._worker = ChatWorker(
            self._callback,
            text,
        )

        self._worker.finishedProcessing.connect(
            self._finished
        )

        self._worker.error.connect(
            self._error
        )

        self._worker.start()

    # --------------------------------------------------

    def _finished(self):

        self.status("🟢 Ready")
        self.thinking_finished.emit()

    # --------------------------------------------------

    def _error(self, text):

        self.system(f"Error: {text}")

    # --------------------------------------------------
    # Normal Messages
    # --------------------------------------------------

    def user(self, text):

        conversation = conversation_service.get_current()

        old_title = conversation.title if conversation else None

        conversation_service.add_user_message(text)

        conversation = conversation_service.get_current()

        if (
            conversation is not None
            and conversation.title != old_title
        ):

            self.conversation_title_changed.emit(
                conversation.id,
                conversation.title,
            )

        self.message_received.emit(
            "You",
            text,
        )
        
    def cipher(self, text):

        conversation_service.add_assistant_message(
            text
        )

        self.message_received.emit(
            "Cipher",
            text,
        )

    def system(self, text):

        conversation_service.add_system_message(
            text
        )

        self.message_received.emit(
            "System",
            text,
        )

    # --------------------------------------------------
    # Streaming API
    # --------------------------------------------------

    def start_stream(self):

        self.stream_started.emit("Cipher")

    def append_stream(self, text):

        if text:
            self.stream_updated.emit(text)

    def finish_stream(self):

        self.stream_finished.emit()

    # --------------------------------------------------

    def status(self, text):

        self.status_changed.emit(text)