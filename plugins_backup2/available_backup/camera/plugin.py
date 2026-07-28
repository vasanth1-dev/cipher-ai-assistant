"""
Cipher v2
Camera Plugin

Capture photos from the default webcam using common Ubuntu
camera utilities.

Features
--------
- Capture a photo
- Timestamped filenames
- Automatic photo directory creation
- Automatic backend detection
"""

from __future__ import annotations

import shutil
import subprocess
from datetime import datetime
from pathlib import Path

from core.logger import logger
from plugins.base_plugin import Plugin


class CameraPlugin(Plugin):
    """
    Camera plugin.
    """

    name = "camera"
    version = "1.0.0"
    description = "Capture photos using the default webcam."

    def __init__(
       self,
    ) -> None:
        super().__init__()

        self.directory = Path.home() / "Pictures" / "Cipher Camera"
        self.directory.mkdir(parents=True, exist_ok=True)

    # --------------------------------------------------
    # Plugin API
    # --------------------------------------------------

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "camera",
            "take photo",
            "take picture",
            "capture photo",
            "capture image",
            "webcam",
            "selfie",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        try:
            image = self._capture()

            return {
                "success": True,
                "message": f"Photo saved to {image}",
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

    def _capture(self) -> Path:
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.jpg")
        destination = self.directory / filename

        if shutil.which("fswebcam"):
            subprocess.run(
                [
                    "fswebcam",
                    "-q",
                    "--no-banner",
                    str(destination),
                ],
                check=True,
            )
            return destination

        if shutil.which("ffmpeg"):
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-f",
                    "video4linux2",
                    "-i",
                    "/dev/video0",
                    "-frames:v",
                    "1",
                    str(destination),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=True,
            )
            return destination

        raise RuntimeError(
            "No supported camera utility found. "
            "Install fswebcam or ffmpeg."
        )