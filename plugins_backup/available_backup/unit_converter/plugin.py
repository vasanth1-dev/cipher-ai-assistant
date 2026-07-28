"""
Cipher v2
Unit Converter Plugin

Provides common unit conversion utilities.

Features
--------
- Length conversion
- Weight conversion
- Temperature conversion
- Speed conversion
- Storage conversion
"""

from __future__ import annotations

from core.logger import logger
from plugins.base_plugin import Plugin


class UnitConverterPlugin(Plugin):
    """
    Unit conversion plugin.
    """

    name = "unit_converter"
    version = "1.0.0"
    description = "Convert between common measurement units."

    LENGTH_FACTORS = {
        "mm": 0.001,
        "cm": 0.01,
        "m": 1.0,
        "km": 1000.0,
        "in": 0.0254,
        "ft": 0.3048,
        "yd": 0.9144,
        "mi": 1609.344,
    }

    WEIGHT_FACTORS = {
        "mg": 0.001,
        "g": 1.0,
        "kg": 1000.0,
        "oz": 28.349523125,
        "lb": 453.59237,
    }

    STORAGE_FACTORS = {
        "b": 1,
        "kb": 1024,
        "mb": 1024**2,
        "gb": 1024**3,
        "tb": 1024**4,
    }

    SPEED_FACTORS = {
        "m/s": 1.0,
        "km/h": 1000 / 3600,
        "mph": 0.44704,
    }

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "convert",
            "unit",
            "kilometer",
            "meter",
            "temperature",
            "celsius",
            "fahrenheit",
            "bytes",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        """
        Unit conversions are intended to be invoked through
        Cipher's structured intent pipeline.
        """

        return {
            "success": True,
            "message": (
                "Unit Converter plugin is available. "
                "Waiting for structured conversion commands."
            ),
        }

    # --------------------------------------------------
    # Length
    # --------------------------------------------------

    def convert_length(self, value: float, source: str, target: str) -> float:
        return self._convert(value, source, target, self.LENGTH_FACTORS)

    # --------------------------------------------------
    # Weight
    # --------------------------------------------------

    def convert_weight(self, value: float, source: str, target: str) -> float:
        return self._convert(value, source, target, self.WEIGHT_FACTORS)

    # --------------------------------------------------
    # Storage
    # --------------------------------------------------

    def convert_storage(self, value: float, source: str, target: str) -> float:
        return self._convert(value, source, target, self.STORAGE_FACTORS)

    # --------------------------------------------------
    # Speed
    # --------------------------------------------------

    def convert_speed(self, value: float, source: str, target: str) -> float:
        return self._convert(value, source, target, self.SPEED_FACTORS)

    # --------------------------------------------------
    # Temperature
    # --------------------------------------------------

    @staticmethod
    def convert_temperature(value: float, source: str, target: str) -> float:
        source = source.lower()
        target = target.lower()

        if source == target:
            return value

        # Celsius conversions
        if source == "c":
            c = value
        elif source == "f":
            c = (value - 32) * 5 / 9
        elif source == "k":
            c = value - 273.15
        else:
            raise ValueError(f"Unsupported temperature unit: {source}")

        if target == "c":
            return c
        if target == "f":
            return (c * 9 / 5) + 32
        if target == "k":
            return c + 273.15

        raise ValueError(f"Unsupported temperature unit: {target}")

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    @staticmethod
    def _convert(
        value: float,
        source: str,
        target: str,
        factors: dict[str, float],
    ) -> float:
        source = source.lower()
        target = target.lower()

        if source not in factors:
            raise ValueError(f"Unsupported unit: {source}")

        if target not in factors:
            raise ValueError(f"Unsupported unit: {target}")

        base = value * factors[source]
        return base / factors[target]

    @staticmethod
    def log_error(exc: Exception):
        logger.exception(exc)