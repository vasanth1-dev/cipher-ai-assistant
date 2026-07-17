from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)
from gui.theme import (
    SURFACE,
    PRIMARY,
    SUCCESS,
    WARNING,
    TEXT,
    TEXT_MUTED,
    TITLE_SIZE,
    SMALL_SIZE,
    CARD_PADDING,
    SPACING,
    SPACING_LARGE,
    BUTTON_HEIGHT,
)


class StatusBadge(QLabel):

    def __init__(self):
        super().__init__("● Online")

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumHeight(32)

        self.setStyleSheet(f"""
        QFrame#Header{{
            background:{SURFACE};
            border-radius:16px;
        }}

        QLabel{{
            color:{TEXT};
        }}

        QPushButton{{
            background:{PRIMARY};
            color:white;
            border:none;
            border-radius:10px;
            padding:8px 16px;
        }}

        QPushButton:hover{{
            background:#60A5FA;
        }}
        """)

    def _update_style(
            self,
            background,
            foreground,
    ):
        
        self.setStyleSheet(f"""
        QLabel{{
            background:{background};
            color:{foreground};
            border-radius:16px;
            padding:6px 14px;
            font-weight:bold;
        }}
        """)

    def set_online(self):

        self.setText("● Online")

        self._update_style(
            "#14532D",
            SUCCESS,
        )

    def set_offline(self):

        self.setText("● Offline")

        self._update_style(
            "#451A03",
            WARNING,
        )

    def set_listening(self):

        self.setText("● Listening")

        self._update_style(
            "#1E3A8A",
            PRIMARY,
        )

    def set_thinking(self):

        self.setText("● Thinking")

        self._update_style(
            "#4C1D95",
            "#C084FC",
        )


    def set_speaking(self):

        self.setText("● Speaking")

        self._update_style(
            "#7C2D12",
            "#FB923C",
        )


    def set_ready(self):

        self.setText("● Ready")

        self._update_style(
            "#14532D",
            SUCCESS,
        )


class Header(QFrame):

    def __init__(self):
        super().__init__()

        self.setObjectName("Header")

        self.setStyleSheet("""
        QFrame#Header{
            background:#1F2937;
            border-radius:14px;
        }

        QLabel{
            color:white;
        }

        QPushButton{
            background:#374151;
            color:white;
            border:none;
            border-radius:10px;
            padding:8px 16px;
        }

        QPushButton:hover{
            background:#4B5563;
        }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            CARD_PADDING,
            SPACING,
            CARD_PADDING,
            SPACING,
        )
        layout.setSpacing(SPACING_LARGE)

        left = QVBoxLayout()

        self.title = QLabel(
            "🤖 Cipher"
        )
        self.title.setStyleSheet(f"""
        font-size:{TITLE_SIZE}px;
        font-weight:bold;
        color:{TEXT};
        """)

        self.subtitle = QLabel(" Ubuntu Desktop AI Assistant")
        self.subtitle.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:{SMALL_SIZE}pt;
        """)

        left.addWidget(self.title)
        left.addWidget(self.subtitle)

        layout.addLayout(left)
        layout.addStretch()

        info = QVBoxLayout()

        info.setSpacing(4)

        self.model = QLabel("🤖 qwen2.5")
        self.voice = QLabel("🎤 Ready")
        self.memory = QLabel("🧠 Active")

        for label in (
            self.model,
            self.voice,
            self.memory,
        ):

            label.setStyleSheet(f"""
            color:{TEXT_MUTED};
            font-size:{SMALL_SIZE}pt;
            """)

            info.addWidget(label)

        layout.addLayout(info)
        layout.addSpacing(
            SPACING_LARGE
        )

        self.status = StatusBadge()

        self.settings_button = QPushButton("⚙")
        self.settings_button.setToolTip(
            "Settings"
        )
        self.settings_button.setFixedSize(
            BUTTON_HEIGHT,
            BUTTON_HEIGHT,
        )

        layout.addWidget(self.status)
        layout.addSpacing(10)
        layout.addWidget(self.settings_button)

    def set_model(self, name):

        self.model.setText(
            f"🤖 {name}"
        )


    def set_voice_status(self, status):

        self.voice.setText(
            f"🎤 {status}"
        )


    def set_memory_status(self, status):

        self.memory.setText(
            f"🧠 {status}"
        )

    def set_online(self):

        self.status.set_online()

        self.set_voice_status(
            "Ready"
        )


    def set_listening(self):

        self.status.set_listening()

        self.set_voice_status(
            "Listening"
        )


    def set_thinking(self):

        self.status.set_thinking()

        self.set_voice_status(
            "Thinking"
        )


    def set_speaking(self):

        self.status.set_speaking()

        self.set_voice_status(
            "Speaking"
        )

    def set_ready(self):

        self.status.set_ready()

        self.set_voice_status(
            "Ready"
        )