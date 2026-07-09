from datetime import datetime

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel


class MessageTimestamp(QLabel):

    def __init__(self, timestamp=None):
        super().__init__()

        if timestamp is None:
            timestamp = datetime.now()

        self.setAlignment(
            Qt.AlignmentFlag.AlignRight
        )

        self.setStyleSheet("""
        QLabel{
            color:#94A3B8;
            font-size:9pt;
            padding-top:2px;
            background:transparent;
        }
        """)

        self.set_timestamp(timestamp)

    # --------------------------------------------------

    def set_timestamp(self, timestamp):

        if isinstance(timestamp, datetime):

            text = timestamp.strftime("%I:%M %p")

        else:

            text = str(timestamp)

        self.setText(text)

    # --------------------------------------------------

    def refresh_now(self):

        self.set_timestamp(
            datetime.now()
        )