from __future__ import annotations

from plugins.base_plugin import BasePlugin
from plugins.plugin_manifest import PluginManifest
from services.media_service import media_service


class MediaPlugin(BasePlugin):
    """
    Built-in Media plugin.

    Delegates media playback operations to Cipher's
    MediaService.
    """

    def __init__(self):

        super().__init__()

        self.manifest = PluginManifest(
            name="media",
            version="1.0.0",
            author="Cipher",
            description="Control media playback.",
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
            "play ",
            "pause",
            "resume",
            "stop",
            "next",
            "previous",
            "shuffle",
            "repeat",
            "mute music",
            "unmute music",
        )

        return command.startswith(prefixes)

    # --------------------------------------------------
    # Command Handler
    # --------------------------------------------------

    def handle(
        self,
        command: str,
    ) -> str:

        command = command.strip()
        lower = command.lower()

        try:

            if lower.startswith("play "):

                media = command[5:].strip()

                if not media:
                    return "Please specify what to play."

                return media_service.play(media)

            if lower == "pause":
                return media_service.pause()

            if lower == "resume":
                return media_service.resume()

            if lower == "stop":
                return media_service.stop()

            if lower == "next":
                return media_service.next()

            if lower == "previous":
                return media_service.previous()

            if lower == "shuffle":
                return media_service.shuffle()

            if lower == "repeat":
                return media_service.repeat()

            if lower == "mute music":
                return media_service.mute()

            if lower == "unmute music":
                return media_service.unmute()

            return "Unsupported media command."

        except Exception as e:

            return f"Media error: {e}"