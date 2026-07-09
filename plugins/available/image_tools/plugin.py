"""
Cipher v2
Image Tools Plugin

Provides common image manipulation utilities.

Features
--------
- Resize images
- Crop images
- Rotate images
- Convert image formats
- Create thumbnails
- Read image metadata
"""

from __future__ import annotations

from pathlib import Path

from core.logger import logger
from plugins.base.plugin import Plugin

try:
    from PIL import Image
except ImportError:
    Image = None


class ImageToolsPlugin(Plugin):
    """
    Image processing plugin.
    """

    name = "image_tools"
    version = "1.0.0"
    description = "Utilities for manipulating images."

    SUPPORTED_FORMATS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".gif",
        ".tiff",
        ".webp",
    }

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "image",
            "picture",
            "photo",
            "resize image",
            "crop image",
            "rotate image",
            "convert image",
            "thumbnail",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        Image operations are intended to be routed through
        Cipher's structured document/image intent pipeline.
        """

        return {
            "success": True,
            "message": (
                "Image Tools plugin is available. "
                "Waiting for structured image commands."
            ),
        }

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _require_library():
        if Image is None:
            raise RuntimeError(
                "Pillow is not installed. "
                "Install it using: pip install pillow"
            )

    # --------------------------------------------------
    # Image Operations
    # --------------------------------------------------

    def resize(
        self,
        source: Path,
        destination: Path,
        width: int,
        height: int,
    ) -> None:
        self._require_library()

        with Image.open(source) as image:
            image = image.resize((width, height))
            image.save(destination)

    def crop(
        self,
        source: Path,
        destination: Path,
        left: int,
        upper: int,
        right: int,
        lower: int,
    ) -> None:
        self._require_library()

        with Image.open(source) as image:
            cropped = image.crop((left, upper, right, lower))
            cropped.save(destination)

    def rotate(
        self,
        source: Path,
        destination: Path,
        degrees: float,
    ) -> None:
        self._require_library()

        with Image.open(source) as image:
            image.rotate(degrees, expand=True).save(destination)

    def convert(
        self,
        source: Path,
        destination: Path,
    ) -> None:
        self._require_library()

        with Image.open(source) as image:
            image.save(destination)

    def thumbnail(
        self,
        source: Path,
        destination: Path,
        size: tuple[int, int] = (256, 256),
    ) -> None:
        self._require_library()

        with Image.open(source) as image:
            image.thumbnail(size)
            image.save(destination)

    def metadata(self, source: Path) -> dict:
        self._require_library()

        with Image.open(source) as image:
            return {
                "format": image.format,
                "mode": image.mode,
                "width": image.width,
                "height": image.height,
            }

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    @classmethod
    def is_supported(cls, path: Path) -> bool:
        return path.suffix.lower() in cls.SUPPORTED_FORMATS

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)