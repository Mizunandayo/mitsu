"""Open-palm fold recognition for explicit foreground-window minimization."""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot

from mitsu.perception.one_euro import Point2D

_WRIST = 0
_INDEX_TIP = 8
_MIDDLE_MCP = 9
_MIDDLE_TIP = 12
_RING_TIP = 16
_PINKY_TIP = 20


@dataclass(frozen=True, slots=True)
class PalmSwipeReading:
    """Whether a hand is open and whether it completed a minimize swipe."""

    is_open_palm: bool
    minimize_triggered: bool


class PalmSwipeDetector:
    """Recognize a wrist-down palm fold, never whole-hand translation."""

    def __init__(
        self,
        *,
        open_palm_extension_ratio: float,
        minimum_open_palm_frames: int,
        minimum_downward_distance_ratio: float,
        downward_velocity_ratio_per_second: float,
    ) -> None:
        if open_palm_extension_ratio <= 1.0:
            raise ValueError("open palm extension ratio must exceed one")
        if minimum_open_palm_frames < 2:
            raise ValueError("open palm stability requires at least two frames")
        if minimum_downward_distance_ratio <= 0.0:
            raise ValueError("minimum downward distance must be positive")
        if downward_velocity_ratio_per_second <= 0.0:
            raise ValueError("downward velocity threshold must be positive")

        self._open_palm_extension_ratio = open_palm_extension_ratio
        self._minimum_open_palm_frames = minimum_open_palm_frames
        self._minimum_downward_distance_ratio = minimum_downward_distance_ratio
        self._downward_velocity_ratio_per_second = downward_velocity_ratio_per_second
        self.reset()

    def reset(self) -> None:
        """Clear gesture history after tracking loss or another interaction."""

        self._previous_fold_ratio: float | None = None
        self._previous_timestamp_seconds: float | None = None
        self._open_palm_frames = 0
        self._downward_distance_ratio = 0.0
        self._minimize_armed = True

    def update(
        self,
        points: tuple[Point2D, ...] | None,
        timestamp_seconds: float,
    ) -> PalmSwipeReading:
        """Return one minimize edge for a deliberate palm swipe."""

        if points is None or len(points) <= _PINKY_TIP:
            self.reset()
            return PalmSwipeReading(
                is_open_palm=False,
                minimize_triggered=False,
            )

        wrist = points[_WRIST]
        middle_mcp = points[_MIDDLE_MCP]
        palm_span = self._distance(wrist, middle_mcp)
        if palm_span <= 1e-6:
            self.reset()
            return PalmSwipeReading(
                is_open_palm=False,
                minimize_triggered=False,
            )

        is_open_palm = self.is_open_palm(points)
        if not is_open_palm:
            self.reset()
            return PalmSwipeReading(
                is_open_palm=False,
                minimize_triggered=False,
            )

        fold_ratio = self._fold_ratio(points)
        self._open_palm_frames += 1
        if self._open_palm_frames < self._minimum_open_palm_frames:
            # Establish a stable open-palm baseline before accepting a wrist
            # fold. Translation moves wrist and fingertips together, so it
            # cannot alter this relative measurement.
            self._previous_fold_ratio = fold_ratio
            self._previous_timestamp_seconds = timestamp_seconds
            return PalmSwipeReading(
                is_open_palm=True,
                minimize_triggered=False,
            )

        fold_velocity, fold_delta_ratio = self._fold_motion(
            fold_ratio,
            timestamp_seconds,
        )
        self._previous_fold_ratio = fold_ratio
        self._previous_timestamp_seconds = timestamp_seconds

        if fold_delta_ratio > 0.0:
            self._downward_distance_ratio += fold_delta_ratio
        elif fold_delta_ratio < 0.0:
            self._downward_distance_ratio = 0.0

        minimize_triggered = (
            self._minimize_armed
            and self._downward_distance_ratio >= self._minimum_downward_distance_ratio
            and fold_velocity >= self._downward_velocity_ratio_per_second
        )
        if minimize_triggered:
            self._minimize_armed = False

        return PalmSwipeReading(
            is_open_palm=True,
            minimize_triggered=minimize_triggered,
        )

    def is_open_palm(
        self,
        points: tuple[Point2D, ...] | None,
        *,
        minimum_extension_ratio: float | None = None,
    ) -> bool:
        """Return whether all four fingertips are extended from the palm."""

        if points is None or len(points) <= _PINKY_TIP:
            return False

        wrist = points[_WRIST]
        palm_span = self._distance(wrist, points[_MIDDLE_MCP])
        if palm_span <= 1e-6:
            return False

        extension_ratio = (
            self._open_palm_extension_ratio
            if minimum_extension_ratio is None
            else minimum_extension_ratio
        )
        return all(
            self._distance(points[tip_index], wrist) / palm_span >= extension_ratio
            for tip_index in (_INDEX_TIP, _MIDDLE_TIP, _RING_TIP, _PINKY_TIP)
        )

    def _fold_motion(
        self,
        fold_ratio: float,
        timestamp_seconds: float,
    ) -> tuple[float, float]:
        if (
            self._previous_fold_ratio is None
            or self._previous_timestamp_seconds is None
        ):
            return (0.0, 0.0)

        elapsed = timestamp_seconds - self._previous_timestamp_seconds
        if elapsed <= 0.0:
            self.reset()
            return (0.0, 0.0)

        fold_delta_ratio = fold_ratio - self._previous_fold_ratio
        return (fold_delta_ratio / elapsed, fold_delta_ratio)

    @staticmethod
    def _fold_ratio(points: tuple[Point2D, ...]) -> float:
        wrist = points[_WRIST]
        average_tip_y = (
            sum(
                points[tip_index].y
                for tip_index in (_INDEX_TIP, _MIDDLE_TIP, _RING_TIP, _PINKY_TIP)
            )
            / 4.0
        )
        return wrist.y - average_tip_y

    @staticmethod
    def _distance(first: Point2D, second: Point2D) -> float:
        return hypot(first.x - second.x, first.y - second.y)
