from core.logger import logger


class IntentService:

    def __init__(
       self,
    ) -> None:

        self.intents = (

            self.__load_default_intents()
        )

        self._build_sorted_phrases()


    def __load_default_intents(
        self
    ) -> dict[str, list[str]]:

        return {
            "open_app": [
                "open",
                "launch",
                "start",
                "run",
            ],

            "close_app": [
                "close",
                "quit",
                "exit",
            ],

            "google_search": [
                "search google",
                "google",
            ],

            "youtube_search": [
                "search youtube",
                "youtube",
            ],

            "camera": [
                "take photo",
                "take picture",
                "capture image",
                "open camera",
            ],

            "screen": [
                "read screen",
                "screen",
            ],

            "memory": [
                "remember",
                "forget",
                "what is my",
                "show memory",
                "show memories",
                "what do you remember",
            ],

            "system": [
                "battery",
                "cpu",
                "ram",
                "disk",
                "time",
                "what time",
                "current time",
                "date",
                "today",
                "volume",
                "volume up",
                "volume down",
                "increase volume",
                "decrease volume",
                "mute",
                "unmute",
                "brightness",
                "brightness up",
                "brightness down",
                "increase brightness",
                "decrease brightness",
                "maximum brightness",
                "minimum brightness",
                "screenshot",
                "take screenshot",
                "capture screen",
                "capture screenshot",
                "screen capture",
                "lock",
                "lock screen",
                "lock computer",
                "lock my computer",
                "wifi",
                "wi-fi",
                "wifi on",
                "wifi off",
                "turn on wifi",
                "turn off wifi",
                "enable wifi",
                "disable wifi",
                "bluetooth",
                "bluetooth on",
                "bluetooth off",
                "turn on bluetooth",
                "turn off bluetooth",
                "enable bluetooth",
                "disable bluetooth",
                "sleep",
                "suspend",
                "hibernate",
                "put computer to sleep",
                "sleep computer",
                "hibernate computer",
                "notification",
                "notify",
                "show notification",
                "send notification",
            ],

            "vision": [
                "what do you see",
                "describe image",
            ],

            "notification": [
                "notify",
                "notification",
            ],

            "todo": [
                "todo",
                "add todo",
                "add a todo",
                "create todo",
                "create a todo",
                "add task",
                "create task",
                "show todo",
                "show todos",
                "show my todos",
                "list todos",
                "list my todos",
                "list tasks",
                "my tasks",
                "complete task",
                "mark task",
                "mark completed",
                "mark as completed",
                "delete task",
                "delete todo",
                "remove todo",
            ],

            "reminder": [
                "remind me",
                "show reminders",
                "list reminders",
                "my reminders",
                "complete reminder",
                "delete reminder",
                "clear reminders",
                "clear completed reminders",
            ],

            "calendar": [
                "calendar",
                "show calendar",
                "my calendar",
                "list events",
                "add event",
                "delete event",
            ],

            "whatsapp": [
                "open whatsapp",
                "send whatsapp",
                "send whatsapp message",
                "whatsapp",
            ],

            "contact": [
                "add contact",
                "show contacts",
                "list contacts",
                "contacts",
                "find contact",
                "delete contact",
            ],

            "files": [
                "open downloads",
                "open documents",
                "open desktop",
                "open pictures",
                "open videos",
                "open music",
                "open home",
                "show downloads",
                "show documents",
                "create folder",
                "delete folder",
                "list downloads",
                "list documents",
            ],

            "settings": [
                "settings",
                "show settings",
                "reset settings",
                "set speech rate",
                "set volume",
                "change model",
                "enable gemini",
                "disable gemini",
                "change theme",
                "dark mode",
                "light mode",
            ],
        }


    def _build_sorted_phrases(
        self,
    ) -> None:
        """
        Build the phrase lookup table.
        """

        self._sorted = []

        for intent, phrases in self.intents.items():

            for phrase in phrases:

                self._sorted.append(

                    (
                        self._normalize_command(
                            phrase,
                        ),
                        intent,
                    )

                )

        self._sorted.sort(

            key=lambda item: len(item[0]),

            reverse=True,

        )

    def _normalize_command(
        self,
        text: str,
    ) -> str:
        """
        Normalize commands and phrases for matching.
        """

        return " ".join(
            text.lower().strip().split()
        )
    
    def _matches_phrase(
        self,
        command: str,
        phrase: str,
    ) -> bool:
        """
        Check whether a command matches a phrase.
        """

        return (
            command == phrase
            or command.startswith(
                phrase + " "
            )
            or f" {phrase} " in f" {command} "
        )
                    
             

    # ------------------------------------------------ #

    def detect(
        self, 
        command: str,
    ) -> str:

        if not command:
            return "ai"

        command = self._normalize_command(
            command,
        )

        for phrase, intent in self._sorted:

            if self._matches_phrase(
                command,
                phrase,
            ):

                logger.info(
                    f"[INTENT] {intent} ({phrase})"
                )

                return intent

        logger.info("[INTENT] ai")

        return "ai"

    # ------------------------------------------------ #

    def register(
        self, 
        intent, 
        phrases: str | list[str],
    ) -> None:

        if isinstance(phrases, str):
            phrases = [phrases]

        if intent not in self.intents:
            self.intents[intent] = []

        self.intents[intent].extend(
            phrases
        )

        self._build_sorted_phrases()

    # ------------------------------------------------ #

    def available(
        self
    ) -> list[str]:

        return sorted(self.intents.keys())


intent_service = IntentService()