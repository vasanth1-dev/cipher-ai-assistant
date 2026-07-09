from __future__ import annotations

from PyQt6.QtCore import QPoint, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QMenu


class ChatContextMenu(QMenu):
    """
    Reusable context menu for the chat area.

    This menu only emits signals.
    It does not perform any chat logic.
    """

    copyRequested = pyqtSignal()
    regenerateRequested = pyqtSignal()
    deleteRequested = pyqtSignal()
    retryRequested = pyqtSignal()
    selectAllRequested = pyqtSignal()
    clearConversationRequested = pyqtSignal()
    exportRequested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setObjectName("chatContextMenu")

        self.setStyleSheet(
            """
            QMenu{
                background:#202124;
                border:1px solid #3B3D42;
                border-radius:10px;
                padding:6px;
                color:white;
            }

            QMenu::item{
                padding:8px 18px;
                border-radius:6px;
            }

            QMenu::item:selected{
                background:#2F6FEB;
                color:white;
            }

            QMenu::separator{
                height:1px;
                background:#3B3D42;
                margin:6px 4px;
            }
            """
        )

        self._create_actions()

    # ---------------------------------------------------------

    def _create_actions(self):

        copy_action = QAction("Copy", self)
        regenerate_action = QAction("Regenerate Response", self)
        retry_action = QAction("Retry", self)

        delete_action = QAction("Delete Message", self)

        select_all_action = QAction("Select All", self)

        clear_action = QAction("Clear Conversation", self)

        export_action = QAction("Export Chat", self)

        copy_action.triggered.connect(self.copyRequested.emit)
        regenerate_action.triggered.connect(
            self.regenerateRequested.emit
        )
        retry_action.triggered.connect(self.retryRequested.emit)
        delete_action.triggered.connect(self.deleteRequested.emit)
        select_all_action.triggered.connect(
            self.selectAllRequested.emit
        )
        clear_action.triggered.connect(
            self.clearConversationRequested.emit
        )
        export_action.triggered.connect(self.exportRequested.emit)

        self.addAction(copy_action)
        self.addAction(regenerate_action)
        self.addAction(retry_action)

        self.addSeparator()

        self.addAction(delete_action)

        self.addSeparator()

        self.addAction(select_all_action)
        self.addAction(clear_action)
        self.addAction(export_action)

    # ---------------------------------------------------------

    def show_at(self, global_pos: QPoint):
        """
        Show the menu at the given global position.
        """
        self.exec(global_pos)