from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(slots=True)
class SearchResult:
    """
    Represents a search match inside a conversation.
    """

    index: int
    role: str
    content: str
    matches: int


class ChatSearchService:
    """
    Provides in-memory searching across chat messages.

    Expected message format:
    {
        "role": "user" | "assistant" | "system",
        "content": "..."
    }

    This service is UI-independent.
    """

    # --------------------------------------------------

    def search(
        self,
        messages: Iterable[dict],
        query: str,
        *,
        case_sensitive: bool = False,
    ) -> list[SearchResult]:

        query = query.strip()

        if not query:
            return []

        needle = query if case_sensitive else query.lower()

        results: list[SearchResult] = []

        for index, message in enumerate(messages):

            content = str(
                message.get("content", "")
            )

            haystack = (
                content
                if case_sensitive
                else content.lower()
            )

            count = haystack.count(needle)

            if count == 0:
                continue

            results.append(
                SearchResult(
                    index=index,
                    role=message.get(
                        "role",
                        "assistant",
                    ),
                    content=content,
                    matches=count,
                )
            )

        return results

    # --------------------------------------------------

    def first(
        self,
        messages: Iterable[dict],
        query: str,
    ) -> SearchResult | None:

        results = self.search(messages, query)

        if results:
            return results[0]

        return None

    # --------------------------------------------------

    def count(
        self,
        messages: Iterable[dict],
        query: str,
    ) -> int:

        return len(
            self.search(messages, query)
        )


chat_search_service = ChatSearchService()