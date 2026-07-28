from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QPushButton


class StopButton(QPushButton):

    stopRequested = pyqtSignal()

    def __init__(
       self,
    ) -> None:
        super().__init__("■ Stop")

        self.setMinimumHeight(34)

        self.setStyleSheet("""
        QPushButton{
            background:#DC2626;
            color:white;
            border:none;
            border-radius:8px;
            padding:6px 14px;
        }

        QPushButton:hover{
            background:#EF4444;
        }

        QPushButton:pressed{
            background:#B91C1C;
        }

        QPushButton:disabled{
            background:#334155;
            color:#94A3B8;
        }
        """)

        self.clicked.connect(
            self.stopRequested.emit
        )

        self.setEnabled(False)

    # --------------------------------------------------

    def enable(self):

        self.setEnabled(True)

    # --------------------------------------------------

    def disable(self):

        self.setEnabled(False)