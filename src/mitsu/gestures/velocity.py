"""Velocity measurement and gain scaling for relative hand movement."""

from __future__ import annotations

from dataclasses import dataclass

from mitsu.perception.one_euro import Point2D


@dataclass(frozen=True, slots=True)
class HandVelocity:
    """A normalized hand velocity in camera-coordinate units per second."""

    x: float
    y: float

    @property
    def magnitude(self) -> float:
        """Return Euclidean speed."""

        return (self.x**2 + self.y**2) ** 0.5


class HandVelocityTracker:
    """Smooth frame-to-frame hand velocity using an exponential low-pass filter."""

    def __init__(self, smoothing_alpha: float) -> None:
        if not 0.0 < smoothing_alpha <= 1.0:
            raise ValueError("smoothing_alpha must be in the interval (0, 1]")

        self._smoothing_alpha = smoothing_alpha
        self.reset()

    def reset(self) -> None:
        """Discard history after a grip ends or hand tracking is lost."""

        self._previous_position: Point2D | None = None
        self._previous_timestamp: float | None = None
        self._smoothed_velocity = HandVelocity(0.0, 0.0)

    def update(
        self,
        position: Point2D,
        timestamp_seconds: float,
    ) -> HandVelocity:
        """Return smoothed velocity for the supplied hand observation."""

        if self._previous_position is None or self._previous_timestamp is None:
            self._previous_position = position
            self._previous_timestamp = timestamp_seconds
            return self._smoothed_velocity

        elapsed = timestamp_seconds - self._previous_timestamp
        if elapsed <= 0.0:
            raise ValueError("timestamps must be strictly increasing")

        raw_velocity = HandVelocity(
            x=(position.x - self._previous_position.x) / elapsed,
            y=(position.y - self._previous_position.y) / elapsed,
        )

        alpha = self._smoothing_alpha
        self._smoothed_velocity = HandVelocity(
            x=alpha * raw_velocity.x + (1.0 - alpha) * self._smoothed_velocity.x,
            y=alpha * raw_velocity.y + (1.0 - alpha) * self._smoothed_velocity.y,
        )

        self._previous_position = position
        self._previous_timestamp = timestamp_seconds
        return self._smoothed_velocity


class VelocityGain:
    """Convert sustained hand speed into a bounded movement gain multiplier."""

    def __init__(
        self,
        activation_speed: float,
        maximum_gain_multiplier: float,
    ) -> None:
        if activation_speed <= 0.0:
            raise ValueError("activation_speed must be positive")
        if maximum_gain_multiplier < 1.0:
            raise ValueError("maximum_gain_multiplier must be at least 1.0")

        self._activation_speed = activation_speed
        self._maximum_gain_multiplier = maximum_gain_multiplier

    def multiplier_for(self, velocity: HandVelocity) -> float:
        """Return a bounded gain multiplier for the current velocity."""

        speed = velocity.magnitude
        if speed <= self._activation_speed:
            return 1.0

        normalized_excess = min(
            (speed - self._activation_speed) / self._activation_speed,
            1.0,
        )
        return 1.0 + normalized_excess * (self._maximum_gain_multiplier - 1.0)
