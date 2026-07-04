class ActionEngine:

    def __init__(self):

        self.actions = {}

    def register(self, intent, handler):

        self.actions[intent] = handler

    def execute(self, intent, command):

        handler = self.actions.get(intent)

        if handler is None:
            return None

        return handler(command)


action_engine = ActionEngine()