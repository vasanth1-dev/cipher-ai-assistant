from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
)


class CodeBlock(QFrame):

    def __init__(
        self,
        code: str,
        language: str = "text",
    ):
        super().__init__()

        self.code = code
        self.language = language

        self._build_ui()

    # --------------------------------------------------

    def _build_ui(self):

        self.setObjectName("CodeBlock")

        self.setStyleSheet("""
        QFrame#CodeBlock{
            background:#0F172A;
            border:1px solid #334155;
            border-radius:10px;
        }

        QLabel{
            color:#CBD5E1;
            font-weight:bold;
            background:transparent;
        }

        QPushButton{
            background:#2563EB;
            color:white;
            border:none;
            border-radius:6px;
            padding:5px 10px;
        }

        QPushButton:hover{
            background:#3B82F6;
        }

        QTextEdit{
            background:transparent;
            border:none;
            color:#E2E8F0;
        }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(10, 10, 10, 10)

        header = QHBoxLayout()

        lang = QLabel(self.language)

        copy_btn = QPushButton("Copy")
        copy_btn.clicked.connect(self.copy_code)

        header.addWidget(lang)
        header.addStretch()
        header.addWidget(copy_btn)

        root.addLayout(header)

        self.editor = QTextEdit()
        self.editor.setReadOnly(True)
        self.editor.setPlainText(self.code)

        font = QFont("JetBrains Mono")
        font.setPointSize(10)
        self.editor.setFont(font)

        self.editor.setLineWrapMode(
            QTextEdit.LineWrapMode.NoWrap
        )

        root.addWidget(self.editor)

    # --------------------------------------------------

    def copy_code(self):

        QApplication.clipboard().setText(
            self.code
        )