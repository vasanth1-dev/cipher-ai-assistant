from pathlib import Path

from core.logger import logger


class PathService:

    def __init__(self):

        self.home = Path.home()

        self.paths = {
            "desktop": self.home / "Desktop",
            "downloads": self.home / "Downloads",
            "documents": self.home / "Documents",
            "pictures": self.home / "Pictures",
            "videos": self.home / "Videos",
            "music": self.home / "Music",
            "home": self.home,
        }

    # --------------------------------------------------
    # Get Path
    # --------------------------------------------------

    def get(self, name: str):

        if not name:
            return None

        key = str(name).strip().lower()

        path = self.paths.get(key)

        if path is None:

            logger.warning(
                f"[PATH] Unknown location: {name}"
            )

            return None

        return path

    # --------------------------------------------------
    # Utilities
    # --------------------------------------------------

    def exists(self, name: str):

        path = self.get(name)

        return (
            path is not None
            and path.exists()
        )

    def available(self):

        return sorted(
            self.paths.keys()
        )


path_service = PathService()