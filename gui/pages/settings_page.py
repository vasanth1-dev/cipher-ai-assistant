from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QFormLayout,
    QLineEdit,
    QCheckBox,
    QComboBox,
    QSlider,
    QPushButton,
    QHBoxLayout,
)

from gui.theme import (
    BACKGROUND,
    SURFACE,
    BORDER,
    PRIMARY,
    PRIMARY_HOVER,
    TEXT,
    TEXT_MUTED,
)


class SettingsPage(QWidget):

    saveClicked = pyqtSignal()
    resetClicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self._build_ui()

    def _build_ui(self):

        self.setStyleSheet(f"""
        QWidget{{
            background:{BACKGROUND};
            color:{TEXT};
        }}

        QGroupBox{{
            background:{SURFACE};
            border:1px solid {BORDER};
            border-radius:12px;
            margin-top:12px;
            padding-top:12px;
            font-weight:bold;
        }}

        QLineEdit,
        QComboBox{{
            background:{BACKGROUND};
            color:{TEXT};
            border:1px solid {BORDER};
            border-radius:8px;
            padding:8px;
            min-height:36px;
        }}

        QSlider::groove:horizontal{{
            height:6px;
            background:{BORDER};
            border-radius:3px;
        }}

        QSlider::handle:horizontal{{
            background:{PRIMARY};
            width:16px;
            margin:-5px 0;
            border-radius:8px;
        }}

        QPushButton{{
            background:{PRIMARY};
            color:white;
            border:none;
            border-radius:10px;
            padding:10px 18px;
            font-weight:bold;
        }}

        QPushButton:hover{{
            background:{PRIMARY_HOVER};
        }}
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(20, 20, 20, 20)
        root.setSpacing(18)

        title = QLabel("⚙ Settings")
        title.setStyleSheet("""
        font-size:24px;
        font-weight:bold;
        """)

        subtitle = QLabel("Configure Cipher")
        subtitle.setStyleSheet(f"""
        color:{TEXT_MUTED};
        font-size:10pt;
        """)

        root.addWidget(title)
        root.addWidget(subtitle)

        general = QGroupBox("General")
        general_form = QFormLayout(general)

        self.assistant_name = QLineEdit("Cipher")
        self.user_name = QLineEdit()

        self.startup = QCheckBox("Start on Login")
        self.tray = QCheckBox("Minimize to Tray")

        general_form.addRow("Assistant", self.assistant_name)
        general_form.addRow("User", self.user_name)
        general_form.addRow("", self.startup)
        general_form.addRow("", self.tray)

        root.addWidget(general)

        ai = QGroupBox("AI")
        ai_form = QFormLayout(ai)

        self.model = QComboBox()
        self.model.addItems([
            "qwen2.5",
            "llama3",
            "phi3",
        ])

        self.temperature = QSlider(Qt.Orientation.Horizontal)
        self.temperature.setRange(0, 100)
        self.temperature.setValue(20)

        ai_form.addRow("Model", self.model)
        ai_form.addRow("Temperature", self.temperature)

        root.addWidget(ai)

        voice = QGroupBox("Voice")
        voice_form = QFormLayout(voice)

        self.voice_enabled = QCheckBox("Enable Voice")

        self.rate = QSlider(Qt.Orientation.Horizontal)
        self.rate.setRange(100, 250)
        self.rate.setValue(170)

        self.volume = QSlider(Qt.Orientation.Horizontal)
        self.volume.setRange(0, 100)
        self.volume.setValue(100)

        voice_form.addRow("", self.voice_enabled)
        voice_form.addRow("Speech Rate", self.rate)
        voice_form.addRow("Volume", self.volume)

        root.addWidget(voice)

        appearance = QGroupBox("Appearance")
        appearance_form = QFormLayout(appearance)

        self.theme = QComboBox()
        self.theme.addItems([
            "Dark",
            "Light",
        ])

        appearance_form.addRow("Theme", self.theme)

        root.addWidget(appearance)

        root.addStretch()

        buttons = QHBoxLayout()
        buttons.addStretch()

        self.reset_button = QPushButton("Reset")
        self.save_button = QPushButton("Save")

        self.reset_button.clicked.connect(
            self.resetClicked.emit
        )

        self.save_button.clicked.connect(
            self.saveClicked.emit
        )

        buttons.addWidget(self.reset_button)
        buttons.addWidget(self.save_button)

        root.addLayout(buttons)