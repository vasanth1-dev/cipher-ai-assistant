from PyQt6.QtCore import (
    Qt,
    pyqtSignal,
)

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
    BORDER,
    get_button_style,
    WARNING,
    TEXT,
    TEXT_MUTED,
    SMALL_SIZE,
    CARD_PADDING,
    SPACING,
    SPACING_LARGE,
    BUTTON_HEIGHT,
    STATUS_ONLINE_BG,
    STATUS_OFFLINE_BG,
    STATUS_LISTENING_BG,
    STATUS_THINKING_BG,
    STATUS_SPEAKING_BG,
    STATUS_READY_BG,
    STATUS_SPEAKING_TEXT,
    STATUS_THINKING_TEXT,
)


class StatusBadge(QLabel):


    def __init__(
       self,
    ) -> None:
        super().__init__("● Online")

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumHeight(32)

        self.setStyleSheet(f"""

        QLabel{{
            color:{TEXT};
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
            STATUS_ONLINE_BG,
            SUCCESS,
        )

    def set_offline(self):

        self.setText("● Offline")

        self._update_style(
            STATUS_OFFLINE_BG,
            WARNING,
        )

    def set_listening(self):

        self.setText("● Listening")

        self._update_style(
            STATUS_LISTENING_BG,
            PRIMARY,
        )

    def set_thinking(self):

        self.setText("● Thinking")

        self._update_style(
            STATUS_THINKING_BG,
            STATUS_THINKING_TEXT,
        )


    def set_speaking(self):

        self.setText("● Speaking")

        self._update_style(
            STATUS_SPEAKING_BG,
            STATUS_SPEAKING_TEXT,
        )


    def set_ready(self):

        self.setText("● Ready")

        self._update_style(
            STATUS_READY_BG,
            SUCCESS,
        )


class Header(QFrame):

    settingsClicked = pyqtSignal()

    def __init__(
       self,
    ) -> None:
        super().__init__()

        self.setObjectName("Header")

        self.setStyleSheet(f"""
        QFrame#Header{{
            background:{SURFACE};
            border:1px solid {BORDER};
            border-radius:16px;
        }}

        QLabel{{
            color:white;
        }}

        QPushButton{{
            background:#374151;
            color:white;
            border:none;
            border-radius:10px;
            padding:8px 16px;
        }}

        QPushButton:hover{{
            background:#4B5563;
        }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
        )
        layout.setSpacing(SPACING_LARGE)

        left = QVBoxLayout()

        self.title = QLabel(
            "🤖 Cipher"
        )
        self.title.setStyleSheet(f"""
        font-size:20px;
        font-weight:700;
        letter-spacing:0.5px;
        color:{TEXT};
        """)

        self.subtitle = QLabel("Ubuntu Desktop AI Assistant")
        self.subtitle.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:10pt;
        """)

        left.addWidget(self.title)
        left.addWidget(self.subtitle)

        layout.addLayout(left)
        layout.addStretch()

        info = QVBoxLayout()

        info.setSpacing(SPACING // 2)

        self.model = QLabel("🤖 Model : qwen2.5")
        self.voice = QLabel("🎤 Voice : Ready")
        self.memory = QLabel("🧠 Memory : Active")

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

        self.settings_button = QPushButton("⚙️")
        self.settings_button.setToolTip(
            "Settings"
        )
        self.settings_button.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.settings_button.setStyleSheet(get_button_style())

        self.settings_button.setFixedSize(
            BUTTON_HEIGHT,
            BUTTON_HEIGHT
        )

        self.settings_button.clicked.connect(
            self.settingsClicked.emit
        )

        layout.addWidget(self.status)
        layout.addSpacing(SPACING)
        layout.addWidget(self.settings_button)

        self.status.set_ready()

    def set_model(self, name: str):

        self.model.setText(
            f"🤖 Model : {name}"
        )


    def set_voice_status(
        self, 
        status: str,
    ):

        self.voice.setText(
            f"🎤 Voice : {status}"
        )


    def set_memory_status(
        self,
        status: str
    ):

        self.memory.setText(
            f"🧠 Memory : {status}"
        )

    def _set_status(
        self,
        badge_method,
        voice_status,
    ):

        badge_method()

        self.set_voice_status(
            voice_status
        )

    def set_online(self):

        self._set_status(
            self.status.set_online,
            "Ready",
        )

    def set_listening(self):

        self._set_status(
            self.status.set_listening,
            "Listening",
        )

    def set_thinking(self):

        self._set_status(
            self.status.set_thinking,
            "Thinking",
        )

    def set_speaking(self):

        self._set_status(
            self.status.set_speaking,
            "Speaking",
        )

    def set_ready(self):

        self._set_status(
            self.status.set_ready,
            "Ready",
        )