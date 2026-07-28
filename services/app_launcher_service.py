from __future__ import annotations

import shutil
import subprocess


class AppLauncherService:
    """
    Application Launcher Service.

    Provides basic application launching support.
    """

    def launch(self, application: str) -> str:
        application = application.strip()

        if not application:
            return "Please specify an application."

        if not shutil.which(application):
            return f"Application '{application}' not found."

        try:
            subprocess.Popen([application])
            return f"Launching {application}."
        except Exception as e:
            return f"Failed to launch {application}: {e}"

    def execute(self, command: str) -> str:
        return self.launch(command)


app_launcher_service = AppLauncherService()