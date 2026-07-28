"""
Cipher v2
Translator Plugin

Provides text translation capabilities.

Features
--------
- Translate text between languages
- Automatic language detection (when supported)
- List supported languages
- Simple API for other Cipher components
"""

from __future__ import annotations

from core.logger import logger
from plugins.base_plugin import Plugin

try:
    # googletrans 4.x
    from googletrans import LANGUAGES, Translator
except ImportError:
    Translator = None
    LANGUAGES = {}


class TranslatorPlugin(Plugin):
    """
    Translator plugin.
    """

    name = "translator"
    version = "1.0.0"
    description = "Translate text between languages."

    def __init__(
       self,
    ) -> None:
        super().__init__()

        self._translator = Translator() if Translator else None

    # --------------------------------------------------
    # Plugin API
    # --------------------------------------------------

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "translate",
            "translation",
            "translate this",
            "convert to",
            "meaning in",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        Translation requests are expected to be routed through
        Cipher's structured intent pipeline.

        Example:

        {
            "text": "...",
            "source": "auto",
            "target": "ta"
        }
        """

        return {
            "success": True,
            "message": (
                "Translator plugin is available. "
                "Waiting for structured translation commands."
            ),
        }

    # --------------------------------------------------
    # Translation
    # --------------------------------------------------

    def translate(
        self,
        text: str,
        target: str,
        source: str = "auto",
    ) -> dict:
        self._require_library()

        result = self._translator.translate(
            text,
            src=source,
            dest=target,
        )

        return {
            "text": result.text,
            "source": result.src,
            "target": target,
            "original": text,
            "pronunciation": getattr(result, "pronunciation", None),
        }

    # --------------------------------------------------
    # Languages
    # --------------------------------------------------

    @staticmethod
    def supported_languages() -> dict:
        return dict(LANGUAGES)

    @staticmethod
    def is_supported(language_code: str) -> bool:
        return language_code.lower() in LANGUAGES

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _require_library():
        if Translator is None:
            raise RuntimeError(
                "googletrans is not installed. "
                "Install it using: pip install googletrans==4.0.2"
            )

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)