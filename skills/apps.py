from services.app_service import app_service


OPEN_WORDS = (
    "open ",
    "launch ",
    "start ",
    "run ",
)

CLOSE_WORDS = (
    "close ",
    "quit ",
    "exit ",
    "stop ",
    "kill ",
)

INTENT = "open_app"


def _extract_app(command, keywords):

    for keyword in keywords:

        if command.startswith(keyword):

            app = command[len(keyword):].strip()

            if app.startswith("the "):
                app = app[4:]

            if app.startswith("application "):
                app = app[12:]

            if app.startswith("app "):
                app = app[4:]

            return app

    return None


def handle(command: str):

    if not command:
        return None

    command = " ".join(
        command.lower().strip().split()
    )

    # ---------------- OPEN ----------------

    app = _extract_app(
        command,
        OPEN_WORDS,
    )

    if app is not None:

        if not app:
            return "Which application should I open?"

        response = app_service.open(app)

        if response:
            return response
        
        app = app.title()

        return f"I couldn't open {app}."

    # ---------------- CLOSE ----------------

    app = _extract_app(
        command,
        CLOSE_WORDS,
    )

    if app is not None:

        if not app:
            return "Which application should I close?"

        response = app_service.close(app)

        if response:
            return response

        return f"I couldn't close {app}."

    return None