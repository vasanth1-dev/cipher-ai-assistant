from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import (
    QFrame,
    QListWidget,
    QListWidgetItem,
    QVBoxLayout,
    QMenu,
)

from gui.widgets.ui.icon_button import IconButton
from gui.widgets.ui.search_box import SearchBox
from gui.widgets.ui.empty_state import EmptyState
from core.logger import logger
from gui.theme import (
    PRIMARY,
    SURFACE,
    TEXT,
    BORDER,
    LIST_WIDGET_STYLE,
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

   

    def __init__(
       self,
    ) -> None:
        super().__init__()

        self._build_ui()

    # --------------------------------------------------

    def _build_ui(self):

        self.setStyleSheet(f"""
        QFrame{{
            background:transparent;
        }}
        """)

        layout = QVBoxLayout(self)

        layout.setSpacing(12)
        layout.setContentsMargins(0, 0, 0, 0)

        # --------------------------

        self.new_chat = IconButton(
            "➕",
            "New Chat",
        )

        self.new_chat.setToolTip(
            "Create New Conversation"
        )

        self.new_chat.clicked.connect(
            self.newChatClicked.emit
        )

        layout.addWidget(
            self.new_chat
        )

        # --------------------------

        self.search = SearchBox(
            "🔍 Search conversations..."
        )

        self.search.setToolTip(
            "Search Conversations"
)

        self.search.textChanged.connect(
            self.searchChanged.emit
        )

        layout.addWidget(
            self.search
        )

        # --------------------------

        self.list = QListWidget()

        self.empty_state = EmptyState(
            icon="💬",
            title="No Conversations",
            message="Start a new chat to begin your conversation history.",
            button_text="New Chat",
        )

        self.empty_state.button_widget().clicked.connect(
            self.newChatClicked.emit
        )

        self.empty_state.hide()

        self.list.setStyleSheet(LIST_WIDGET_STYLE)

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
            self.empty_state
        )

        layout.addWidget(
            self.list,
            1,
        )

    def _format_title(
        self,
        title: str,
        pinned: bool,
    ) -> str:

        if pinned:
            return f"📌 💬 {title}"

        return f"💬 {title}"

    # --------------------------------------------------

    def add_conversation(
        self,
        conversation_id,
        title,
        is_pinned=False
    ):

        
        title = self._format_title(
            title,
            is_pinned,
        )

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

    def clear(self) -> None:

        self.list.clear()

        self.list.hide()

        self.empty_state.show()


    def _find_item(
        self,
        conversation_id: str,
    ):

        for index in range(
            self.list.count()
        ):

            item = self.list.item(index)

            if item.data(
                Qt.ItemDataRole.UserRole
            ) == conversation_id:

                return item, index

        return None, -1

    # --------------------------------------------------

    def load(
        self, 
        conversations,
    ) -> None:

        self.clear()

        if not conversations:

            self.list.hide()

            self.empty_state.show()

            return
        
        self.empty_state.hide()

        self.list.show()

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

        item, _ = self._find_item(
            conversation_id
        )

        if item is None:
            return    
        is_pinned = item.text().startswith("📌")

        item.setText(
            self._format_title(
                title,
                is_pinned,
            )
        )


    # --------------------------------------------------

    def remove_conversation(
        self, 
        conversation_id,
    ):
                

        item, index = self._find_item(
            conversation_id
        )

        if item is None:
                return

        

        self.list.takeItem(index)

    # --------------------------------------------------

    def clicked(
        self, 
        item: QListWidgetItem,
    ) -> None:

        conversation_id = item.data(
            Qt.ItemDataRole.UserRole
        )

        if conversation_id is None:
            return

        self.conversationSelected.emit(
            conversation_id
        )

    def filter_conversations(self, text: str) -> None:
        """
        Filter conversations by title.
        """

        text = text.casefold().strip()

        visible_count = 0

        for index in range(self.list.count()):

            item = self.list.item(index)

            title = item.text().casefold()

            matched = text in title

            item.setHidden(not matched)

            if matched:
                visible_count += 1

        has_items = self.list.count() > 0
        has_results = visible_count > 0

        self.list.setVisible(has_items and has_results)
        self.empty_state.setVisible(not has_results)


    # --------------------------------------------------

    def _show_context_menu(
        self, 
        position,
    ) -> None:

        logger.debug("Context menu opened")

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
            padding:8px 16px;
            border-radius:8px;
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