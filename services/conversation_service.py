from core.logger import logger
from config import USER_NAME, ASSISTANT_NAME


class ConversationService:

    def __init__(
       self,
    ) -> None:

        self.last_topic = None

        self.responses = (
            self._load_default_responses()
        )

    def _load_default_responses(
        self,
    ) -> dict[str, str]:
        """
        Load built-in conversation responses.
        """

        return {

            "hello": f"Hello {USER_NAME}! How can I help you today?",

            "hi": f"Hello {USER_NAME}! How can I help you today?",

            "hey": f"Hello {USER_NAME}! How can I help you today?",

            "good morning": "Good morning!",

            "good afternoon": "Good afternoon!",

            "good evening": "Good evening!",

            "how are you": (
                "I'm doing well. How can I help you?"
            ),

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

            "see you": "Goodbye",


        }
    
    def _normalize_command(
        self,
        text: str,
    ) -> str:

        return " ".join(
            text.lower().strip().split()
        )
    
    def _find_partial_match(
        self,
        command: str,
    ):

        for phrase, response in self.responses.items():

            if (

                command == phrase
                or command.startswith(
                    phrase + " "
                )
                or command.endswith(
                    " " + phrase
                )
                or (
                    " " + phrase + " "
                ) in (
                    " " + command + " "
                )

            ):

                return (
                    phrase,
                    response,
                )

        return (
            None,
            None,
        )
    # ------------------------------------------------ #

    def process(
        self, 
        command: str,
    ) -> str | None:

        if not command:
            return None

        command = self._normalize_command(
            command,
        )

        # Exact match
        if command in self.responses:

            response = self.responses[command]

            logger.info(
                f"[CONVERSATION] {command} -> {response}"
            )

            return response

        # Partial match
        phrase, response = (
            self._find_partial_match(
                command,
            )
        )

        if response:

            logger.info(

                f"[CONVERSATION] "

                f"{phrase} -> {response}"

            )

            return response

        logger.debug(
            "[CONVERSATION] No conversation match."
        )

        return None

    # ------------------------------------------------ #

    def register(
        self, 
        phrase: str, 
        response: str,
    ) -> None:

        if not phrase or not response:
            return

        self.responses[
            phrase.lower().strip()
        ] = response

        logger.info(
            f"[CONVERSATION] Registered: {phrase}"
        )

    # ------------------------------------------------ #

    def remove(
        self, 
        phrase: str,
    ) -> None:

        phrase = self._normalize_command(
            phrase,
        )

        if phrase in self.responses:

            del self.responses[phrase]

            logger.info(
                f"[CONVERSATION] Removed: {phrase}"
            )

    # ------------------------------------------------ #

    def available(
        self,
    ) -> list[str]:

        return sorted(self.responses.keys())
    
    def set_topic(
            self,
            topic: str,
    ):
        
        if topic:
            self.last_topic = topic.strip()

    def get_topic(
        self,
    ) -> str | None:

        return self.last_topic
    
    def clear_topic(
        self,
    ) -> None:

        self.last_topic = None


conversation_service = ConversationService()