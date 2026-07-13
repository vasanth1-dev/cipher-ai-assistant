import shutil
import subprocess

from PyQt6.QtCore import QObject, pyqtSignal


class DashboardActions(QObject):
    """
    Cipher v2 Dashboard Actions

    Responsibilities
    ----------------
    • Open Terminal
    • Open Browser
    • Open Files
    • Open Settings

    Emits:
        success(str)
        error(str)
    """

    success = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    # --------------------------------------------------
    # Internal
    # --------------------------------------------------

    def _run(self, *command):

        executable = command[0]

        if shutil.which(executable) is None:
            self.error.emit(f"{executable} is not installed.")
            return False

        try:
            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            self.success.emit(f"Started {executable}")
            return True

        except Exception as exc:
            self.error.emit(str(exc))
            return False

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def open_terminal(self):

        for terminal in (
            "gnome-terminal",
            "kgx",
            "x-terminal-emulator",
            "konsole",
            "xfce4-terminal",
        ):
            if shutil.which(terminal):
                return self._run(terminal)

        self.error.emit("No supported terminal found.")
        return False

    def open_browser(self):

        for browser in (
            "firefox",
            "google-chrome",
            "chromium",
            "brave-browser",
        ):
            if shutil.which(browser):
                return self._run(browser)

        self.error.emit("No supported browser found.")
        return False

    def open_files(self):

        for manager in (
            "nautilus",
            "nemo",
            "thunar",
            "dolphin",
            "pcmanfm",
        ):
            if shutil.which(manager):
                return self._run(manager)

        self.error.emit("No supported file manager found.")
        return False

    def open_settings(self):

        candidates = (
            ("gnome-control-center",),
            ("systemsettings",),
        )

        for command in candidates:
            if shutil.which(command[0]):
                return self._run(*command)

        self.error.emit("System Settings application not found.")
        return False