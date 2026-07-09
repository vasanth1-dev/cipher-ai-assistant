"""
Cipher v2
XML Tools Plugin

Provides XML parsing, formatting, validation, and conversion utilities.

Features
--------
- Parse XML
- Pretty-print XML
- Validate XML
- Convert XML to dictionary
- Read XML attributes
"""

from __future__ import annotations

from xml.dom import minidom
import xml.etree.ElementTree as ET

from core.logger import logger
from plugins.base.plugin import Plugin


class XMLToolsPlugin(Plugin):
    """
    XML utilities plugin.
    """

    name = "xml_tools"
    version = "1.0.0"
    description = "Utilities for working with XML documents."

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "xml",
            "format xml",
            "validate xml",
            "parse xml",
            "pretty xml",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        XML operations are expected to be invoked through
        Cipher's structured developer/document intent pipeline.
        """

        return {
            "success": True,
            "message": (
                "XML Tools plugin is available. "
                "Waiting for structured XML commands."
            ),
        }

    # --------------------------------------------------
    # Validation
    # --------------------------------------------------

    @staticmethod
    def validate(text: str) -> tuple[bool, str]:
        try:
            ET.fromstring(text)
            return True, "Valid XML"
        except ET.ParseError as exc:
            return False, str(exc)

    # --------------------------------------------------
    # Parsing
    # --------------------------------------------------

    @staticmethod
    def parse(text: str) -> ET.Element:
        return ET.fromstring(text)

    @classmethod
    def to_dict(cls, text: str) -> dict:
        root = cls.parse(text)
        return cls._element_to_dict(root)

    @classmethod
    def _element_to_dict(cls, element: ET.Element):
        children = list(element)

        if not children:
            return element.text or ""

        data = {}

        for child in children:
            data[child.tag] = cls._element_to_dict(child)

        if element.attrib:
            data["@attributes"] = dict(element.attrib)

        return data

    # --------------------------------------------------
    # Formatting
    # --------------------------------------------------

    @staticmethod
    def pretty(text: str) -> str:
        parsed = minidom.parseString(text)

        return parsed.toprettyxml(indent="    ")

    # --------------------------------------------------
    # Logging
    # --------------------------------------------------

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)