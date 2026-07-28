from services.conversation_service import conversation_service
from services.intent_service import intent_service
from services.ai_service import ai_service

from core.action_engine import action_engine
from core.logger import logger
from core.registry import register_actions


class Router:

    def __init__(
       self,
    ) -> None:

        register_actions()


    def _normalize_command(
        self,
        command: str,
    ) -> str | None:

        if not command:
            return None

        command = str(command).strip().lower()

        return command or None


    def _handle_conversation(
        self,
        command: str,
    ):

        response = conversation_service.process(
            command
        )

        if response is not None:

            logger.info(
                "[ROUTER] Conversation handled."
            )

        return response


    def _handle_plugins(
        self,
        command: str,
    ):

        try:

            from plugins import plugin_manager

            logger.debug(
                "[PLUGIN] Checking plugins..."
            )


            for plugin in plugin_manager.plugins():

                if not plugin.enabled:
                    continue

                if not plugin.can_handle(command):
                    continue

                commands = plugin.commands()

                for trigger, handler in commands.items():

                    if (
                        command == trigger
                        or command.startswith(
                            trigger + " "
                        )
                    ):

                        result = handler(command)

                        if result is not None:

                            logger.info(
                                f"[PLUGIN] {plugin.name}"
                            )

                            return result

        except Exception:

            logger.exception(
                "[PLUGIN] Plugin execution failed."
            )

        return None


    def _ai_fallback(
        self,
        command: str,
    ) -> str:

        logger.info(
            "[ROUTER] AI fallback."
        )

        try:

            logger.debug(
                "[AI] Sending prompt..."
            )

            response = ai_service.generate(
                command
            )

            if response:
                return response

        except Exception:

            logger.exception(
                "[AI] AI fallback failed."
            )

        return (
            "Sorry, I couldn't process "
            "your request."
        )

    # --------------------------------------------------

    def route(
        self,
        command: str,
    ):

        command = self._normalize_command(command)

        if command is None:
            return None

        logger.info(
            f"[ROUTER] Processing: {command}"
        )

        try:

            # ----------------------------------------
            # Conversation
            # ----------------------------------------

            response = self._handle_conversation(
                command
            )

            if response is not None:


                logger.debug(
                    "[ROUTER] Conversation response returned."
                )

                return response

            # ----------------------------------------
            # Plugins
            # ----------------------------------------

            response = self._handle_plugins(
                command
            )

            if response is not None:
                return response

            # ----------------------------------------
            # Intent Detection
            # ----------------------------------------

            intent = (
                intent_service.detect(command)
                or "ai"
            )

            logger.info(
                f"[INTENT] {intent}"
            )

            # ----------------------------------------
            # Local Skills
            # ----------------------------------------

            if intent != "ai":

                logger.debug(
                    f"[ACTION] Executing '{intent}'"
                )

                try:

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

                except Exception:

                    logger.exception(
                        f"[ACTION] '{intent}' failed."
                    )

            # ----------------------------------------
            # AI Fallback
            # ----------------------------------------

            response = self._ai_fallback(
                command
            )

            logger.info(
                "[ROUTER] Completed."
            )

            return response

        except Exception:

            logger.exception(
                "[ROUTER] Routing failed."
            )

            return (
                "Sorry, I couldn't process "
                "that request."
            )
    
router = Router()