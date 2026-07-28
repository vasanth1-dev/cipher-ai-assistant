import subprocess

from core.logger import logger


INTENT = "system"


def _run(
    command: list[str],
    wait: bool = False,
) -> bool:

    try:

        if wait:

            subprocess.run(
                command,
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

        else:

            subprocess.Popen(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )

        logger.info(
            f"[SYSTEM] {' '.join(command)}"
        )

        return True

    except Exception as e:

        logger.exception(e)

        return False

def _launch(command: list[str]) -> bool:

    try:

        subprocess.Popen(
            command,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )

        logger.info(
            f"[APP] {' '.join(command)}"
        )

        return True

    except Exception as e:

        logger.exception(e)

        return False


def handle(command: str):

    from datetime import datetime

    #TIME

    if not command:
        return None
    
    command = " ".join(
        command.lower().strip().split()
    )

    if (
        "what time" in command
        or command == "time"
        or "current time" in command
    ):
        
        return (
            "The current time is "
            + datetime.now().strftime("%I:%M %p")
        )
    
    if (
        command == "date"
        or command == "today"
        or "what date" in command
        or "today's date" in command
    ):

        return (
            "Today's date is "
            + datetime.now().strftime("%d %B %Y")
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

        return "Shutdown is currently disabled."

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
    
    if command == "battery":

        try:

            import psutil

            battery = psutil.sensors_battery()

            if battery is None:
                return "Battery information is not available."

            status = (
                "charging"
                if battery.power_plugged
                else "discharging"
            )

            return (
                f"Battery is {battery.percent:.0f}% "
                f"and currently {status}."
            )

        except Exception as e:

            logger.exception(e)

            return "Unable to read battery status."

    if command == "cpu":

        try:

            import psutil

            usage = psutil.cpu_percent(interval=1)

            return f"Current CPU usage is {usage:.0f}%."

        except Exception as e:

            logger.exception(e)

            return "Unable to read CPU usage."

    if command == "ram":

        try:

            import psutil

            memory = psutil.virtual_memory()

            used = memory.used / (1024 ** 3)
            total = memory.total / (1024 ** 3)

            return (
                f"RAM usage is "
                f"{used:.1f} GB of {total:.1f} GB "
                f"({memory.percent:.0f}%)."
            )

        except Exception as e:

            logger.exception(e)

            return "Unable to read RAM usage."

    # -------------------------------------------------
    # Volume
    # -------------------------------------------------

    if command in (
        "volume up",
        "increase volume",
    ):

        if _run(
            [
                "pactl",
                "set-sink-volume",
                "@DEFAULT_SINK@",
                "+10%",
            ],
            wait=True,
        ):
            return "Volume increased."

        return "Unable to increase the volume."


    if command in (
        "volume down",
        "decrease volume",
    ):

        if _run(
            [
                "pactl",
                "set-sink-volume",
                "@DEFAULT_SINK@",
                "-10%",
            ],
            wait=True,
        ):
            return "Volume decreased."

        return "Unable to decrease the volume."


    if command == "mute":

        if _run(
            [
                "pactl",
                "set-sink-mute",
                "@DEFAULT_SINK@",
                "1",
            ],
            wait=True,
        ):
            return "Volume muted."

        return "Unable to mute the volume."


    if command == "unmute":

        if _run(
            [
                "pactl",
                "set-sink-mute",
                "@DEFAULT_SINK@",
                "0",
            ],
            wait=True,
        ):
            return "Volume unmuted."

        return "Unable to unmute the volume."

    # -------------------------------------------------
    # Brightness
    # -------------------------------------------------

    if command in (
        "brightness up",
        "increase brightness",
    ):

        if _run(
            [
                "brightnessctl",
                "set",
                "+10%",
            ],
            wait=True,
        ):
            return "Brightness increased."

        return "Unable to increase brightness."


    if command in (
        "brightness down",
        "decrease brightness",
    ):

        if _run(
            [
                "brightnessctl",
                "set",
                "10%-",
            ],
            wait=True,
        ):
            return "Brightness decreased."

        return "Unable to decrease brightness."


    if command == "maximum brightness":

        if _run(
            [
                "brightnessctl",
                "set",
                "100%",
            ],
            wait=True,
        ):
            return "Brightness set to maximum."

        return "Unable to change brightness."


    if command == "minimum brightness":

        if _run(
            [
                "brightnessctl",
                "set",
                "10%",
            ],
            wait=True,
        ):
            return "Brightness set to minimum."

        return "Unable to change brightness."

    # -------------------------------------------------
    # Screenshot
    # -------------------------------------------------

    if command in (
        "screenshot",
        "take screenshot",
        "capture screen",
        "capture screenshot",
        "screen capture",
    ):

        try:

            from pathlib import Path
            from datetime import datetime

            screenshot_dir = (
                Path.home()
                / "Pictures"
                / "Screenshots"
            )

            screenshot_dir.mkdir(
                parents=True,
                exist_ok=True,
            )

            filename = (
                datetime.now().strftime(
                    "Screenshot_%Y%m%d_%H%M%S.png"
                )
            )

            filepath = screenshot_dir / filename

            result = subprocess.run(
                [
                    "gnome-screenshot",
                    "-f",
                    str(filepath),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            if result.returncode == 0:

                logger.info(
                    f"[SYSTEM] Screenshot saved: {filepath}"
                )

                return (
                    f"Screenshot saved to "
                    f"{filepath}"
                )

            return "Unable to capture the screenshot."

        except Exception as e:

            logger.exception(e)

            return "Unable to capture the screenshot."


    # -------------------------------------------------
    # Lock Screen
    # -------------------------------------------------

    if command in (
        "lock",
        "lock screen",
        "lock computer",
        "lock my computer",
    ):

        if _run(
            [
                "loginctl",
                "lock-session",
            ],
            wait=True,
        ):
            return "Computer locked."

        return "Unable to lock the computer."

    # -------------------------------------------------
    # Wi-Fi
    # -------------------------------------------------

    if command in (
        "wifi",
        "wi-fi",
    ):

        try:

            result = subprocess.run(
                [
                    "nmcli",
                    "radio",
                    "wifi",
                ],
                capture_output=True,
                text=True,
            )

            status = result.stdout.strip()

            if status == "enabled":
                return "Wi-Fi is currently enabled."

            if status == "disabled":
                return "Wi-Fi is currently disabled."

            return "Unable to determine Wi-Fi status."

        except Exception as e:

            logger.exception(e)

            return "Unable to determine Wi-Fi status."


    if command in (
        "wifi on",
        "turn on wifi",
        "enable wifi",
    ):

        if _run(
            [
                "nmcli",
                "radio",
                "wifi",
                "on",
            ],
            wait=True,
        ):
            return "Wi-Fi enabled."

        return "Unable to enable Wi-Fi."


    if command in (
        "wifi off",
        "turn off wifi",
        "disable wifi",
    ):

        if _run(
            [
                "nmcli",
                "radio",
                "wifi",
                "off",
            ],
            wait=True,
        ):
            return "Wi-Fi disabled."

        return "Unable to disable Wi-Fi."

    # -------------------------------------------------
    # Bluetooth
    # -------------------------------------------------

    if command == "bluetooth":

        try:

            result = subprocess.run(
                [
                    "bluetoothctl",
                    "show",
                ],
                capture_output=True,
                text=True,
            )

            output = result.stdout.lower()

            if "powered: yes" in output:
                return "Bluetooth is currently enabled."

            if "powered: no" in output:
                return "Bluetooth is currently disabled."

            return "Unable to determine Bluetooth status."

        except Exception as e:

            logger.exception(e)

            return "Unable to determine Bluetooth status."

    if command in (
        "bluetooth on",
        "turn on bluetooth",
        "enable bluetooth",
    ):

        if _run(
            [
                "bluetoothctl",
                "power",
                "on",
            ],
            wait=True,
        ):
            return "Bluetooth enabled."

        return "Unable to enable Bluetooth."

    if command in (
        "bluetooth off",
        "turn off bluetooth",
        "disable bluetooth",
    ):

        if _run(
            [
                "bluetoothctl",
                "power",
                "off",
            ],
            wait=True,
        ):
            return "Bluetooth disabled."

        return "Unable to disable Bluetooth."

    # -------------------------------------------------
    # Suspend
    # -------------------------------------------------

    if command in (
        "sleep",
        "suspend",
        "put computer to sleep",
        "sleep computer",
    ):

        if _run(
            [
                "systemctl",
                "suspend",
            ],
            wait=True,
        ):
            return "Computer is going to sleep."

        return "Unable to suspend the computer."

    # -------------------------------------------------
    # Hibernate
    # -------------------------------------------------

    if command in (
        "hibernate",
        "hibernate computer",
    ):

        return (
            "Hibernate is not supported on this system."
        )

    # -------------------------------------------------
    # Desktop Notification
    # -------------------------------------------------

    if command in (
        "notification",
        "notify",
        "show notification",
        "send notification",
    ):

        if _run(
            [
                "notify-send",
                "Cipher",
                "This is a test notification.",
            ],
            wait=True,
        ):
            return "Notification sent."

        return "Unable to send the notification."

    if command == "disk":

        try:

            import psutil

            disk = psutil.disk_usage("/")

            used = disk.used / (1024 ** 3)
            total = disk.total / (1024 ** 3)

            return (
                f"Disk usage is "
                f"{used:.1f} GB of {total:.1f} GB "
                f"({disk.percent:.0f}%)."
            )

        except Exception as e:

            logger.exception(e)

            return "Unable to read disk usage."

    # -------------------------------------------------
    # Application Launcher
    # -------------------------------------------------

    APPS = {
        "chrome": ["google-chrome"],
        "firefox": ["firefox"],
        "edge": ["microsoft-edge"],
        "terminal": ["gnome-terminal"],
        "files": ["nautilus"],
        "calculator": ["gnome-calculator"],
        "settings": ["gnome-control-center"],
        "vs code": ["code"],
        "libreoffice": ["libreoffice"],
        "spotify": ["spotify"],
        "telegram": ["telegram-desktop"],
    }

    for app, executable in APPS.items():

        if command in (
            f"open {app}",
            f"launch {app}",
            f"start {app}",
            f"run {app}",
        ):

            if _launch(executable):
                return f"Opening {app.title()}."

            return f"Unable to open {app.title()}."

    return None

    