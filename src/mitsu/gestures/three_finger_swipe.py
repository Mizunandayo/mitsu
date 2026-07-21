"""Three-finger downstroke recognition for explicit window minimization."""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot

from mitsu.perception.one_euro import Point2D

_WRIST = 0
_THUMB_TIP = 4
_INDEX_TIP = 8
_MIDDLE_MCP = 9
_MIDDLE_TIP = 12
_RING_TIP = 16
_PINKY_TIP = 20
_TRIAD_TIPS = (_INDEX_TIP, _MIDDLE_TIP, _RING_TIP)


@dataclass(frozen=True, slots=True)
class ThreeFingerSwipeReading:
    """The raw three-finger pose and one-shot minimize action."""

    is_three_finger_pose: bool
    minimize_triggered: bool


class ThreeFingerMinimizeDetector:
    """Require a stable index-middle-ring cluster and deliberate downstroke."""

    def __init__(
        self,
        *,
        triad_close_ratio: float,
        triad_extension_ratio: float,
        folded_pinky_extension_ratio: float,
        minimum_thumb_index_ratio: float,
        minimum_pose_frames: int,
        minimum_downward_distance_ratio: float,
        downward_velocity_ratio_per_second: float,
    ) -> None:
        if triad_close_ratio <= 0.0:
            raise ValueError("triad close ratio must be positive")
        if triad_extension_ratio <= 1.0:
            raise ValueError("triad extension ratio must exceed one")
        if folded_pinky_extension_ratio <= 0.0:
            raise ValueError("folded pinky ratio must be positive")
        if minimum_thumb_index_ratio <= 0.0:
            raise ValueError("thumb-index separation must be positive")
        if minimum_pose_frames < 2:
            raise ValueError("three-finger pose requires at least two frames")
        if minimum_downward_distance_ratio <= 0.0:
            raise ValueError("downward distance must be positive")
        if downward_velocity_ratio_per_second <= 0.0:
            raise ValueError("downward velocity must be positive")

        self._triad_close_ratio = triad_close_ratio
        self._triad_extension_ratio = triad_extension_ratio
        self._folded_pinky_extension_ratio = folded_pinky_extension_ratio
        self._minimum_thumb_index_ratio = minimum_thumb_index_ratio
        self._minimum_pose_frames = minimum_pose_frames
        self._minimum_downward_distance_ratio = minimum_downward_distance_ratio
        self._downward_velocity_ratio_per_second = downward_velocity_ratio_per_second
        self.reset()

    def reset(self) -> None:
        """Clear pose and motion history."""

        self._pose_frames = 0
        self._previous_centroid: Point2D | None = None
        self._previous_timestamp_seconds: float | None = None
        self._downward_distance_ratio = 0.0
        self._armed = True

    def update(
        self,
        points: tuple[Point2D, ...] | None,
        timestamp_seconds: float,
    ) -> ThreeFingerSwipeReading:
        """Return an action only for the configured three-finger downstroke."""

        if points is None or len(points) <= _PINKY_TIP:
            self.reset()
            return ThreeFingerSwipeReading(False, False)

        wrist = points[_WRIST]
        palm_span = self._distance(wrist, points[_MIDDLE_MCP])
        if palm_span <= 1e-6 or not self._is_pose(points, palm_span):
            self.reset()
            return ThreeFingerSwipeReading(False, False)

        centroid = Point2D(
            sum(points[index].x for index in _TRIAD_TIPS) / len(_TRIAD_TIPS),
            sum(points[index].y for index in _TRIAD_TIPS) / len(_TRIAD_TIPS),
        )
        self._pose_frames += 1
        if self._pose_frames < self._minimum_pose_frames:
            self._previous_centroid = centroid
            self._previous_timestamp_seconds = timestamp_seconds
            return ThreeFingerSwipeReading(True, False)

        velocity, delta_ratio = self._downstroke(centroid, timestamp_seconds, palm_span)
        self._previous_centroid = centroid
        self._previous_timestamp_seconds = timestamp_seconds
        self._downward_distance_ratio = (
            self._downward_distance_ratio + delta_ratio if delta_ratio > 0.0 else 0.0
        )
        minimize_triggered = (
            self._armed
            and self._downward_distance_ratio >= self._minimum_downward_distance_ratio
            and velocity >= self._downward_velocity_ratio_per_second
        )
        if minimize_triggered:
            self._armed = False

        return ThreeFingerSwipeReading(True, minimize_triggered)

    def _is_pose(self, points: tuple[Point2D, ...], palm_span: float) -> bool:
        triad = tuple(points[index] for index in _TRIAD_TIPS)
        triad_extended = all(
            self._distance(point, points[_WRIST]) / palm_span
            >= self._triad_extension_ratio
            for point in triad
        )
        widest_gap = max(
            self._distance(first, second) / palm_span
            for first, second in (
                (triad[0], triad[1]),
                (triad[1], triad[2]),
                (triad[0], triad[2]),
            )
        )
        pinky_folded = (
            self._distance(points[_PINKY_TIP], points[_WRIST]) / palm_span
            <= self._folded_pinky_extension_ratio
        )
        thumb_away = (
            self._distance(points[_THUMB_TIP], points[_INDEX_TIP]) / palm_span
            >= self._minimum_thumb_index_ratio
        )
        return (
            triad_extended
            and widest_gap <= self._triad_close_ratio
            and pinky_folded
            and thumb_away
        )

    def _downstroke(
        self,
        centroid: Point2D,
        timestamp_seconds: float,
        palm_span: float,
    ) -> tuple[float, float]:
        if self._previous_centroid is None or self._previous_timestamp_seconds is None:
            return (0.0, 0.0)

        elapsed = timestamp_seconds - self._previous_timestamp_seconds
        if elapsed <= 0.0:
            self.reset()
            return (0.0, 0.0)

        delta_ratio = (centroid.y - self._previous_centroid.y) / palm_span
        return (delta_ratio / elapsed, delta_ratio)

    @staticmethod
    def _distance(first: Point2D, second: Point2D) -> float:
        return hypot(first.x - second.x, first.y - second.y)
