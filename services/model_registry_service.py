from __future__ import annotations

from pathlib import Path

from services.model_profile_service import (
    ModelProfile,
    model_profile_service,
)


class ModelRegistryService:
    """
    Keeps track of installed and available models.

    This service is independent of Ollama or any
    specific backend. It simply maintains the list
    of models known to Cipher.
    """

    def __init__(
       self,
    ) -> None:

        self._installed: set[str] = set()

    # --------------------------------------------------

    def register_installed(
        self,
        model_name: str,
    ):

        self._installed.add(model_name)

    # --------------------------------------------------

    def unregister(
        self,
        model_name: str,
    ):

        self._installed.discard(model_name)

    # --------------------------------------------------

    def installed(self) -> list[str]:

        return sorted(self._installed)

    # --------------------------------------------------

    def available_profiles(
        self,
    ) -> list[ModelProfile]:

        profiles = []

        for name in self.installed():

            profile = model_profile_service.get(name)

            if profile is not None:
                profiles.append(profile)

        return profiles

    # --------------------------------------------------

    def is_installed(
        self,
        model_name: str,
    ) -> bool:

        return model_name in self._installed

    # --------------------------------------------------

    def clear(self):

        self._installed.clear()


model_registry_service = ModelRegistryService()