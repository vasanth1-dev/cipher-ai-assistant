"""
Cipher v2
Event Bus

Lightweight publish/subscribe event system used for communication
between services, plugins, GUI components, and the core assistant.

Features
--------
- Publish events
- Subscribe to events
- Unsubscribe from events
- Wildcard subscriptions
- Thread-safe
"""

from __future__ import annotations

import threading
from collections import defaultdict
from typing import Any, Callable

from core.logger import logger


class EventBus:
    """
    Thread-safe publish/subscribe event bus.
    """

    WILDCARD = "*"

    def __init__(self):
        self._subscribers: dict[str, list[Callable]] = defaultdict(list)
        self._lock = threading.RLock()

    # --------------------------------------------------
    # Subscription
    # --------------------------------------------------

    def subscribe(
        self,
        event: str,
        callback: Callable[..., Any],
    ) -> None:
        """
        Subscribe to an event.
        """
        with self._lock:
            if callback not in self._subscribers[event]:
                self._subscribers[event].append(callback)

        logger.debug("Subscribed to event: %s", event)

    def unsubscribe(
        self,
        event: str,
        callback: Callable[..., Any],
    ) -> bool:
        """
        Remove an event subscription.
        """
        with self._lock:
            listeners = self._subscribers.get(event)

            if not listeners:
                return False

            try:
                listeners.remove(callback)
                return True
            except ValueError:
                return False

    # --------------------------------------------------
    # Publishing
    # --------------------------------------------------

    def publish(
        self,
        event: str,
        *args,
        **kwargs,
    ) -> int:
        """
        Publish an event.

        Returns
        -------
        int
            Number of listeners notified.
        """
        callbacks: list[Callable] = []

        with self._lock:
            callbacks.extend(self._subscribers.get(event, []))
            callbacks.extend(
                self._subscribers.get(self.WILDCARD, [])
            )

        notified = 0

        for callback in callbacks:
            try:
                callback(*args, **kwargs)
                notified += 1

            except Exception:
                logger.exception(
                    "Error while handling event '%s'",
                    event,
                )

        return notified

    # --------------------------------------------------
    # Information
    # --------------------------------------------------

    def listener_count(
        self,
        event: str | None = None,
    ) -> int:
        """
        Return listener count.
        """
        with self._lock:
            if event is not None:
                return len(
                    self._subscribers.get(event, [])
                )

            return sum(
                len(callbacks)
                for callbacks in self._subscribers.values()
            )

    def events(self) -> list[str]:
        """
        Return registered event names.
        """
        with self._lock:
            return sorted(self._subscribers.keys())

    # --------------------------------------------------
    # Maintenance
    # --------------------------------------------------

    def clear(self) -> None:
        """
        Remove every subscription.
        """
        with self._lock:
            self._subscribers.clear()

        logger.info("Event bus cleared.")