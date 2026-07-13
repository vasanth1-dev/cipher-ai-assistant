from __future__ import annotations

import shutil
import subprocess

from PyQt6.QtCore import QObject, pyqtSignal


class QuickActionsService(QObject):
    """
    Quick Actions Service

    Executes dashboard quick actions and reports the result.

    Signals
    -------
    actionSucceeded(str)
    actionFailed(str)
    """

    actionSucceeded = pyqtSignal(str)
    actionFailed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    # --------------------------------------------------

    def _launch(self, *command) -> bool:

        executable = command[0]

        if shutil.which(executable) is None:
            self.actionFailed.emit(
                f"{executable} is not available."
            )
            return False

        try:

            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            self.actionSucceeded.emit(
                f"{executable} started."
            )

            return True

        except Exception as exc:

            self.actionFailed.emit(str(exc))
            return False

    # --------------------------------------------------

    def open_terminal(self):

        for terminal in (
            "kgx",
            "gnome-terminal",
            "x-terminal-emulator",
            "konsole",
            "xfce4-terminal",
        ):
            if shutil.which(terminal):
                return self._launch(terminal)

        self.actionFailed.emit(
            "No supported terminal found."
        )
        return False

    # --------------------------------------------------

    def open_browser(self):

        for browser in (
            "firefox",
            "google-chrome",
            "chromium",
            "brave-browser",
        ):
            if shutil.which(browser):
                return self._launch(browser)

        self.actionFailed.emit(
            "No supported browser found."
        )
        return False

    # --------------------------------------------------

    def open_files(self):

        for manager in (
            "nautilus",
            "nemo",
            "thunar",
            "dolphin",
            "pcmanfm",
        ):
            if shutil.which(manager):
                return self._launch(manager)

        self.actionFailed.emit(
            "No supported file manager found."
        )
        return False

    # --------------------------------------------------

    def open_settings(self):

        for app in (
            "gnome-control-center",
            "systemsettings",
        ):
            if shutil.which(app):
                return self._launch(app)

        self.actionFailed.emit(
            "System Settings not found."
        )
        return False