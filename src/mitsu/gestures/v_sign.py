"""Stable V-sign recognition for opening the minimized-window shelf."""

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
class VSignReading:
    """The current pose and its one-shot shelf-open edge."""

    is_v_sign: bool
    activated: bool


class VSignDetector:
    """Recognize an intentional V sign without colliding with click poses."""

    def __init__(
        self,
        *,
        extension_ratio: float,
        folded_finger_ratio: float,
        minimum_finger_gap_ratio: float,
        minimum_hold_frames: int,
    ) -> None:
        if extension_ratio <= 1.0:
            raise ValueError("V-sign extension ratio must exceed one")
        if folded_finger_ratio <= 0.0:
            raise ValueError("folded finger ratio must be positive")
        if minimum_finger_gap_ratio <= 0.0:
            raise ValueError("V-sign finger gap must be positive")
        if minimum_hold_frames < 2:
            raise ValueError("V-sign hold requires at least two frames")

        self._extension_ratio = extension_ratio
        self._folded_finger_ratio = folded_finger_ratio
        self._minimum_finger_gap_ratio = minimum_finger_gap_ratio
        self._minimum_hold_frames = minimum_hold_frames
        self.reset()

    def reset(self) -> None:
        """Clear pose history after tracking loss or an interaction change."""

        self._frames = 0
        self._latched = False

    def update(self, points: tuple[Point2D, ...] | None) -> VSignReading:
        """Return a shelf-open edge after a stable V-sign hold."""

        if points is None or len(points) <= _PINKY_TIP:
            self.reset()
            return VSignReading(False, False)

        wrist = points[_WRIST]
        palm_span = self._distance(wrist, points[_MIDDLE_MCP])
        if palm_span <= 1e-6:
            self.reset()
            return VSignReading(False, False)

        index_extended = (
            self._distance(points[_INDEX_TIP], wrist) / palm_span
            >= self._extension_ratio
        )
        middle_extended = (
            self._distance(points[_MIDDLE_TIP], wrist) / palm_span
            >= self._extension_ratio
        )
        ring_folded = (
            self._distance(points[_RING_TIP], wrist) / palm_span
            <= self._folded_finger_ratio
        )
        pinky_folded = (
            self._distance(points[_PINKY_TIP], wrist) / palm_span
            <= self._folded_finger_ratio
        )
        fingers_separated = (
            self._distance(points[_INDEX_TIP], points[_MIDDLE_TIP]) / palm_span
            >= self._minimum_finger_gap_ratio
        )
        is_v_sign = (
            index_extended
            and middle_extended
            and ring_folded
            and pinky_folded
            and fingers_separated
        )
        if not is_v_sign:
            self.reset()
            return VSignReading(False, False)

        self._frames += 1
        activated = not self._latched and self._frames >= self._minimum_hold_frames
        if activated:
            self._latched = True

        return VSignReading(True, activated)

    @staticmethod
    def _distance(first: Point2D, second: Point2D) -> float:
        return hypot(first.x - second.x, first.y - second.y)
