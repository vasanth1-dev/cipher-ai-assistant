from services.intent_service import intent_service
from core.action_engine import action_engine
from core.registry import register_actions

from skills.ai import handle as ai


class Router:

    def __init__(self):

        register_actions()

    def route(self, command):

        print(f"[ROUTER] {command}")

        intent = intent_service.detect(command)

        response = action_engine.execute(intent, command)

        if response is not None:
            return response

        return ai(command)


router = Router()