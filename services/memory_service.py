import json
from pathlib import Path


class MemoryService:

    def __init__(self):

        self.file = Path("data/memory.json")
        self.file.parent.mkdir(parents=True, exist_ok=True)

        if not self.file.exists():
            self._save({})

    def _load(self):

        try:
            with open(self.file, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}

    def _save(self, data):

        with open(self.file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    def remember(self, key, value):

        data = self._load()
        data[key.lower()] = value
        self._save(data)

    def recall(self, key):

        data = self._load()
        return data.get(key.lower())

    def forget(self, key):

        data = self._load()

        if key.lower() in data:
            del data[key.lower()]
            self._save(data)
            return True

        return False

    def all(self):

        return self._load()

    def memory_prompt(self):

        data = self._load()

        if not data:
            return ""

        text = "Known facts about the user:\n"

        for key, value in data.items():
            text += f"- {key}: {value}\n"

        return text


memory_service = MemoryService()