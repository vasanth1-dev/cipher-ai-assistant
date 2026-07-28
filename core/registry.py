from core.action_engine import action_engine
from core.logger import logger

from skills.apps import handle as apps
from skills.browser import handle as browser
from skills.memory import handle as memory
from skills.system import handle as system
from skills.vision import handle as vision
from skills.notification import handle as notification
from skills.todo import handle as todo
from skills.reminder import handle as reminder
from skills.calendar import handle as calendar
from skills.whatsapp import handle as whatsapp
from skills.contact import handle as contact
from skills.files import handle as files
from skills.settings import handle as settings


_registered = False


def register_actions() -> None:
    """
    Register all built-in skill handlers.

    Safe to call multiple times.
    """

    global _registered

    if _registered:

        logger.info(
            "[REGISTRY] Skills already registered."
        )
        return

    registrations = [
        (["open_app", "close_app"], apps),
        (["google_search", "youtube_search"], browser),
        ("memory", memory),
        ("system", system),
        (["camera", "vision"], vision),
        ("notification", notification),
        ("todo", todo),
        ("reminder", reminder),
        ("calendar", calendar),
        ("whatsapp", whatsapp),
        ("contact", contact),
        ("files", files),
        ("settings", settings),
    ]

    loaded = 0

    for intents, handler in registrations:

        try:
            action_engine.register(intents, handler)
            loaded += 1

        except Exception:
            logger.exception(
                f"[REGISTRY] Failed to register {handler.__module__}"
            )

    _registered = True

    logger.info(
        f"[REGISTRY] Loaded {loaded} skill(s)."
    )