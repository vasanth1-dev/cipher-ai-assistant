class IntentService:

    def __init__(self):

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
        }

    def detect(self, command: str):

        command = command.lower().strip()

        for intent, phrases in self.intents.items():

            for phrase in phrases:

                if command.startswith(phrase):
                    return intent

        return "ai"


intent_service = IntentService()