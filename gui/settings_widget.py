from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QLabel,
    QComboBox,
    QCheckBox,
    QPushButton,
    QHBoxLayout,
    QListWidget,
    QStackedWidget,
    QFileDialog,
    QMessageBox,
    QInputDialog,
    QLineEdit,
    QFormLayout,
)
from PyQt6.QtGui import (
    QKeySequence,
    QShortcut,
)
import platform

from gui.theme import (
    register_widget,
    unregister_widget,
    load_custom_stylesheet,
)
from PyQt6.QtCore import QT_VERSION_STR
from services.settings_service import SettingsService


class SettingsWidget(QWidget):

    def __init__(
       self,
    ) -> None:
        super().__init__()

        register_widget(self)

        self.settings_service = SettingsService()
        
        self.setWindowTitle("Cipher Settings")
        self.setWindowModified(False)
        self.resize(500, 450)

        main_layout = QHBoxLayout()

        navigation = QListWidget()

        navigation.setFixedWidth(180)

        navigation.addItems([
            "General",
            "AI",
            "Voice",
            "Appearance",
            "About",
        ])

        self.pages = QStackedWidget()

        main_layout.addWidget(navigation)
        main_layout.addWidget(self.pages, 1)

        content_layout = QVBoxLayout()

        # -------------------------
        # Search
        # -------------------------

        self.search_edit = QLineEdit()

        self.search_edit.setPlaceholderText(
            "Search settings..."
        )

        self.search_edit.textChanged.connect(
            self.filter_settings
        )

        content_layout.addWidget(self.search_edit)

        # -------------------------
        # General
        # -------------------------

        general_group = QGroupBox("General")

        self.general_group = general_group

        general_layout = QVBoxLayout()

        self.minimize_tray_checkbox = QCheckBox(
            "Minimize to System Tray"
        )

        self.minimize_tray_checkbox.setChecked(True)

        general_layout.addWidget(
            self.minimize_tray_checkbox
        )

        self.launch_startup_checkbox = QCheckBox(
            "Launch on Startup"
        )

        general_layout.addWidget(
            self.launch_startup_checkbox
        )

        general_group.setLayout(general_layout)

        content_layout.addWidget(general_group)

        # -------------------------
        # AI Settings
        # -------------------------

        ai_group = QGroupBox("AI")

        self.ai_group = ai_group

        ai_layout = QVBoxLayout()

        ai_layout.addWidget(QLabel("Preferred AI"))

        self.ai_combo = QComboBox()

        self.ai_combo.addItems([
            "Auto",
            "qwen2.5",
            "llama3",
            "gemma3",
            "phi3",
            "Gemini",
        ])

        ai_layout.addWidget(self.ai_combo)

        ai_layout.addWidget(
            QLabel("Temperature")
        )

        self.temperature_combo = QComboBox()

        self.temperature_combo.addItems([
            "0.0",
            "0.2",
            "0.5",
            "0.7",
            "1.0",
        ])

        self.temperature_combo.setCurrentText("0.2")

        ai_layout.addWidget(
            self.temperature_combo
        )

        ai_group.setLayout(ai_layout)

        content_layout.addWidget(ai_group)


        self.setStyleSheet("""
        QWidget{
            background:#111827;
            color:white;
        }

        QGroupBox{
            background:#1F2937;
            border:1px solid #374151;
            border-radius:12px;
            margin-top:10px;
            font-weight:bold;
            color:white;
        }

        QGroupBox::title{
            subcontrol-origin: margin;
            left:10px;
            padding:0 5px;
        }

        QComboBox{
            background:#0F172A;
            color:white;
            border:1px solid #374151;
            border-radius:8px;
            padding:8px;
        }

        QCheckBox{
            color:white;
        }

        QPushButton{
            background:#2563EB;
            color:white;
            border:none;
            border-radius:8px;
            padding:10px;
        }

        QPushButton:hover{
            background:#3B82F6;
        }
        """)

        # -------------------------
        # Voice Settings
        # -------------------------

        voice_group = QGroupBox("Voice")

        self.voice_group = voice_group

        voice_layout = QVBoxLayout()

        self.voice_checkbox = QCheckBox(
            "Enable Voice Response"
        )

        self.voice_checkbox.setChecked(True)

        voice_layout.addWidget(self.voice_checkbox)

        voice_group.setLayout(voice_layout)

        content_layout.addWidget(voice_group)

        # -------------------------
        # Startup
        # -------------------------

        startup_group = QGroupBox("Startup")

        self.startup_group = startup_group

        startup_layout = QVBoxLayout()

        self.startup_checkbox = QCheckBox(
            "Start Cipher when Ubuntu starts"
        )

        startup_layout.addWidget(
            self.startup_checkbox
        )

        startup_group.setLayout(startup_layout)

        content_layout.addWidget(startup_group)

        # -------------------------
        # Appearance
        # -------------------------

        appearance_group = QGroupBox("Appearance")

        self.appearance_group = appearance_group

        appearance_layout = QVBoxLayout()

        appearance_layout.addWidget(
            QLabel("Theme")
        )

        self.theme_combo = QComboBox()

        self.theme_combo.addItems([
            "dark",
            "light",
            "midnight",
            "cyber",
        ])

        self.accent_combo = QComboBox()
        
        self.accent_combo.addItems([
            "Blue",
            "Green",
            "Purple",
            "Orange",
            "Red",
        ])

        self.theme_combo.currentTextChanged.connect(
            self.apply_theme
        )

        self.accent_combo.currentTextChanged.connect(
            self.apply_theme
        )

        appearance_layout.addWidget(
            self.theme_combo
        )

        appearance_layout.addWidget(
            QLabel("Accent Color")
        )


        appearance_layout.addWidget(
            self.accent_combo
        )

        appearance_layout.addWidget(
            QLabel("Font Size")
        )

        self.font_size_combo = QComboBox()

        appearance_layout.addWidget(
            QLabel("Animation Speed")
        )

        self.animation_combo = QComboBox()

        self.animation_combo.addItems([
            "Slow",
            "Normal",
            "Fast",
            "Instant",
        ])

        appearance_layout.addWidget(
            self.animation_combo
        )

        self.high_contrast_checkbox = QCheckBox("High Contrast")

        self.reduced_motion_checkbox = QCheckBox("Reduced Motion")

        self.large_click_targets_checkbox = QCheckBox(
            "Large Click Targets"
        )

        appearance_layout.addWidget(
            self.high_contrast_checkbox
        )

        appearance_layout.addWidget(
            self.reduced_motion_checkbox
        )

        appearance_layout.addWidget(
            self.large_click_targets_checkbox
        )

        self.custom_style_button = QPushButton(
            "Load Custom Theme (.qss)"
        )

        appearance_layout.addWidget(
            self.custom_style_button
        )

        self.custom_style_button.clicked.connect(
            self.load_custom_stylesheet
        )

        appearance_layout.addWidget(
            QLabel("UI Scale")
        )

        self.ui_scale_combo = QComboBox()

        self.ui_scale_combo.addItems([
            "100%",
            "125%",
            "150%",
            "175%",
            "200%",
        ])

        appearance_layout.addWidget(
            self.ui_scale_combo
        )

        self.font_size_combo.addItems([
            "12",
            "13",
            "14",
            "15",
            "16",
        ])

        self.font_size_combo.setCurrentText("14")

        appearance_layout.addWidget(
            self.font_size_combo
        )

        appearance_layout.addWidget(
            QLabel("Appearance Profile")
        )

        self.profile_combo = QComboBox()

        appearance_layout.addWidget(
            self.profile_combo
        )

        self.save_profile_button = QPushButton(
            "Save Profile"
        )

        appearance_layout.addWidget(
            self.save_profile_button)

        appearance_group.setLayout(
            appearance_layout
        )

        content_layout.addWidget(
            appearance_group
        )

        # -------------------------
        # Save Button
        # -------------------------

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(
            self.save_settings
        )

        self.save_button.setEnabled(False)

        self.reset_button = QPushButton("Reset to Defaults")
        self.reset_button.clicked.connect(
            self.reset_settings
        )

        button_layout = QHBoxLayout()

        self.export_button = QPushButton("Export")
        self.export_button.clicked.connect(
            self.export_settings
        )

        self.import_button = QPushButton("Import")
        self.import_button.clicked.connect(
            self.import_settings
        )

        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.export_button)
        button_layout.addWidget(self.import_button)

        content_layout.addLayout(button_layout)

        # Detect changes
        for widget in (
            self.ai_combo,
            self.temperature_combo,
            self.theme_combo,
            self.accent_combo,
            self.font_size_combo,
            self.ui_scale_combo,
            self.animation_combo,
        ):
            
            widget.currentTextChanged.connect(
                self.on_settings_changed
            )

        for checkbox in (
            self.voice_checkbox,
            self.startup_checkbox,
            self.minimize_tray_checkbox,
            self.high_contrast_checkbox,
            self.reduced_motion_checkbox,
            self.large_click_targets_checkbox,
        ):
            
            checkbox.toggled.connect(
                self.on_settings_changed
            )

            # -------------------------
            # Keyboard Shortcuts
            # -------------------------

            QShortcut(
                QKeySequence("Ctrl+S"),
                self,
                activated=self.save_settings,
            )

            QShortcut(
                QKeySequence("Escape"),
                self,
                activated=self.close,
            )

            QShortcut(
                QKeySequence("Ctrl+R"),
                self,
                activated=self.confirm_reset,
            )

            page = QWidget()

            page.setLayout(content_layout)

            self.pages.addWidget(page)

            navigation.currentRowChanged.connect(
                self.pages.setCurrentIndex
            )

            navigation.setCurrentRow(0)

            about_page = QWidget()

            about_layout = QFormLayout()

            about_layout.addRow(
                "Application",
                QLabel("Cipher v2"),
            )

            about_layout.addRow(
                "Version",
                QLabel("2.0.0"),
            )

            about_layout.addRow(
                "Python",
                QLabel(platform.python_version()),
            )

            about_layout.addRow(
                "Qt",
                QLabel(QT_VERSION_STR),
            )

            about_layout.addRow(
                "Operating System",
                QLabel(platform.platform()),
            )

            about_layout.addRow(
                "Architecture",
                QLabel(platform.machine()),
            )

            about_layout.addRow(
                "Description",
                QLabel("Professional Ubuntu AI Assistant"),
            )

            about_layout.addRow(
                "Developer",
                QLabel("VK"),
            )

            about_page.setLayout(
                about_layout
            )

            self.pages.addWidget(
                about_page
            )

            self.ui_scale_combo.currentTextChanged.connect(
                self.apply_theme
            )

            self.animation_combo.currentTextChanged.connect(
                self.apply_theme
            )

            self.font_size_combo.currentTextChanged.connect(
                self.apply_theme
            )

            self.high_contrast_checkbox.toggled.connect(
                self.apply_theme
            )

            self.reduced_motion_checkbox.toggled.connect(
                self.apply_theme
            )

            self.large_click_targets_checkbox.toggled.connect(
                self.apply_theme
            )

            self.save_profile_button.clicked.connect(
                self.save_profile
            )

            self.profile_combo.currentTextChanged.connect(
                self.load_profile
            )

            self.setLayout(main_layout)

            self.load_settings()

    def save_settings(self):

        if not self.save_button.isEnabled():
            return

        settings = {
            "model": self.ai_combo.currentText(),
            "temperature": self.temperature_combo.currentText(),
            "voice": self.voice_checkbox.isChecked(),
            "startup": self.startup_checkbox.isChecked(),
            "tray": self.minimize_tray_checkbox.isChecked(),
            "theme": self.theme_combo.currentText(),
            "accent": self.accent_combo.currentText(),
            "font_size": self.font_size_combo.currentText(),
            "ui_scale": self.ui_scale_combo.currentText(),
            "animation_speed": self.animation_combo.currentText(),
            "high_contrast": self.high_contrast_checkbox.isChecked(),
            "reduced_motion": self.reduced_motion_checkbox.isChecked(),
            "large_click_targets": self.large_click_targets_checkbox.isChecked(),
        }

        self.settings_service.update(**settings)

        self.save_button.setEnabled(False)

        self.setWindowModified(False)

        self.apply_theme()

        print("Settings saved successfully.")

    def confirm_reset(self):

        reply = QMessageBox.question(
            self,
            "Reset Settings",
            "Reset all settings to their default values?",
            QMessageBox.StandardButton.Yes
            | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No,
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.reset_settings()

    def reset_settings(self):

        self.settings_service.reset()

        self.load_settings()

        self.apply_theme()

        self.save_button.setEnabled(False)

        self.setWindowModified(False)

        print("Settings reset successfully.")

    def export_settings(self):

        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Export Settings",
            "cipher_settings.json",
            "JSON Files (*.json)",
        )

        if not file_name:
            return

        import shutil

        try:

            self.save_settings()

            shutil.copy(
                self.settings_service.file,
                file_name,
            )

            QMessageBox.information(
                self,
                "Export",
                "Settings exported successfully.",
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Export Failed",
                str(e),
            )

    def import_settings(self):

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Import Settings",
            "",
            "JSON Files (*.json)",
        )

        if not file_name:
            return

        import shutil

        try:

            shutil.copy(
                file_name,
                self.settings_service.file,
            )

            self.load_settings()

            self.apply_theme()

            self.save_button.setEnabled(False)
            self.setWindowModified(False)

            QMessageBox.information(
                self,
                "Import",
                "Settings imported successfully.",
            )
        except Exception as e:

            QMessageBox.critical(
                self,
                "Import Failed",
                str(e),
            )

    def filter_settings(self, text):

        text = text.strip().lower()

        groups = [
            self.general_group,
            self.ai_group,
            self.voice_group,
            self.startup_group,
            self.appearance_group,
        ]

        if not text:

            for group in groups:
                group.show()

            return

        for group in groups:

            searchable_text = group.title().lower()

            for label in group.findChildren(QLabel):
                searchable_text += " " + label.text().lower()

            for checkbox in group.findChildren(QCheckBox):
                searchable_text += " " + checkbox.text().lower()

            visible = text in searchable_text

            group.setVisible(visible)

    def on_settings_changed(self):

        self.save_button.setEnabled(True)
        self.setWindowModified(True)

    def apply_theme(self):

        from gui.theme import (
            set_theme,
            set_accent,
            set_font_size,
            set_ui_scale,
            set_animation_speed,
            set_accessibility,
        )

        theme = self.theme_combo.currentText().lower()

        set_theme(theme)

        set_accent(
            self.accent_combo.currentText()
        )

        
        font_map = {
            "12": "Small",
            "14": "Medium",
            "16": "Large",
        }

        set_font_size(
            font_map.get(
                self.font_size_combo.currentText(),
                "Medium",
            )
        )

        set_ui_scale(
            self.ui_scale_combo.currentText()
        )

        set_animation_speed(
            self.animation_combo.currentText()
        )

        set_accessibility(
            high_contrast=self.high_contrast_checkbox.isChecked(),
            reduced_motion=self.reduced_motion_checkbox.isChecked(),
            large_click_targets=self.large_click_targets_checkbox.isChecked(),
        )

        theme = self.theme_combo.currentText()
        accent = self.accent_combo.currentText()

        self.settings_service.update(
            theme=theme,
            accent=accent,
        )

        stylesheet = self.build_stylesheet(
            theme,
            accent,
        )

        parent = self.parentWidget()
        if parent is not None:
            parent.setStyleSheet(stylesheet)


    def build_stylesheet(
        self,
        theme,
        accent,
    ):

        colors = {
            "Blue": "#2563EB",
            "Green": "#16A34A",
            "Purple": "#7C3AED",
            "Orange": "#EA580C",
            "Red": "#DC2626",
        }

        accent_color = colors.get(
            accent,
            "#2563EB",
        )

        if theme == "light":

            background = "#F8FAFC"
            text = "#111827"
            card = "#FFFFFF"

        else:

            background = "#111827"
            text = "white"
            card = "#1F2937"

        return f"""
        QWidget{{
            background:{background};
            color:{text};
        }}

        QGroupBox{{
            background:{card};
            border:1px solid #374151;
            border-radius:12px;
        }}

        QPushButton{{
            background:{accent_color};
            color:white;
            border:none;
            border-radius:8px;
            padding:10px;
        }}

        QPushButton:hover{{
            opacity:0.9;
        }}
        """

    def load_settings(self):

        settings = self.settings_service.load()

        if settings is None:
            return

        if not settings:
            return

        self.ai_combo.setCurrentText(
            settings.get("model", "Auto")
        )

        self.temperature_combo.setCurrentText(
            settings.get("temperature", "0.2")
        )

        self.voice_checkbox.setChecked(
            settings.get("voice", True)
        )

        self.startup_checkbox.setChecked(
            settings.get("startup", False)
        )

        self.minimize_tray_checkbox.setChecked(
            settings.get("tray", True)
        )

        self.animation_combo.setCurrentText(
            settings.get(
                "animation_speed",
                "Normal",
            )
        )

        self.high_contrast_checkbox.setChecked(
            settings.get("high_contrast", False)
        )

        self.reduced_motion_checkbox.setChecked(
            settings.get("reduced_motion", False)
        )

        self.large_click_targets_checkbox.setChecked(
            settings.get("large_click_targets", False)
        )

        self.theme_combo.setCurrentText(
            settings.get("theme", "dark")
        )

        self.accent_combo.setCurrentText(
            settings.get("accent", "Blue")
        )

        self.font_size_combo.setCurrentText(
            settings.get("font_size", "14")
        )

        self.ui_scale_combo.setCurrentText(
            settings.get(
                "ui_scale",
                "100%",
            )
        )

        self.apply_theme()

        self.save_button.setEnabled(False)

        self.setWindowModified(False)

    def closeEvent(self, event):

        unregister_widget(self)

        super().closeEvent(event)

    def load_custom_stylesheet(self):

        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Stylesheet",
            "",
            "Qt Stylesheet (*.qss)"
        )

        if not file_name:
            return

        if load_custom_stylesheet(file_name):
            self.apply_theme()

    def save_profile(self):

        name, ok = QInputDialog.getText(
            self,
            "Profile",
            "Profile Name"
        )

        if ok and name:

            self.settings_service.save_profile(name)

            self.profile_combo.addItem(name)


    def load_profile(self, name):

        if not name:
            return

        profile = self.settings_service.load_profile(name)

        if profile:

            self.load_settings()