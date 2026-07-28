from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QHBoxLayout,
    QListWidgetItem,
    QFileDialog,

)

from gui.widgets.ui.page_header import PageHeader
from gui.widgets.ui.card import Card
from gui.widgets.ui.section import Section
from gui.widgets.ui.icon_button import IconButton
from gui.widgets.ui.empty_state import EmptyState

from gui.theme import (
    BACKGROUND,
    CARD_PADDING,
)


class FilesPage(QWidget):

    fileOpened = pyqtSignal(str)

    def __init__(
        self,
    ) -> None:
        
        super().__init__()

        self._build_ui()

    def _build_ui(
        self,
    ) -> None:

        self.setStyleSheet(f"""
        QWidget{{
            background:{BACKGROUND};
        }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
        )
        root.setSpacing(18)

        header = PageHeader(
            "📁 Files",
            "Recently opened files"
        )

        root.addWidget(header)

        self.file_list = QListWidget()
        self.file_list.itemDoubleClicked.connect(
            self._open_selected
        )

        file_card = Card()

        card_layout = QVBoxLayout(file_card)

        section = Section("Recent Files")

        card_layout.addWidget(section)

        card_layout.addWidget(self.file_list)

        root.addWidget(
            file_card,
            1,
        )

        self.empty_state = EmptyState(
            "📁",
            "No files yet",
            "Open a file to get started."
        )

        root.addWidget(self.empty_state)

        buttons = QHBoxLayout()

        self.open_button = IconButton(
            "📂",
            "Open File"
        )

        self.clear_button = IconButton(
            "🗑",
            "Clear"
        )

        self.open_button.clicked.connect(
            self._browse
        )

        self.clear_button.clicked.connect(
            self.clear_files
        )

        buttons.addWidget(self.open_button)
        buttons.addStretch()
        buttons.addWidget(self.clear_button)

        root.addLayout(buttons)

    # --------------------------------------------------

    def add_file(
        self, 
        path: str,
    ) -> None:

        self.empty_state.hide()
        self.file_list.show()

        self.file_list.addItem(
            QListWidgetItem(path)
        )

    def clear_files(
        self,
    ) -> None:

        self.file_list.clear()

        self.file_list.hide()

        self.empty_state.show()

    # --------------------------------------------------

    def _browse(
        self,
    ) -> None:

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
        )

        if file_name:

            self.add_file(file_name)

            self.fileOpened.emit(file_name)

    def _open_selected(
        self, 
        item: QListWidgetItem,
    ) -> None:

        self.fileOpened.emit(item.text())