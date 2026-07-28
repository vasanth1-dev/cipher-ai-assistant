from __future__ import annotations

from plugins.base_plugin import BasePlugin
from plugins.plugin_manifest import PluginManifest
from services.weather_service import weather_service


class WeatherPlugin(BasePlugin):
    """
    Built-in Weather plugin.

    This plugin delegates all weather retrieval to
    Cipher's WeatherService.
    """

    def __init__(
       self,
    ) -> None:

        super().__init__()

        self.manifest = PluginManifest(
            id="weather",
            name="weather",
            version="1.0.0",
            author="Cipher",
            description="Provides current weather information.",
        )

    # --------------------------------------------------
    # Lifecycle
    # --------------------------------------------------

    def on_load(self) -> None:
        pass

    def on_unload(self) -> None:
        pass

    # --------------------------------------------------
    # Command Detection
    # --------------------------------------------------

    def can_handle(
        self,
        command: str,
    ) -> bool:

        command = command.lower().strip()

        prefixes = (
            "weather",
            "weather in",
            "what's the weather",
            "what is the weather",
            "current weather",
            "forecast",
        )

        return command.startswith(prefixes)

    # --------------------------------------------------
    # Command Handler
    # --------------------------------------------------

    def handle(
        self,
        command: str,
    ) -> str:

        location = self._extract_location(command)

        try:

            if location:
                return weather_service.get_weather(location)

            return weather_service.get_weather()

        except Exception as e:

            return f"Unable to retrieve weather information: {e}"

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _extract_location(
        command: str,
    ) -> str:

        lower = command.lower().strip()

        prefixes = (
            "weather in ",
            "what's the weather in ",
            "what is the weather in ",
            "forecast for ",
            "forecast in ",
        )

        for prefix in prefixes:

            if lower.startswith(prefix):

                return command[len(prefix):].strip()

        return ""