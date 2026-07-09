from __future__ import annotations

import json
from collections import Counter
from datetime import datetime
from pathlib import Path


class ChatStatisticsService:
    """
    Maintains lifetime chat statistics.

    These statistics are independent from individual
    conversations and can be displayed on the dashboard.
    """

    DEFAULTS = {
        "total_sessions": 0,
        "total_messages": 0,
        "user_messages": 0,
        "assistant_messages": 0,
        "system_messages": 0,
        "total_words": 0,
        "last_updated": None,
    }

    def __init__(self):

        self._file = Path("data/chat_statistics.json")
        self._file.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._stats = self._load()

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

        stats = dict(self.DEFAULTS)
        stats.update(data)

        return stats

    # --------------------------------------------------

    def _save(self):

        self._stats["last_updated"] = (
            datetime.now().isoformat()
        )

        with open(
            self._file,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                self._stats,
                file,
                indent=4,
                ensure_ascii=False,
                sort_keys=True,
            )

    # --------------------------------------------------

    def record_session(self):

        self._stats["total_sessions"] += 1
        self._save()

    # --------------------------------------------------

    def record_messages(
        self,
        messages: list[dict],
    ):

        counter = Counter()
        words = 0

        for message in messages:

            role = message.get(
                "role",
                "assistant",
            )

            counter[role] += 1

            words += len(
                str(
                    message.get(
                        "content",
                        "",
                    )
                ).split()
            )

        self._stats["total_messages"] += len(messages)
        self._stats["user_messages"] += counter["user"]
        self._stats["assistant_messages"] += counter["assistant"]
        self._stats["system_messages"] += counter["system"]
        self._stats["total_words"] += words

        self._save()

    # --------------------------------------------------

    def get(self):

        return dict(self._stats)

    # --------------------------------------------------

    def reset(self):

        self._stats = dict(self.DEFAULTS)
        self._save()


chat_statistics_service = ChatStatisticsService()