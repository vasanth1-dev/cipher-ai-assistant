from services.app_service import app_service


OPEN_WORDS = (
    "open ",
    "launch ",
    "start ",
)

CLOSE_WORDS = (
    "close ",
    "exit ",
    "quit ",
)


def handle(command: str):

    if not command:
        return None

    command = command.lower().strip()

    # ---------------- OPEN ----------------

    for word in OPEN_WORDS:

        if command.startswith(word):

            app = command.replace(word, "", 1).strip()

            if not app:
                return "Which application should I open?"

            response = app_service.open(app)

            if response:
                return response

    # ---------------- CLOSE ----------------

    for word in CLOSE_WORDS:

        if command.startswith(word):

            app = command.replace(word, "", 1).strip()

            if not app:
                return "Which application should I close?"

            response = app_service.close(app)

            if response:
                return response

    return None