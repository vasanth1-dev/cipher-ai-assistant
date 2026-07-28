from __future__ import annotations

from pathlib import Path


class NotesService:
    """
    Basic Notes Service.
    """

    def __init__(
       self,
    ) -> None:
        self.notes_dir = Path("data/notes")
        self.notes_dir.mkdir(parents=True, exist_ok=True)

    def create(self, name: str, content: str) -> str:
        note_file = self.notes_dir / f"{name}.txt"

        try:
            note_file.write_text(content, encoding="utf-8")
            return f"Note '{name}' created successfully."
        except Exception as e:
            return f"Failed to create note: {e}"

    def read(self, name: str) -> str:
        note_file = self.notes_dir / f"{name}.txt"

        if not note_file.exists():
            return f"Note '{name}' not found."

        try:
            return note_file.read_text(encoding="utf-8")
        except Exception as e:
            return f"Failed to read note: {e}"

    def delete(self, name: str) -> str:
        note_file = self.notes_dir / f"{name}.txt"

        if not note_file.exists():
            return f"Note '{name}' not found."

        try:
            note_file.unlink()
            return f"Note '{name}' deleted."
        except Exception as e:
            return f"Failed to delete note: {e}"

    def execute(self, command: str) -> str:
        return f"Notes service received command: {command}"


notes_service = NotesService()