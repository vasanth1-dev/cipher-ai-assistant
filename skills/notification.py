import shutil
import subprocess


def notify(title: str, message: str):

    if shutil.which("notify-send") is None:
        return False

    try:

        subprocess.Popen(
            [
                "notify-send",
                title,
                message,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        return True

    except Exception:
        return False


def handle(command: str):

    if not command:
        return None

    command = command.lower().strip()

    # ------------------------------------
    # Notify
    # ------------------------------------

    if command.startswith("notify "):

        message = command.replace("notify ", "", 1).strip()

        if not message:
            return "What should I notify?"

        notify("Cipher", message)

        return "Notification sent."

    return None