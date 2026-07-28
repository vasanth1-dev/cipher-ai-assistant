from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(slots=True)
class BenchmarkResult:
    """
    Stores benchmark information for a model.
    """

    model_name: str
    average_latency_ms: float = 0.0
    average_tokens_per_second: float = 0.0
    prompt_count: int = 0
    total_time_ms: float = 0.0
    updated_at: datetime = field(
        default_factory=datetime.now
    )


class ModelBenchmarkService:
    """
    Maintains runtime benchmark statistics.

    Another component can feed benchmark data into
    this service after each completed request.
    """

    def __init__(
       self,
    ) -> None:

        self._results: dict[
            str,
            BenchmarkResult,
        ] = {}

    # --------------------------------------------------

    def record(
        self,
        model_name: str,
        *,
        latency_ms: float,
        tokens_per_second: float,
    ):

        result = self._results.get(model_name)

        if result is None:

            result = BenchmarkResult(
                model_name=model_name,
            )

            self._results[model_name] = result

        result.prompt_count += 1
        result.total_time_ms += latency_ms

        result.average_latency_ms = (
            result.total_time_ms
            / result.prompt_count
        )

        if result.average_tokens_per_second == 0:

            result.average_tokens_per_second = (
                tokens_per_second
            )

        else:

            count = result.prompt_count

            result.average_tokens_per_second = (
                (
                    result.average_tokens_per_second
                    * (count - 1)
                )
                + tokens_per_second
            ) / count

        result.updated_at = datetime.now()

    # --------------------------------------------------

    def get(
        self,
        model_name: str,
    ) -> BenchmarkResult | None:

        return self._results.get(model_name)

    # --------------------------------------------------

    def all(self):

        return sorted(
            self._results.values(),
            key=lambda item: item.model_name,
        )

    # --------------------------------------------------

    def clear(self):

        self._results.clear()


model_benchmark_service = ModelBenchmarkService()