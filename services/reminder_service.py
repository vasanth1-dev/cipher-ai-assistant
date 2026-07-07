import json
import os
from datetime import datetime
from threading import Lock


class ReminderService:

    def __init__(self):

        self.file = "data/reminders.json"
        self.lock = Lock()

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.file):
            self._write([])

    # --------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------

    def _read(self):

        try:
            with open(self.file, "r", encoding="utf-8") as f:
                data = json.load(f)

                if isinstance(data, list):
                    return data

        except (json.JSONDecodeError, FileNotFoundError):
            pass

        self._write([])
        return []

    def _write(self, reminders):

        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(
                reminders,
                f,
                indent=4,
                ensure_ascii=False,
            )

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def load(self):

        with self.lock:
            return self._read()

    def save(self, reminders):

        with self.lock:
            self._write(reminders)

    def add(self, reminder, remind_at):

        with self.lock:

            reminders = self._read()

            reminders.append(
                {
                    "message": reminder.strip(),
                    "time": remind_at,
                    "created_at": datetime.now().isoformat(timespec="seconds"),
                    "completed": False,
                }
            )

            reminders.sort(key=lambda r: r["time"])

            self._write(reminders)

        return f"Reminder saved for {remind_at}."

    def list(self):

        reminders = self.load()

        if not reminders:
            return "No reminders found."

        lines = []

        for i, reminder in enumerate(reminders, start=1):

            status = "✅" if reminder.get("completed") else "⏰"

            lines.append(
                f"{i}. {status} {reminder['message']} ({reminder['time']})"
            )

        return "\n".join(lines)

    def complete(self, index):

        with self.lock:

            reminders = self._read()

            if index < 1 or index > len(reminders):
                return "Invalid reminder number."

            reminder = reminders[index - 1]

            if reminder.get("completed"):
                return "Reminder is already completed."

            reminder["completed"] = True
            reminder["completed_at"] = datetime.now().isoformat(timespec="seconds")

            self._write(reminders)

        return "Reminder marked as completed."

    def delete(self, index):

        with self.lock:

            reminders = self._read()

            if index < 1 or index > len(reminders):
                return "Invalid reminder number."

            removed = reminders.pop(index - 1)

            self._write(reminders)

        return f"Deleted reminder: {removed['message']}"

    def clear_completed(self):

        with self.lock:

            reminders = self._read()

            remaining = [
                reminder
                for reminder in reminders
                if not reminder.get("completed")
            ]

            removed = len(reminders) - len(remaining)

            self._write(remaining)

        return f"Removed {removed} completed reminder(s)."

    def due(self):

        now = datetime.now()

        due_list = []

        with self.lock:

            reminders = self._read()

            updated = False

            for reminder in reminders:

                if reminder.get("completed"):
                    continue

                try:
                    remind_time = datetime.fromisoformat(reminder["time"])
                except ValueError:
                    continue

                if remind_time <= now:

                    reminder["completed"] = True
                    reminder["completed_at"] = now.isoformat(timespec="seconds")

                    due_list.append(reminder["message"])
                    updated = True

            if updated:
                self._write(reminders)

        return due_list


reminder_service = ReminderService()