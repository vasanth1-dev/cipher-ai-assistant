from __future__ import annotations

from collections import defaultdict
from typing import Callable, DefaultDict, Dict, List

from core.logger import logger
from plugins.plugin_event import PluginEvent


EventHandler = Callable[[PluginEvent], None]


class PluginEventBus:
    """
    Internal event bus for the Cipher plugin framework.

    Features
    --------
    • Subscribe to events
    • Unsubscribe from events
    • Emit events
    • Wildcard event listeners
    • Safe exception handling
    """

    WILDCARD = "*"

    def __init__(
       self,
    ) -> None:

        self._handlers: DefaultDict[
            str,
            List[EventHandler],
        ] = defaultdict(list)

    # --------------------------------------------------
    # Subscribe
    # --------------------------------------------------

    def subscribe(
        self,
        event_name: str,
        handler: EventHandler,
    ) -> None:

        if handler in self._handlers[event_name]:
            return

        self._handlers[event_name].append(handler)

        logger.debug(
            f"Subscribed handler to '{event_name}'"
        )

    # --------------------------------------------------
    # Unsubscribe
    # --------------------------------------------------

    def unsubscribe(
        self,
        event_name: str,
        handler: EventHandler,
    ) -> bool:

        handlers = self._handlers.get(event_name)

        if not handlers:
            return False

        try:

            handlers.remove(handler)

            logger.debug(
                f"Unsubscribed handler from '{event_name}'"
            )

            if not handlers:
                del self._handlers[event_name]

            return True

        except ValueError:

            return False

    # --------------------------------------------------
    # Emit
    # --------------------------------------------------

    def emit(
        self,
        event: PluginEvent,
    ) -> PluginEvent:

        listeners: List[EventHandler] = []

        listeners.extend(
            self._handlers.get(event.name, [])
        )

        listeners.extend(
            self._handlers.get(self.WILDCARD, [])
        )

        logger.debug(
            f"Dispatching event '{event.name}' "
            f"to {len(listeners)} listener(s)"
        )

        for handler in listeners:

            if event.cancelled:
                break

            try:

                handler(event)

            except Exception:

                logger.exception(
                    f"Plugin event handler failed "
                    f"for '{event.name}'"
                )

        return event

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def clear(self) -> None:

        self._handlers.clear()

    def listeners(
        self,
        event_name: str,
    ) -> List[EventHandler]:

        return list(
            self._handlers.get(event_name, [])
        )

    def has_listeners(
        self,
        event_name: str,
    ) -> bool:

        return bool(
            self._handlers.get(event_name)
        )

    @property
    def events(self) -> Dict[str, int]:

        return {
            name: len(handlers)
            for name, handlers in self._handlers.items()
        }


# Global event bus instance
plugin_event_bus = PluginEventBus()