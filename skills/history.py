from pathlib import Path

HISTORY_FILE = Path("logs/history.log")


def save_history(command: str):

    HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(HISTORY_FILE, "a", encoding="utf-8") as file:
        file.write(command.strip() + "\n")


def read_history(limit=10):

    if not HISTORY_FILE.exists():
        return "No command history found."

    with open(HISTORY_FILE, "r", encoding="utf-8") as file:

        lines = [
            line.strip()
            for line in file.readlines()
            if line.strip()
        ]

    if not lines:
        return "No command history found."

    lines = lines[-limit:]

    output = "Recent Commands:\n"

    for index, command in enumerate(lines, start=1):
        output += f"{index}. {command}\n"

    return output.strip()


def handle(command: str):

    if not command:
        return None

    command = command.lower().strip()

    # -------------------------
    # Show History
    # -------------------------

    if command in (
        "history",
        "show history",
        "command history",
        "recent commands",
    ):
        return read_history()

    return None