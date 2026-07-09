from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QLabel


class TypingIndicator(QLabel):

    def __init__(self):
        super().__init__()

        self._frame = 0

        self.setText("")

        self.setStyleSheet("""
        QLabel{
            color:#9CA3AF;
            font-size:11pt;
            padding:8px;
        }
        """)

        self.timer = QTimer(self)
        self.timer.setInterval(350)
        self.timer.timeout.connect(self._animate)

    # --------------------------------------------------

    def start(self):

        self._frame = 0

        self.show()

        self.timer.start()

    # --------------------------------------------------

    def stop(self):

        self.timer.stop()

        self.setText("")

        self.hide()

    # --------------------------------------------------

    def _animate(self):

        self._frame = (self._frame + 1) % 4

        self.setText(
            "Cipher is typing" + "." * self._frame
        )