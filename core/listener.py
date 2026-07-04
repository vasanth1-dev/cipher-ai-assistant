import tempfile

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

print("Loading Whisper model...")

model = WhisperModel(
    WHISPER_MODEL,
    device=DEVICE,
    compute_type=COMPUTE_TYPE,
)

print("Whisper model loaded.")


class Listener:

    def __init__(self):

        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8

    def google_stt(self):

        try:

            with sr.Microphone(sample_rate=16000) as source:

                print("🎤 Listening...")

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
                language="en-IN",
            )

            print(f"Recognized (Google): {text}")

            return text.lower().strip()

        except Exception:

            return None

    def whisper_stt(self):

        try:

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

                sf.write(
                    temp.name,
                    audio,
                    SAMPLE_RATE,
                )

                segments, _ = model.transcribe(
                    temp.name,
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

            return text.lower()

        except Exception:

            return ""

    def listen(self):

        text = self.google_stt()

        if text:
            return text

        print("Google STT failed. Using Whisper...")

        return self.whisper_stt()


listener = Listener()