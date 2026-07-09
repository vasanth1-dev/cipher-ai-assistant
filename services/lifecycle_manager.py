"""
Cipher v2
Lifecycle Manager

Coordinates high-level application lifecycle transitions.

Responsibilities
----------------
- Startup
- Ready
- Pause
- Resume
- Shutdown
- Lifecycle event publication
"""

from __future__ import annotations

from enum import Enum

from core.logger import logger


class LifecycleState(str, Enum):
    """
    Application lifecycle states.
    """

    CREATED = "created"
    STARTING = "starting"
    READY = "ready"
    PAUSED = "paused"
    STOPPING = "stopping"
    STOPPED = "stopped"


class LifecycleManager:
    """
    Manages the runtime lifecycle of Cipher.
    """

    def __init__(
        self,
        *,
        application_state=None,
        event_bus=None,
    ):
        self.application_state = application_state
        self.event_bus = event_bus

        self._state = LifecycleState.CREATED

    # --------------------------------------------------
    # State
    # --------------------------------------------------

    @property
    def state(self) -> LifecycleState:
        return self._state

    def is_ready(self) -> bool:
        return self._state == LifecycleState.READY

    # --------------------------------------------------
    # Transitions
    # --------------------------------------------------

    def starting(self) -> None:
        self._transition(LifecycleState.STARTING)

    def ready(self) -> None:
        self._transition(LifecycleState.READY)

        if self.application_state is not None:
            self.application_state.ready = True

    def pause(self) -> None:
        self._transition(LifecycleState.PAUSED)

        if self.application_state is not None:
            self.application_state.listening = False

    def resume(self) -> None:
        self._transition(LifecycleState.READY)

        if self.application_state is not None:
            self.application_state.listening = True

    def stopping(self) -> None:
        self._transition(LifecycleState.STOPPING)

        if self.application_state is not None:
            self.application_state.ready = False

    def stopped(self) -> None:
        self._transition(LifecycleState.STOPPED)

    # --------------------------------------------------
    # Internal
    # --------------------------------------------------

    def _transition(
        self,
        state: LifecycleState,
    ) -> None:
        previous = self._state
        self._state = state

        logger.info(
            "Lifecycle transition: %s -> %s",
            previous.value,
            state.value,
        )

        if self.event_bus is not None:
            try:
                self.event_bus.publish(
                    "lifecycle.changed",
                    previous=previous.value,
                    current=state.value,
                )
            except Exception:
                logger.exception(
                    "Failed to publish lifecycle event."
                )

    # --------------------------------------------------
    # Diagnostics
    # --------------------------------------------------

    def status(self) -> dict:
        """
        Return lifecycle information.
        """
        return {
            "state": self._state.value,
            "ready": self.is_ready(),
        }