from services.settings_service import settings_service


INTENT = "settings"


def handle(command: str):

    command = command.lower().strip()

    # --------------------------
    # Show Settings
    # --------------------------

    if command in (
        "show settings",
        "settings",
    ):

        settings = settings_service.load()

        if not settings:
            return "No settings have been configured yet."

        result = []

        for key, value in settings.items():

            result.append(
                f"{key} : {value}"
            )

        return "\n".join(result)

    # --------------------------
    # Reset Settings
    # --------------------------

    if command == "reset settings":

        return settings_service.reset()

    # --------------------------
    # Speech Rate
    # --------------------------

    if command.startswith("set speech rate to"):

        try:

            value = int(
                command.replace(
                    "set speech rate to",
                    "",
                    1,
                ).strip()
            )

            return settings_service.set(
                "speech_rate",
                value,
            )

        except Exception:

            return "Please provide a valid speech rate."

    # --------------------------
    # Speech Volume
    # --------------------------

    if command.startswith("set volume to"):

        try:

            value = float(
                command.replace(
                    "set volume to",
                    "",
                    1,
                ).strip()
            )

            return settings_service.set(
                "speech_volume",
                value,
            )

        except Exception:

            return "Please provide a valid volume."

    # --------------------------
    # AI Model
    # --------------------------

    if command.startswith("change model to"):

        model = command.replace(
            "change model to",
            "",
            1,
        ).strip()

        if not model:
            return "Please provide a model name."

        return settings_service.set(
            "ollama_model",
            model,
        )
    
    if command.startswith("change theme to"):

        theme = command.replace(
            "change theme to",
            "",
            1,
        ).strip()

        return (
            f"Theme '{theme}' is not implemented yet."
        )

    # --------------------------
    # Gemini
    # --------------------------

    if command == "enable gemini":

        return settings_service.set(
            "gemini_enabled",
            True,
        )

    if command == "disable gemini":

        return settings_service.set(
            "gemini_enabled",
            False,
        )

    return None