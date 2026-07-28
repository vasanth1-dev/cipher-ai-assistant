from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
)

from gui.widgets.ui.page_header import PageHeader
from gui.widgets.ui.search_box import SearchBox
from gui.widgets.ui.icon_button import IconButton
from gui.widgets.ui.card import Card
from gui.widgets.ui.empty_state import EmptyState
from gui.widgets.ui.section import Section

from gui.theme import (
    BACKGROUND,
)


class MemoryPage(QWidget):
    """
    Cipher v2 Memory Center (UI)

    Public API
    ----------
    set_memories(list[str])
    add_memory(str)
    clear_memories()
    """

    exportClicked = pyqtSignal()
    importClicked = pyqtSignal()
    clearClicked = pyqtSignal()
    deleteClicked = pyqtSignal(str)

    def __init__(
        self,
    ) -> None:
        super().__init__()

        self._build_ui()

    # --------------------------------------------------

    def _build_ui(
        self,
    ) -> None:

        self.setStyleSheet(f"""
        QWidget{{
            background:{BACKGROUND};
        }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(15)

        header = PageHeader(
            "🧠 Memory"
            "Manage everything Cipher remebers.",
        )

        root.addWidget(header)

        self.search = SearchBox(
            "Search memories..."
        )
        self.search.setPlaceholderText(
            "Search memories..."
        )
        self.search.textChanged.connect(
            self._filter_memories
        )

        root.addWidget(self.search)

        self.memory_list = QListWidget()

        memory_card = Card()

        card_layout = QVBoxLayout(memory_card)

        section = Section("Stored Memories")

        card_layout.addWidget(section)

        card_layout.addWidget(
            self.memory_list
        )

        root.addWidget(
            memory_card,
            1,
        )

        self.empty_state = EmptyState(
            "🧠",
            "No memories stored",
            "Cipher hasn't saved anything yet."
        )

        root.addWidget(self.empty_state)


        buttons = QHBoxLayout()

        self.import_button = IconButton("📥", "Import")
        self.export_button = IconButton("📤", "Export")
        self.delete_button = IconButton("🗑", "Delete")
        self.clear_button = IconButton("❌", "Clear")

        self.import_button.clicked.connect(
            self.importClicked.emit
        )

        self.export_button.clicked.connect(
            self.exportClicked.emit
        )

        self.delete_button.clicked.connect(
            self._delete_selected
        )

        self.clear_button.clicked.connect(
            self._clear_all
        )

        buttons.addWidget(self.import_button)
        buttons.addWidget(self.export_button)

        buttons.addStretch()

        buttons.addWidget(self.delete_button)
        buttons.addWidget(self.clear_button)

        root.addLayout(buttons)

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def set_memories(self, memories):

        self.memory_list.clear()

        for memory in memories:
            self.memory_list.addItem(
                QListWidgetItem(str(memory))
            )

        self.empty_state.setVisible(len(memories) == 0)
        self.memory_list.setVisible(len(memories) > 0)

    def add_memory(self, memory):

        self.memory_list.addItem(
            QListWidgetItem(str(memory))
        )

        self.empty_state.hide()

        self.memory_list.show()


    def clear_memories(self):
        self.memory_list.clear()

        self.memory_list.hide()

        self.empty_state.show()

    # --------------------------------------------------
    # Internal
    # --------------------------------------------------

    def _filter_memories(self, text):

        text = text.lower().strip()

        for row in range(self.memory_list.count()):

            item = self.memory_list.item(row)

            visible = text in item.text().lower()

            item.setHidden(not visible)

    def _delete_selected(self):

        item = self.memory_list.currentItem()

        if item is None:
            return

        self.deleteClicked.emit(item.text())

        self.memory_list.takeItem(
            self.memory_list.row(item)
        )

    def _clear_all(self):

        if self.memory_list.count() == 0:
            return

        answer = QMessageBox.question(
            self,
            "Clear Memories",
            "Delete all memories?",
        )

        if answer == QMessageBox.StandardButton.Yes:

            self.memory_list.clear()

            self.clearClicked.emit()