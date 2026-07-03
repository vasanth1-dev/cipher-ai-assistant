import tempfile

import sounddevice as sd
import soundfile as sf
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
        self.sample_rate = SAMPLE_RATE

    def listen(self):

        try:

            print("🎤 Listening...")

            audio = sd.rec(
                int(LISTEN_SECONDS * self.sample_rate),
                samplerate=self.sample_rate,
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
                    self.sample_rate,
                )

                segments, info = model.transcribe(
                    temp.name,
                    beam_size=1,
                    vad_filter=True,
                )

            text = " ".join(
                segment.text.strip()
                for segment in segments
            ).strip()

            if not text:
                return ""

            text = text.lower()

            # ---------- Indian Accent Corrections ----------

            corrections = {
                "fire fox": "firefox",
                "vs code": "vscode",
                "visual studio": "vscode",
                "google chrome": "chrome",

                # Wake word variations
                "safer": "cipher",
                "safe her": "cipher",
                "cypher": "cipher",
                "sifer": "cipher",
                "cifer": "cipher",
            }

            for old, new in corrections.items():
                text = text.replace(old, new)

            print(f"Recognized: {text}")

            return text

        except Exception as e:

            print(f"Listener Error: {e}")
            return ""


listener = Listener()