from __future__ import annotations

import platform
import subprocess


class SystemService:
    """
    Basic System Service.
    """

    def system_info(self) -> dict:
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        }

    def execute(self, command: str) -> str:
        command = command.strip()

        if not command:
            return "Please provide a system command."

        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
            )

            if result.stdout.strip():
                return result.stdout.strip()

            if result.stderr.strip():
                return result.stderr.strip()

            return "Command executed successfully."

        except Exception as e:
            return f"System error: {e}"


system_service = SystemService()