from __future__ import annotations

import json
from pathlib import Path


class ModelConfigurationService:
    """
    Stores per-model configuration.

    This service is backend-independent and only manages
    user preferences for each model.
    """

    DEFAULTS = {
        "temperature": 0.7,
        "top_p": 0.9,
        "top_k": 40,
        "repeat_penalty": 1.1,
        "max_tokens": 2048,
        "stream": True,
    }

    def __init__(
       self,
    ) -> None:

        self._file = Path("data/model_configurations.json")
        self._file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._configs = self._load()

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
                self._configs,
                file,
                indent=4,
                ensure_ascii=False,
                sort_keys=True,
            )

    # --------------------------------------------------

    def get(
        self,
        model_name: str,
    ) -> dict:

        config = dict(self.DEFAULTS)
        config.update(
            self._configs.get(model_name, {})
        )

        return config

    # --------------------------------------------------

    def set(
        self,
        model_name: str,
        **settings,
    ):

        config = self.get(model_name)
        config.update(settings)

        self._configs[model_name] = config

        self._save()

    # --------------------------------------------------

    def reset(
        self,
        model_name: str,
    ):

        self._configs.pop(model_name, None)
        self._save()

    # --------------------------------------------------

    def models(self):

        return sorted(self._configs.keys())

    # --------------------------------------------------

    def clear(self):

        self._configs.clear()
        self._save()


model_configuration_service = ModelConfigurationService()