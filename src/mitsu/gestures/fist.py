"""Closed-fist detection for an intentional whole-hand window grip."""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot

from mitsu.perception.one_euro import Point2D

_WRIST = 0
_MIDDLE_MCP = 9
_TIP_INDICES = (4, 8, 12, 16, 20)


@dataclass(frozen=True, slots=True)
class FistReading:
    """The hysteresis-stabilized whole-hand grip state."""

    is_fist: bool


class FistGripDetector:
    """Detect a closed fist without confusing it with a two-finger click pose."""

    def __init__(
        self,
        *,
        engage_tip_distance_ratio: float,
        release_tip_distance_ratio: float,
        release_debounce_frames: int,
    ) -> None:
        if not 0.0 < engage_tip_distance_ratio < release_tip_distance_ratio:
            raise ValueError("fist thresholds must satisfy 0 < engage < release")
        if release_debounce_frames < 2:
            raise ValueError("fist release debounce requires at least two frames")

        self._engage_tip_distance_ratio = engage_tip_distance_ratio
        self._release_tip_distance_ratio = release_tip_distance_ratio
        self._release_debounce_frames = release_debounce_frames
        self.reset()

    def reset(self) -> None:
        """Clear grip state after tracking loss or a higher-priority palm pose."""

        self._is_fist = False
        self._release_frames = 0

    def update(self, points: tuple[Point2D, ...] | None) -> FistReading:
        """Return a stable fist state from all five fingertip distances."""

        if points is None or len(points) <= max(_TIP_INDICES):
            self.reset()
            return FistReading(is_fist=False)

        wrist = points[_WRIST]
        palm_span = self._distance(wrist, points[_MIDDLE_MCP])
        if palm_span <= 1e-6:
            self.reset()
            return FistReading(is_fist=False)

        largest_tip_ratio = max(
            self._distance(points[tip_index], wrist) / palm_span
            for tip_index in _TIP_INDICES
        )
        if self._is_fist:
            if largest_tip_ratio <= self._release_tip_distance_ratio:
                self._release_frames = 0
            else:
                self._release_frames += 1
                if self._release_frames >= self._release_debounce_frames:
                    self._is_fist = False
                    self._release_frames = 0
        else:
            self._is_fist = largest_tip_ratio <= self._engage_tip_distance_ratio

        return FistReading(is_fist=self._is_fist)

    @staticmethod
    def _distance(first: Point2D, second: Point2D) -> float:
        return hypot(first.x - second.x, first.y - second.y)
