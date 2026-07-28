"""
Cipher v2
Archive Plugin

Create and extract archive files.

Supported Formats
-----------------
- ZIP
- TAR
- TAR.GZ
- TAR.BZ2

Features
--------
- Create archives
- Extract archives
- List archive contents
- Validate archive files
"""

from __future__ import annotations

import tarfile
import zipfile
from pathlib import Path

from core.logger import logger
from plugins.base_plugin import BasePlugin


class ArchivePlugin(BasePlugin):
    """
    Archive management plugin.
    """

    name = "archive"
    version = "1.0.0"
    description = "Create and extract archive files."

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "zip",
            "archive",
            "compress",
            "extract",
            "unzip",
            "untar",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        This plugin provides archive operations.

        Higher-level intent parsing should supply:
            action
            source
            destination

        Example:

            {
                "action": "extract",
                "source": "...",
                "destination": "..."
            }

        The current implementation returns capability information until
        integrated with the assistant's file-intent pipeline.
        """

        return {
            "success": True,
            "message": (
                "Archive plugin is available. "
                "Waiting for structured archive commands."
            ),
        }

    # --------------------------------------------------
    # ZIP
    # --------------------------------------------------

    def create_zip(self, source: Path, destination: Path):
        source = Path(source)
        destination = Path(destination)

        with zipfile.ZipFile(
            destination,
            "w",
            compression=zipfile.ZIP_DEFLATED,
        ) as archive:

            if source.is_file():
                archive.write(source, arcname=source.name)
                return

            for file in source.rglob("*"):
                if file.is_file():
                    archive.write(
                        file,
                        arcname=file.relative_to(source),
                    )

    def extract_zip(self, archive_path: Path, destination: Path):
        with zipfile.ZipFile(archive_path, "r") as archive:
            archive.extractall(destination)

    def list_zip(self, archive_path: Path):
        with zipfile.ZipFile(archive_path, "r") as archive:
            return archive.namelist()

    # --------------------------------------------------
    # TAR
    # --------------------------------------------------

    def create_tar(
        self,
        source: Path,
        destination: Path,
        mode: str = "w",
    ):
        source = Path(source)

        with tarfile.open(destination, mode) as archive:
            archive.add(source, arcname=source.name)

    def extract_tar(self, archive_path: Path, destination: Path):
        with tarfile.open(archive_path, "r:*") as archive:
            archive.extractall(destination)

    def list_tar(self, archive_path: Path):
        with tarfile.open(archive_path, "r:*") as archive:
            return archive.getnames()

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    @staticmethod
    def is_supported(path: Path):
        suffixes = "".join(path.suffixes).lower()

        return suffixes in (
            ".zip",
            ".tar",
            ".tar.gz",
            ".tgz",
            ".tar.bz2",
            ".tbz2",
        )

    @staticmethod
    def exists(path: Path):
        return Path(path).exists()

    # --------------------------------------------------
    # Logging helper
    # --------------------------------------------------

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)