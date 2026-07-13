from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QMessageBox,
)

from gui.theme import (
    BACKGROUND,
    SURFACE,
    BORDER,
    PRIMARY,
    PRIMARY_HOVER,
    TEXT,
    TEXT_MUTED,
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

    def __init__(self):
        super().__init__()

        self._build_ui()

    # --------------------------------------------------

    def _build_ui(self):

        self.setStyleSheet(f"""
        QWidget{{
            background:{BACKGROUND};
            color:{TEXT};
        }}

        QLineEdit{{
            background:{SURFACE};
            color:{TEXT};
            border:1px solid {BORDER};
            border-radius:10px;
            padding:10px;
        }}

        QListWidget{{
            background:{SURFACE};
            border:1px solid {BORDER};
            border-radius:12px;
            outline:none;
        }}

        QListWidget::item{{
            padding:12px;
            border-bottom:1px solid {BORDER};
        }}

        QListWidget::item:selected{{
            background:{PRIMARY};
            color:white;
        }}

        QPushButton{{
            background:{PRIMARY};
            color:white;
            border:none;
            border-radius:10px;
            padding:10px 18px;
            font-weight:bold;
        }}

        QPushButton:hover{{
            background:{PRIMARY_HOVER};
        }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(15)

        title = QLabel("🧠 Memory Center")
        title.setStyleSheet("""
        font-size:24px;
        font-weight:bold;
        """)

        subtitle = QLabel(
            "Manage everything Cipher remembers."
        )

        subtitle.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:10pt;
        """)

        root.addWidget(title)
        root.addWidget(subtitle)

        self.search = QLineEdit()
        self.search.setPlaceholderText(
            "Search memories..."
        )
        self.search.textChanged.connect(
            self._filter_memories
        )

        root.addWidget(self.search)

        self.memory_list = QListWidget()

        root.addWidget(
            self.memory_list,
            1,
        )

        buttons = QHBoxLayout()

        self.import_button = QPushButton("Import")
        self.export_button = QPushButton("Export")
        self.delete_button = QPushButton("Delete")
        self.clear_button = QPushButton("Clear All")

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

    def add_memory(self, memory):

        self.memory_list.addItem(
            QListWidgetItem(str(memory))
        )

    def clear_memories(self):

        self.memory_list.clear()

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