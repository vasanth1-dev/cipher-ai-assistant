from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QPushButton


class RegenerateButton(QPushButton):

    regenerateRequested = pyqtSignal()

    def __init__(self):
        super().__init__("↻ Regenerate")

        self.setMinimumHeight(34)

        self.setStyleSheet("""
        QPushButton{
            background:#1E293B;
            color:white;
            border:1px solid #334155;
            border-radius:8px;
            padding:6px 14px;
        }

        QPushButton:hover{
            background:#2563EB;
            border:1px solid #2563EB;
        }

        QPushButton:pressed{
            background:#1D4ED8;
        }

        QPushButton:disabled{
            background:#0F172A;
            color:#64748B;
            border:1px solid #1E293B;
        }
        """)

        self.clicked.connect(
            self.regenerateRequested.emit
        )

        self.setEnabled(False)

    # --------------------------------------------------

    def enable(self):

        self.setEnabled(True)

    # --------------------------------------------------

    def disable(self):

        self.setEnabled(False)