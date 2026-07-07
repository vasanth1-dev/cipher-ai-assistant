from config import WAKE_WORDS


class WakeWord:

    def __init__(self):
        self.wake_words = [w.lower().strip() for w in WAKE_WORDS]

    def normalize(self, text: str):

        text = text.lower().strip()

        corrections = {
            "cypher": "cipher",
            "cifer": "cipher",
            "sifer": "cipher",
            "safer": "cipher",
            "safe her": "cipher",
        }

        for wrong, correct in corrections.items():
            text = text.replace(wrong, correct)

        return text

    def detect(self, text: str):

        if not text:
            return False

        text = self.normalize(text)

        return any(text.startswith(word) for word in self.wake_words)

    def remove(self, text: str):

        if not text:
            return ""

        text = self.normalize(text)

        for word in self.wake_words:
            if text.startswith(word):
                return text[len(word):].strip()

        return text


wakeword = WakeWord()