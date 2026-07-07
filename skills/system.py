import subprocess

from core.logger import logger


INTENT = "system"


def _run(command):

    try:

        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )

        logger.info(f"[SYSTEM] {' '.join(command)}")

        return True

    except Exception as e:

        logger.exception(e)

        return False


def handle(command: str):

    if not command:
        return None

    command = " ".join(
        command.lower().strip().split()
    )

    # -------------------------------------------------
    # Shutdown
    # -------------------------------------------------

    if command in (
        "shutdown",
        "power off",
        "turn off computer",
    ):

        # Uncomment when you are ready to enable it.
        # _run(["shutdown", "-h", "now"])

        return "Shutting down the computer."

    # -------------------------------------------------
    # Restart
    # -------------------------------------------------

    if command in (
        "restart",
        "reboot",
    ):

        if _run(["shutdown", "-r", "now"]):
            return "Restarting the computer."

        return "Unable to restart the computer."

    # -------------------------------------------------
    # Logout
    # -------------------------------------------------

    if command in (
        "logout",
        "log out",
        "sign out",
    ):

        if _run([
            "gnome-session-quit",
            "--logout",
            "--no-prompt",
        ]):
            return "Logging out."

        return "Unable to log out."

    return None