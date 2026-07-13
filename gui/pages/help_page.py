from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QFrame,
    QTextBrowser,
)

from gui.theme import (
    BACKGROUND,
    SURFACE,
    BORDER,
    TEXT,
    TEXT_MUTED,
)


class HelpPage(QWidget):

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

        QTextBrowser {{
            background:{SURFACE};
            color:{TEXT};
            border:none;
            font-size:11pt;
            padding:10px;
        }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(18)

        title = QLabel("❓ Help")
        title.setStyleSheet("""
        font-size:24px;
        font-weight:bold;
        """)

        subtitle = QLabel("Cipher User Guide")
        subtitle.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:10pt;
        """)

        card = QFrame()

        layout = QVBoxLayout(card)
        layout.setContentsMargins(20, 20, 20, 20)

        self.help_text = QTextBrowser()

        self.help_text.setHtml("""
        <h2>Welcome to Cipher</h2>

        <h3>Chat</h3>
        <ul>
            <li>Type your message and press <b>Enter</b>.</li>
            <li>Use the microphone button for voice input.</li>
        </ul>

        <h3>Dashboard</h3>
        <ul>
            <li>View CPU, RAM, Disk and System information.</li>
        </ul>

        <h3>Memory</h3>
        <ul>
            <li>Search, export and manage saved memories.</li>
        </ul>

        <h3>Settings</h3>
        <ul>
            <li>Configure AI, Voice and Appearance.</li>
        </ul>

        <h3>Plugins</h3>
        <ul>
            <li>Enable or disable installed plugins.</li>
        </ul>

        <h3>Voice Commands</h3>
        <ul>
            <li>Use your configured wake word to start voice interaction.</li>
        </ul>
        """)

        layout.addWidget(self.help_text)

        root.addWidget(title)
        root.addWidget(subtitle)
        root.addWidget(card)