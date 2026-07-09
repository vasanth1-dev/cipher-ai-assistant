from __future__ import annotations

import json
from pathlib import Path


class ChatPreferencesService:
    """
    Stores chat-specific user preferences.

    These settings are independent from the main
    application settings and can evolve separately.
    """

    DEFAULTS = {
        "auto_scroll": True,
        "show_timestamps": True,
        "render_markdown": True,
        "render_code_blocks": True,
        "show_typing_indicator": True,
        "compact_mode": False,
        "enter_to_send": True,
        "font_size": 14,
    }

    def __init__(self):

        self._file = Path("data/chat_preferences.json")
        self._file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._preferences = self._load()

    # --------------------------------------------------

    def _load(self):

        if not self._file.exists():
            return dict(self.DEFAULTS)

        try:

            with open(
                self._file,
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(file)

        except Exception:
            return dict(self.DEFAULTS)

        preferences = dict(self.DEFAULTS)
        preferences.update(data)

        return preferences

    # --------------------------------------------------

    def _save(self):

        with open(
            self._file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self._preferences,
                file,
                indent=4,
                ensure_ascii=False,
                sort_keys=True,
            )

    # --------------------------------------------------

    def get(
        self,
        key: str,
        default=None,
    ):

        return self._preferences.get(
            key,
            default,
        )

    # --------------------------------------------------

    def set(
        self,
        key: str,
        value,
    ):

        self._preferences[key] = value
        self._save()

    # --------------------------------------------------

    def all(self):

        return dict(self._preferences)

    # --------------------------------------------------

    def reset(self):

        self._preferences = dict(self.DEFAULTS)
        self._save()


chat_preferences_service = ChatPreferencesService()