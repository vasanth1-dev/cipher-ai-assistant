import os
import shutil
import subprocess

from services.path_service import path_service


class FileService:

    # ----------------------------
    # Open Folder
    # ----------------------------

    def open_folder(self, folder):

        path = path_service.get(folder)

        if path is None:
            return "Folder not found."

        try:

            subprocess.Popen(
                [
                    "xdg-open",
                    str(path),
                ]
            )

            return f"Opening {folder}."

        except Exception as e:

            return f"Error: {e}"

    # ----------------------------
    # Create Folder
    # ----------------------------

    def create_folder(self, name, location="home"):

        base = path_service.get(location)

        if base is None:
            return "Location not found."

        folder = os.path.join(base, name)

        try:

            os.makedirs(folder, exist_ok=True)

            return "Folder created successfully."

        except Exception as e:

            return f"Error: {e}"

    # ----------------------------
    # Delete Folder
    # ----------------------------

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

            return f"Error: {e}"

    # ----------------------------
    # List Folder
    # ----------------------------

    def list_folder(self, location="home"):

        base = path_service.get(location)

        if base is None:
            return "Location not found."

        try:

            files = os.listdir(base)

            if not files:
                return "Folder is empty."

            return "\n".join(sorted(files))

        except Exception as e:

            return f"Error: {e}"

    # ----------------------------
    # Open File
    # ----------------------------

    def open_file(self, filepath):

        if not os.path.exists(filepath):
            return "File not found."

        try:

            subprocess.Popen(
                [
                    "xdg-open",
                    filepath,
                ]
            )

            return "Opening file."

        except Exception as e:

            return f"Error: {e}"

    # ----------------------------
    # Copy File
    # ----------------------------

    def copy_file(self, source, destination):

        try:

            shutil.copy2(source, destination)

            return "File copied successfully."

        except Exception as e:

            return f"Error: {e}"

    # ----------------------------
    # Move File
    # ----------------------------

    def move_file(self, source, destination):

        try:

            shutil.move(source, destination)

            return "File moved successfully."

        except Exception as e:

            return f"Error: {e}"

    # ----------------------------
    # Rename File
    # ----------------------------

    def rename_file(self, source, new_name):

        if not os.path.exists(source):
            return "File not found."

        try:

            directory = os.path.dirname(source)

            destination = os.path.join(
                directory,
                new_name,
            )

            os.rename(
                source,
                destination,
            )

            return "File renamed successfully."

        except Exception as e:

            return f"Error: {e}"


file_service = FileService()