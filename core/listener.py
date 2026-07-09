import os
import tempfile
import threading

import sounddevice as sd
import soundfile as sf
import speech_recognition as sr
from faster_whisper import WhisperModel

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

print("Loading Whisper model...")

model = WhisperModel(
    WHISPER_MODEL,
    device=DEVICE,
    compute_type=COMPUTE_TYPE,
)

print("Whisper model loaded.")


class Listener:

    def __init__(self):

        self.on_listening = None
        self.on_processing = None
        self.on_idle = None

        self.recognizer = sr.Recognizer()

        self.recognizer.energy_threshold = 200
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.5

    # --------------------------------------------------

    def google_stt(self):

        try:

            if self.on_listening:
                self.on_listening()

            with sr.Microphone(sample_rate=16000) as source:

                print("🎤 Listening...")

                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=1.0,
                )

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=6,
                )

            if self.on_processing:
                self.on_processing()

            text = self.recognizer.recognize_google(
                audio,
                language="en-US",
            )

            if text:
                print(f"Recognized (Google): {text}")
                return text._normalize(text)

            return ""

        except Exception:

            return ""

        finally:

            if self.on_idle:
                self.on_idle()

    # --------------------------------------------------

    def whisper_stt(self):

        filename = None

        try:

            if self.on_listening:
                self.on_listening()

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

            segments, _ = model.transcribe(
                filename,
                language="en",
                beam_size=5,
                best_of=5,
                vad_filter=True,
                condition_on_previous_text=False,
            )

            text = " ".join(
                segment.text.strip()
                for segment in segments
            ).strip()

            if text:

                print(f"Recognized (Whisper): {text}")

                return self._normalize(text)

            return ""

        except Exception as e:

            print("Whisper Error:", e)

            return ""

        finally:

            if filename and os.path.exists(filename):
                os.remove(filename)

            if self.on_idle:
                self.on_idle()


    def _normalize(self, text: str) -> str:

        text = text.lower().strip()

        corrections = {
            "cypher": "cipher",
            "cycle": "cipher",
            "sai": "cipher",
            "safe her": "cipher",
            "cifer": "cipher",
            "firefox": "firefox",
        }

        for wrong, correct in corrections.items():
            text = text.replace(wrong, correct)

        return text

    # --------------------------------------------------

    def listen(self):

        LISTEN_ENABLED.wait()

        text = self.google_stt()

        if text:
            return text

        print("Google STT failed. Using Whisper...")

        return self.whisper_stt()


listener = Listener()


def pause_listening():
    LISTEN_ENABLED.clear()


def resume_listening():
    LISTEN_ENABLED.set()