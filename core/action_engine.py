from core.logger import logger


class ActionEngine:

    def __init__(
       self,
    ) -> None:

        from collections.abc import Callable

        self.actions: dict[str, Callable[[str], object]] = {}

        from threading import RLock

        self._lock = RLock()

    def _normalize_intent(
        self,
        intent: str,
    ) -> str | None:

        if not isinstance(intent, str):
            return None

        intent = " ".join(
            intent.strip().split()
        ).lower()

        return intent or None

    # ----------------------------------------
    # Register
    # ----------------------------------------

    def register(
        self, 
        intents: str | list[str], 
        handler,
    ) -> None:

        if isinstance(intents, str):
            intents = [intents]

        with self._lock:

            for intent in intents:

                if not isinstance(intent, str):
                    continue

                intent = self._normalize_intent(
                    intent
                )

                if intent is None:
                    continue

                if intent in self.actions:
                    logger.warning(
                        f"[ACTION] '{intent}' is already registered. Overwriting."
                    )

                if not callable(handler):

                    logger.error(
                        f"[ACTION] Invalid handler for '{intent}'."
                    )

                    continue

                self.actions[intent] = handler

                logger.debug(f"[ACTION REGISTERED] {intent}")

    # ----------------------------------------
    # Execute
    # ----------------------------------------

    def execute(
        self, 
        intent: str, 
        command: str
    ):

        if not intent:
            return None

        intent = self._normalize_intent(
            intent
        )

        if intent is None:
            return None

        with self._lock:

            handler = self.actions.get(intent)

        if handler is None:

            logger.warning(
                f"[ACTION] No handler for intent: {intent}"
            )

            return None

        if not callable(handler):

            logger.error(
                f"[ACTION] Invalid handler: {intent}"
            )

            return None

        try:

            logger.debug(f"[ACTION EXECUTE] {intent}")

            return handler(command)

        except Exception:

            logger.exception(
                f"[ACTION FAILED] {intent}"
            )

            return "Sorry, something went wrong while executing that action."

    # ----------------------------------------
    # Utilities
    # ----------------------------------------

    def registered(
        self,
    ) -> tuple[str, ...]:

        with self._lock:

            return tuple(
                sorted(self.actions)
            )

    def has(
        self, 
        intent: str,
    ) -> bool:

        if not intent:
            return False

        return intent.strip().lower() in self.actions

    def clear(
        self,
    ) -> None:

        with self._lock:

            self.actions.clear()

            logger.info("[ACTION] Registry cleared.")


action_engine = ActionEngine()