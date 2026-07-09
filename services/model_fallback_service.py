from __future__ import annotations

from services.model_health_service import (
    model_health_service,
)
from services.model_profile_service import (
    model_profile_service,
)
from services.model_routing_service import (
    model_routing_service,
)


class ModelFallbackService:
    """
    Determines the best fallback model when the preferred
    model is unavailable.

    This service makes routing decisions only.
    It does not communicate with any AI backend.
    """

    # --------------------------------------------------

    def primary(self):

        profile = model_routing_service.route()

        if profile is None:
            return None

        return profile.name

    # --------------------------------------------------

    def fallback(self):

        primary = self.primary()

        available = set(
            model_health_service.available_models()
        )

        if primary in available:
            return primary

        for name in model_profile_service.names():

            if name in available:
                return name

        return primary

    # --------------------------------------------------

    def can_fallback(self) -> bool:

        primary = self.primary()

        if primary is None:
            return False

        return self.fallback() != primary

    # --------------------------------------------------

    def all_candidates(self):

        available = set(
            model_health_service.available_models()
        )

        return [
            name
            for name in model_profile_service.names()
            if name in available
        ]


model_fallback_service = ModelFallbackService()