from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


class ModelUsageService:
    """
    Tracks model usage statistics.

    This service records how each model is used without
    depending on any AI backend.
    """

    def __init__(
       self,
    ) -> None:

        self._file = Path("data/model_usage.json")
        self._file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._usage = self._load()

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
                self._usage,
                file,
                indent=4,
                ensure_ascii=False,
                sort_keys=True,
            )

    # --------------------------------------------------

    def record_request(
        self,
        model_name: str,
        prompt_tokens: int = 0,
        completion_tokens: int = 0,
    ):

        stats = self._usage.setdefault(
            model_name,
            {
                "requests": 0,
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "last_used": None,
            },
        )

        stats["requests"] += 1
        stats["prompt_tokens"] += prompt_tokens
        stats["completion_tokens"] += completion_tokens
        stats["last_used"] = datetime.now().isoformat()

        self._save()

    # --------------------------------------------------

    def get(
        self,
        model_name: str,
    ) -> dict:

        return dict(
            self._usage.get(model_name, {})
        )

    # --------------------------------------------------

    def all(self):

        return dict(self._usage)

    # --------------------------------------------------

    def reset(
        self,
        model_name: str,
    ):

        self._usage.pop(model_name, None)
        self._save()

    # --------------------------------------------------

    def clear(self):

        self._usage.clear()
        self._save()


model_usage_service = ModelUsageService()