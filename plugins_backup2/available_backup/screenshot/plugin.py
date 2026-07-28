"""
Cipher v2
Screenshot Plugin

Capture screenshots using common Ubuntu screenshot utilities.

Features
--------
- Full screen capture
- Active window capture
- Area selection capture
- Automatic screenshots directory creation
- Timestamped filenames
"""

from __future__ import annotations

import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from core.logger import logger
from plugins.base_plugin import Plugin


class ScreenshotPlugin(Plugin):
    """
    Screenshot plugin.
    """

    name = "screenshot"
    version = "1.0.0"
    description = "Capture screenshots."

    def __init__(
       self,
    ) -> None:
        super().__init__()

        self.directory = Path.home() / "Pictures" / "Cipher Screenshots"
        self.directory.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------
    # Plugin API
    # --------------------------------------------------

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "screenshot",
            "screen shot",
            "capture screen",
            "take screenshot",
            "take a screenshot",
        )

        return any(word in text for word in keywords)

    def handle(self, text: str):
        text = text.lower()

        try:
            image = self._capture(text)

            return {
                "success": True,
                "message": f"Screenshot saved to {image}",
                "path": str(image),
            }

        except Exception as exc:
            logger.exception(exc)

            return {
                "success": False,
                "message": str(exc),
            }

    # --------------------------------------------------
    # Capture
    # --------------------------------------------------

    def _capture(self, text: str) -> Path:
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.png")
        destination = self.directory / filename

        if shutil.which("gnome-screenshot"):

            command = ["gnome-screenshot"]

            if "window" in text:
                command.append("-w")

            elif any(word in text for word in ("area", "selection", "select")):
                command.append("-a")

            command.extend(["-f", str(destination)])

            subprocess.run(command, check=True)

            return destination

        if shutil.which("grim"):
            subprocess.run(
                ["grim", str(destination)],
                check=True,
            )
            return destination

        raise RuntimeError(
            "No supported screenshot utility found. "
            "Install gnome-screenshot or grim."
        )