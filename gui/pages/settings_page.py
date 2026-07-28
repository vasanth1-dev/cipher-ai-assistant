from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QCheckBox,
    QComboBox,
    QSlider,
)

from gui.theme import (
    BACKGROUND,
    CARD_PADDING,
    SPACING,
)

from gui.widgets.ui.page_header import PageHeader
from gui.widgets.ui.card import Card
from gui.widgets.ui.section import Section
from gui.widgets.ui.icon_button import IconButton


class SettingsPage(QWidget):

    saveClicked = pyqtSignal()
    resetClicked = pyqtSignal()

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
        }}
        """)

        root = QVBoxLayout(self)

        root.setContentsMargins(
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
            CARD_PADDING,
        )

        root.setSpacing(SPACING)

        # --------------------------------------------------
        # Header
        # --------------------------------------------------

        header = PageHeader(
            "⚙ Settings",
            "Configure Cipher preferences"
        )

        root.addWidget(header)

        # --------------------------------------------------
        # General
        # --------------------------------------------------

        general_card = Card()
        general_layout = QVBoxLayout(general_card)

        general_layout.addWidget(
            Section("General")
        )

        general_form = QFormLayout()

        self.assistant_name = QLineEdit("Cipher")
        self.user_name = QLineEdit()

        self.startup = QCheckBox("Start on Login")
        self.tray = QCheckBox("Minimize to Tray")

        general_form.addRow("Assistant", self.assistant_name)
        general_form.addRow("User", self.user_name)
        general_form.addRow("", self.startup)
        general_form.addRow("", self.tray)

        general_layout.addLayout(general_form)

        root.addWidget(general_card)

        # --------------------------------------------------
        # AI
        # --------------------------------------------------

        ai_card = Card()
        ai_layout = QVBoxLayout(ai_card)

        ai_layout.addWidget(
            Section("AI")
        )

        ai_form = QFormLayout()

        self.model = QComboBox()

        self.model.addItems([
            "qwen2.5",
            "llama3",
            "phi3",
        ])

        self.temperature = QSlider(
            Qt.Orientation.Horizontal
        )

        self.temperature.setRange(0, 100)
        self.temperature.setValue(20)

        ai_form.addRow("Model", self.model)
        ai_form.addRow("Temperature", self.temperature)

        ai_layout.addLayout(ai_form)

        root.addWidget(ai_card)

        # --------------------------------------------------
        # Voice
        # --------------------------------------------------

        voice_card = Card()
        voice_layout = QVBoxLayout(voice_card)

        voice_layout.addWidget(
            Section("Voice")
        )

        voice_form = QFormLayout()

        self.voice_enabled = QCheckBox(
            "Enable Voice"
        )

        self.rate = QSlider(
            Qt.Orientation.Horizontal
        )

        self.rate.setRange(100, 250)
        self.rate.setValue(170)

        self.volume = QSlider(
            Qt.Orientation.Horizontal
        )

        self.volume.setRange(0, 100)
        self.volume.setValue(100)

        voice_form.addRow("", self.voice_enabled)
        voice_form.addRow("Speech Rate", self.rate)
        voice_form.addRow("Volume", self.volume)

        voice_layout.addLayout(voice_form)

        root.addWidget(voice_card)

        # --------------------------------------------------
        # Appearance
        # --------------------------------------------------

        appearance_card = Card()
        appearance_layout = QVBoxLayout(
            appearance_card
        )

        appearance_layout.addWidget(
            Section("Appearance")
        )

        appearance_form = QFormLayout()

        self.theme = QComboBox()

        self.theme.addItems([
            "Dark",
            "Light",
        ])

        appearance_form.addRow(
            "Theme",
            self.theme
        )

        appearance_layout.addLayout(
            appearance_form
        )

        root.addWidget(appearance_card)

        root.addStretch()

        # --------------------------------------------------
        # Buttons
        # --------------------------------------------------

        buttons = QHBoxLayout()

        buttons.addStretch()

        self.reset_button = IconButton(
            "↺",
            "Reset"
        )

        self.save_button = IconButton(
            "💾",
            "Save"
        )

        self.reset_button.clicked.connect(
            self.resetClicked.emit
        )

        self.save_button.clicked.connect(
            self.saveClicked.emit
        )

        buttons.addWidget(
            self.reset_button
        )

        buttons.addWidget(
            self.save_button
        )

        root.addLayout(buttons)