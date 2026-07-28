from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QFrame,
)

from gui.theme import (
    BACKGROUND,
    SURFACE,
    BORDER,
    TEXT,
    TEXT_MUTED,
)


class AboutPage(QWidget):
    """About page for the Cipher application."""

    def __init__(
        self,
    ) -> None:
        super().__init__()

        self.setStyleSheet(f"""
        QWidget {{
            background:{BACKGROUND};
            color:{TEXT};
        }}

        QFrame {{
            background:{SURFACE};
            border:1px solid {BORDER};
            border-radius:14px;
        }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)

        title = QLabel("About Cipher")
        title.setStyleSheet("""
        font-size:24px;
        font-weight:bold;
        """)

        subtitle = QLabel("Professional Ubuntu AI Assistant")
        subtitle.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:11pt;
        """)

        card = QFrame()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        info = [
            ("Version", "2.0.0"),
            ("Edition", "Ubuntu"),
            ("AI Model", "qwen2.5"),
            ("Python", "3.x"),
            ("Framework", "PyQt6"),
            ("Speech", "Faster Whisper"),
            ("LLM", "Ollama"),
            ("Developer", "Vasanth"),
        ]

        for key, value in info:

            row = QLabel(f"<b>{key}</b> : {value}")
            row.setTextFormat(Qt.TextFormat.RichText)
            layout.addWidget(row)

        layout.addStretch()

        copyright_label = QLabel(
            "© 2026 Cipher AI Assistant"
        )

        copyright_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        copyright_label.setStyleSheet(f"""
        color:{TEXT_MUTED};
        """)

        root.addWidget(title)
        root.addWidget(subtitle)
        root.addSpacing(15)
        root.addWidget(card)
        root.addStretch()
        root.addWidget(copyright_label)