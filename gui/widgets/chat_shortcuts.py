from __future__ import annotations

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QKeySequence, QShortcut
from PyQt6.QtWidgets import QWidget


class ChatShortcuts(QObject):
    """
    Centralized keyboard shortcuts for the chat UI.

    This class only emits signals.
    It does not perform any application logic.
    """

    newChatRequested = pyqtSignal()
    searchRequested = pyqtSignal()
    exportRequested = pyqtSignal()
    focusInputRequested = pyqtSignal()
    clearRequested = pyqtSignal()

    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self._shortcuts = []

        self._register(
            "Ctrl+N",
            self.newChatRequested.emit,
        )

        self._register(
            "Ctrl+F",
            self.searchRequested.emit,
        )

        self._register(
            "Ctrl+E",
            self.exportRequested.emit,
        )

        self._register(
            "Ctrl+L",
            self.clearRequested.emit,
        )

        self._register(
            "/",
            self.focusInputRequested.emit,
        )

    # ---------------------------------------------------------

    def _register(self, sequence: str, callback):

        shortcut = QShortcut(
            QKeySequence(sequence),
            self.parent(),
        )

        shortcut.activated.connect(callback)

        self._shortcuts.append(shortcut)