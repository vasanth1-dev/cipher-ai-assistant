import pyttsx3

from config import (
    ASSISTANT_NAME,
    SPEECH_RATE,
    SPEECH_VOLUME,
)


class Speaker:

    def __init__(self):

        self.engine = pyttsx3.init()

        self.engine.setProperty("rate", SPEECH_RATE)
        self.engine.setProperty("volume", SPEECH_VOLUME)

        voices = self.engine.getProperty("voices")

        if voices:
            self.engine.setProperty("voice", voices[0].id)

    def speak(self, text: str):

        if not text:
            return

        print(f"{ASSISTANT_NAME} : {text}")

        self.engine.say(text)
        self.engine.runAndWait()

    def stop(self):
        self.engine.stop()


speaker = Speaker()