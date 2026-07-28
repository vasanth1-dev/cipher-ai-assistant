"""
Built-in Cipher plugins.

Each subpackage inside this directory represents a single
plugin.

Example layout
--------------

plugins/
    available/
        weather/
        reminder/
        calculator/
        clipboard/
        system/
        notes/

Each plugin package should expose exactly one class derived
from BasePlugin.

Example
-------

from .weather_plugin import WeatherPlugin

__all__ = [
    "WeatherPlugin",
]
"""

__all__: list[str] = []