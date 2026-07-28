"""
Cipher v2
Volume Plugin

Control the system volume using common Ubuntu audio utilities.

Features
--------
- Increase volume
- Decrease volume
- Set volume to a specific percentage
- Mute / Unmute
- Toggle mute
- Get current volume
"""

from __future__ import annotations

import re
import shutil
import subprocess

from core.logger import logger
from plugins.base_plugin import BasePlugin


class VolumePlugin(BasePlugin):
    """
    Ubuntu volume control plugin.
    """

    name = "volume"
    version = "1.0.0"
    description = "Control system volume."

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "volume",
            "sound",
            "mute",
            "unmute",
            "speaker",
            "audio",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        text = text.lower()

        try:
            if "mute" in text and "unmute" not in text:
                self._mute()
                return self._success("Audio muted.")

            if "unmute" in text:
                self._unmute()
                return self._success("Audio unmuted.")

            if "toggle" in text and "mute" in text:
                self._toggle_mute()
                return self._success("Mute toggled.")

            if any(word in text for word in ("increase", "raise", "up")):
                amount = self._extract_percentage(text, default=10)
                self._increase(amount)
                return self._success(f"Volume increased by {amount}%.")

            if any(word in text for word in ("decrease", "lower", "down", "reduce")):
                amount = self._extract_percentage(text, default=10)
                self._decrease(amount)
                return self._success(f"Volume decreased by {amount}%.")

            if "set" in text:
                value = self._extract_percentage(text)
                if value is None:
                    raise ValueError("No volume percentage specified.")
                self._set(value)
                return self._success(f"Volume set to {value}%.")

            if any(word in text for word in ("current", "status", "what")):
                volume = self._current_volume()
                return {
                    "success": True,
                    "message": f"Current volume is {volume}.",
                    "volume": volume,
                }

            return {
                "success": False,
                "message": "Volume command not recognized.",
            }

        except Exception as exc:
            logger.exception(exc)

            return {
                "success": False,
                "message": str(exc),
            }
        
    def on_load(self) -> None:
        pass

    def on_unload(self) -> None:
        pass

    # --------------------------------------------------
    # Backend selection
    # --------------------------------------------------

    def _backend(self) -> str:
        if shutil.which("wpctl"):
            return "wpctl"

        if shutil.which("pactl"):
            return "pactl"

        raise RuntimeError(
            "No supported audio backend found (wpctl or pactl)."
        )

    # --------------------------------------------------
    # Volume operations
    # --------------------------------------------------

    def _increase(self, amount: int):
        if self._backend() == "wpctl":
            subprocess.run(
                ["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", f"{amount}%+"],
                check=True,
            )
            return

        subprocess.run(
            [
                "pactl",
                "set-sink-volume",
                "@DEFAULT_SINK@",
                f"+{amount}%",
            ],
            check=True,
        )

    def _decrease(self, amount: int):
        if self._backend() == "wpctl":
            subprocess.run(
                ["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", f"{amount}%-"],
                check=True,
            )
            return

        subprocess.run(
            [
                "pactl",
                "set-sink-volume",
                "@DEFAULT_SINK@",
                f"-{amount}%",
            ],
            check=True,
        )

    def _set(self, value: int):
        value = max(0, min(100, value))

        if self._backend() == "wpctl":
            subprocess.run(
                ["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", f"{value}%"],
                check=True,
            )
            return

        subprocess.run(
            [
                "pactl",
                "set-sink-volume",
                "@DEFAULT_SINK@",
                f"{value}%",
            ],
            check=True,
        )

    def _mute(self):
        if self._backend() == "wpctl":
            subprocess.run(
                ["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "1"],
                check=True,
            )
            return

        subprocess.run(
            [
                "pactl",
                "set-sink-mute",
                "@DEFAULT_SINK@",
                "1",
            ],
            check=True,
        )

    def _unmute(self):
        if self._backend() == "wpctl":
            subprocess.run(
                ["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "0"],
                check=True,
            )
            return

        subprocess.run(
            [
                "pactl",
                "set-sink-mute",
                "@DEFAULT_SINK@",
                "0",
            ],
            check=True,
        )

    def _toggle_mute(self):
        if self._backend() == "wpctl":
            subprocess.run(
                ["wpctl", "set-mute", "@DEFAULT_AUDIO_SINK@", "toggle"],
                check=True,
            )
            return

        subprocess.run(
            [
                "pactl",
                "set-sink-mute",
                "@DEFAULT_SINK@",
                "toggle",
            ],
            check=True,
        )

    def _current_volume(self) -> str:
        backend = self._backend()

        if backend == "wpctl":
            output = subprocess.check_output(
                ["wpctl", "get-volume", "@DEFAULT_AUDIO_SINK@"],
                text=True,
            ).strip()
            return output

        output = subprocess.check_output(
            ["pactl", "get-sink-volume", "@DEFAULT_SINK@"],
            text=True,
        ).splitlines()[0]

        return output.strip()

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _extract_percentage(text: str, default=None):
        match = re.search(r"(\d{1,3})", text)

        if not match:
            return default

        value = int(match.group(1))
        return max(0, min(100, value))

    @staticmethod
    def _success(message: str):
        return {
            "success": True,
            "message": message,
        }