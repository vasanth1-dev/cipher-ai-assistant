from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QProgressBar,
)

from gui.theme import (
    BACKGROUND,
    SURFACE,
    BORDER,
    PRIMARY,
    SUCCESS,
    WARNING,
    TEXT,
    TEXT_MUTED,
)


class VoicePage(QWidget):

    def __init__(self):
        super().__init__()

        self._build_ui()

    def _build_ui(self):

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

        QProgressBar {{
            border:none;
            background:#1E293B;
            border-radius:8px;
            text-align:center;
            height:18px;
        }}

        QProgressBar::chunk {{
            background:{PRIMARY};
            border-radius:8px;
        }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(20)

        title = QLabel("🎤 Voice")
        title.setStyleSheet("""
        font-size:24px;
        font-weight:bold;
        """)

        subtitle = QLabel("Voice Assistant Status")
        subtitle.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:10pt;
        """)

        root.addWidget(title)
        root.addWidget(subtitle)

        card = QFrame()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        self.status = QLabel("Ready")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status.setStyleSheet(f"""
        font-size:20px;
        font-weight:bold;
        color:{SUCCESS};
        """)

        self.wave = QProgressBar()
        self.wave.setRange(0, 100)
        self.wave.setValue(0)
        self.wave.setTextVisible(False)

        self.info = QLabel("Waiting for voice input...")
        self.info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.info.setStyleSheet(f"""
        color:{TEXT_MUTED};
        """)

        layout.addWidget(self.status)
        layout.addWidget(self.wave)
        layout.addWidget(self.info)

        root.addWidget(card)
        root.addStretch()

    # --------------------------------------------------

    def set_ready(self):

        self.status.setText("Ready")
        self.status.setStyleSheet(f"""
        color:{SUCCESS};
        font-size:20px;
        font-weight:bold;
        """)

        self.info.setText("Waiting for voice input...")
        self.wave.setValue(0)

    def set_listening(self):

        self.status.setText("Listening")
        self.status.setStyleSheet(f"""
        color:{PRIMARY};
        font-size:20px;
        font-weight:bold;
        """)

        self.info.setText("Listening...")
        self.wave.setValue(35)

    def set_thinking(self):

        self.status.setText("Thinking")
        self.status.setStyleSheet(f"""
        color:{WARNING};
        font-size:20px;
        font-weight:bold;
        """)

        self.info.setText("Generating response...")
        self.wave.setValue(70)

    def set_speaking(self):

        self.status.setText("Speaking")
        self.status.setStyleSheet(f"""
        color:{PRIMARY};
        font-size:20px;
        font-weight:bold;
        """)

        self.info.setText("Speaking...")
        self.wave.setValue(100)