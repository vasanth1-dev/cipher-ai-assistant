from __future__ import annotations

from plugins.base_plugin import BasePlugin
from plugins.plugin_manifest import PluginManifest
from services.file_manager_service import file_manager_service


class FileManagerPlugin(BasePlugin):
    """
    Built-in File Manager plugin.

    Delegates all filesystem operations to Cipher's
    FileManagerService.
    """

    def __init__(
       self,
    ) -> None:

        super().__init__()

        self.manifest = PluginManifest(
            id=self.name.lower().replace(" ", "_"),
            name="file_manager",
            version="1.0.0",
            author="Cipher",
            description="Manage files and folders.",
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
            "create folder",
            "create directory",
            "make folder",
            "mkdir",
            "create file",
            "delete file",
            "delete folder",
            "rename file",
            "rename folder",
            "move file",
            "copy file",
            "list files",
            "list folders",
            "open file",
            "open folder",
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

            if lower.startswith(
                (
                    "create folder",
                    "create directory",
                    "make folder",
                    "mkdir",
                )
            ):
                return file_manager_service.create_folder(command)

            if lower.startswith("create file"):
                return file_manager_service.create_file(command)

            if lower.startswith("delete file"):
                return file_manager_service.delete_file(command)

            if lower.startswith("delete folder"):
                return file_manager_service.delete_folder(command)

            if lower.startswith("rename file"):
                return file_manager_service.rename_file(command)

            if lower.startswith("rename folder"):
                return file_manager_service.rename_folder(command)

            if lower.startswith("move file"):
                return file_manager_service.move_file(command)

            if lower.startswith("copy file"):
                return file_manager_service.copy_file(command)

            if lower.startswith("list files"):
                return file_manager_service.list_files(command)

            if lower.startswith("list folders"):
                return file_manager_service.list_folders(command)

            if lower.startswith("open file"):
                return file_manager_service.open_file(command)

            if lower.startswith("open folder"):
                return file_manager_service.open_folder(command)

            return "Unsupported file manager command."

        except Exception as e:

            return f"File manager error: {e}"