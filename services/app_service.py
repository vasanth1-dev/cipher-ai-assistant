import shutil
import subprocess

from config import APPLICATIONS


class AppService:

    def __init__(self):
        self.apps = APPLICATIONS

    def open(self, app_name: str):

        if not app_name:
            return None

        app_name = app_name.lower().strip()

        if app_name not in self.apps:
            return None

        program = self.apps[app_name]

        executable = shutil.which(program)

        if executable is None:
            return f"{app_name} is not installed."

        try:

            subprocess.Popen(
                [executable],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True,
            )

            return f"Opening {app_name}."

        except Exception as e:
            return f"Failed to open {app_name}: {e}"

    def close(self, app_name: str):

        if not app_name:
            return None

        app_name = app_name.lower().strip()

        if app_name not in self.apps:
            return None

        program = self.apps[app_name]

        try:

            subprocess.run(
                ["pkill", "-f", program],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )

            return f"Closing {app_name}."

        except Exception as e:
            return f"Failed to close {app_name}: {e}"


app_service = AppService()