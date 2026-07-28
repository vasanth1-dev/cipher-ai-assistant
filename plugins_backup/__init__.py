"""
Cipher Plugin Framework

This package provides the complete plugin infrastructure for
Cipher AI Assistant.

Main Components
---------------
- BasePlugin
- PluginManager
- PluginRegistry
- PluginManifest
- PluginContext
- PluginEventBus
- PluginHooks
- PluginCommandRegistry
- PluginServiceRegistry

Typical usage
-------------
    from plugins import plugin_manager

    plugin_manager.start()
"""

from plugins.base_plugin import Plugin
from plugins.plugin_command import PluginCommand
from plugins.plugin_command_registry import (
    plugin_command_registry,
)
from plugins.plugin_context import PluginContext
from plugins.plugin_event import PluginEvent
from plugins.plugin_event_bus import (
    plugin_event_bus,
)
from plugins.plugin_hooks import (
    Hook,
    plugin_hooks,
)
from plugins.plugin_manager import (
    PluginManager,
    plugin_manager,
)
from plugins.plugin_manifest import PluginManifest
from plugins.plugin_registry import PluginRegistry
from plugins.plugin_service import PluginService
from plugins.plugin_service_registry import (
    plugin_service_registry,
)

__all__ = [
    "BasePlugin",
    "PluginCommand",
    "PluginContext",
    "PluginEvent",
    "PluginHooks",
    "PluginManager",
    "PluginManifest",
    "PluginRegistry",
    "PluginService",
    "Hook",
    "plugin_command_registry",
    "plugin_event_bus",
    "plugin_hooks",
    "plugin_manager",
    "plugin_service_registry",
]