class ActionEngine:

    def __init__(self):
        self.actions = {}

    def register(self, intents, handler):

        if isinstance(intents, str):
            intents = [intents]

        for intent in intents:
            self.actions[intent] = handler

    def execute(self, intent, command):

        handler = self.actions.get(intent)

        if handler:
            return handler(command)

        return None

    def registered(self):

        return list(self.actions.keys())


action_engine = ActionEngine()