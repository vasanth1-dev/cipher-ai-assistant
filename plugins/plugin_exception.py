from __future__ import annotations


class PluginError(Exception):
    """
    Base exception for all plugin-related errors.
    """

    pass


class PluginLoadError(PluginError):
    """
    Raised when a plugin cannot be imported or initialized.
    """

    pass


class PluginRegistrationError(PluginError):
    """
    Raised when plugin registration fails.
    """

    pass


class PluginManifestError(PluginError):
    """
    Raised when a plugin manifest is invalid.
    """

    pass


class PluginDependencyError(PluginError):
    """
    Raised when one or more plugin dependencies
    cannot be resolved.
    """

    pass


class PluginAlreadyRegisteredError(PluginRegistrationError):
    """
    Raised when attempting to register
    a plugin with a duplicate name.
    """

    pass


class PluginNotFoundError(PluginError):
    """
    Raised when a requested plugin
    does not exist.
    """

    pass


class PluginDisabledError(PluginError):
    """
    Raised when attempting to use
    a disabled plugin.
    """

    pass


class PluginExecutionError(PluginError):
    """
    Raised when a plugin throws
    an exception during execution.
    """

    pass


class PluginConfigurationError(PluginError):
    """
    Raised when plugin configuration
    is missing or invalid.
    """

    pass


class PluginPermissionError(PluginError):
    """
    Raised when a plugin attempts
    an operation that is not permitted.
    """

    pass