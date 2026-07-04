from core.action_engine import action_engine

from skills.apps import handle as apps
from skills.browser import handle as browser
from skills.memory import handle as memory
from skills.system import handle as system
from skills.vision import handle as vision


def register_actions():

    action_engine.register(
        ["open_app", "close_app"],
        apps,
    )

    action_engine.register(
        ["google_search", "youtube_search"],
        browser,
    )

    action_engine.register(
        "memory",
        memory,
    )

    action_engine.register(
        "system",
        system,
    )

    action_engine.register(
        ["camera", "vision"],
        vision,
    )