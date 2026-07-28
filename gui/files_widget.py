from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class FilesWidget(QWidget):

    openRequested = pyqtSignal(str)
    refreshRequested = pyqtSignal()
    searchRequested = pyqtSignal(str)
    folderChanged = pyqtSignal(str)

    def __init__(
       self,
    ) -> None:
        super().__init__()

        self.current_folder = ""

        self._build_ui()

    # --------------------------------------------------

    def _build_ui(self):

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(15)

        title = QLabel("📁 Files")
        title.setStyleSheet("""
        font-size:22px;
        font-weight:bold;
        color:white;
        """)

        subtitle = QLabel(
            "Browse and open files from Cipher."
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

        self.path_edit = QLineEdit()
        self.path_edit.setPlaceholderText("Folder path...")

        self.browse_btn = QPushButton("Browse")
        self.refresh_btn = QPushButton("Refresh")

        bar.addWidget(self.path_edit)
        bar.addWidget(self.browse_btn)
        bar.addWidget(self.refresh_btn)

        root.addWidget(toolbar)

        self.search = QLineEdit()
        self.search.setPlaceholderText("Search files...")

        root.addWidget(self.search)

        self.file_list = QListWidget()
        self.file_list.setStyleSheet("""
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

        root.addWidget(self.file_list)

        self.search.textChanged.connect(
            self.searchRequested.emit
        )

        self.refresh_btn.clicked.connect(
            self.refreshRequested.emit
        )

        self.browse_btn.clicked.connect(
            self._browse_folder
        )

        self.file_list.itemDoubleClicked.connect(
            lambda item: self.openRequested.emit(item.text())
        )

    # --------------------------------------------------

    def _browse_folder(self):

        folder = QFileDialog.getExistingDirectory(
            self,
            "Select Folder",
            self.current_folder or "",
        )

        if not folder:
            return

        self.current_folder = folder
        self.path_edit.setText(folder)
        self.folderChanged.emit(folder)

    # --------------------------------------------------

    def set_files(self, files):

        self.file_list.clear()

        for file in files:
            self.file_list.addItem(str(file))

    # --------------------------------------------------

    def clear_files(self):

        self.file_list.clear()

    # --------------------------------------------------

    def selected_file(self):

        item = self.file_list.currentItem()

        if item is None:
            return None

        return item.text()