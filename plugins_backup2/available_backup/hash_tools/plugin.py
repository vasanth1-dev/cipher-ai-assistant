"""
Cipher v2
Hash Tools Plugin

Provides hashing and checksum utilities.

Features
--------
- MD5
- SHA1
- SHA224
- SHA256
- SHA384
- SHA512
- File hashing
- Text hashing
"""

from __future__ import annotations

import hashlib
from pathlib import Path

from core.logger import logger
from plugins.base_plugin import Plugin


class HashToolsPlugin(Plugin):
    """
    Hash generation plugin.
    """

    name = "hash_tools"
    version = "1.0.0"
    description = "Generate hashes for text and files."

    BUFFER_SIZE = 1024 * 1024

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "hash",
            "checksum",
            "sha256",
            "sha512",
            "md5",
            "generate hash",
            "verify hash",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        Hash operations are expected to be routed through
        Cipher's structured intent pipeline.
        """

        return {
            "success": True,
            "message": (
                "Hash Tools plugin is available. "
                "Waiting for structured hash commands."
            ),
        }

    # --------------------------------------------------
    # Text Hashing
    # --------------------------------------------------

    @staticmethod
    def hash_text(text: str, algorithm: str = "sha256") -> str:
        hasher = HashToolsPlugin._new_hasher(algorithm)
        hasher.update(text.encode("utf-8"))
        return hasher.hexdigest()

    # --------------------------------------------------
    # File Hashing
    # --------------------------------------------------

    @classmethod
    def hash_file(cls, path: Path, algorithm: str = "sha256") -> str:
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(path)

        hasher = cls._new_hasher(algorithm)

        with path.open("rb") as fp:
            while True:
                chunk = fp.read(cls.BUFFER_SIZE)
                if not chunk:
                    break
                hasher.update(chunk)

        return hasher.hexdigest()

    # --------------------------------------------------
    # Verification
    # --------------------------------------------------

    @classmethod
    def verify_file(
        cls,
        path: Path,
        expected_hash: str,
        algorithm: str = "sha256",
    ) -> bool:
        return (
            cls.hash_file(path, algorithm).lower()
            == expected_hash.lower()
        )

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def algorithms() -> list[str]:
        return sorted(hashlib.algorithms_available)

    @staticmethod
    def _new_hasher(name: str):
        try:
            return hashlib.new(name.lower())
        except ValueError as exc:
            raise ValueError(
                f"Unsupported hash algorithm: {name}"
            ) from exc

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)