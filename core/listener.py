import os
import tempfile
import threading

import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from faster_whisper import WhisperModel

from core.logger import logger

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

RECORD_LOCK =threading.Lock()


class Listener:

    def __init__(self):

        self.on_listening = None
        self.on_processing = None
        self.on_idle = None

        self.recognizer = sr.Recognizer()

        self.recognizer.energy_threshold = 200
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.5

        self.model = None
        self.running = True

    # --------------------------------------------------

    def _load_whisper_model(self):

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

    def whisper_stt(self):

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

            self._load_whisper_model()

            segments, _ = self.model.transcribe(
                filename,
                language="en",
                beam_size=5,
                best_of=5,
                vad_filter=True,
                condition_on_previous_text=False,
                initial_prompt="The wake word is Hey Cipher. "
            )

            text = " ".join(
                segment.text.strip()
                for segment in segments
            ).strip()

            text = self._normalize(text)

            if text:

                logger.info(
                    f"Recognized (Whisper): {text}"
                )

                return text

            return ""

        except Exception as e:

            logger.exception(e)

            return ""

        finally:

            if filename and os.path.exists(filename):
                os.remove(filename)

            if self.on_idle:
                self.on_idle()

    # --------------------------------------------------
    # Google STT (Fallback)
    # --------------------------------------------------

    def google_stt(self):



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
                    timeout=5,
                    phrase_time_limit=6,
                )

            text = self.recognizer.recognize_google(
                audio,
                language="en-US",
            )

            text = self._normalize(text)


            if text:

                logger.info(
                    f"Recognized (Google): {text}"
                )

                return text

            return ""

        except Exception:

            return ""

    # --------------------------------------------------

    def _normalize(self, text):

        if not text:
            return ""

        text = text.lower().strip()

        corrections = {

            "cypher": "cipher",
            "cifer": "cipher",
            "cycle": "cipher",
            "sifer": "cipher",
            "safer": "cipher",
            "safe her": "cipher",
            "sai": "cipher",
            "fire fox": "firefox",

        }

        for wrong, correct in corrections.items():
            text = text.replace(wrong, correct)

        return " ".join(text.split())

    # --------------------------------------------------

    def listen(self):

        LISTEN_ENABLED.wait()

        # Whisper First

        text = self.whisper_stt()

        if text:
            return text

        logger.warning(
            "Whisper failed. Trying Google STT..."
        )

        return self.google_stt()
    
    def stop(self):

        self.running = False

        resume_listening()


listener = Listener()


def pause_listening():
    LISTEN_ENABLED.clear()


def resume_listening():
    LISTEN_ENABLED.set()

