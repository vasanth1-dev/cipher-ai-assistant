"""
Cipher v2
Command Pipeline

Coordinates the complete request lifecycle.

Pipeline
--------
Text Input / Speech Input
        │
        ▼
Preprocessing
        │
        ▼
Intent Router
        │
        ├── Plugin
        └── AI
        │
        ▼
Postprocessing
        │
        ▼
Text-to-Speech (optional)
        │
        ▼
GUI / API Response
"""

from __future__ import annotations

from typing import Any

from core.logger import logger


class CommandPipeline:
    """
    Main execution pipeline for Cipher.
    """

    def __init__(
        self,
        intent_router,
        tts_service=None,
        event_bus=None,
    ):
        self.intent_router = intent_router
        self.tts_service = tts_service
        self.event_bus = event_bus

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def execute(
        self,
        text: str,
        *,
        speak: bool = True,
    ) -> dict[str, Any]:
        """
        Execute a complete command through the pipeline.
        """
        request = self._preprocess(text)

        if self.event_bus:
            self.event_bus.publish(
                "command.received",
                request,
            )

        result = self.intent_router.route(request)

        result = self._postprocess(result)

        if self.event_bus:
            self.event_bus.publish(
                "command.completed",
                result,
            )

        if (
            speak
            and self.tts_service is not None
            and result.get("success", False)
        ):
            self._speak(result)

        return result

    # --------------------------------------------------
    # Processing
    # --------------------------------------------------

    @staticmethod
    def _preprocess(text: str) -> str:
        """
        Normalize user input before routing.
        """
        return " ".join((text or "").strip().split())

    @staticmethod
    def _postprocess(result: dict[str, Any]) -> dict[str, Any]:
        """
        Ensure a consistent response format.
        """
        result.setdefault("success", True)
        result.setdefault("message", "")
        result.setdefault("source", "unknown")

        return result

    # --------------------------------------------------
    # Speech
    # --------------------------------------------------

    def _speak(self, result: dict[str, Any]) -> None:
        message = result.get("message")

        if not message:
            return

        try:
            if hasattr(self.tts_service, "speak"):
                self.tts_service.speak(message)
            elif hasattr(self.tts_service, "say"):
                self.tts_service.say(message)

        except Exception:
            logger.exception(
                "Text-to-speech failed."
            )

    # --------------------------------------------------
    # Convenience
    # --------------------------------------------------

    def execute_silent(
        self,
        text: str,
    ) -> dict[str, Any]:
        """
        Execute without speech output.
        """
        return self.execute(
            text,
            speak=False,
        )