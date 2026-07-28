from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QLabel


class ThinkingIndicator(QLabel):

    def __init__(
       self,
    ) -> None:
        super().__init__()

        self._frame = 0

        self.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        self.setStyleSheet("""
        QLabel{
            color:#60A5FA;
            font-size:11pt;
            padding:8px;
            background:transparent;
        }
        """)

        self.hide()

        self.timer = QTimer(self)
        self.timer.setInterval(250)
        self.timer.timeout.connect(
            self._update_frame
        )

    # --------------------------------------------------

    def start(self):

        self._frame = 0

        self.show()

        self.timer.start()

        self._update_frame()

    # --------------------------------------------------

    def stop(self):

        self.timer.stop()

        self.hide()

    # --------------------------------------------------

    def _update_frame(self):

        dots = "." * (self._frame % 4)

        self.setText(
            f"🧠 Cipher is thinking{dots}"
        )

        self._frame += 1