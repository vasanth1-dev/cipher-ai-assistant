"""
Cipher v2
Runtime Initializer

Initializes the shared runtime after all core components have
been constructed.

Responsibilities
----------------
- Register runtime objects
- Initialize optional components
- Publish initialization events
- Mark application ready
"""

from __future__ import annotations

from core.logger import logger


class RuntimeInitializer:
    """
    Performs final runtime initialization.
    """

    def __init__(
        self,
        *,
        runtime_registry,
        application_state,
        event_bus=None,
    ):
        self.runtime_registry = runtime_registry
        self.application_state = application_state
        self.event_bus = event_bus

    # --------------------------------------------------
    # Initialization
    # --------------------------------------------------

    def initialize(self, **components) -> None:
        """
        Register runtime components and mark the
        application as initialized.
        """
        for name, component in components.items():
            if component is None:
                continue

            try:
                self.runtime_registry.register(
                    name,
                    component,
                )
            except ValueError:
                # Already registered; leave the existing instance.
                logger.debug(
                    "Runtime object already registered: %s",
                    name,
                )

        self.application_state.initialized = True
        self.application_state.ready = True

        if self.event_bus is not None:
            try:
                self.event_bus.publish(
                    "runtime.initialized",
                    registry=self.runtime_registry,
                )
            except Exception:
                logger.exception(
                    "Failed to publish runtime.initialized event."
                )

        logger.info("Runtime initialization complete.")

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    def validate(
        self,
        required: list[str],
    ) -> tuple[bool, list[str]]:
        """
        Validate that required runtime objects exist.
        """
        missing = [
            name
            for name in required
            if not self.runtime_registry.contains(name)
        ]

        return (len(missing) == 0, missing)