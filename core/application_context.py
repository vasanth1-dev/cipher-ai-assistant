"""
Cipher v2
Application Context

Provides a shared application context that can be accessed
throughout the application without introducing circular imports.

Unlike RuntimeRegistry, this class owns the currently active
CipherApplication instance.
"""

from __future__ import annotations

from typing import Optional

from core.application import CipherApplication


class ApplicationContext:
    """
    Global application context.
    """

    _application: Optional[CipherApplication] = None

    @classmethod
    def set_application(
        cls,
        application: CipherApplication,
    ) -> None:
        cls._application = application

    @classmethod
    def application(cls) -> CipherApplication:
        if cls._application is None:
            raise RuntimeError(
                "Cipher application has not been initialized."
            )

        return cls._application

    @classmethod
    def runtime(cls):
        return cls.application().runtime

    @classmethod
    def plugin_manager(cls):
        return cls.application().plugin_manager

    @classmethod
    def service_manager(cls):
        return cls.application().service_manager

    @classmethod
    def event_bus(cls):
        return cls.application().event_bus

    @classmethod
    def application_state(cls):
        return cls.application().application_state

    @classmethod
    def initialized(cls) -> bool:
        return cls._application is not None