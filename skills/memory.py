from services.memory_service import memory_service


def handle(command: str):

    if not command:
        return None

    command = command.lower().strip()

    # ---------------------------------------
    # Remember
    # Example:
    # remember my bike is duke 125
    # ---------------------------------------

    if command.startswith("remember "):

        text = command.replace("remember ", "", 1).strip()

        if " is " not in text:
            return "Please say it like: remember my bike is Duke 125."

        key, value = text.split(" is ", 1)

        key = key.strip()
        value = value.strip()

        memory_service.remember(key, value)

        return f"I'll remember your {key}."

    # ---------------------------------------
    # Recall
    # Example:
    # what is my bike
    # ---------------------------------------

    if command.startswith("what is "):

        key = command.replace("what is ", "", 1).strip()

        value = memory_service.recall(key)

        if value:
            return f"Your {key} is {value}."

        return f"I don't know your {key}."

    # ---------------------------------------
    # Forget
    # Example:
    # forget my bike
    # ---------------------------------------

    if command.startswith("forget "):

        key = command.replace("forget ", "", 1).strip()

        if memory_service.forget(key):
            return f"I forgot your {key}."

        return f"I don't know your {key}."

    # ---------------------------------------
    # Show Memory
    # ---------------------------------------

    if command in (
        "show memory",
        "show memories",
        "what do you remember",
    ):

        data = memory_service.all()

        if not data:
            return "I don't remember anything yet."

        result = []

        for key, value in data.items():
            result.append(f"{key} : {value}")

        return "\n".join(result)

    return None