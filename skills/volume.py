import subprocess


def set_volume(percent: int):

    percent = max(0, min(100, percent))

    subprocess.run(
        [
            "pactl",
            "set-sink-volume",
            "@DEFAULT_SINK@",
            f"{percent}%"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def change_volume(direction: str):

    if direction == "up":

        subprocess.run(
            [
                "pactl",
                "set-sink-volume",
                "@DEFAULT_SINK@",
                "+10%"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

    elif direction == "down":

        subprocess.run(
            [
                "pactl",
                "set-sink-volume",
                "@DEFAULT_SINK@",
                "-10%"
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )


def mute():

    subprocess.run(
        [
            "pactl",
            "set-sink-mute",
            "@DEFAULT_SINK@",
            "toggle"
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def handle(command: str):

    if not command:
        return None

    command = command.lower().strip()

    # -------------------------
    # Mute
    # -------------------------

    if command in (
        "mute",
        "mute volume",
        "mute sound",
    ):

        mute()
        return "Volume muted."

    # -------------------------
    # Volume Up
    # -------------------------

    if command in (
        "volume up",
        "increase volume",
        "increase sound",
    ):

        change_volume("up")
        return "Volume increased."

    # -------------------------
    # Volume Down
    # -------------------------

    if command in (
        "volume down",
        "decrease volume",
        "decrease sound",
    ):

        change_volume("down")
        return "Volume decreased."

    # -------------------------
    # Set Volume
    # -------------------------

    if command.startswith("set volume to "):

        try:

            value = int(
                command.replace(
                    "set volume to",
                    ""
                ).replace("%", "").strip()
            )

            set_volume(value)

            return f"Volume set to {value} percent."

        except:

            return "Invalid volume value."

    return None