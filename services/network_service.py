from __future__ import annotations

import subprocess


class NetworkService:
    """
    Basic Network Service.
    """

    def status(self) -> str:
        try:
            result = subprocess.run(
                ["nmcli", "networking", "connectivity"],
                capture_output=True,
                text=True,
                check=True,
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Unable to determine network status: {e}"

    def enable(self) -> str:
        try:
            subprocess.run(
                ["nmcli", "networking", "on"],
                check=True,
            )
            return "Network enabled."
        except Exception as e:
            return f"Failed to enable network: {e}"

    def disable(self) -> str:
        try:
            subprocess.run(
                ["nmcli", "networking", "off"],
                check=True,
            )
            return "Network disabled."
        except Exception as e:
            return f"Failed to disable network: {e}"

    def execute(self, command: str) -> str:
        command = command.lower().strip()

        if command in ("status", "state"):
            return self.status()

        if command in ("on", "enable"):
            return self.enable()

        if command in ("off", "disable"):
            return self.disable()

        return f"Unsupported network command: {command}"


network_service = NetworkService()