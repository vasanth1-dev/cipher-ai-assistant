from pathlib import Path


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

    def get(self, name: str):

        return self.paths.get(name.lower())


path_service = PathService()