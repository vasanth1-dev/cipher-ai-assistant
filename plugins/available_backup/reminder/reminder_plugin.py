from __future__ import annotations

from datetime import datetime
from typing import List

from plugins.base_plugin import Plugin
from plugins.plugin_manifest import PluginManifest
from services.reminder_service import reminder_service
from services.time_parser import time_parser


class ReminderPlugin(BasePlugin):
    """
    Built-in Reminder plugin.

    This plugin delegates reminder management to the
    existing ReminderService so that all reminders are
    stored in one place.
    """

    def __init__(
       self,
    ) -> None:

        super().__init__()

        self.manifest = PluginManifest(
            name="reminder",
            version="1.0.0",
            author="Cipher",
            description="Create, list and complete reminders.",
        )

    # --------------------------------------------------
    # Lifecycle
    # --------------------------------------------------

    def on_load(self) -> None:
        pass

    def on_unload(self) -> None:
        pass

    # --------------------------------------------------
    # Command Detection
    # --------------------------------------------------

    def can_handle(
        self,
        command: str,
    ) -> bool:

        command = command.lower().strip()

        prefixes = (
            "remind me",
            "set reminder",
            "add reminder",
            "show reminders",
            "list reminders",
            "my reminders",
            "complete reminder",
            "delete reminder",
        )

        return command.startswith(prefixes)

    # --------------------------------------------------
    # Command Handler
    # --------------------------------------------------

    def handle(
        self,
        command: str,
    ) -> str:

        command = command.strip()

        lower = command.lower()

        if lower in (
            "show reminders",
            "list reminders",
            "my reminders",
        ):
            return reminder_service.list()

        if lower.startswith("complete reminder"):
            return reminder_service.complete(
                self._extract_suffix(
                    command,
                    "complete reminder",
                )
            )

        if lower.startswith("delete reminder"):
            return reminder_service.delete(
                self._extract_suffix(
                    command,
                    "delete reminder",
                )
            )

        return self._create_reminder(command)

    # --------------------------------------------------
    # Create Reminder
    # --------------------------------------------------

    def _create_reminder(
        self,
        command: str,
    ) -> str:

        reminder_time = time_parser.parse(command)

        if reminder_time is None:

            return (
                "I couldn't determine the reminder time."
            )

        text = self._extract_message(command)

        if not text:

            return (
                "Please tell me what you want "
                "to be reminded about."
            )

        reminder_service.add(
            text=text,
            reminder_time=reminder_time,
        )

        formatted = reminder_time.strftime(
            "%d %b %Y %I:%M %p"
        )

        return (
            f"Reminder created for {formatted}.\n"
            f"Task: {text}"
        )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _extract_suffix(
        command: str,
        prefix: str,
    ) -> str:

        return command[len(prefix):].strip()

    @staticmethod
    def _extract_message(
        command: str,
    ) -> str:

        lower = command.lower()

        prefixes: List[str] = [
            "remind me to",
            "remind me",
            "set reminder to",
            "set reminder",
            "add reminder to",
            "add reminder",
        ]

        for prefix in prefixes:

            if lower.startswith(prefix):

                return command[len(prefix):].strip()

        return command.strip()