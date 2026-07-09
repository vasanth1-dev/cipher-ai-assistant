"""
Cipher v2
Power Plugin

Provides safe power management commands for Ubuntu.

Features:
- Shutdown
- Restart
- Logout
- Suspend
- Hibernate
- Lock Screen

Destructive actions require explicit confirmation.
"""

from __future__ import annotations

import shutil
import subprocess

from core.logger import logger
from plugins.base.plugin import Plugin


class PowerPlugin(Plugin):
    """
    Power management plugin.
    """

    name = "power"
    version = "1.0.0"
    description = "Power management for the operating system."

    COMMANDS = {
        "shutdown": [
            "shutdown",
            "power off",
            "poweroff",
            "turn off",
            "turn off computer",
            "switch off",
        ],
        "restart": [
            "restart",
            "reboot",
            "restart computer",
            "reboot computer",
        ],
        "logout": [
            "logout",
            "log out",
            "sign out",
        ],
        "suspend": [
            "suspend",
            "sleep",
            "sleep computer",
        ],
        "hibernate": [
            "hibernate",
        ],
        "lock": [
            "lock",
            "lock screen",
            "lock computer",
        ],
    }

    CONFIRM_REQUIRED = {
        "shutdown",
        "restart",
        "logout",
    }

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        for phrases in self.COMMANDS.values():
            if any(p in text for p in phrases):
                return True

        return False

    def handle(self, text: str):
        text = text.lower()

        for action, phrases in self.COMMANDS.items():
            if any(p in text for p in phrases):
                return self._execute(action, text)

        return False

    # --------------------------------------------------
    # Execution
    # --------------------------------------------------

    def _execute(self, action: str, text: str):
        confirmed = any(
            word in text
            for word in (
                "confirm",
                "confirmed",
                "yes",
                "do it",
                "proceed",
                "continue",
                "now",
            )
        )

        if action in self.CONFIRM_REQUIRED and not confirmed:
            return {
                "success": False,
                "requires_confirmation": True,
                "action": action,
                "message": (
                    f"{action.title()} requires confirmation. "
                    f"Say '{action} now' or '{action} confirmed'."
                ),
            }

        try:
            self._run(action)

            return {
                "success": True,
                "message": f"{action.title()} command executed.",
            }

        except Exception as exc:
            logger.exception(exc)

            return {
                "success": False,
                "message": str(exc),
            }

    # --------------------------------------------------
    # Commands
    # --------------------------------------------------

    def _run(self, action: str):
        if action == "shutdown":
            self._systemctl("poweroff")
            return

        if action == "restart":
            self._systemctl("reboot")
            return

        if action == "logout":
            self._logout()
            return

        if action == "suspend":
            self._systemctl("suspend")
            return

        if action == "hibernate":
            self._systemctl("hibernate")
            return

        if action == "lock":
            self._lock()
            return

        raise RuntimeError(f"Unsupported action: {action}")

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def _systemctl(self, command: str):
        subprocess.Popen(
            ["systemctl", command],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def _logout(self):
        subprocess.Popen(
            ["gnome-session-quit", "--logout", "--no-prompt"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    def _lock(self):
        if shutil.which("loginctl"):
            subprocess.Popen(
                ["loginctl", "lock-session"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return

        if shutil.which("gnome-screensaver-command"):
            subprocess.Popen(
                ["gnome-screensaver-command", "-l"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            return

        raise RuntimeError("No supported screen lock command found.")