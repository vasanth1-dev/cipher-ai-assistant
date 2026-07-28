from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)
from gui.widgets.suggestion_card import SuggestionCard
from PyQt6.QtCore import pyqtSignal
from gui.theme import (
    TEXT,
    TEXT_MUTED,
    TITLE_SIZE,
    HEADER_SIZE,
    TEXT_SIZE,
    SMALL_SIZE,
    SPACING_LARGE,
)


class WelcomeWidget(QWidget):
    
    promptSelected = pyqtSignal(str)

    def __init__(
       self,
    ) -> None:
        super().__init__()

        self._build_ui()

    def _build_ui(self):

        root = QVBoxLayout(self)

        root.setAlignment(Qt.AlignmentFlag.AlignCenter)

        root.setSpacing(SPACING_LARGE)

        root.setContentsMargins(
            40,
            40,
            40,
            40,
        )

        # ------------------------------------
        # Logo
        # ------------------------------------

        logo = QLabel("🤖")

        logo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        logo.setStyleSheet(f"""
        font-size:{TITLE_SIZE + 18}px;
        """)

        root.addWidget(logo)

        # ------------------------------------
        # Title
        # ------------------------------------

        title = QLabel("Welcome to Cipher")

        title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        title.setStyleSheet(f"""
        font-size:{TITLE_SIZE}px;
        font-weight:bold;
        color:{TEXT};
        """)

        root.addWidget(title)

        # ------------------------------------
        # Subtitle
        # ------------------------------------

        subtitle = QLabel(
            "Your Ubuntu AI Assistant"
        )

        subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        subtitle.setStyleSheet(f"""
        font-size:{HEADER_SIZE}pt;
        color:{TEXT_MUTED};
        """)

        root.addWidget(subtitle)

        root.addSpacing(10)

        # ------------------------------------
        # Suggestions
        # ------------------------------------

        cards = [

            (
                "💬",
                "Ask Coding",
                "Write a Python program to reverse a string.",
            ),

            (
                "📁",
                "Files",
                "Open my Downloads folder.",
            ),

            (
                "🧠",
                "Memory",
                "Remember that my name is Vasanth.",
            ),

            (
                "⚙",
                "System",
                "Show CPU and RAM usage.",
            ),

        ]

        for icon, title, prompt in cards:

            card = SuggestionCard(
                icon,
                title,
                prompt,
            )
            card.clicked.connect(
                self.promptSelected.emit
            )

            root.addWidget(card)

        root.addSpacing(10)

        # ------------------------------------
        # Footer
        # ------------------------------------

        footer = QLabel(
            "Start typing below..."
        )

        footer.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        footer.setStyleSheet(f"""
        font-size:{SMALL_SIZE}pt;
        color:{TEXT_MUTED};
        """)

        root.addWidget(footer)