from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


class ChatSnippetService:
    """
    Stores reusable text/code snippets.

    Snippets are intended for frequently used prompts,
    code fragments, shell commands, SQL queries, etc.
    """

    def __init__(
       self,
    ) -> None:

        self._file = Path("data/chat_snippets.json")
        self._file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._snippets = self._load()

    # --------------------------------------------------

    def _load(self):

        if not self._file.exists():
            return {}

        try:

            with open(
                self._file,
                "r",
                encoding="utf-8",
            ) as file:

                return json.load(file)

        except Exception:
            return {}

    # --------------------------------------------------

    def _save(self):

        with open(
            self._file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self._snippets,
                file,
                indent=4,
                ensure_ascii=False,
                sort_keys=True,
            )

    # --------------------------------------------------

    def add(
        self,
        name: str,
        content: str,
        category: str = "General",
    ):

        self._snippets[name] = {
            "category": category,
            "content": content,
            "updated_at": datetime.now().isoformat(),
        }

        self._save()

    # --------------------------------------------------

    def remove(
        self,
        name: str,
    ):

        if name in self._snippets:
            del self._snippets[name]
            self._save()

    # --------------------------------------------------

    def get(
        self,
        name: str,
    ):

        item = self._snippets.get(name)

        if item is None:
            return None

        return dict(item)

    # --------------------------------------------------

    def names(self):

        return sorted(self._snippets.keys())

    # --------------------------------------------------

    def categories(self):

        return sorted(
            {
                item["category"]
                for item in self._snippets.values()
            }
        )

    # --------------------------------------------------

    def by_category(
        self,
        category: str,
    ):

        return {
            name: value
            for name, value in self._snippets.items()
            if value["category"] == category
        }

    # --------------------------------------------------

    def clear(self):

        self._snippets.clear()
        self._save()


chat_snippet_service = ChatSnippetService()