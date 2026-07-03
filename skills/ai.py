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

    # Local commands are handled by other skills.
    for item in LOCAL_COMMANDS:

        if command.startswith(item):
            return None

    # Offline AI (Ollama)
    return ai_service.ask(command)