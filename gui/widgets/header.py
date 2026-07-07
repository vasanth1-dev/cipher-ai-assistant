from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
)


class StatusBadge(QLabel):

    def __init__(self):
        super().__init__("● Online")

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setMinimumHeight(32)

        self.setStyleSheet("""
        QLabel{
            background:#14532D;
            color:#22C55E;
            border-radius:16px;
            padding:6px 14px;
            font-weight:bold;
        }
        """)

    def set_online(self):
        self.setText("● Online")
        self.setStyleSheet("""
        QLabel{
            background:#14532D;
            color:#22C55E;
            border-radius:16px;
            padding:6px 14px;
            font-weight:bold;
        }
        """)

    def set_offline(self):
        self.setText("● Offline")
        self.setStyleSheet("""
        QLabel{
            background:#451A03;
            color:#F59E0B;
            border-radius:16px;
            padding:6px 14px;
            font-weight:bold;
        }
        """)

    def set_listening(self):
        self.setText("● Listening")
        self.setStyleSheet("""
        QLabel{
            background:#1E3A8A;
            color:#60A5FA;
            border-radius:16px;
            padding:6px 14px;
            font-weight:bold;
        }
        """)


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
        layout.setContentsMargins(20, 16, 20, 16)

        left = QVBoxLayout()

        self.title = QLabel("Cipher AI Assistant")
        self.title.setStyleSheet("""
        font-size:22px;
        font-weight:bold;
        """)

        self.subtitle = QLabel("Professional Ubuntu Desktop Assistant")
        self.subtitle.setStyleSheet("""
        color:#9CA3AF;
        font-size:10pt;
        """)

        left.addWidget(self.title)
        left.addWidget(self.subtitle)

        layout.addLayout(left)
        layout.addStretch()

        self.status = StatusBadge()

        self.settings_button = QPushButton("⚙ Settings")
        self.settings_button.setFixedHeight(36)

        layout.addWidget(self.status)
        layout.addSpacing(10)
        layout.addWidget(self.settings_button)