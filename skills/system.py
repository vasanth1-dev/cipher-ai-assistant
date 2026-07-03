import subprocess


def handle(command: str):

    if not command:
        return None

    command = command.lower().strip()

    # ---------------- Shutdown ----------------

    if command in (
        "shutdown",
        "power off",
        "turn off computer",
    ):

        #subprocess.Popen(["shutdown", "-h", "now"])
        return "Shutting down the computer."

    # ---------------- Restart ----------------

    if command in (
        "restart",
        "reboot",
    ):

        subprocess.Popen(["shutdown", "-r", "now"])
        return "Restarting the computer."

    # ---------------- Logout ----------------

    if command in (
        "logout",
        "log out",
        "sign out",
    ):

        subprocess.Popen(
            [
                "gnome-session-quit",
                "--logout",
                "--no-prompt",
            ]
        )

        return "Logging out."

    return None