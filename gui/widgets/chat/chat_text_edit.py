from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
)

from PyQt6.QtGui import (
    QKeyEvent,
)

from PyQt6.QtWidgets import (
    QTextEdit,
)


class ChatTextEdit(QTextEdit):
    """
    Chat input editor.

    Enter       -> Send message
    Shift+Enter -> New line
    """

    sendRequested = pyqtSignal()

    def keyPressEvent(
        self,
        event: QKeyEvent,
    ) ->None:

        if (
            event.key() in (
                Qt.Key.Key_Return,
                Qt.Key.Key_Enter,
            )
            and not (
                event.modifiers()
                & Qt.KeyboardModifier.ShiftModifier
            )
        ):

            self.sendRequested.emit()

            event.accept()

            return

        super().keyPressEvent(event)