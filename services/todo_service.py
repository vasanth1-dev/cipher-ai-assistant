import json
import os
from datetime import datetime
from threading import Lock


class TodoService:

    def __init__(
       self,
    ) -> None:

        self.file = "data/todo.json"
        self.lock = Lock()

        os.makedirs("data", exist_ok=True)

        if not os.path.exists(self.file):
            self._write([])

    # --------------------------------------------------
    # Internal Helpers
    # --------------------------------------------------

    def _read(self):

        try:

            with open(
                self.file,
                "r",
                encoding="utf-8",
            ) as f:

                data = json.load(f)

                if isinstance(data, list):
                    return data

        except (json.JSONDecodeError, FileNotFoundError) as e:
            from core.logger import logger

            logger.exception(
                f"[TODO] Failed to load todo list: {e}"
            )

        self._write([])

        return []

    def _write(self, tasks):

        try:

            with open(
                self.file,
                "w",
                encoding="utf-8",
            ) as f:

                json.dump(
                    tasks,
                    f,
                    indent=4,
                    ensure_ascii=False,
                )

        except Exception as e:

            from core.logger import logger

            logger.exception(
                f"[TODO] Failed to save todo list: {e}"
            )

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def load(self):

        with self.lock:
            return self._read()

    def save(self, tasks):

        with self.lock:
            self._write(tasks)

    def add(self, task):

        task = str(task).strip()

        if not task:
            return "Task cannot be empty."

        with self.lock:

            tasks = self._read()

            tasks.append(
                {
                    "task": task,
                    "created_at": datetime.now().isoformat(
                        timespec="seconds"
                    ),
                    "completed": False,
                }
            )

            self._write(tasks)

        return "Task added."

    def list(self):

        tasks = self.load()

        if not tasks:
            return "Your to-do list is empty."

        lines = []

        for index, task in enumerate(tasks, start=1):

            status = (
                "✅"
                if task.get("completed")
                else "⏳"
            )

            lines.append(
                f"{index}. {status} {task['task']}"
            )

        return "\n".join(lines)

    def complete(self, index):

        with self.lock:

            tasks = self._read()

            if index < 1 or index > len(tasks):
                return "Invalid task number."

            task = tasks[index - 1]

            if task.get("completed"):
                return "Task is already completed."

            task["completed"] = True
            task["completed_at"] = datetime.now().isoformat(
                timespec="seconds"
            )

            self._write(tasks)

        return "Task completed."

    def delete(self, index):

        with self.lock:

            tasks = self._read()

            if index < 1 or index > len(tasks):
                return "Invalid task number."

            removed = tasks.pop(index - 1)

            self._write(tasks)

        return f"Deleted task: {removed['task']}"

    def clear_completed(self):

        with self.lock:

            tasks = self._read()

            remaining = [
                task
                for task in tasks
                if not task.get("completed")
            ]

            removed = len(tasks) - len(remaining)

            self._write(remaining)

        return f"Removed {removed} completed task(s)."
    
    def count(self):

        return len(self.load())
    
    def is_empty(self):

        return len(self.load()) == 0


todo_service = TodoService()