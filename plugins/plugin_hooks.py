from __future__ import annotations

from collections import defaultdict
from enum import Enum
from typing import Callable, DefaultDict, List

from core.logger import logger


HookCallback = Callable[..., None]


class Hook(str, Enum):
    """
    Standard lifecycle hooks supported by Cipher.

    Additional hooks can be registered using their
    string names if needed.
    """

    BEFORE_STARTUP = "before_startup"
    AFTER_STARTUP = "after_startup"

    BEFORE_SHUTDOWN = "before_shutdown"
    AFTER_SHUTDOWN = "after_shutdown"

    BEFORE_COMMAND = "before_command"
    AFTER_COMMAND = "after_command"

    BEFORE_AI_REQUEST = "before_ai_request"
    AFTER_AI_RESPONSE = "after_ai_response"

    BEFORE_SPEECH = "before_speech"
    AFTER_SPEECH = "after_speech"


class PluginHooks:
    """
    Hook manager used by the plugin framework.

    Unlike the event bus, hooks are intended for
    lifecycle extension points inside Cipher.
    """

    def __init__(self):

        self._hooks: DefaultDict[
            str,
            List[HookCallback],
        ] = defaultdict(list)

    # --------------------------------------------------
    # Register
    # --------------------------------------------------

    def register(
        self,
        hook: Hook | str,
        callback: HookCallback,
    ) -> None:

        hook_name = str(hook)

        if callback in self._hooks[hook_name]:
            return

        self._hooks[hook_name].append(callback)

        logger.debug(
            f"Registered hook '{hook_name}'"
        )

    # --------------------------------------------------
    # Unregister
    # --------------------------------------------------

    def unregister(
        self,
        hook: Hook | str,
        callback: HookCallback,
    ) -> bool:

        hook_name = str(hook)

        callbacks = self._hooks.get(hook_name)

        if not callbacks:
            return False

        try:

            callbacks.remove(callback)

            if not callbacks:
                del self._hooks[hook_name]

            return True

        except ValueError:

            return False

    # --------------------------------------------------
    # Execute
    # --------------------------------------------------

    def run(
        self,
        hook: Hook | str,
        *args,
        **kwargs,
    ) -> None:

        hook_name = str(hook)

        callbacks = list(
            self._hooks.get(hook_name, [])
        )

        logger.debug(
            f"Running hook '{hook_name}' "
            f"({len(callbacks)} callback(s))"
        )

        for callback in callbacks:

            try:

                callback(*args, **kwargs)

            except Exception:

                logger.exception(
                    f"Hook '{hook_name}' failed."
                )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def clear(self) -> None:

        self._hooks.clear()

    def has(
        self,
        hook: Hook | str,
    ) -> bool:

        return bool(
            self._hooks.get(str(hook))
        )

    def callbacks(
        self,
        hook: Hook | str,
    ) -> List[HookCallback]:

        return list(
            self._hooks.get(str(hook), [])
        )


# Global hook manager
plugin_hooks = PluginHooks()