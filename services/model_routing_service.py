from __future__ import annotations

from services.model_profile_service import (
    ModelProfile,
    model_profile_service,
)


class ModelRoutingService:
    """
    Determines which model should be used for a task.

    This service only makes routing decisions. It does
    not execute prompts or communicate with any backend.
    """

    def __init__(self):

        self._default_model = "phi3"

    # --------------------------------------------------

    def default(self) -> str:

        return self._default_model

    # --------------------------------------------------

    def set_default(
        self,
        model_name: str,
    ) -> bool:

        if model_profile_service.get(model_name) is None:
            return False

        self._default_model = model_name
        return True

    # --------------------------------------------------

    def route(
        self,
        *,
        task: str = "chat",
        requires_vision: bool = False,
        requires_tools: bool = False,
    ) -> ModelProfile | None:

        profiles = model_profile_service.all()

        for profile in profiles:

            if (
                requires_vision
                and not profile.supports_vision
            ):
                continue

            if (
                requires_tools
                and not profile.supports_tools
            ):
                continue

            if profile.name == self._default_model:
                return profile

        return model_profile_service.get(
            self._default_model
        )

    # --------------------------------------------------

    def recommended_model(
        self,
        task: str,
    ) -> str:

        recommendations = {
            "chat": self._default_model,
            "coding": "llama3",
            "reasoning": "llama3",
            "summary": "phi3",
            "translation": "phi3",
        }

        return recommendations.get(
            task,
            self._default_model,
        )


model_routing_service = ModelRoutingService()