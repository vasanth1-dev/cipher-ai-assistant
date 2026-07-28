from __future__ import annotations

import json
from pathlib import Path


class ChatTemplateService:
    """
    Manages reusable prompt templates.

    Templates can later be used for:
    - Coding
    - Email writing
    - Summarization
    - Translation
    - SQL generation
    """

    DEFAULT_TEMPLATES = {
        "Explain": "Explain the following in simple terms:\n\n{input}",
        "Summarize": "Summarize the following text:\n\n{input}",
        "Translate": "Translate the following text to English:\n\n{input}",
        "Python": "Write Python code for the following:\n\n{input}",
        "SQL": "Write an SQL query for the following requirement:\n\n{input}",
    }

    def __init__(
       self,
    ) -> None:

        self._file = Path("data/chat_templates.json")
        self._file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._templates = self._load()

    # --------------------------------------------------

    def _load(self):

        if not self._file.exists():

            self._save_defaults()

            return dict(self.DEFAULT_TEMPLATES)

        try:

            with open(
                self._file,
                "r",
                encoding="utf-8",
            ) as file:

                return json.load(file)

        except Exception:

            return dict(self.DEFAULT_TEMPLATES)

    # --------------------------------------------------

    def _save(self):

        with open(
            self._file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self._templates,
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
                self.DEFAULT_TEMPLATES,
                file,
                indent=4,
                ensure_ascii=False,
                sort_keys=True,
            )

    # --------------------------------------------------

    def list(self):

        return dict(self._templates)

    # --------------------------------------------------

    def get(
        self,
        name: str,
    ):

        return self._templates.get(name)

    # --------------------------------------------------

    def add(
        self,
        name: str,
        template: str,
    ):

        self._templates[name] = template
        self._save()

    # --------------------------------------------------

    def remove(
        self,
        name: str,
    ):

        if name in self._templates:

            del self._templates[name]
            self._save()

    # --------------------------------------------------

    def render(
        self,
        name: str,
        text: str,
    ) -> str:

        template = self.get(name)

        if template is None:
            return text

        return template.replace(
            "{input}",
            text,
        )


chat_template_service = ChatTemplateService()