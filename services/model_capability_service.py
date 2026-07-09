from __future__ import annotations

from services.model_profile_service import (
    ModelProfile,
    model_profile_service,
)


class ModelCapabilityService:
    """
    Helper service for querying model capabilities.

    This keeps capability checks centralized instead
    of scattering them throughout the application.
    """

    # --------------------------------------------------

    def profile(
        self,
        model_name: str,
    ) -> ModelProfile | None:

        return model_profile_service.get(model_name)

    # --------------------------------------------------

    def supports_streaming(
        self,
        model_name: str,
    ) -> bool:

        profile = self.profile(model_name)

        return (
            profile.supports_streaming
            if profile
            else False
        )

    # --------------------------------------------------

    def supports_tools(
        self,
        model_name: str,
    ) -> bool:

        profile = self.profile(model_name)

        return (
            profile.supports_tools
            if profile
            else False
        )

    # --------------------------------------------------

    def supports_vision(
        self,
        model_name: str,
    ) -> bool:

        profile = self.profile(model_name)

        return (
            profile.supports_vision
            if profile
            else False
        )

    # --------------------------------------------------

    def context_window(
        self,
        model_name: str,
    ) -> int:

        profile = self.profile(model_name)

        if profile is None:
            return 0

        return profile.context_window

    # --------------------------------------------------

    def max_output_tokens(
        self,
        model_name: str,
    ) -> int:

        profile = self.profile(model_name)

        if profile is None:
            return 0

        return profile.max_output_tokens


model_capability_service = ModelCapabilityService()