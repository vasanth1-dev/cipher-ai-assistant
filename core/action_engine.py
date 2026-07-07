from core.logger import logger


class ActionEngine:

    def __init__(self):

        self.actions = {}

    # ----------------------------------------
    # Register
    # ----------------------------------------

    def register(self, intents, handler):

        if isinstance(intents, str):
            intents = [intents]

        for intent in intents:

            if not intent:
                continue

            intent = intent.strip().lower()

            self.actions[intent] = handler

            logger.info(f"[ACTION REGISTERED] {intent}")

    # ----------------------------------------
    # Execute
    # ----------------------------------------

    def execute(self, intent, command):

        if not intent:
            return None

        intent = intent.strip().lower()

        handler = self.actions.get(intent)

        if handler is None:

            logger.warning(f"[ACTION] No handler for intent: {intent}")

            return None

        try:

            logger.info(f"[ACTION] Executing: {intent}")

            return handler(command)

        except Exception as e:

            logger.exception(e)

            return "Sorry, something went wrong while executing that action."

    # ----------------------------------------
    # Utilities
    # ----------------------------------------

    def registered(self):

        return sorted(self.actions.keys())

    def has(self, intent):

        if not intent:
            return False

        return intent.strip().lower() in self.actions

    def clear(self):

        self.actions.clear()


action_engine = ActionEngine()