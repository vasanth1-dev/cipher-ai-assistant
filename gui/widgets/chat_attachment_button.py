from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QFileDialog, QPushButton


class ChatAttachmentButton(QPushButton):
    """
    Attachment button for the chat input.

    Responsibilities
    ----------------
    • Opens a file picker
    • Emits the selected file path
    • Does not process the file itself
    """

    fileSelected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__("📎", parent)

        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setToolTip("Attach a file")

        self.setFixedSize(40, 40)

        self.setStyleSheet(
            """
            QPushButton{
                background:#202124;
                color:white;
                border:1px solid #3B3D42;
                border-radius:10px;
                font-size:18px;
            }

            QPushButton:hover{
                background:#2B2D31;
                border:1px solid #5B8CFF;
            }

            QPushButton:pressed{
                background:#34373C;
            }
            """
        )

        self.clicked.connect(self._choose_file)

    # ------------------------------------------------------------------

    def _choose_file(self):
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Select File",
            "",
            (
                "All Files (*);;"
                "Text Files (*.txt *.md *.pdf);;"
                "Images (*.png *.jpg *.jpeg *.bmp *.webp);;"
                "Python (*.py);;"
                "CSV (*.csv);;"
                "JSON (*.json)"
            ),
        )

        if not filename:
            return

        self.fileSelected.emit(str(Path(filename)))

    # ------------------------------------------------------------------

    def openDialog(self):
        """
        Public helper if another widget wants
        to trigger the file picker.
        """
        self._choose_file()