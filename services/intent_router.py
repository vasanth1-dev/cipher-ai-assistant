"""
Cipher v2
Intent Router

Routes user requests to the appropriate plugin before falling
back to the language model.

Responsibilities
----------------
- Find a plugin that can handle the request
- Execute the plugin safely
- Fall back to the AI service when needed
- Return a standardized response
"""

from __future__ import annotations

from typing import Any

from core.logger import logger


class IntentRouter:
    """
    Routes requests between plugins and the AI model.
    """

    def __init__(
        self,
        plugin_manager,
        ai_service=None,
    ):
        self.plugin_manager = plugin_manager
        self.ai_service = ai_service

    # --------------------------------------------------
    # Public API
    # --------------------------------------------------

    def route(self, text: str) -> dict[str, Any]:
        """
        Route a user request.

        Priority:
            1. Matching plugin
            2. AI model
        """
        text = (text or "").strip()

        if not text:
            return {
                "success": False,
                "source": "router",
                "message": "Empty request.",
            }

        plugin = self._find_plugin(text)

        if plugin is not None:
            try:
                result = plugin.handle(text)

                if isinstance(result, dict):
                    result.setdefault("source", "plugin")
                    result.setdefault("plugin", plugin.name)
                    return result

                return {
                    "success": True,
                    "source": "plugin",
                    "plugin": plugin.name,
                    "result": result,
                }

            except Exception:
                logger.exception(
                    "Plugin '%s' failed while handling request.",
                    plugin.name,
                )

        return self._fallback_to_ai(text)

    # --------------------------------------------------
    # Helpers
    # --------------------------------------------------

    def _find_plugin(self, text: str):
        try:
            return self.plugin_manager.find_handler(text)
        except Exception:
            logger.exception(
                "Plugin lookup failed."
            )
            return None

    def _fallback_to_ai(self, text: str) -> dict[str, Any]:
        """
        Route to the configured AI service.
        """
        if self.ai_service is None:
            return {
                "success": False,
                "source": "router",
                "message": "No plugin matched and no AI service is configured.",
            }

        try:
            response = self.ai_service.generate(text)

            if isinstance(response, dict):
                response.setdefault("source", "ai")
                return response

            return {
                "success": True,
                "source": "ai",
                "message": str(response),
            }

        except Exception:
            logger.exception("AI service failed.")

            return {
                "success": False,
                "source": "ai",
                "message": "AI service failed to generate a response.",
            }

    # --------------------------------------------------
    # Diagnostics
    # --------------------------------------------------

    def capabilities(self) -> dict[str, Any]:
        """
        Return router diagnostics.
        """
        return {
            "plugins": self.plugin_manager.names(),
            "ai_available": self.ai_service is not None,
        }