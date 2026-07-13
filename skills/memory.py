from services.memory_service import memory_service


INTENT = "memory"


def _normalize(text):

    return " ".join(
        text.strip().split()
    )


def handle(command: str):

    if not command:
        return None

    original = _normalize(command)
    command = original.lower()

    # -------------------------------------------------
    # Remember
    # Example:
    # remember my bike is Duke 125
    # -------------------------------------------------

    if command.startswith("remember "):

        text = original[len("remember "):].strip()

        lower_text = text.lower()

        if " is " not in lower_text:
            return (
                "Please say it like: "
                "remember my bike is Duke 125."
            )

        index = lower_text.find(" is ")

        key = text[:index].strip()
        value = text[index + 4:].strip()

        if not key or not value:
            return (
                "Please tell me both the name "
                "and the value to remember."
            )

        memory_service.remember(key, value)

        return f"I'll remember your {key}."

    # -------------------------------------------------
    # Recall
    # -------------------------------------------------

    if command.startswith("what is "):

        key = original[len("what is "):].strip()

        key = key.strip()

        if key.lower().startswith("my "):
            key = key[3:].strip()

        elif key.lower().startswith("the "):
            key = key[4:].strip()

        elif key.lower().startswith("our "):
            key = key[4:].strip()

        if not key:
            return "What would you like me to recall?"

        value = memory_service.recall(key)

        if value is not None:
            return f"Your {key} is {value}."

        return f"I don't know your {key}."

    # -------------------------------------------------
    # Forget
    # -------------------------------------------------

    if command.startswith("forget "):

        key = original[len("forget "):].strip()

        key = key.strip()

        if key.lower().startswith("my "):
            key = key[3:].strip()

        elif key.lower().startswith("the "):
            key = key[4:].strip()

        elif key.lower().startswith("our "):
            key = key[4:].strip()

        elif not key:
            return "What should I forget?"

        elif memory_service.forget(key):
            return f"I forgot your {key}."

        return f"I don't know your {key}."

    # -------------------------------------------------
    # Show Memory
    # -------------------------------------------------

    if command in (
        "show memory",
        "show memories",
        "what do you remember",
    ):

        data = memory_service.all()

        if not data:
            return "I don't remember anything yet."

        lines = []

        for key in sorted(data):
            lines.append(f"{key}: {data[key]}")

        return "\n".join(lines)

    return None