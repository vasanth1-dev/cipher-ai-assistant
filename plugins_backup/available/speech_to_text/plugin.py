"""
Cipher v2
Speech-to-Text Plugin

Provides speech recognition utilities.

Features
--------
- Transcribe audio files
- Live microphone transcription
- Language selection
- Timestamp support (when available)
"""

from __future__ import annotations

from pathlib import Path

from core.logger import logger
from plugins.base_plugin import Plugin

try:
    from faster_whisper import WhisperModel
except ImportError:
    WhisperModel = None


class SpeechToTextPlugin(Plugin):
    """
    Speech-to-Text plugin.
    """

    name = "speech_to_text"
    version = "1.0.0"
    description = "Convert speech into text."

    def __init__(
       self,
    ) -> None:
        super().__init__()

        self._model = None

    # --------------------------------------------------
    # Plugin API
    # --------------------------------------------------

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "speech to text",
            "transcribe",
            "transcription",
            "voice to text",
            "audio to text",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        Speech recognition requests are expected to be routed
        through Cipher's structured speech intent pipeline.
        """

        return {
            "success": True,
            "message": (
                "Speech-to-Text plugin is available. "
                "Waiting for structured STT commands."
            ),
        }

    # --------------------------------------------------
    # Model
    # --------------------------------------------------

    def load_model(
        self,
        model_name: str = "base.en",
        device: str = "cpu",
        compute_type: str = "int8",
    ) -> None:
        if WhisperModel is None:
            raise RuntimeError(
                "faster-whisper is not installed. "
                "Install it using: pip install faster-whisper"
            )

        self._model = WhisperModel(
            model_name,
            device=device,
            compute_type=compute_type,
        )

    def _require_model(self):
        if self._model is None:
            raise RuntimeError(
                "Speech model is not loaded. "
                "Call load_model() first."
            )

    # --------------------------------------------------
    # Transcription
    # --------------------------------------------------

    def transcribe(
        self,
        audio_path: Path,
        language: str = "en",
    ) -> dict:
        """
        Transcribe an audio file.
        """
        self._require_model()

        audio_path = Path(audio_path)

        if not audio_path.exists():
            raise FileNotFoundError(audio_path)

        segments, info = self._model.transcribe(
            str(audio_path),
            language=language,
            beam_size=5,
            vad_filter=True,
        )

        transcript = []
        timeline = []

        for segment in segments:
            transcript.append(segment.text)

            timeline.append(
                {
                    "start": segment.start,
                    "end": segment.end,
                    "text": segment.text,
                }
            )

        return {
            "text": " ".join(transcript).strip(),
            "language": getattr(info, "language", language),
            "duration": getattr(info, "duration", None),
            "segments": timeline,
        }

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)