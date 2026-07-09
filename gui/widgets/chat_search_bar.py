from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QWidget,
)


class ChatSearchBar(QWidget):

    searchRequested = pyqtSignal(str)
    clearRequested = pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        self.search = QLineEdit()
        self.search.setPlaceholderText(
            "Search conversation..."
        )

        self.search.setStyleSheet("""
        QLineEdit{
            background:#1E293B;
            color:white;
            border:1px solid #334155;
            border-radius:8px;
            padding:8px;
        }
        """)

        self.find_button = QPushButton("🔍")
        self.clear_button = QPushButton("✕")

        for button in (
            self.find_button,
            self.clear_button,
        ):
            button.setFixedWidth(40)
            button.setStyleSheet("""
            QPushButton{
                background:#2563EB;
                color:white;
                border:none;
                border-radius:8px;
            }

            QPushButton:hover{
                background:#3B82F6;
            }
            """)

        self.find_button.clicked.connect(
            self._search
        )

        self.clear_button.clicked.connect(
            self._clear
        )

        self.search.returnPressed.connect(
            self._search
        )

        layout.addWidget(self.search)
        layout.addWidget(self.find_button)
        layout.addWidget(self.clear_button)

    # --------------------------------------------------

    def _search(self):

        text = self.search.text().strip()

        if text:
            self.searchRequested.emit(text)

    # --------------------------------------------------

    def _clear(self):

        self.search.clear()

        self.clearRequested.emit()