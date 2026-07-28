from __future__ import annotations

import subprocess


class BluetoothService:
    """
    Basic Bluetooth Service.
    """

    def enable(self) -> str:
        try:
            subprocess.run(
                ["bluetoothctl", "power", "on"],
                check=True,
                capture_output=True,
                text=True,
            )
            return "Bluetooth enabled."
        except Exception as e:
            return f"Failed to enable Bluetooth: {e}"

    def disable(self) -> str:
        try:
            subprocess.run(
                ["bluetoothctl", "power", "off"],
                check=True,
                capture_output=True,
                text=True,
            )
            return "Bluetooth disabled."
        except Exception as e:
            return f"Failed to disable Bluetooth: {e}"

    def execute(self, command: str) -> str:
        command = command.lower().strip()

        if command in ("on", "enable"):
            return self.enable()

        if command in ("off", "disable"):
            return self.disable()

        return f"Bluetooth command not supported: {command}"


bluetooth_service = BluetoothService()