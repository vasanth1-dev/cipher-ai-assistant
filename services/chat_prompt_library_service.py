from __future__ import annotations

import json
from pathlib import Path


class ChatPromptLibraryService:
    """
    Stores reusable prompts organized by category.

    Unlike chat_template_service, this service stores
    complete prompts instead of parameterized templates.
    """

    DEFAULT_LIBRARY = {
        "Programming": [
            "Explain this code step by step.",
            "Find bugs in the following code.",
            "Optimize this algorithm.",
        ],
        "Writing": [
            "Improve the grammar of this text.",
            "Rewrite this professionally.",
            "Summarize the following content.",
        ],
        "Linux": [
            "Explain this Linux command.",
            "Write a bash script for this task.",
            "Help me troubleshoot this error.",
        ],
    }

    def __init__(
       self,
    ) -> None:

        self._file = Path("data/chat_prompt_library.json")
        self._file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._library = self._load()

    # --------------------------------------------------

    def _load(self):

        if not self._file.exists():

            self._save_defaults()

            return dict(self.DEFAULT_LIBRARY)

        try:

            with open(
                self._file,
                "r",
                encoding="utf-8",
            ) as file:

                return json.load(file)

        except Exception:

            return dict(self.DEFAULT_LIBRARY)

    # --------------------------------------------------

    def _save(self):

        with open(
            self._file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self._library,
                file,
                indent=4,
                ensure_ascii=False,
                sort_keys=True,
            )

    # --------------------------------------------------

    def _save_defaults(self):

        with open(
            self._file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self.DEFAULT_LIBRARY,
                file,
                indent=4,
                ensure_ascii=False,
                sort_keys=True,
            )

    # --------------------------------------------------

    def categories(self):

        return sorted(self._library.keys())

    # --------------------------------------------------

    def prompts(self, category: str):

        return list(
            self._library.get(category, [])
        )

    # --------------------------------------------------

    def add_prompt(
        self,
        category: str,
        prompt: str,
    ):

        category = category.strip()

        if not category or not prompt.strip():
            return

        self._library.setdefault(category, [])

        if prompt not in self._library[category]:

            self._library[category].append(prompt)
            self._save()

    # --------------------------------------------------

    def remove_prompt(
        self,
        category: str,
        prompt: str,
    ):

        if category not in self._library:
            return

        if prompt in self._library[category]:

            self._library[category].remove(prompt)

            if not self._library[category]:
                del self._library[category]

            self._save()


chat_prompt_library_service = ChatPromptLibraryService()