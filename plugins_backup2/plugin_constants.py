from __future__ import annotations

"""
Common constants used by the Cipher Plugin Framework.

Keeping these values in one place avoids hardcoded strings
throughout the plugin system.
"""

# --------------------------------------------------
# Directories
# --------------------------------------------------

PLUGIN_PACKAGE = "plugins.available"

PLUGIN_DIRECTORY = "plugins/available"

PLUGIN_CONFIG_DIRECTORY = "data/plugins"

# --------------------------------------------------
# Manifest
# --------------------------------------------------

MANIFEST_FILE = "plugin.json"

INIT_FILE = "__init__.py"

# --------------------------------------------------
# Version
# --------------------------------------------------

PLUGIN_API_VERSION = "1.0"

# --------------------------------------------------
# Plugin States
# --------------------------------------------------

STATE_DISCOVERED = "discovered"
STATE_REGISTERED = "registered"
STATE_LOADED = "loaded"
STATE_ENABLED = "enabled"
STATE_DISABLED = "disabled"
STATE_ERROR = "error"
STATE_UNLOADED = "unloaded"

# --------------------------------------------------
# Event Names
# --------------------------------------------------

EVENT_PLUGIN_DISCOVERED = "plugin.discovered"
EVENT_PLUGIN_REGISTERED = "plugin.registered"
EVENT_PLUGIN_LOADED = "plugin.loaded"
EVENT_PLUGIN_ENABLED = "plugin.enabled"
EVENT_PLUGIN_DISABLED = "plugin.disabled"
EVENT_PLUGIN_UNLOADED = "plugin.unloaded"
EVENT_PLUGIN_ERROR = "plugin.error"

# --------------------------------------------------
# Hook Names
# --------------------------------------------------

HOOK_BEFORE_STARTUP = "before_startup"
HOOK_AFTER_STARTUP = "after_startup"

HOOK_BEFORE_SHUTDOWN = "before_shutdown"
HOOK_AFTER_SHUTDOWN = "after_shutdown"

HOOK_BEFORE_COMMAND = "before_command"
HOOK_AFTER_COMMAND = "after_command"

HOOK_BEFORE_AI_REQUEST = "before_ai_request"
HOOK_AFTER_AI_RESPONSE = "after_ai_response"

HOOK_BEFORE_SPEECH = "before_speech"
HOOK_AFTER_SPEECH = "after_speech"

# --------------------------------------------------
# Permissions
# --------------------------------------------------

PERMISSION_AI = "ai"
PERMISSION_AUDIO = "audio"
PERMISSION_CAMERA = "camera"
PERMISSION_CLIPBOARD = "clipboard"
PERMISSION_FILESYSTEM = "filesystem"
PERMISSION_GUI = "gui"
PERMISSION_MEMORY = "memory"
PERMISSION_MICROPHONE = "microphone"
PERMISSION_NETWORK = "network"
PERMISSION_NOTIFICATIONS = "notifications"
PERMISSION_PROCESS = "process"
PERMISSION_SETTINGS = "settings"
PERMISSION_SHELL = "shell"
PERMISSION_SYSTEM = "system"
PERMISSION_TTS = "tts"