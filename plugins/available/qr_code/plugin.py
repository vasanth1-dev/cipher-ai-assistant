"""
Cipher v2
QR Code Plugin

Generate and decode QR codes.

Features
--------
- Generate QR codes from text
- Decode QR codes from images
- Automatic output directory
- PNG output
"""

from __future__ import annotations

from pathlib import Path

from core.logger import logger
from plugins.base.plugin import Plugin

try:
    import qrcode
    from PIL import Image
    from pyzbar.pyzbar import decode
except ImportError:
    qrcode = None
    Image = None
    decode = None


class QRCodePlugin(Plugin):
    """
    QR code plugin.
    """

    name = "qr_code"
    version = "1.0.0"
    description = "Generate and decode QR codes."

    def __init__(self):
        super().__init__()

        self.output_directory = (
            Path.home() /
            "Pictures" /
            "Cipher QR Codes"
        )
        self.output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    # --------------------------------------------------
    # Plugin API
    # --------------------------------------------------

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "qr",
            "qr code",
            "generate qr",
            "scan qr",
            "decode qr",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        QR operations are expected to be routed through
        Cipher's structured intent pipeline.
        """

        return {
            "success": True,
            "message": (
                "QR Code plugin is available. "
                "Waiting for structured QR commands."
            ),
        }

    # --------------------------------------------------
    # Generation
    # --------------------------------------------------

    @staticmethod
    def _require_generation():
        if qrcode is None:
            raise RuntimeError(
                "qrcode is not installed. "
                "Install it using: pip install qrcode[pil]"
            )

    @staticmethod
    def _require_decoding():
        if Image is None or decode is None:
            raise RuntimeError(
                "QR decoding dependencies are missing. "
                "Install pillow and pyzbar."
            )

    def generate(
        self,
        text: str,
        filename: str,
    ) -> Path:
        self._require_generation()

        image = qrcode.make(text)

        output = self.output_directory / f"{filename}.png"

        image.save(output)

        return output

    # --------------------------------------------------
    # Decoding
    # --------------------------------------------------

    def decode(self, image_path: Path) -> list[str]:
        self._require_decoding()

        image = Image.open(image_path)

        return [
            item.data.decode("utf-8")
            for item in decode(image)
        ]

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)