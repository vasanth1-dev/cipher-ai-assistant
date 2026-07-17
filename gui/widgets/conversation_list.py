from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QFrame,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QMenu,
)

from gui.theme import (
    PRIMARY,
    PRIMARY_HOVER,
    SURFACE,
    TEXT,
    BORDER,
)


class ConversationList(QFrame):
    """
    Displays all conversations.

    Responsibilities
    ----------------
    • Show conversations
    • Search conversations
    • Emit selected conversation
    • Emit new chat request
    """

    newChatClicked = pyqtSignal()

    conversationSelected = pyqtSignal(str)

    searchChanged = pyqtSignal(str)

    renameRequested = pyqtSignal(str)

    deleteRequested = pyqtSignal(str)

    pinRequested = pyqtSignal(str)

   

    def __init__(self):
        super().__init__()

        self._build_ui()

    # --------------------------------------------------

    def _build_ui(self):

        self.setStyleSheet(f"""
        QFrame{{
            background:transparent;
        }}

        QLineEdit{{
            background:{SURFACE};
            color:{TEXT};
            border:1px solid {BORDER};
            border-radius:8px;
            padding:8px;
        }}

        QListWidget{{
            background:transparent;
            border:none;
            color:{TEXT};
        }}

        QListWidget::item{{
            padding:10px;
            border-radius:8px;
        }}

        QListWidget::item:selected{{
            background:{PRIMARY};
            color:white;
        }}

        QListWidget::item:hover{{
            background:{PRIMARY_HOVER};
        }}

        QPushButton{{
            background:{PRIMARY};
            color:white;
            border:none;
            border-radius:8px;
            padding:10px;
            font-weight:bold;
        }}

        QPushButton:hover{{
            background:{PRIMARY_HOVER};
        }}
        """)

        layout = QVBoxLayout(self)

        layout.setSpacing(10)

        # --------------------------

        self.new_chat = QPushButton(
            "➕ New Chat"
        )

        self.new_chat.clicked.connect(
            self.newChatClicked.emit
        )

        layout.addWidget(
            self.new_chat
        )

        # --------------------------

        self.search = QLineEdit()

        self.search.setPlaceholderText(
            "Search conversations..."
        )

        self.search.textChanged.connect(
            self.searchChanged.emit
        )

        layout.addWidget(
            self.search
        )

        # --------------------------

        self.list = QListWidget()

        self.list.itemClicked.connect(
            self.clicked
        )

        self.list.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )

        self.list.customContextMenuRequested.connect(
            self._show_context_menu
        )

        layout.addWidget(
            self.list,
            1,
        )

    # --------------------------------------------------

    def add_conversation(
        self,
        conversation_id,
        title,
        pinned=False
    ):
        
        if pinned:
            title = f"📌 {title}"

        item = QListWidgetItem(title)

        item.setData(
            Qt.ItemDataRole.UserRole,
            conversation_id,
        )

        self.list.insertItem(
            0,
            item,
        )

    # --------------------------------------------------

    def clear(self):

        self.list.clear()

    # --------------------------------------------------

    def load(self, conversations):

        self.clear()

        for conversation in conversations:

            self.add_conversation(

                conversation.id,

                conversation.title,

                conversation.pinned,

            )

    # --------------------------------------------------

    def update_title(
        self,
        conversation_id,
        title,
    ):

        for index in range(self.list.count()):

            item = self.list.item(index)

            if item.data(
                Qt.ItemDataRole.UserRole
            ) == conversation_id:

                item.setText(title)

                return


    # --------------------------------------------------

    def remove_conversation(self, conversation_id):

        for index in range(self.list.count()):

            item = self.list.item(index)

            if item.data(
                Qt.ItemDataRole.UserRole
            ) == conversation_id:

                self.list.takeItem(index)

                return

    # --------------------------------------------------

    def clicked(self, item):

        conversation_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        self.conversationSelected.emit(
            conversation_id
        )


    # --------------------------------------------------

    def _show_context_menu(self, position):

        print("Context menu opened")

        item = self.list.itemAt(position)

        if item is None:
            return

        conversation_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        menu = QMenu(self)

        menu.setStyleSheet(f"""
        QMenu {{
            background: {SURFACE};
            color: {TEXT};
            border: 1px solid {BORDER};
        }}

        QMenu::item {{
            padding: 8px 24px;
        }}
        
        QMenu::item:selected {{
            background: {PRIMARY};
            color: white;
        }}
        """)

        rename_action = QAction(
            "✏ Rename",
            self,
        )

        is_pinned = item.text().startswith("📌")

        pin_action = QAction(
            "📍 Unpin" if is_pinned else "📌 Pin",
            self,
        )

        delete_action = QAction(
            "🗑 Delete",
            self,
        )

        menu.addAction(rename_action)
        menu.addAction(pin_action)
        menu.addSeparator()
        menu.addAction(delete_action)

        action = menu.exec(
            self.list.mapToGlobal(position)
        )

        if action == rename_action:

            self.renameRequested.emit(
                conversation_id
            )

        elif action == pin_action:

            self.pinRequested.emit(
                conversation_id
            )

        elif action == delete_action:

            self.deleteRequested.emit(
                conversation_id
            )