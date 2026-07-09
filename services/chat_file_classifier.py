from __future__ import annotations

from pathlib import Path


class ChatFileClassifier:
    """
    Classifies files into high-level categories.

    This service only classifies files. It does not
    read, parse, upload, or process their contents.
    """

    IMAGE = {
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".gif",
        ".webp",
        ".svg",
    }

    DOCUMENT = {
        ".txt",
        ".md",
        ".pdf",
        ".doc",
        ".docx",
        ".odt",
        ".rtf",
    }

    CODE = {
        ".py",
        ".cpp",
        ".c",
        ".h",
        ".hpp",
        ".java",
        ".kt",
        ".js",
        ".ts",
        ".html",
        ".css",
        ".php",
        ".go",
        ".rs",
        ".swift",
        ".cs",
        ".sql",
        ".sh",
        ".json",
        ".yaml",
        ".yml",
        ".xml",
        ".toml",
        ".ini",
    }

    ARCHIVE = {
        ".zip",
        ".tar",
        ".gz",
        ".7z",
        ".rar",
    }

    AUDIO = {
        ".wav",
        ".mp3",
        ".ogg",
        ".flac",
        ".aac",
        ".m4a",
    }

    VIDEO = {
        ".mp4",
        ".mkv",
        ".avi",
        ".mov",
        ".webm",
    }

    # --------------------------------------------------

    def category(
        self,
        filepath: str | Path,
    ) -> str:

        suffix = Path(filepath).suffix.lower()

        if suffix in self.IMAGE:
            return "image"

        if suffix in self.DOCUMENT:
            return "document"

        if suffix in self.CODE:
            return "code"

        if suffix in self.ARCHIVE:
            return "archive"

        if suffix in self.AUDIO:
            return "audio"

        if suffix in self.VIDEO:
            return "video"

        return "unknown"

    # --------------------------------------------------

    def is_code(
        self,
        filepath: str | Path,
    ) -> bool:

        return self.category(filepath) == "code"

    # --------------------------------------------------

    def is_document(
        self,
        filepath: str | Path,
    ) -> bool:

        return self.category(filepath) == "document"

    # --------------------------------------------------

    def is_image(
        self,
        filepath: str | Path,
    ) -> bool:

        return self.category(filepath) == "image"

    # --------------------------------------------------

    def is_archive(
        self,
        filepath: str | Path,
    ) -> bool:

        return self.category(filepath) == "archive"


chat_file_classifier = ChatFileClassifier()