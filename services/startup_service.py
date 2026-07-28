import os
import shutil
import requests

from config import OLLAMA_URL


class StartupService:

    def __init__(
       self,
    ) -> None:
        self.results = []

    def check_python(self):
        self.results.append(("Python", True))

    def check_tesseract(self):
        self.results.append(
            (
                "Tesseract",
                shutil.which("tesseract") is not None,
            )
        )

    def check_ollama(self):

        try:
            response = requests.get(
                OLLAMA_URL.rsplit("/api", 1)[0],
                timeout=2,
            )

            self.results.append(
                (
                    "Ollama Server",
                    response.status_code == 200,
                )
            )

        except Exception:
            self.results.append(
                (
                    "Ollama Server",
                    False,
                )
            )

    def check_camera_folder(self):

        self.results.append(
            (
                "Camera Folder",
                os.path.isdir("data/images"),
            )
        )

    def check_face_folder(self):

        self.results.append(
            (
                "Face Folder",
                os.path.isdir("data/faces"),
            )
        )

    def check_screen_folder(self):

        self.results.append(
            (
                "Screen Folder",
                os.path.isdir("data/screens"),
            )
        )

    def check_memory(self):

        self.results.append(
            (
                "Memory File",
                os.path.exists("data/memory.json"),
            )
        )

    def check(self):

        self.results = []

        self.check_python()
        self.check_tesseract()
        self.check_ollama()
        self.check_camera_folder()
        self.check_face_folder()
        self.check_screen_folder()
        self.check_memory()

        return self.results


startup_service = StartupService()