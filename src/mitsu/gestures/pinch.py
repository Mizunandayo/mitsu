"""Scale-invariant pinch detection with hysteresis."""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot

from mitsu.perception.one_euro import Point2D


@dataclass(frozen=True, slots=True)
class HandLandmarks:
    """Only landmarks needed by the pinch detector."""

    wrist: Point2D
    thumb_tip: Point2D
    index_tip: Point2D
    middle_mcp: Point2D
    middle_tip: Point2D | None = None
    ring_mcp: Point2D | None = None
    ring_tip: Point2D | None = None
    pinky_mcp: Point2D | None = None
    pinky_tip: Point2D | None = None


@dataclass(frozen=True, slots=True)
class PinchReading:
    """Current pinch decision and its normalized measurement."""

    is_pinched: bool
    ratio: float | None


class PinchDetector:
    """Detect a thumb-index pinch using palm-relative hysteresis."""

    def __init__(
        self,
        engage_ratio: float,
        release_ratio: float,
        release_debounce_frames: int = 4,
    ) -> None:
        if not 0.0 < engage_ratio < release_ratio < 1.0:
            raise ValueError(
                "thresholds must satisfy 0 < engage_ratio < release_ratio < 1"
            )
        if release_debounce_frames < 2:
            raise ValueError("release debounce requires at least two frames")
        self._engage_ratio = engage_ratio
        self._release_ratio = release_ratio
        self._release_debounce_frames = release_debounce_frames
        self._is_pinched = False
        self._release_frames = 0

    def reset(self) -> None:
        """Clear the latched pinch state after hand tracking is lost."""
        self._is_pinched = False
        self._release_frames = 0

    def update(self, landmarks: HandLandmarks | None) -> PinchReading:
        """Update the latch from current landmarks."""

        if landmarks is None:
            self.reset()
            return PinchReading(is_pinched=False, ratio=None)

        palm_span = self._distance(landmarks.wrist, landmarks.middle_mcp)
        if palm_span <= 1e-6:
            self.reset()
            return PinchReading(is_pinched=False, ratio=None)

        tip_distance = self._distance(landmarks.thumb_tip, landmarks.index_tip)
        ratio = tip_distance / palm_span

        if self._is_pinched:
            if ratio < self._release_ratio:
                self._release_frames = 0
            else:
                self._release_frames += 1
                self._is_pinched = self._release_frames < self._release_debounce_frames
        else:
            self._is_pinched = ratio <= self._engage_ratio
            self._release_frames = 0

        return PinchReading(is_pinched=self._is_pinched, ratio=ratio)

    @staticmethod
    def _distance(first: Point2D, second: Point2D) -> float:
        return hypot(first.x - second.x, first.y - second.y)
