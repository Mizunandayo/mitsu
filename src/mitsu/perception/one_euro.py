"""Speed-adaptive smoothing for normalized hand coordinates."""

from __future__ import annotations
from dataclasses import dataclass
from math import pi







@dataclass(frozen=True, slots=True)
class Point2D:
    """A two-dimensional point in normalized camera coordinates."""

    x: float
    y: float

    def __add__(self, other: Point2D) -> Point2D:
        return Point2D(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Point2D) -> Point2D:
        return Point2D(self.x - other.x, self.y - other.y)

    def scale(self, scalar: float) -> Point2D:
        return Point2D(self.x * scalar, self.y * scalar)

    def magnitude(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5


class OneEuroFilter:
    """One Euro Filter for a 2D point stream.

    Timestamps must be strictly increasing monotonic seconds. The filter is
    intentionally dependency-free, deterministic, and independently testable.
    """

    def __init__(
        self,
        minimum_cutoff_hz: float,
        beta: float,
        derivative_cutoff_hz: float,
    ) -> None:
        if minimum_cutoff_hz <= 0.0:
            raise ValueError("minimum_cutoff_hz must be positive")
        if beta < 0.0:
            raise ValueError("beta must not be negative")
        if derivative_cutoff_hz <= 0.0:
            raise ValueError("derivative_cutoff_hz must be positive")

        self._minimum_cutoff_hz = minimum_cutoff_hz
        self._beta = beta
        self._derivative_cutoff_hz = derivative_cutoff_hz
        self.reset()

    def reset(self) -> None:
        """Discard history, for example after tracking loss."""

        self._previous_timestamp: float | None = None
        self._previous_raw: Point2D | None = None
        self._previous_filtered: Point2D | None = None
        self._filtered_derivative = Point2D(0.0, 0.0)

    def filter(self, point: Point2D, timestamp_seconds: float) -> Point2D:
        """Return a speed-adaptively smoothed point."""

        if self._previous_timestamp is None:
            self._previous_timestamp = timestamp_seconds
            self._previous_raw = point
            self._previous_filtered = point
            return point

        elapsed = timestamp_seconds - self._previous_timestamp
        if elapsed <= 0.0:
            raise ValueError("timestamps must be strictly increasing")

        assert self._previous_raw is not None
        assert self._previous_filtered is not None

        raw_derivative = (point - self._previous_raw).scale(1.0 / elapsed)
        derivative_alpha = self._alpha(self._derivative_cutoff_hz, elapsed)
        self._filtered_derivative = self._low_pass(
            raw_derivative,
            self._filtered_derivative,
            derivative_alpha,
        )

        dynamic_cutoff = (
            self._minimum_cutoff_hz
            + self._beta * self._filtered_derivative.magnitude()
        )
        position_alpha = self._alpha(dynamic_cutoff, elapsed)
        filtered = self._low_pass(point, self._previous_filtered, position_alpha)

        self._previous_timestamp = timestamp_seconds
        self._previous_raw = point
        self._previous_filtered = filtered
        return filtered

    @staticmethod
    def _alpha(cutoff_hz: float, elapsed_seconds: float) -> float:
        time_constant = 1.0 / (2.0 * pi * cutoff_hz)
        return 1.0 / (1.0 + time_constant / elapsed_seconds)

    @staticmethod
    def _low_pass(
        current: Point2D,
        previous: Point2D,
        alpha: float,
    ) -> Point2D:
        return current.scale(alpha) + previous.scale(1.0 - alpha)