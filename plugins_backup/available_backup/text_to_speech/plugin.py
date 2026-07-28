"""
Cipher v2
Text-to-Speech Plugin

Provides speech synthesis utilities.

Features
--------
- Speak text
- Save speech to audio file
- List available voices
- Configure speech rate and volume
"""

from __future__ import annotations

from pathlib import Path

from core.logger import logger
from plugins.base_plugin import Plugin

try:
    import pyttsx3
except ImportError:
    pyttsx3 = None


class TextToSpeechPlugin(Plugin):
    """
    Text-to-Speech plugin.
    """

    name = "text_to_speech"
    version = "1.0.0"
    description = "Convert text into spoken audio."

    def __init__(
       self,
    ) -> None:
        super().__init__()

        self._engine = None

        if pyttsx3 is not None:
            self._engine = pyttsx3.init()

    # --------------------------------------------------
    # Plugin API
    # --------------------------------------------------

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "text to speech",
            "tts",
            "speak",
            "read aloud",
            "say this",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        Text-to-speech requests are expected to be routed through
        Cipher's structured speech intent pipeline.
        """

        return {
            "success": True,
            "message": (
                "Text-to-Speech plugin is available. "
                "Waiting for structured TTS commands."
            ),
        }

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def _require_engine(self):
        if self._engine is None:
            raise RuntimeError(
                "pyttsx3 is not installed. "
                "Install it using: pip install pyttsx3"
            )

    # --------------------------------------------------
    # Speech
    # --------------------------------------------------

    def speak(self, text: str) -> None:
        self._require_engine()

        self._engine.say(text)
        self._engine.runAndWait()

    def save_to_file(self, text: str, output: Path) -> Path:
        self._require_engine()

        output = Path(output)

        self._engine.save_to_file(text, str(output))
        self._engine.runAndWait()

        return output

    # --------------------------------------------------
    # Voice Configuration
    # --------------------------------------------------

    def voices(self) -> list[dict]:
        self._require_engine()

        result = []

        for voice in self._engine.getProperty("voices"):
            result.append(
                {
                    "id": voice.id,
                    "name": getattr(voice, "name", ""),
                    "languages": getattr(voice, "languages", []),
                }
            )

        return result

    def set_voice(self, voice_id: str) -> None:
        self._require_engine()
        self._engine.setProperty("voice", voice_id)

    def set_rate(self, rate: int) -> None:
        self._require_engine()
        self._engine.setProperty("rate", rate)

    def set_volume(self, volume: float) -> None:
        self._require_engine()
        volume = max(0.0, min(1.0, volume))
        self._engine.setProperty("volume", volume)

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)