from core.logger import logger


class IntentService:

    def __init__(self):

        self.intents = {}

        self.__load_builtin_intents()

            
        self._sorted = []

        for intent, phrases in self.intents.items():

            for phrase in phrases:

                self._sorted.append(
                    (
                        phrase.lower().strip(),
                        intent,
                    )
                )

        self._sorted.sort(
            key=lambda item: len(item[0]),
            reverse=True,
        )
    def __load_builtin_intents(self):

        self.intents = {

            "open_app": [
                "open",
                "launch",
                "start",
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
            ],

            "system": [
                "battery",
                "cpu",
                "ram",
                "disk",
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
                "add task",
                "show task",
                "list tasks",
                "my tasks",
                "todo",
                "complete task",
                "delete task",
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
                "send whatsapp",
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
            ],
        }
            
             

    # ------------------------------------------------ #

    def detect(self, command: str):

        if not command:
            return "ai"

        command = " ".join(
            command.lower().strip().split()
        )

        for phrase, intent in self._sorted:

            if (
                command == phrase
                or command.startswith(phrase + " ")
                or phrase in command
            ):

                logger.info(
                    f"[INTENT] {intent} ({phrase})"
                )

                return intent

        logger.info("[INTENT] ai")

        return "ai"

    # ------------------------------------------------ #

    def register(self, intent, phrases):

        if isinstance(phrases, str):
            phrases = [phrases]

        if intent not in self.intents:
            self.intents[intent] = []

        self.intents[intent].extend(phrases)

        self.__init__()

    # ------------------------------------------------ #

    def available(self):

        return sorted(self.intents.keys())


intent_service = IntentService()