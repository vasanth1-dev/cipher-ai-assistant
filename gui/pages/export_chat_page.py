from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QHBoxLayout,
    QFileDialog,
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


class ExportChatPage(QWidget):

    exportRequested = pyqtSignal(str)

    def __init__(
        self,
    ) -> None:
        super().__init__()

        self._build_ui()

    def _build_ui(
        self,
    ) -> None:

        self.setStyleSheet(f"""
        QWidget {{
            background:{BACKGROUND};
            color:{TEXT};
        }}

        QTextEdit {{
            background:{SURFACE};
            color:{TEXT};
            border:1px solid {BORDER};
            border-radius:12px;
            padding:10px;
        }}

        QPushButton {{
            background:{PRIMARY};
            color:white;
            border:none;
            border-radius:10px;
            padding:10px 18px;
            font-weight:bold;
        }}

        QPushButton:hover {{
            background:{PRIMARY_HOVER};
        }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(15)

        title = QLabel("📄 Export Chat")
        title.setStyleSheet("""
        font-size:24px;
        font-weight:bold;
        """)

        subtitle = QLabel("Preview and export your conversation")
        subtitle.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:10pt;
        """)

        self.preview = QTextEdit()
        self.preview.setReadOnly(True)

        buttons = QHBoxLayout()

        self.export_button = QPushButton("Export")
        self.clear_button = QPushButton("Clear Preview")

        self.export_button.clicked.connect(
            self._export
        )

        self.clear_button.clicked.connect(
            self.preview.clear
        )

        buttons.addStretch()
        buttons.addWidget(self.clear_button)
        buttons.addWidget(self.export_button)

        root.addWidget(title)
        root.addWidget(subtitle)
        root.addWidget(self.preview)
        root.addLayout(buttons)

    # --------------------------------------------------

    def set_chat(
        self, 
        text: str
    ) -> None:

        self.preview.setPlainText(text)

    # --------------------------------------------------

    def _export(
        self,
    ) -> None:

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Export Chat",
            "chat.txt",
            "Text Files (*.txt);;Markdown (*.md)"
        )

        if filename:
            self.exportRequested.emit(filename)