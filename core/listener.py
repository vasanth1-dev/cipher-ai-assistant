
import tempfile
import threading

import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from faster_whisper import WhisperModel

from core.logger import logger
from pathlib import Path

from config import (
    WHISPER_MODEL,
    DEVICE,
    COMPUTE_TYPE,
    SAMPLE_RATE,
    CHANNELS,
    LISTEN_SECONDS,
)

# --------------------------------------------------
# Listener Control
# --------------------------------------------------

LISTEN_ENABLED = threading.Event()
LISTEN_ENABLED.set()

RECORD_LOCK = threading.Lock()


class Listener:

    
    CORRECTIONS = {

            "cypher": "cipher",
            "hey cypher": "hey cipher",
            "hi cypher": "hi cipher",
            "okay cypher": "okay cipher",
            "cifer": "cipher",
            "cycle": "cipher",
            "sifer": "cipher",
            "safer": "cipher",
            "safe her": "cipher",
            "sai": "cipher",
            "fire fox": "firefox",

        }
    

    def __init__(
       self,
    ) -> None:

        self.on_listening = None
        self.on_processing = None
        self.on_idle = None

        self.recognizer = sr.Recognizer()

        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

        self.model: WhisperModel | None = None
        self.running = True
        self.model_lock = threading.Lock()

    # --------------------------------------------------

    def _load_whisper_model(
        self,
    ) -> None:

        with self.model_lock:

            if self.model is not None:
                return

            logger.info("Loading Whisper model...")

            self.model = WhisperModel(
                WHISPER_MODEL,
                device=DEVICE,
                compute_type=COMPUTE_TYPE,
            )

            logger.info("Whisper model loaded.")

    # --------------------------------------------------
    # Whisper STT (Primary)
    # --------------------------------------------------

    def whisper_stt(
        self,
    ) -> str:

        if not self.running:
            return ""

        filename = None

        try:

            if self.on_listening:
                self.on_listening()

            logger.info("🎤 Listening...")

            with RECORD_LOCK:

                audio = sd.rec(
                    int(LISTEN_SECONDS * SAMPLE_RATE),
                    samplerate=SAMPLE_RATE,
                    channels=CHANNELS,
                    dtype="float32",
                )

                sd.wait()

            with tempfile.NamedTemporaryFile(
                suffix=".wav",
                delete=False,
            ) as temp:

                filename = temp.name

            sf.write(
                filename,
                audio,
                SAMPLE_RATE,
            )

            if self.on_processing:
                self.on_processing()

            text = self._transcribe(
                filename,
            )

            text = self._normalize(text)

            if text:

                logger.info(
                    f"[WHISPER] {text}"
                )

                return text

            return ""

        except Exception as e:

            logger.exception(
                f"Whisper STT failed: {e}"
            )

            return ""

        finally:

            self._delete_temp_file(
                filename
            )

            if self.on_idle:
                self.on_idle()

    # --------------------------------------------------
    # Google STT (Fallback)
    # --------------------------------------------------

    def google_stt(
        self,
    ) -> str:

        if not self.running:
            return ""

        try:

            with sr.Microphone(
                sample_rate=SAMPLE_RATE
            ) as source:

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5,
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=LISTEN_SECONDS,
                    phrase_time_limit=LISTEN_SECONDS,
                )

            text = self.recognizer.recognize_google(
                audio,
                language="en-US",
            )

            text = self._normalize(text)


            if text:

                logger.info(
                    f"[GOOGLE] {text}"
                )

                return text

            return ""

        except Exception as e:

            logger.warning(
                f"Google STT failed: {e}"
            )

            return ""
        
    def _delete_temp_file(
        self,
        filename: str | None,
    ) -> None:

        if not filename:
            return

        try:
            path = Path(filename)

            if path.exists():
                path.unlink()


        except Exception as e:
            logger.warning(
                f"Failed to delete temporary audio file: {e}"
            )

    def _transcribe(
        self,
        filename: str,
    ) -> str:

        self._load_whisper_model()

        segments, _ = self.model.transcribe(
            filename,
            language="en",
            beam_size=5,
            best_of=5,
            vad_filter=True,
            condition_on_previous_text=False,
            initial_prompt="The wake word is Hey Cipher.",
        )

        text = " ".join(
            segment.text.strip()
            for segment in segments
        ).strip()

        logger.info(
            f"[TRANSCRIBE] {text!r}"
        )

        return text

    # --------------------------------------------------

    def _normalize(
        self, 
        text: str,
    ) -> str:

        if not text:
            return ""

        text = text.lower().strip()

        

        for wrong, correct in self.CORRECTIONS.items():
            text = text.replace(wrong, correct)

        return " ".join(text.split())

    # --------------------------------------------------

    def listen(
        self,
    ) -> str:

        if not self.running:
            return ""

        logger.info("Before LISTEN_ENABLED.wait()")

        LISTEN_ENABLED.wait(timeout=2)

        logger.info("After LISTEN_ENABLED.wait()")

        if not self.running:
            return ""

        if not LISTEN_ENABLED.is_set():
            return ""

        # Whisper First

        text = self.whisper_stt()

        logger.info(
            f"[LISTEN] Whisper returned: {text!r}"
        )

        if not self.running:
            return ""

        if text:
            return text

        logger.warning(
            "Whisper failed. Trying Google STT..."
        )

        return self.google_stt()
                

        
    def stop(
        self,
    ) -> None:

        self.running = False

        LISTEN_ENABLED.set()

        with self.model_lock:
            self.model = None


listener = Listener()


def pause_listening() -> None:
    LISTEN_ENABLED.clear()


def resume_listening() -> None:
    LISTEN_ENABLED.set()

