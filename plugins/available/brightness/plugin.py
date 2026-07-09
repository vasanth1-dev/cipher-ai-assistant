"""
Cipher v2
Brightness Plugin

Control the display brightness on Ubuntu.

Features
--------
- Increase brightness
- Decrease brightness
- Set brightness percentage
- Get current brightness
- Automatic backend detection (brightnessctl / xrandr)
"""

from __future__ import annotations

import re
import shutil
import subprocess

from core.logger import logger
from plugins.base.plugin import Plugin


class BrightnessPlugin(Plugin):
    """
    System brightness control plugin.
    """

    name = "brightness"
    version = "1.0.0"
    description = "Control display brightness."

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        return any(
            keyword in text
            for keyword in (
                "brightness",
                "screen brightness",
                "display brightness",
            )
        )

    def handle(self, text: str):
        text = text.lower()

        try:
            if any(word in text for word in ("increase", "raise", "up")):
                amount = self._extract_percentage(text, default=10)
                self._increase(amount)
                return self._success(f"Brightness increased by {amount}%.")

            if any(word in text for word in ("decrease", "lower", "down", "reduce")):
                amount = self._extract_percentage(text, default=10)
                self._decrease(amount)
                return self._success(f"Brightness decreased by {amount}%.")

            if "set" in text:
                value = self._extract_percentage(text)
                if value is None:
                    raise ValueError("No brightness percentage specified.")
                self._set(value)
                return self._success(f"Brightness set to {value}%.")

            if any(word in text for word in ("current", "status", "what")):
                value = self._current()
                return {
                    "success": True,
                    "message": f"Current brightness is {value}%.",
                    "brightness": value,
                }

            return {
                "success": False,
                "message": "Brightness command not recognized.",
            }

        except Exception as exc:
            logger.exception(exc)

            return {
                "success": False,
                "message": str(exc),
            }

    # --------------------------------------------------
    # Backend
    # --------------------------------------------------

    def _backend(self):
        if shutil.which("brightnessctl"):
            return "brightnessctl"

        if shutil.which("xrandr"):
            return "xrandr"

        raise RuntimeError(
            "No supported brightness backend found."
        )

    # --------------------------------------------------
    # Actions
    # --------------------------------------------------

    def _increase(self, amount: int):
        if self._backend() == "brightnessctl":
            subprocess.run(
                ["brightnessctl", "set", f"{amount}%+"],
                check=True,
            )
            return

        raise RuntimeError(
            "Brightness increase is not supported with the current backend."
        )

    def _decrease(self, amount: int):
        if self._backend() == "brightnessctl":
            subprocess.run(
                ["brightnessctl", "set", f"{amount}%-"],
                check=True,
            )
            return

        raise RuntimeError(
            "Brightness decrease is not supported with the current backend."
        )

    def _set(self, value: int):
        value = max(1, min(100, value))

        if self._backend() == "brightnessctl":
            subprocess.run(
                ["brightnessctl", "set", f"{value}%"],
                check=True,
            )
            return

        raise RuntimeError(
            "Setting brightness is not supported with the current backend."
        )

    def _current(self) -> int:
        if self._backend() == "brightnessctl":
            output = subprocess.check_output(
                ["brightnessctl"],
                text=True,
            )

            match = re.search(r"\((\d+)%\)", output)

            if not match:
                raise RuntimeError("Unable to determine current brightness.")

            return int(match.group(1))

        raise RuntimeError(
            "Reading brightness is not supported with the current backend."
        )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _extract_percentage(text: str, default=None):
        match = re.search(r"(\d{1,3})", text)

        if not match:
            return default

        value = int(match.group(1))
        return max(1, min(100, value))

    @staticmethod
    def _success(message: str):
        return {
            "success": True,
            "message": message,
        }