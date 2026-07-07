from services.file_service import file_service


INTENT = "files"


FOLDERS = (
    "downloads",
    "documents",
    "desktop",
    "pictures",
    "videos",
    "music",
    "home",
)


def _normalize(text):

    return " ".join(
        text.lower().strip().split()
    )


def _extract_name(command, prefix):

    if not command.startswith(prefix):
        return None

    return command[len(prefix):].strip()


def handle(command: str):

    if not command:
        return None

    command = _normalize(command)

    # -------------------------------------------------
    # Open Folder
    # -------------------------------------------------

    for folder in FOLDERS:

        if command in (
            f"open {folder}",
            f"show {folder}",
        ):
            return file_service.open_folder(folder)

    # -------------------------------------------------
    # List Folder
    # -------------------------------------------------

    for folder in FOLDERS:

        if command in (
            f"list {folder}",
            f"{folder} files",
        ):
            return file_service.list_folder(folder)

    # -------------------------------------------------
    # Create Folder
    # -------------------------------------------------

    name = _extract_name(
        command,
        "create folder",
    )

    if name is not None:

        if not name:
            return "Please tell me the folder name."

        return file_service.create_folder(name)

    # -------------------------------------------------
    # Delete Folder
    # -------------------------------------------------

    name = _extract_name(
        command,
        "delete folder",
    )

    if name is not None:

        if not name:
            return "Please tell me the folder name."

        return file_service.delete_folder(name)

    return None