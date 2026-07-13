from core.logger import logger
from config import USER_NAME, ASSISTANT_NAME


class ConversationService:

    def __init__(self):

        self.last_topic = None

        self.responses = {
            "hello": f"Hello {USER_NAME}! How can I help you today?",
            "hi": f"Hello {USER_NAME}! How can I help you today?",
            "hey": f"Hello {USER_NAME}! How can I help you today?",
            "good morning": "Good morning!",
            "good afternoon": "Good afternoon!",
            "good evening": "Good evening!",
            "how are you": "I'm doing well. How can I help you?",
            "who are you": (
                f"I am {ASSISTANT_NAME}, your personal Ubuntu AI assistant."
            ),
            "what is your name": (
                f"My name is {ASSISTANT_NAME}."
            ),
            "thank you": "You're welcome.",
            "thanks": "You're welcome.",
            "bye": "Goodbye.",
            "goodbye": "Goodbye.",
        }

    # ------------------------------------------------ #

    def process(self, command: str):

        if not command:
            return None

        command = " ".join(
            command.lower().strip().split()
        )

        # Exact match
        if command in self.responses:

            response = self.responses[command]

            logger.info(
                f"[CONVERSATION] {command} -> {response}"
            )

            return response

        # Partial match
        for phrase, response in self.responses.items():

            if phrase in command:

                logger.info(
                    f"[CONVERSATION] {phrase} -> {response}"
                )

                return response

        return None

    # ------------------------------------------------ #

    def register(self, phrase: str, response: str):

        if not phrase or not response:
            return

        self.responses[
            phrase.lower().strip()
        ] = response

    # ------------------------------------------------ #

    def remove(self, phrase: str):

        phrase = phrase.lower().strip()

        if phrase in self.responses:
            del self.responses[phrase]

    # ------------------------------------------------ #

    def available(self):

        return sorted(self.responses.keys())
    
    def set_topic(
            self,
            topic: str,
    ):
        
        if topic:
            self.last_topic = topic.strip()

    def get_topic(self):

        return self.last_topic
    
    def clear_topic(self):

        self.last_topic = None


conversation_service = ConversationService()