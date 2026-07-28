"""
Cipher v2
Location Plugin

Provides location information for the current device using
IP-based geolocation services.

Features
--------
- Detect current public IP
- Get city, region, country
- Get latitude and longitude
- Get timezone
- Open current location in Google Maps
"""

from __future__ import annotations

import webbrowser

import requests

from core.logger import logger
from plugins.base_plugin import BasePlugin


class LocationPlugin(BasePlugin):
    """
    Location plugin.
    """

    name = "location"
    version = "1.0.0"
    description = "Get current location information."

    GEO_URL = "https://ipapi.co/json/"

    def can_handle(self, text: str) -> bool:
        text = text.lower()

        keywords = (
            "location",
            "where am i",
            "my location",
            "current location",
            "where are we",
            "maps",
        )

        return any(keyword in text for keyword in keywords)

    def handle(self, text: str):
        text = text.lower()

        try:
            location = self._fetch_location()

            if "map" in text or "maps" in text:
                self._open_map(
                    location["latitude"],
                    location["longitude"],
                )

                return {
                    "success": True,
                    "message": "Opened current location in Google Maps.",
                    "location": location,
                }

            return {
                "success": True,
                "message": (
                    f"You are currently in "
                    f"{location['city']}, "
                    f"{location['region']}, "
                    f"{location['country']}."
                ),
                "location": location,
            }

        except Exception as exc:
            logger.exception(exc)

            return {
                "success": False,
                "message": str(exc),
            }

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def _fetch_location(self):
        response = requests.get(
            self.GEO_URL,
            timeout=10,
        )

        response.raise_for_status()

        data = response.json()

        return {
            "ip": data.get("ip"),
            "city": data.get("city"),
            "region": data.get("region"),
            "country": data.get("country_name"),
            "postal": data.get("postal"),
            "latitude": data.get("latitude"),
            "longitude": data.get("longitude"),
            "timezone": data.get("timezone"),
            "org": data.get("org"),
        }

    @staticmethod
    def _open_map(latitude, longitude):
        url = (
            "https://www.google.com/maps"
            f"?q={latitude},{longitude}"
        )

        webbrowser.open(url)