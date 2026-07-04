from services.intent_service import intent_service
from core.action_engine import action_engine

from skills.apps import handle as apps
from skills.browser import handle as browser
from skills.system import handle as system
from skills.memory import handle as memory
from skills.ai import handle as ai
from skills.vision import handle as vision


class Router:

    def __init__(self):

        action_engine.register("open_app", apps)
        action_engine.register("close_app", apps)

        action_engine.register("google_search", browser)
        action_engine.register("youtube_search", browser)

        action_engine.register("memory", memory)

        action_engine.register("system", system)

        action_engine.register("camera", vision)
        action_engine.register("vision", vision)

    def route(self, command):

        print(f"[ROUTER] {command}")

        intent = intent_service.detect(command)

        response = action_engine.execute(intent, command)

        if response is not None:
            return response

        return ai(command)


router = Router()