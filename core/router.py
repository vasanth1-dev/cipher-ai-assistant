from services.conversation_service import conversation_service
from services.intent_service import intent_service
from services.ai_service import ai_service

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

            try:

                from plugins import plugin_manager

                for plugin in plugin_manager.plugins():

                    if not plugin.enabled:
                        continue

                    if not plugin.can_handle(command):
                        continue

                    for trigger, handler in plugin.commands().items():

                        if (
                            command == trigger
                            or command.startswith(trigger + " ")

                        ):

                            result = handler(command)

                            if result is not None:

                                logger.info(
                                    f"[PLUGIN] {plugin.name}"
                            )

                            return result
                        
            except Exception as e:

                logger.exception(e)

            # ----------------------------------------
            # AI Fallback
            # ----------------------------------------

            logger.info(
                "[ROUTER] AI fallback."
            )

            response = None

            try:

                response = ai_service.generate(command)

            except Exception as e:

                logger.exception(e)

            if response:

                return response
            
            return (
                "Sorry, I couldn't process your request."
            )

        except Exception as e:

            logger.exception(e)

            return (
                "Sorry, I couldn't process "
                "that request."
            )


router = Router()