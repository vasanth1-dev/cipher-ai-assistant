from __future__ import annotations

from collections import defaultdict
from typing import Any, Callable


class ChatEventBus:
    """
    Lightweight publish/subscribe event bus.

    This service is intentionally independent from Qt so it can
    be used by services, plugins, and background workers.

    Example:
        event_bus.subscribe("message.sent", callback)
        event_bus.publish("message.sent", text="Hello")
    """

    def __init__(self):

        self._subscribers: dict[
            str,
            list[Callable[..., Any]]
        ] = defaultdict(list)

    # --------------------------------------------------

    def subscribe(
        self,
        event: str,
        callback: Callable[..., Any],
    ):

        if callback not in self._subscribers[event]:
            self._subscribers[event].append(callback)

    # --------------------------------------------------

    def unsubscribe(
        self,
        event: str,
        callback: Callable[..., Any],
    ):

        if event not in self._subscribers:
            return

        try:
            self._subscribers[event].remove(callback)
        except ValueError:
            pass

        if not self._subscribers[event]:
            del self._subscribers[event]

    # --------------------------------------------------

    def publish(
        self,
        event: str,
        *args,
        **kwargs,
    ):

        for callback in list(
            self._subscribers.get(event, [])
        ):

            callback(*args, **kwargs)

    # --------------------------------------------------

    def clear(self):

        self._subscribers.clear()

    # --------------------------------------------------

    def events(self) -> list[str]:

        return sorted(
            self._subscribers.keys()
        )

    # --------------------------------------------------

    def subscriber_count(
        self,
        event: str,
    ) -> int:

        return len(
            self._subscribers.get(event, [])
        )


chat_event_bus = ChatEventBus()