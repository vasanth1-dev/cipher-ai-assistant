from config import WAKE_WORDS


class WakeWord:

    CORRECTIONS = {
        "cypher": "cipher",
        "cifer": "cipher",
        "sifer": "cipher",
        "safer": "cipher",
        "safe her": "cipher",
        "sai": "cipher",
        "sire": "cipher",
        "cyper": "cipher",
        "cipher": "cipher",
        "zipper": "cipher",
        "super": "cipher",
        "cycle": "cipher",
    }


    def __init__(
       self,
    ) -> None:
        self.wake_words = sorted(
            [w.lower().strip() for w in WAKE_WORDS],
            key=len,
            reverse=True,
        )

    def normalize(
        self, 
        text: str,
    ) -> str:

        if not text:
            return ""

        text = text.lower().strip()

        for wrong, correct in self.CORRECTIONS.items():
            text = text.replace(
                wrong,
                correct,
            )

        return " ".join(text.split())
    
    def _matches(
        self,
        text: str,
        wake_word: str,
    ) -> bool:

        return (
            text == wake_word
            or text.startswith(wake_word + " ")
            or f" {wake_word} " in f" {text} "
        )

    def detect(
        self, 
        text: str,
    ) -> bool:

        if not text:
            return False

        text = self.normalize(text)

        for wake_word in self.wake_words:

            if self._matches(
                text,
                wake_word,
            ):
                return True
            
        return False

            

    def remove(
        self, 
        text: str,
    ) -> str:

        if not text:
            return ""

        text = self.normalize(text)

        for word in self.wake_words:

            if self._matches(
                text,
                word,
            ) and text.startswith(word):

                return text[len(word):].strip()

        return text


wakeword = WakeWord()