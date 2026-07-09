from __future__ import annotations

from abc import ABC, abstractmethod


class BasePlugin(ABC):
    """
    Base class for every Cipher plugin.

    Every plugin should inherit from this class.
    """

    name = "Unnamed Plugin"
    version = "1.0.0"
    author = "Unknown"
    description = ""

    # --------------------------------------------------

    @abstractmethod
    def on_load(self):
        """
        Called when the plugin is loaded.
        """
        raise NotImplementedError

    # --------------------------------------------------

    @abstractmethod
    def on_unload(self):
        """
        Called before the plugin is unloaded.
        """
        raise NotImplementedError

    # --------------------------------------------------

    def commands(self) -> dict:
        """
        Return plugin commands.

        Example:
            {
                "weather": self.weather,
                "news": self.news,
            }
        """
        return {}
    
    def can_handle(
        self,
        command: str,
    ) -> bool:
        """
        Return True if this plugin can handle thecommand.
        """

        command = command.lower().strip()

        for trigger in self.commands().keys():

            trigger = trigger.lower().strip()

            if (
                command == trigger
                or command.startswith(trigger + " ")
            ):
                return True
        
        return False
    # --------------------------------------------------

    def settings(self) -> dict:
        """
        Return plugin settings.
        """

        return {}

    # --------------------------------------------------

    def startup(self):
        """
        Optional startup hook.
        """

        pass

    # --------------------------------------------------

    def shutdown(self):
        """
        Optional shutdown hook.
        """

        pass

    # --------------------------------------------------

    def __repr__(self):

        return (
            f"<Plugin "
            f"{self.name} "
            f"v{self.version}>"
        )