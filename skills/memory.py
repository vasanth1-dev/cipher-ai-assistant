from pathlib import Path

MEMORY_FILE = Path("data/memory.txt")


def save_memory(text: str):

    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(MEMORY_FILE, "a", encoding="utf-8") as file:
        file.write(text.strip() + "\n")


def read_memory():

    if not MEMORY_FILE.exists():
        return "I don't have any saved memories."

    with open(MEMORY_FILE, "r", encoding="utf-8") as file:

        lines = [
            line.strip()
            for line in file.readlines()
            if line.strip()
        ]

    if not lines:
        return "I don't have any saved memories."

    return "\n".join(lines)


def handle(command: str):

    if not command:
        return None

    command = command.lower().strip()

    # -------------------------
    # Remember
    # -------------------------

    if command.startswith("remember "):

        text = command.replace("remember ", "", 1).strip()

        if not text:
            return "What should I remember?"

        save_memory(text)

        return "I'll remember that."

    # -------------------------
    # Recall
    # -------------------------

    if command in (
        "what do you remember",
        "show memory",
        "show memories",
        "my memories",
        "remembered things",
    ):

        return read_memory()

    return None