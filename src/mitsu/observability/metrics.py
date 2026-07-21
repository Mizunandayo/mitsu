from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from math import sqrt


@dataclass(frozen=True)
class MetricSummary:
    count: int
    p50: float
    p95: float
    minimum: float
    maximum: float


class RollingMetric:
    def __init__(self, maximum_samples: int) -> None:
        if maximum_samples < 1:
            raise ValueError("maximum_samples must be positive.")

        self._samples: deque[float] = deque(maxlen=maximum_samples)

    def record(self, value: float) -> None:
        if value < 0.0:
            raise ValueError("Metric values cannot be negative.")
        self._samples.append(value)

    def summary(self) -> MetricSummary | None:
        if not self._samples:
            return None

        ordered = sorted(self._samples)
        return MetricSummary(
            count=len(ordered),
            p50=self._percentile(ordered, 0.50),
            p95=self._percentile(ordered, 0.95),
            minimum=ordered[0],
            maximum=ordered[-1],
        )

    @staticmethod
    def _percentile(values: list[float], percentile: float) -> float:
        index = (len(values) - 1) * percentile
        lower = int(index)
        upper = min(lower + 1, len(values) - 1)
        fraction = index - lower
        return values[lower] + (values[upper] - values[lower]) * fraction


class JitterMeter:
    """Measures point dispersion; lower standard deviation means less jitter."""

    def __init__(self, maximum_samples: int) -> None:
        if maximum_samples < 1:
            raise ValueError("maximum_samples must be positive.")

        self._raw_points: deque[tuple[float, float]] = deque(maxlen=maximum_samples)
        self._filtered_points: deque[tuple[float, float]] = deque(
            maxlen=maximum_samples
        )

    def record(
        self,
        *,
        raw_x: float,
        raw_y: float,
        filtered_x: float,
        filtered_y: float,
    ) -> None:
        self._raw_points.append((raw_x, raw_y))
        self._filtered_points.append((filtered_x, filtered_y))

    def raw_standard_deviation(self) -> float | None:
        return self._spatial_standard_deviation(self._raw_points)

    def filtered_standard_deviation(self) -> float | None:
        return self._spatial_standard_deviation(self._filtered_points)

    @staticmethod
    def _spatial_standard_deviation(
        points: deque[tuple[float, float]],
    ) -> float | None:
        if len(points) < 2:
            return None

        mean_x = sum(point[0] for point in points) / len(points)
        mean_y = sum(point[1] for point in points) / len(points)
        mean_squared_distance = sum(
            (point[0] - mean_x) ** 2 + (point[1] - mean_y) ** 2 for point in points
        ) / len(points)
        return sqrt(mean_squared_distance)
