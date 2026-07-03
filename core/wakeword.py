from config import WAKE_WORD


class WakeWord:

    def __init__(self):
        self.wake_word = WAKE_WORD.lower()

        self.aliases = [
            "hey cipher",
            "cipher",
            "cypher",
            "safer",
            "software",
            "cifer",
            "yes sir",
        ]

    def detect(self, text: str) -> bool:

        if not text:
            return False

        text = text.lower().strip()

        return any(alias in text for alias in self.aliases)

    def remove(self, text: str) -> str:

        if not text:
            return ""

        text = text.lower().strip()

        for alias in self.aliases:
            if alias in text:
                return text.replace(alias, "", 1).strip()

        return text


wakeword = WakeWord()