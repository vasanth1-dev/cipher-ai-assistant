from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QHBoxLayout,
    QWidget,
)

from gui.widgets.regenerate_button import RegenerateButton
from gui.widgets.stop_button import StopButton


class ChatToolbar(QWidget):

    regenerateRequested = pyqtSignal()
    stopRequested = pyqtSignal()

    def __init__(self):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.regenerate_button = RegenerateButton()
        self.stop_button = StopButton()

        self.regenerate_button.regenerateRequested.connect(
            self.regenerateRequested.emit
        )

        self.stop_button.stopRequested.connect(
            self.stopRequested.emit
        )

        layout.addStretch()
        layout.addWidget(self.regenerate_button)
        layout.addWidget(self.stop_button)

    # --------------------------------------------------

    def generation_started(self):

        self.stop_button.enable()
        self.regenerate_button.disable()

    # --------------------------------------------------

    def generation_finished(self):

        self.stop_button.disable()
        self.regenerate_button.enable()

    # --------------------------------------------------

    def reset(self):

        self.stop_button.disable()
        self.regenerate_button.disable()