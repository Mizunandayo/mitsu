"""Pure relative-delta coordinate mapping for window movement."""

from __future__ import annotations
from dataclasses import dataclass
from mitsu.perception.one_euro import Point2D



@dataclass(frozen=True, slots=True)
class ScreenBounds:
    """Inclusive top-left and exclusive bottom-right screen bounds."""

    left: int
    top: int
    right: int
    bottom: int

    
    def __post_init__(self) -> None:
        if self.right <= self.left:
            raise ValueError("right must exceed left")
        if self.bottom <= self.top:
            raise ValueError("bottom must exceed top")


    @property
    def width(self) -> int:
        return self.right - self.left
    
    @property
    def height(self) -> int:
        return self.bottom - self.top
    


@dataclass(frozen=True, slots=True)
class WindowPosition:
    """The physical-pixel top-left position of a window."""

    x: int
    y: int


class RelativeCoordinateMapper:
    """Map normalized camera deltas to clamped physical-pixel window deltas."""

    def __init__(
        self,
        movement_gain: float,
        minimum_delta_pixels: float,
        bounds: ScreenBounds,
    ) -> None:
        if movement_gain <= 0.0:
            raise ValueError("movement_gain must be positive")
        if minimum_delta_pixels < 0.0:
            raise ValueError("minimum_delta_pixels must not be negative")

        self._movement_gain = movement_gain
        self._minimum_delta_pixels = minimum_delta_pixels
        self._bounds = bounds
        self._previous_hand: Point2D | None = None

    def reset(self) -> None:
        """Forget the prior hand point at the end of a drag."""

        self._previous_hand = None

    def begin(self, hand_position: Point2D) -> None:
        """Anchor movement without changing the current window position."""

        self._previous_hand = hand_position

    def move(
        self,
        hand_position: Point2D,
        current_position: WindowPosition,
        window_width: int,
        window_height: int,
    ) -> WindowPosition:
        """Return a new clamped top-left position from relative hand motion."""

        if window_width <= 0 or window_height <= 0:
            raise ValueError("window dimensions must be positive")

        if self._previous_hand is None:
            self.begin(hand_position)
            return current_position

        hand_delta = hand_position - self._previous_hand
        self._previous_hand = hand_position

        delta_x = hand_delta.x * self._movement_gain
        delta_y = hand_delta.y * self._movement_gain

        if abs(delta_x) < self._minimum_delta_pixels:
            delta_x = 0.0
        if abs(delta_y) < self._minimum_delta_pixels:
            delta_y = 0.0

        proposed_x = round(current_position.x + delta_x)
        proposed_y = round(current_position.y + delta_y)

        maximum_x = max(self._bounds.left, self._bounds.right - window_width)
        maximum_y = max(self._bounds.top, self._bounds.bottom - window_height)

        return WindowPosition(
            x=min(max(proposed_x, self._bounds.left), maximum_x),
            y=min(max(proposed_y, self._bounds.top), maximum_y),
        )