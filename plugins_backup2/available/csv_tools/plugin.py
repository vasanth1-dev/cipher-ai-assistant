"""
Cipher v2
CSV Tools Plugin

Provides CSV file processing utilities.

Features
--------
- Read CSV files
- Write CSV files
- Validate CSV
- Convert CSV to dictionaries
- Get column information
"""

from __future__ import annotations

import csv
from pathlib import Path

from core.logger import logger
from plugins.base_plugin import BasePlugin


class CSVToolsPlugin(BasePlugin):
    """
    CSV utilities plugin.
    """

    name = "csv_tools"
    version = "1.0.0"
    description = "Utilities for reading and writing CSV files."

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "csv",
            "comma separated",
            "read csv",
            "write csv",
            "validate csv",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        CSV operations are intended to be invoked through
        Cipher's structured developer/document intent pipeline.
        """

        return {
            "success": True,
            "message": (
                "CSV Tools plugin is available. "
                "Waiting for structured CSV commands."
            ),
        }

    # --------------------------------------------------
    # Reading
    # --------------------------------------------------

    @staticmethod
    def read(path: Path) -> list[dict]:
        with Path(path).open(
            "r",
            newline="",
            encoding="utf-8",
        ) as fp:
            reader = csv.DictReader(fp)
            return list(reader)

    @staticmethod
    def headers(path: Path) -> list[str]:
        with Path(path).open(
            "r",
            newline="",
            encoding="utf-8",
        ) as fp:
            reader = csv.reader(fp)
            return next(reader)

    # --------------------------------------------------
    # Writing
    # --------------------------------------------------

    @staticmethod
    def write(
        path: Path,
        rows: list[dict],
    ):
        if not rows:
            raise ValueError("No rows supplied.")

        fieldnames = list(rows[0].keys())

        with Path(path).open(
            "w",
            newline="",
            encoding="utf-8",
        ) as fp:
            writer = csv.DictWriter(
                fp,
                fieldnames=fieldnames,
            )

            writer.writeheader()
            writer.writerows(rows)

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    @staticmethod
    def validate(path: Path) -> tuple[bool, str]:
        try:
            CSVToolsPlugin.read(path)
            return True, "Valid CSV"
        except Exception as exc:
            return False, str(exc)

    # --------------------------------------------------
    # Metadata
    # --------------------------------------------------

    @staticmethod
    def info(path: Path) -> dict:
        rows = CSVToolsPlugin.read(path)

        return {
            "rows": len(rows),
            "columns": len(rows[0]) if rows else 0,
            "headers": CSVToolsPlugin.headers(path),
        }

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)