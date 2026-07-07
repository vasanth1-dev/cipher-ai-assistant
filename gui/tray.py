from pathlib import Path

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QMenu,
    QMessageBox,
    QSystemTrayIcon,
)


class CipherTray(QObject):

    pauseRequested = pyqtSignal()
    resumeRequested = pyqtSignal()
    settingsRequested = pyqtSignal()
    exitRequested = pyqtSignal()

    def __init__(self, window):

        super().__init__()

        self.window = window

        icon = Path(__file__).parent / "resources" / "cipher.png"

        self.tray = QSystemTrayIcon(
            QIcon(str(icon)),
            self.window,
        )

        self.tray.setToolTip("Cipher AI Assistant")

        self._create_menu()

        self.tray.activated.connect(
            self.icon_clicked
        )

        self.tray.show()

    # --------------------------------------------------

    def _create_menu(self):

        menu = QMenu()

        self.show_action = QAction("Open Cipher")
        self.show_action.triggered.connect(
            self.show_window
        )
        menu.addAction(self.show_action)

        self.hide_action = QAction("Hide")
        self.hide_action.triggered.connect(
            self.hide_window
        )
        menu.addAction(self.hide_action)

        menu.addSeparator()

        self.pause_action = QAction(
            "Pause Listening"
        )
        self.pause_action.triggered.connect(
            self.pauseRequested.emit
        )
        menu.addAction(self.pause_action)

        self.resume_action = QAction(
            "Resume Listening"
        )
        self.resume_action.triggered.connect(
            self.resumeRequested.emit
        )
        menu.addAction(self.resume_action)

        menu.addSeparator()

        self.settings_action = QAction(
            "Settings"
        )
        self.settings_action.triggered.connect(
            self.settingsRequested.emit
        )
        menu.addAction(self.settings_action)

        self.about_action = QAction(
            "About Cipher"
        )
        self.about_action.triggered.connect(
            self.about
        )
        menu.addAction(self.about_action)

        menu.addSeparator()

        self.exit_action = QAction("Exit")
        self.exit_action.triggered.connect(
            self._exit
        )
        menu.addAction(self.exit_action)

        self.tray.setContextMenu(menu)

    # --------------------------------------------------

    def icon_clicked(self, reason):

        if (
            reason
            == QSystemTrayIcon.ActivationReason.Trigger
        ):

            if self.window.isVisible():
                self.hide_window()
            else:
                self.show_window()

    # --------------------------------------------------

    def show_window(self):

        self.window.showNormal()
        self.window.raise_()
        self.window.activateWindow()

    # --------------------------------------------------

    def hide_window(self):

        self.window.hide()

    # --------------------------------------------------

    def show_notification(
        self,
        title,
        message,
    ):

        self.tray.showMessage(
            title,
            message,
            QSystemTrayIcon.MessageIcon.Information,
            3000,
        )

    # --------------------------------------------------

    def about(self):

        QMessageBox.information(
            self.window,
            "Cipher",
            (
                "Cipher v2\n\n"
                "Professional Ubuntu AI Assistant\n\n"
                "Powered by Python, PyQt6 and Ollama."
            ),
        )

    # --------------------------------------------------

    def _exit(self):

        self.exitRequested.emit()

        QApplication.quit()