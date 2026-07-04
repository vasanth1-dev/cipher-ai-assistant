from skills.apps import handle as apps
from skills.browser import handle as browser
from skills.system import handle as system
from skills.volume import handle as volume
from skills.weather import handle as weather
from skills.memory import handle as memory
from skills.history import handle as history
from skills.notification import handle as notification
from skills.vision import handle as vision
from skills.ai import handle as ai


class Router:

    def __init__(self):

        # Local handlers (Fast)
        self.handlers = [
            apps,
            browser,
            system,
            volume,
            weather,
            memory,
            history,
            notification,
            vision,
        ]

    def route(self, command: str):

        if not command:
            return None

        command = command.lower().strip()

        print(f"[ROUTER] {command}")

        # ---------- Local Skills ----------
        for handler in self.handlers:

            try:

                response = handler(command)

                if response:
                    return response

            except Exception as e:
                print(f"[{handler.__module__}] {e}")

        # ---------- AI Fallback ----------
        return ai(command)


router = Router()