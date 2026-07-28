"""
Cipher v2
OCR Plugin

Provides Optical Character Recognition (OCR) capabilities.

Features
--------
- Extract text from images
- Support PNG, JPG, JPEG, BMP, TIFF, WEBP
- Language selection
- Basic image validation
"""

from __future__ import annotations

from pathlib import Path

from core.logger import logger
from plugins.base_plugin import Plugin

try:
    import pytesseract
    from PIL import Image
except ImportError:
    pytesseract = None
    Image = None


class OCRPlugin(Plugin):
    """
    OCR plugin.
    """

    name = "ocr"
    version = "1.0.0"
    description = "Extract text from images."

    SUPPORTED_EXTENSIONS = {
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".tif",
        ".tiff",
        ".webp",
    }

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "ocr",
            "extract text",
            "read image",
            "scan image",
            "recognize text",
            "image text",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        OCR operations are intended to be invoked through Cipher's
        document/image intent pipeline.
        """

        return {
            "success": True,
            "message": (
                "OCR plugin is available. "
                "Waiting for structured OCR commands."
            ),
        }

    # --------------------------------------------------
    # OCR
    # --------------------------------------------------

    @staticmethod
    def _require_dependencies():
        if pytesseract is None or Image is None:
            raise RuntimeError(
                "OCR dependencies are missing. "
                "Install with: pip install pytesseract pillow"
            )

    def extract_text(
        self,
        image_path: Path,
        language: str = "eng",
    ) -> str:
        self._require_dependencies()

        image_path = Path(image_path)

        if not image_path.exists():
            raise FileNotFoundError(image_path)

        if not self.is_supported(image_path):
            raise ValueError(
                f"Unsupported image format: {image_path.suffix}"
            )

        image = Image.open(image_path)

        return pytesseract.image_to_string(
            image,
            lang=language,
        ).strip()

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    def is_supported(self, path: Path) -> bool:
        return path.suffix.lower() in self.SUPPORTED_EXTENSIONS

    @staticmethod
    def exists(path: Path) -> bool:
        return Path(path).exists()

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)