"""
Cipher v2
PDF Plugin

Provides PDF document utilities.

Features
--------
- Read PDF metadata
- Extract text
- Count pages
- Merge PDFs
- Split PDFs
"""

from __future__ import annotations

from pathlib import Path

from core.logger import logger
from plugins.base.plugin import Plugin

try:
    from pypdf import PdfReader, PdfWriter
except ImportError:
    PdfReader = None
    PdfWriter = None


class PDFPlugin(Plugin):
    """
    PDF document plugin.
    """

    name = "pdf"
    version = "1.0.0"
    description = "Read and manipulate PDF documents."

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "pdf",
            "merge pdf",
            "split pdf",
            "extract pdf",
            "read pdf",
            "document",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        return {
            "success": True,
            "message": (
                "PDF plugin is available. "
                "Waiting for structured PDF commands."
            ),
        }

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _require_library():
        if PdfReader is None:
            raise RuntimeError(
                "PyPDF is not installed. Install it using: pip install pypdf"
            )

    # --------------------------------------------------
    # Read
    # --------------------------------------------------

    def page_count(self, pdf_path: Path) -> int:
        self._require_library()

        reader = PdfReader(str(pdf_path))
        return len(reader.pages)

    def extract_text(self, pdf_path: Path) -> str:
        self._require_library()

        reader = PdfReader(str(pdf_path))

        text = []

        for page in reader.pages:
            page_text = page.extract_text() or ""
            text.append(page_text)

        return "\n".join(text)

    def metadata(self, pdf_path: Path):
        self._require_library()

        reader = PdfReader(str(pdf_path))

        return dict(reader.metadata or {})

    # --------------------------------------------------
    # Merge
    # --------------------------------------------------

    def merge(self, pdf_files: list[Path], output: Path):
        self._require_library()

        writer = PdfWriter()

        for pdf in pdf_files:
            reader = PdfReader(str(pdf))

            for page in reader.pages:
                writer.add_page(page)

        with output.open("wb") as fp:
            writer.write(fp)

    # --------------------------------------------------
    # Split
    # --------------------------------------------------

    def split(self, pdf_path: Path, output_directory: Path):
        self._require_library()

        output_directory.mkdir(parents=True, exist_ok=True)

        reader = PdfReader(str(pdf_path))

        created_files = []

        for index, page in enumerate(reader.pages, start=1):
            writer = PdfWriter()
            writer.add_page(page)

            output = output_directory / f"page_{index}.pdf"

            with output.open("wb") as fp:
                writer.write(fp)

            created_files.append(output)

        return created_files

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    @staticmethod
    def is_pdf(path: Path) -> bool:
        return Path(path).suffix.lower() == ".pdf"

    @staticmethod
    def exists(path: Path) -> bool:
        return Path(path).exists()

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)