import os
import shutil
import subprocess

from core.logger import logger
from services.path_service import path_service


class FileService:

    def open_folder(self, folder):

        path = path_service.get(folder)

        if path is None:
            return "Folder not found."

        try:

            subprocess.Popen(
                [
                    "xdg-open",
                    str(path),
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )

            return f"Opening {folder}."

        except Exception as e:

            logger.exception(e)

            return "Unable to open the folder."

    def create_folder(self, name, location="home"):

        base = path_service.get(location)

        if base is None:
            return "Location not found."

        folder = os.path.join(base, name)

        try:

            os.makedirs(folder, exist_ok=True)

            return "Folder created successfully."

        except Exception as e:

            logger.exception(e)

            return "Unable to create folder."

    def delete_folder(self, name, location="home"):

        base = path_service.get(location)

        if base is None:
            return "Location not found."

        folder = os.path.join(base, name)

        if not os.path.exists(folder):
            return "Folder not found."

        try:

            shutil.rmtree(folder)

            return "Folder deleted."

        except Exception as e:

            logger.exception(e)

            return "Unable to delete the folder."

    def list_folder(self, location="home"):

        base = path_service.get(location)

        if base is None:
            return "Location not found."

        try:

            files = os.listdir(base)

            if not files:
                return "Folder is empty."

            return "\n".join(files)

        except Exception as e:
            logger.exception(e)

            return "Error"


file_service = FileService()