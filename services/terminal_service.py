from __future__ import annotations

import subprocess


class TerminalService:

    def execute(self, command: str) -> str:
        command = command.strip()

        if not command:
            return "No command provided."

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
            return f"Terminal error: {e}"


terminal_service = TerminalService()