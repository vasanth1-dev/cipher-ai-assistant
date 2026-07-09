from __future__ import annotations

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QGridLayout,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
)


class SuggestionButton(QPushButton):
    """
    Clickable suggestion chip.
    """

    def __init__(self, text: str, parent=None):
        super().__init__(text, parent)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(48)
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.setStyleSheet(
            """
            QPushButton{
                background:#202124;
                color:white;
                border:1px solid #3A3B3F;
                border-radius:12px;
                text-align:left;
                padding:12px;
                font-size:13px;
            }

            QPushButton:hover{
                background:#2A2C31;
                border:1px solid #5A8DFF;
            }

            QPushButton:pressed{
                background:#32353A;
            }
            """
        )


class ChatSuggestions(QFrame):
    """
    Displays starter prompts similar to ChatGPT/Claude.
    """

    suggestionClicked = pyqtSignal(str)

    DEFAULT_SUGGESTIONS = [
        "Explain Python decorators",
        "Write a Flask REST API",
        "Summarize this document",
        "Generate SQL query",
        "Debug my Python code",
        "Optimize this algorithm",
    ]

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("chatSuggestions")
        self.setStyleSheet(
            """
            QFrame#chatSuggestions{
                background:transparent;
                border:none;
            }
            """
        )

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        self.grid = QGridLayout()
        self.grid.setSpacing(12)

        root.addLayout(self.grid)

        self.setSuggestions(self.DEFAULT_SUGGESTIONS)

    # ------------------------------------------------------------------

    def clearSuggestions(self):
        while self.grid.count():
            item = self.grid.takeAt(0)

            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

    # ------------------------------------------------------------------

    def setSuggestions(self, suggestions: list[str]):
        self.clearSuggestions()

        columns = 2

        for index, text in enumerate(suggestions):
            button = SuggestionButton(text)

            button.clicked.connect(
                lambda _, t=text: self.suggestionClicked.emit(t)
            )

            row = index // columns
            col = index % columns

            self.grid.addWidget(button, row, col)

    # ------------------------------------------------------------------

    def hideSuggestions(self):
        self.hide()

    def showSuggestions(self):
        self.show()