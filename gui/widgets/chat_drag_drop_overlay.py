from __future__ import annotations

from pathlib import Path

from PyQt6.QtGui import (
    QColor,
    QPainter,
    QPen,
    QResizeEvent,
    QPaintEvent,
    QDragEnterEvent,
    QDragMoveEvent,
    QDragLeaveEvent,
    QDropEvent,
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QLabel, QWidget


class ChatDragDropOverlay(QWidget):
    """
    Semi-transparent overlay displayed while files
    are dragged over the chat area.
    """

    filesDropped = pyqtSignal(list)

    def __init__(
        self, 
        parent: QWidget | None = None,
    ) -> None:
        super().__init__(parent)

        self.setAcceptDrops(True)
        self.hide()

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.label = QLabel("Drop files here", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.label.setStyleSheet(
            """
            QLabel{
                color:white;
                background:transparent;
                font-size:22px;
                font-weight:700;
            }
            """
        )

    # ---------------------------------------------------------

    def resizeEvent(
        self, 
        event: QResizeEvent,
    ) -> None:
        super().resizeEvent(event)
        self.label.setGeometry(self.rect())

    # ---------------------------------------------------------

    def paintEvent(
        self, 
        event: QPaintEvent,
    ) -> None:
        del event

        painter = QPainter(self)

        painter.fillRect(
            self.rect(),
            QColor(20, 20, 20, 170),
        )

        pen = QPen(QColor("#4F8DFF"))
        pen.setWidth(3)
        pen.setStyle(Qt.PenStyle.DashLine)

        painter.setPen(pen)

        rect = self.rect().adjusted(
            30,
            30,
            -30,
            -30,
        )

        painter.drawRoundedRect(rect, 16, 16)

    # ---------------------------------------------------------

    def dragEnterEvent(
        self, 
        event: QDragEnterEvent,
    ) -> None:

        mime = event.mimeData()

        if mime.hasUrls():
            event.acceptProposedAction()
            self.show()
        else:
            event.ignore()

    # ---------------------------------------------------------

    def dragMoveEvent(
        self, 
        event: QDragMoveEvent,
    ) -> None:
        event.acceptProposedAction()

    # ---------------------------------------------------------

    def dragLeaveEvent(
        self, 
        event: QDragLeaveEvent,
    ) -> None:
        del event
        self.hide()

    # ---------------------------------------------------------

    def dropEvent(
        self, 
        event: QDropEvent):

        self.hide()

        paths = []

        for url in event.mimeData().urls():
            if url.isLocalFile():
                paths.append(str(Path(url.toLocalFile())))

        if paths:
            self.filesDropped.emit(paths)

        event.acceptProposedAction()