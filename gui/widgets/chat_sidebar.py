from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
)

from gui.theme import (
    SURFACE,
    PRIMARY,
    PRIMARY_HOVER,
    TEXT,
    TEXT_MUTED,
)


class ChatSidebar(QFrame):

    newChatClicked = pyqtSignal()
    chatSelected = pyqtSignal(str)

    def __init__(
       self,
    ) -> None:
        super().__init__()

        self.setFixedWidth(260)

        self.setStyleSheet(f"""
        QFrame {{
            background:{SURFACE};
            border-radius:16px;
        }}

        QLabel {{
            color:{TEXT};
        }}
        """)

        layout = QVBoxLayout(self)

        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        title = QLabel("Chats")

        title.setStyleSheet(f"""
        font-size:18px;
        font-weight:bold;
        color:{TEXT};
        """)

        layout.addWidget(title)

        self.new_chat_btn = QPushButton("+ New Chat")

        self.new_chat_btn.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.new_chat_btn.setMinimumHeight(42)

        self.new_chat_btn.setStyleSheet(f"""
        QPushButton {{
            background:{PRIMARY};
            color:white;
            border:none;
            border-radius:10px;
            font-size:11pt;
            font-weight:bold;
        }}

        QPushButton:hover {{
            background:{PRIMARY_HOVER};
        }}
        """)

        self.new_chat_btn.clicked.connect(
            self.newChatClicked.emit
        )

        layout.addWidget(self.new_chat_btn)

        self.chat_list = QListWidget()

        self.chat_list.setStyleSheet(f"""
        QListWidget {{
            background:transparent;
            border:none;
            color:{TEXT};
            font-size:10.5pt;
        }}

        QListWidget::item {{
            padding:10px;
            border-radius:8px;
        }}

        QListWidget::item:selected {{
            background:{PRIMARY};
            color:white;
        }}

        QListWidget::item:hover {{
            background:{PRIMARY_HOVER};
        }}
        """)

        self.chat_list.itemClicked.connect(
            self._chat_clicked
        )

        layout.addWidget(self.chat_list, 1)

    # ----------------------------------------

    def add_chat(self, chat_id, title):

        item = QListWidgetItem(title)

        item.setData(
            Qt.ItemDataRole.UserRole,
            chat_id,
        )

        self.chat_list.insertItem(0, item)

    # ----------------------------------------

    def clear(self):

        self.chat_list.clear()

    # ----------------------------------------

    def _chat_clicked(self, item):

        chat_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        self.chatSelected.emit(chat_id)

    def load_conversations(
            self,
            conversation,
    ):
        
        self.clear()

        for conversation in conversations:

            self.add_chat(

                conversation.id,

                conversation.title,
            )