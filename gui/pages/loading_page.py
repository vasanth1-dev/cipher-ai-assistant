from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar,
)

from gui.theme import (
    BACKGROUND,
    PRIMARY,
    TEXT,
    TEXT_MUTED,
)


class LoadingPage(QWidget):

    def __init__(self):
        super().__init__()

        self._build_ui()

    def _build_ui(self):

        self.setStyleSheet(f"""
        QWidget {{
            background:{BACKGROUND};
            color:{TEXT};
        }}

        QProgressBar {{
            border:none;
            background:#1E293B;
            border-radius:8px;
            height:18px;
            text-align:center;
        }}

        QProgressBar::chunk {{
            background:{PRIMARY};
            border-radius:8px;
        }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(20)

        layout.addStretch()

        self.logo = QLabel("Cipher")
        self.logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.logo.setStyleSheet("""
        font-size:34px;
        font-weight:bold;
        """)

        self.subtitle = QLabel("Professional AI Assistant")
        self.subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.subtitle.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:12pt;
        """)

        self.status = QLabel("Initializing...")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setStyleSheet(f"""
        color:{TEXT_MUTED};
        """)

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(False)

        layout.addWidget(self.logo)
        layout.addWidget(self.subtitle)
        layout.addSpacing(10)
        layout.addWidget(self.progress)
        layout.addWidget(self.status)

        layout.addStretch()

    # --------------------------------------------------

    def set_progress(self, value: int):
        self.progress.setValue(max(0, min(100, value)))

    def set_status(self, text: str):
        self.status.setText(text)