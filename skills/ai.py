from services.ai_service import ai_service


LOCAL_COMMANDS = (
    "open ",
    "close ",
    "launch ",
    "start ",
    "shutdown",
    "restart",
    "reboot",
    "logout",
    "volume",
    "mute",
    "weather",
    "search google",
    "search youtube",
    "remember",
    "history",
    "notify",
)


def handle(command: str):

    if not command:
        return None

    command = command.strip()

    for item in LOCAL_COMMANDS:
        if command.startswith(item):
            return None

    # AI is handled by assistant streaming
    return None