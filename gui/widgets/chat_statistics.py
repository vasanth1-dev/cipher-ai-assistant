from dataclasses import dataclass


@dataclass
class ChatStatistics:

    user_messages: int = 0
    assistant_messages: int = 0
    system_messages: int = 0

    total_messages: int = 0

    total_words: int = 0
    total_characters: int = 0

    # --------------------------------------------------

    def add(self, sender: str, text: str):

        sender = sender.lower()

        self.total_messages += 1

        self.total_words += len(text.split())

        self.total_characters += len(text)

        if sender == "you":

            self.user_messages += 1

        elif sender == "system":

            self.system_messages += 1

        else:

            self.assistant_messages += 1

    # --------------------------------------------------

    def reset(self):

        self.user_messages = 0
        self.assistant_messages = 0
        self.system_messages = 0

        self.total_messages = 0
        self.total_words = 0
        self.total_characters = 0

    # --------------------------------------------------

    def to_dict(self):

        return {
            "user_messages": self.user_messages,
            "assistant_messages": self.assistant_messages,
            "system_messages": self.system_messages,
            "total_messages": self.total_messages,
            "total_words": self.total_words,
            "total_characters": self.total_characters,
        }