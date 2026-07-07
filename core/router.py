from services.conversation_service import conversation_service
from services.intent_service import intent_service

from core.action_engine import action_engine
from core.logger import logger
from core.registry import register_actions


class Router:

    def __init__(self):

        register_actions()

    # --------------------------------------------------

    def route(self, command):

        if not command:
            return None

        command = str(command).strip().lower()

        if not command:
            return None

        logger.info(f"[ROUTER] {command}")

        try:

            # ----------------------------------------
            # Conversation Commands
            # ----------------------------------------

            response = conversation_service.process(
                command
            )

            if response is not None:

                logger.info(
                    "[ROUTER] Conversation handled."
                )

                return response

            # ----------------------------------------
            # Intent Detection
            # ----------------------------------------

            intent = intent_service.detect(
                command
            )

            if not intent:
                intent = "ai"

            logger.info(
                f"[INTENT] {intent}"
            )

            # ----------------------------------------
            # Local Skills
            # ----------------------------------------

            if intent != "ai":

                response = action_engine.execute(
                    intent,
                    command,
                )

                if response is not None:

                    logger.info(
                        f"[ACTION] {intent}"
                    )

                    return response

                logger.warning(
                    f"[ACTION] '{intent}' returned None."
                )

            # ----------------------------------------
            # AI Fallback
            # ----------------------------------------

            logger.info(
                "[ROUTER] AI fallback."
            )

            return None

        except Exception as e:

            logger.exception(e)

            return (
                "Sorry, I couldn't process "
                "that request."
            )


router = Router()