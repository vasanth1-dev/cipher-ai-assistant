from PyQt6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QComboBox,
    QCheckBox,
    QPushButton,
    QMessageBox,
)


class SettingsWindow(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Cipher Settings")
        self.resize(500, 450)

        layout = QVBoxLayout()

        # -------------------------
        # AI Settings
        # -------------------------

        ai_group = QGroupBox("AI")

        ai_layout = QVBoxLayout()

        ai_layout.addWidget(QLabel("Preferred AI"))

        self.ai_combo = QComboBox()

        self.ai_combo.addItems([
            "Auto",
            "Offline (Ollama)",
            "Online (Gemini)",
        ])

        ai_layout.addWidget(self.ai_combo)

        ai_group.setLayout(ai_layout)

        layout.addWidget(ai_group)

        # -------------------------
        # Voice Settings
        # -------------------------

        voice_group = QGroupBox("Voice")

        voice_layout = QVBoxLayout()

        self.voice_checkbox = QCheckBox(
            "Enable Voice Response"
        )

        self.voice_checkbox.setChecked(True)

        voice_layout.addWidget(self.voice_checkbox)

        voice_group.setLayout(voice_layout)

        layout.addWidget(voice_group)

        # -------------------------
        # Startup
        # -------------------------

        startup_group = QGroupBox("Startup")

        startup_layout = QVBoxLayout()

        self.startup_checkbox = QCheckBox(
            "Start Cipher when Ubuntu starts"
        )

        startup_layout.addWidget(
            self.startup_checkbox
        )

        startup_group.setLayout(startup_layout)

        layout.addWidget(startup_group)

        # -------------------------
        # Save Button
        # -------------------------

        self.save_button = QPushButton("Save")

        self.save_button.clicked.connect(
            self.save_settings
        )

        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_settings(self):

        QMessageBox.information(
            self,
            "Cipher",
            "Settings saved successfully."
        )