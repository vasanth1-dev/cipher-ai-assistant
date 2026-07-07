from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MemoryWidget(QWidget):

    refreshRequested = pyqtSignal()
    deleteRequested = pyqtSignal(str)
    clearRequested = pyqtSignal()
    searchRequested = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self._build_ui()

    # --------------------------------------------------

    def _build_ui(self):

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(15)

        title = QLabel("🧠 Memory")
        title.setStyleSheet("""
        font-size:22px;
        font-weight:bold;
        color:white;
        """)

        subtitle = QLabel(
            "View and manage Cipher conversation memory."
        )

        subtitle.setStyleSheet("""
        color:#9CA3AF;
        """)

        root.addWidget(title)
        root.addWidget(subtitle)

        toolbar = QFrame()
        toolbar.setStyleSheet("""
        QFrame{
            background:#1F2937;
            border-radius:12px;
        }

        QLineEdit{
            background:#111827;
            color:white;
            border:1px solid #374151;
            border-radius:8px;
            padding:10px;
        }

        QPushButton{
            background:#2563EB;
            color:white;
            border:none;
            border-radius:8px;
            padding:10px 16px;
        }

        QPushButton:hover{
            background:#3B82F6;
        }
        """)

        bar = QHBoxLayout(toolbar)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search memory...")

        self.refresh_btn = QPushButton("Refresh")
        self.delete_btn = QPushButton("Delete")
        self.clear_btn = QPushButton("Clear All")

        bar.addWidget(self.search)
        bar.addWidget(self.refresh_btn)
        bar.addWidget(self.delete_btn)
        bar.addWidget(self.clear_btn)

        root.addWidget(toolbar)

        self.memory_list = QListWidget()

        self.memory_list.setStyleSheet("""
        QListWidget{
            background:#0F172A;
            color:white;
            border:1px solid #334155;
            border-radius:12px;
            padding:8px;
        }

        QListWidget::item{
            padding:10px;
        }

        QListWidget::item:selected{
            background:#2563EB;
        }
        """)

        root.addWidget(self.memory_list)

        # Signals
        self.search.textChanged.connect(
            self.searchRequested.emit
        )

        self.refresh_btn.clicked.connect(
            self.refreshRequested.emit
        )

        self.clear_btn.clicked.connect(
            self.clearRequested.emit
        )

        self.delete_btn.clicked.connect(
            self._delete_selected
        )

    # --------------------------------------------------

    def set_memories(self, items):

        self.memory_list.clear()

        for item in items:
            self.memory_list.addItem(str(item))

    # --------------------------------------------------

    def add_memory(self, text):

        self.memory_list.addItem(str(text))

    # --------------------------------------------------

    def clear_memories(self):

        self.memory_list.clear()

    # --------------------------------------------------

    def _delete_selected(self):

        item = self.memory_list.currentItem()

        if item is None:
            return

        self.deleteRequested.emit(item.text())

    # --------------------------------------------------

    def selected_memory(self):

        item = self.memory_list.currentItem()

        if item is None:
            return None

        return item.text()