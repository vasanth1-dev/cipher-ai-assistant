"""
Cipher v2
Application Bootstrap

Builds and initializes the core runtime for Cipher.

Responsibilities
----------------
- Create core managers
- Register background services
- Wire shared dependencies
- Create the command pipeline
- Start the application through StartupManager

This module intentionally performs dependency wiring only.
"""

from __future__ import annotations

from services.application_state import ApplicationState
from services.command_pipeline import CommandPipeline
from services.context_manager import ContextManager
from services.conversation_manager import ConversationManager
from services.event_bus import EventBus
from services.health_monitor import HealthMonitor
from services.intent_router import IntentRouter
from services.plugin_manager import PluginManager
from services.service_manager import ServiceManager
from services.session_manager import SessionManager
from services.startup_manager import StartupManager

from core.logger import logger


class ApplicationBootstrap:
    """
    Creates and wires the Cipher runtime.
    """

    def __init__(
        self,
        *,
        ai_service=None,
        tts_service=None,
        gui=None,
    ):
        self.ai_service = ai_service
        self.tts_service = tts_service
        self.gui = gui

        # Core managers
        self.application_state = ApplicationState()
        self.event_bus = EventBus()
        self.session_manager = SessionManager()
        self.context_manager = ContextManager()
        self.conversation_manager = ConversationManager()

        self.service_manager = ServiceManager()
        self.plugin_manager = PluginManager()

        self.intent_router = IntentRouter(
            plugin_manager=self.plugin_manager,
            ai_service=self.ai_service,
        )

        self.command_pipeline = CommandPipeline(
            intent_router=self.intent_router,
            tts_service=self.tts_service,
            event_bus=self.event_bus,
        )

        self.health_monitor = HealthMonitor(
            service_manager=self.service_manager,
            plugin_manager=self.plugin_manager,
        )

        self.startup_manager = StartupManager(
            service_manager=self.service_manager,
            plugin_manager=self.plugin_manager,
            ai_service=self.ai_service,
            gui=self.gui,
        )

    # --------------------------------------------------
    # Service Registration
    # --------------------------------------------------

    def register_default_services(self) -> None:
        """
        Register built-in services.

        Services that already exist elsewhere in the project
        can be registered by the caller before startup.
        """
        self.service_manager.register(
            "health_monitor",
            self.health_monitor,
        )

    # --------------------------------------------------
    # Startup
    # --------------------------------------------------

    def initialize(self) -> bool:
        """
        Initialize the Cipher runtime.
        """
        logger.info("Initializing Cipher runtime...")

        self.register_default_services()

        ok = self.startup_manager.start()

        self.application_state.initialized = ok
        self.application_state.ready = ok

        return ok

    # --------------------------------------------------
    # Shutdown
    # --------------------------------------------------

    def shutdown(self) -> None:
        """
        Shutdown the Cipher runtime.
        """
        self.application_state.ready = False

        self.startup_manager.shutdown()

    # --------------------------------------------------
    # Convenience
    # --------------------------------------------------

    def runtime(self) -> dict:
        """
        Return commonly used runtime objects.
        """
        return {
            "application_state": self.application_state,
            "event_bus": self.event_bus,
            "session_manager": self.session_manager,
            "context_manager": self.context_manager,
            "conversation_manager": self.conversation_manager,
            "service_manager": self.service_manager,
            "plugin_manager": self.plugin_manager,
            "intent_router": self.intent_router,
            "command_pipeline": self.command_pipeline,
            "health_monitor": self.health_monitor,
        }