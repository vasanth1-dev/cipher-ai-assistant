from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class ModelHealth:
    """
    Runtime health information for an AI model.
    """

    name: str
    available: bool = False
    status: str = "Unknown"
    latency_ms: float = 0.0
    last_checked: datetime | None = None
    last_error: str = ""


class ModelHealthService:
    """
    Maintains runtime health information for models.

    This service does not communicate with Ollama or any
    other backend. It only stores health information that
    another component can update.
    """

    def __init__(self):

        self._health: dict[str, ModelHealth] = {}

    # --------------------------------------------------

    def register(
        self,
        model_name: str,
    ):

        self._health.setdefault(
            model_name,
            ModelHealth(name=model_name),
        )

    # --------------------------------------------------

    def update(
        self,
        model_name: str,
        *,
        available: bool,
        status: str,
        latency_ms: float = 0.0,
        last_error: str = "",
    ):

        self.register(model_name)

        health = self._health[model_name]

        health.available = available
        health.status = status
        health.latency_ms = latency_ms
        health.last_error = last_error
        health.last_checked = datetime.now()

    # --------------------------------------------------

    def get(
        self,
        model_name: str,
    ) -> ModelHealth | None:

        return self._health.get(model_name)

    # --------------------------------------------------

    def all(self) -> list[ModelHealth]:

        return sorted(
            self._health.values(),
            key=lambda item: item.name,
        )

    # --------------------------------------------------

    def available_models(self) -> list[str]:

        return sorted(
            health.name
            for health in self._health.values()
            if health.available
        )

    # --------------------------------------------------

    def clear(self):

        self._health.clear()


model_health_service = ModelHealthService()