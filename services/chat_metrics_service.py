from __future__ import annotations

from collections import defaultdict
from datetime import datetime


class ChatMetricsService:
    """
    Collects lightweight runtime metrics for Cipher.

    These metrics are intended for diagnostics,
    dashboards, and performance monitoring.
    """

    def __init__(self):

        self.reset()

    # --------------------------------------------------

    def increment(
        self,
        metric: str,
        amount: int = 1,
    ):

        self._counters[metric] += amount

    # --------------------------------------------------

    def set(
        self,
        metric: str,
        value,
    ):

        self._values[metric] = value

    # --------------------------------------------------

    def get(
        self,
        metric: str,
        default=None,
    ):

        if metric in self._values:
            return self._values[metric]

        return self._counters.get(
            metric,
            default,
        )

    # --------------------------------------------------

    def counters(self):

        return dict(self._counters)

    # --------------------------------------------------

    def values(self):

        return dict(self._values)

    # --------------------------------------------------

    def snapshot(self):

        return {
            "timestamp": datetime.now().isoformat(),
            "counters": self.counters(),
            "values": self.values(),
        }

    # --------------------------------------------------

    def reset(self):

        self._counters = defaultdict(int)

        self._values = {}


chat_metrics_service = ChatMetricsService()