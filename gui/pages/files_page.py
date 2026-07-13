from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
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


class FilesPage(QWidget):

    fileOpened = pyqtSignal(str)

    def __init__(self):
        super().__init__()

        self._build_ui()

    def _build_ui(self):

        self.setStyleSheet(f"""
        QWidget{{
            background:{BACKGROUND};
            color:{TEXT};
        }}

        QListWidget{{
            background:{SURFACE};
            border:1px solid {BORDER};
            border-radius:12px;
        }}

        QListWidget::item{{
            padding:10px;
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
        root.setSpacing(18)

        title = QLabel("📁 Files")
        title.setStyleSheet("""
        font-size:24px;
        font-weight:bold;
        """)

        subtitle = QLabel("Recently opened files")

        subtitle.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:10pt;
        """)

        root.addWidget(title)
        root.addWidget(subtitle)

        self.file_list = QListWidget()
        self.file_list.itemDoubleClicked.connect(
            self._open_selected
        )

        root.addWidget(self.file_list)

        buttons = QHBoxLayout()

        self.open_button = QPushButton("Open File")
        self.clear_button = QPushButton("Clear List")

        self.open_button.clicked.connect(
            self._browse
        )

        self.clear_button.clicked.connect(
            self.file_list.clear
        )

        buttons.addWidget(self.open_button)
        buttons.addStretch()
        buttons.addWidget(self.clear_button)

        root.addLayout(buttons)

    # --------------------------------------------------

    def add_file(self, path):

        self.file_list.addItem(
            QListWidgetItem(path)
        )

    def clear_files(self):

        self.file_list.clear()

    # --------------------------------------------------

    def _browse(self):

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
        )

        if file_name:

            self.add_file(file_name)

            self.fileOpened.emit(file_name)

    def _open_selected(self, item):

        self.fileOpened.emit(item.text())