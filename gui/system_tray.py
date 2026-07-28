from pathlib import Path

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
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

        if not icon.exists():
            raise FileNotFoundError(
                f"Tray icon not found: {icon}"
            )

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

    def setContextMenu(self, menu):
        self.tray.setContextMenu(menu)

    # --------------------------------------------------

    def _create_menu(self):

        self.menu = QMenu()

        self.show_action = QAction("Open Cipher")
        self.show_action.triggered.connect(
            self.show_window
        )
        self.menu.addAction(self.show_action)

        self.hide_action = QAction("Hide")
        self.hide_action.triggered.connect(
            self.hide_window
        )
        self.menu.addAction(self.hide_action)

        self.menu.addSeparator()

        self.pause_action = QAction(
            "Pause Listening"
        )
        self.pause_action.triggered.connect(
            self.pauseRequested.emit
        )
        self.menu.addAction(self.pause_action)

        self.resume_action = QAction(
            "Resume Listening"
        )
        self.resume_action.triggered.connect(
            self.resumeRequested.emit
        )
        self.resume_action.setVisible(False)
        self.menu.addAction(self.resume_action)

        self.menu.addSeparator()

        self.settings_action = QAction(
            "Settings"
        )
        self.settings_action.triggered.connect(
            self.settingsRequested.emit
        )
        self.menu.addAction(self.settings_action)

        self.about_action = QAction(
            "About Cipher"
        )
        self.about_action.triggered.connect(
            self.about
        )
        self.menu.addAction(self.about_action)

        self.menu.addSeparator()

        self.exit_action = QAction("Exit")
        self.exit_action.triggered.connect(
            self._exit
        )
        self.menu.addAction(self.exit_action)

        self.tray.setContextMenu(self.menu)

    # --------------------------------------------------

    def icon_clicked(
        self, 
        reason: QSystemTrayIcon.ActivationReason,
    ) -> None:

        if (
            reason
            in (
                QSystemTrayIcon.ActivationReason.Trigger,
                QSystemTrayIcon.ActivationReason.DoubleClick,
            )
        ):

            if self.window.isVisible():
                self.hide_window()
            else:
                self.show_window()

    # --------------------------------------------------

    def show_window(
        self,
    ) -> None:

        if self.window.isMinimized():
            self.window.showNormal()
        else:
            self.window.show()

        self.window.raise_()
        self.window.activateWindow()

    # --------------------------------------------------

    def hide_window(
        self,
        notify: bool = True,
    ) -> None:

        self.window.hide()

        if notify:
            self.show_notification(
                "Cipher",
                "Cipher is running in the system tray."
            )

    def set_listening(
        self,
        listening: bool,
    ) -> None:

        self.pause_action.setVisible(listening)

        self.resume_action.setVisible(
            not listening
        )

    # --------------------------------------------------

    def show_notification(
        self,
        title: str,
        message: str,
        icon: QSystemTrayIcon.MessageIcon = (
            QSystemTrayIcon.MessageIcon.Information
        ),
        timeout: int = 3000,
    ) -> None:

        if not self.tray.supportsMessages():
            return

        self.tray.showMessage(
            title,
            message,
            icon,
            timeout,
        )

    def show(self) -> None:
        self.tray.show()

    def hide(self) -> None:
        self.tray.hide()

    def set_status(
        self,
        status: str,
    ) -> None:

        self.tray.setToolTip(
            f"Cipher AI Assistant\n{status}"
        )

    def is_visible(
        self,
    ) -> bool:

        return self.tray.isVisible()

    # --------------------------------------------------

    def about(
        self,
    ) -> None:

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

    def _exit(
        self,
    ) -> None:
        
        self.tray.hide()

        self.exitRequested.emit()

    @property
    def activated(self):
        return self.tray.activated