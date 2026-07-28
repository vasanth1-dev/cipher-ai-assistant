from __future__ import annotations

from services.model_profile_service import (
    ModelProfile,
    model_profile_service,
)


class ModelSelectionService:
    """
    Tracks the currently selected AI model.

    This service does not load or execute models.
    It only manages which model Cipher should use.
    """

    def __init__(
       self,
    ) -> None:

        self._current_model = None

    # --------------------------------------------------

    def select(
        self,
        model_name: str,
    ) -> bool:

        profile = model_profile_service.get(model_name)

        if profile is None:
            return False

        self._current_model = model_name

        return True

    # --------------------------------------------------

    def current(self) -> str | None:

        return self._current_model

    # --------------------------------------------------

    def current_profile(self) -> ModelProfile | None:

        if self._current_model is None:
            return None

        return model_profile_service.get(
            self._current_model
        )

    # --------------------------------------------------

    def is_selected(
        self,
        model_name: str,
    ) -> bool:

        return self._current_model == model_name

    # --------------------------------------------------

    def clear(self):

        self._current_model = None


model_selection_service = ModelSelectionService()