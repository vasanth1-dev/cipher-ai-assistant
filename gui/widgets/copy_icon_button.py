from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import QApplication, QPushButton


class CopyIconButton(QPushButton):

    def __init__(self, text_provider):
        super().__init__("📋")

        self._text_provider = text_provider

        self.setToolTip("Copy")

        self.setFixedSize(32, 32)
        self.setIconSize(QSize(16, 16))

        self.setStyleSheet("""
        QPushButton{
            background:#1E293B;
            color:white;
            border:none;
            border-radius:8px;
            font-size:11pt;
        }

        QPushButton:hover{
            background:#2563EB;
        }

        QPushButton:pressed{
            background:#1D4ED8;
        }
        """)

        self.clicked.connect(self.copy)

    # --------------------------------------------------

    def copy(self):

        text = self._text_provider()

        if not text:
            return

        QApplication.clipboard().setText(text)

        self.setText("✓")

        self.repaint()

        from PyQt6.QtCore import QTimer

        QTimer.singleShot(
            1200,
            lambda: self.setText("📋"),
        )