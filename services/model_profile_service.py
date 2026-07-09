from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ModelProfile:
    """
    Describes an AI model's capabilities.
    """

    name: str
    display_name: str
    context_window: int
    supports_streaming: bool
    supports_tools: bool
    supports_vision: bool
    max_output_tokens: int


class ModelProfileService:
    """
    Registry of available AI models.

    This service is read-only. It allows the rest of
    Cipher to query model capabilities without
    hardcoding them throughout the application.
    """

    def __init__(self):

        self._profiles: dict[str, ModelProfile] = {}

    # --------------------------------------------------

    def register(
        self,
        profile: ModelProfile,
    ):

        self._profiles[profile.name] = profile

    # --------------------------------------------------

    def get(
        self,
        name: str,
    ) -> ModelProfile | None:

        return self._profiles.get(name)

    # --------------------------------------------------

    def names(self):

        return sorted(self._profiles.keys())

    # --------------------------------------------------

    def all(self):

        return list(self._profiles.values())

    # --------------------------------------------------

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._profiles


model_profile_service = ModelProfileService()

# Default profiles

model_profile_service.register(
    ModelProfile(
        name="phi3",
        display_name="Phi-3",
        context_window=4096,
        supports_streaming=True,
        supports_tools=False,
        supports_vision=False,
        max_output_tokens=2048,
    )
)

model_profile_service.register(
    ModelProfile(
        name="llama3",
        display_name="Llama 3",
        context_window=8192,
        supports_streaming=True,
        supports_tools=False,
        supports_vision=False,
        max_output_tokens=4096,
    )
)