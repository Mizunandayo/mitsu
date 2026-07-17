"""Stateful composition of Day-2 virtual-desktop drag movement."""

from __future__ import annotations

from dataclasses import dataclass

from mitsu.config import Settings
from mitsu.control.coordinate_mapper import RelativeCoordinateMapper, WindowPosition
from mitsu.control.monitor_layout import MonitorLayout, discover_monitor_layout
from mitsu.gestures.velocity import HandVelocityTracker, VelocityGain
from mitsu.perception.one_euro import Point2D


@dataclass(frozen=True, slots=True)
class GripSession:
    """The immutable window dimensions and mutable-in-practice drag position."""

    handle: int
    position: WindowPosition
    width: int
    height: int

    def __post_init__(self) -> None:
        if self.handle <= 0:
            raise ValueError("window handle must be positive")
        if self.width <= 0 or self.height <= 0:
            raise ValueError("window dimensions must be positive")


class DragRuntime:
    """Own coordinate mapping and velocity state for one active window drag.

    The application is the single writer: it starts a grip after hit-testing,
    calls ``move`` for each ``MOVE_GRIPPED_WINDOW`` effect, moves the returned
    position with the window manager, and always calls ``release`` on cleanup.
    """

    def __init__(self, settings: Settings, layout: MonitorLayout) -> None:
        self._layout = layout
        self._mapper = RelativeCoordinateMapper(
            movement_gain=settings.gesture.movement_gain,
            minimum_delta_pixels=settings.gesture.minimum_delta_pixels,
            bounds=layout.virtual_bounds,
        )
        self._velocity_tracker = HandVelocityTracker(
            smoothing_alpha=settings.gesture.velocity.smoothing_alpha
        )
        self._velocity_gain = VelocityGain(
            activation_speed=settings.gesture.velocity.activation_speed,
            maximum_gain_multiplier=(settings.gesture.velocity.maximum_gain_multiplier),
        )
        self._session: GripSession | None = None

    @classmethod
    def discover(cls, settings: Settings) -> DragRuntime:
        """Create a runtime from the post-DPI-awareness monitor topology."""

        layout = discover_monitor_layout(
            require_consistency=settings.window.require_monitor_consistency
        )
        return cls(settings=settings, layout=layout)

    @property
    def layout(self) -> MonitorLayout:
        """Return the fixed monitor topology used for this application run."""

        return self._layout

    @property
    def active_handle(self) -> int | None:
        """Return the active drag target, if one exists."""

        return None if self._session is None else self._session.handle

    def begin_grip(
        self,
        handle: int,
        position: WindowPosition,
        width: int,
        height: int,
        hand_position: Point2D,
        timestamp_seconds: float,
    ) -> None:
        """Anchor a newly hit-tested window without an initial position jump."""

        if self._session is not None:
            raise RuntimeError("cannot begin a grip while another grip is active")

        self._session = GripSession(handle, position, width, height)
        self._mapper.begin(hand_position)
        self._velocity_tracker.reset()
        self._velocity_tracker.update(hand_position, timestamp_seconds)

    def move(self, hand_position: Point2D, timestamp_seconds: float) -> WindowPosition:
        """Return the next virtual-desktop position for the active grip."""

        if self._session is None:
            raise RuntimeError("cannot move without an active grip")

        velocity = self._velocity_tracker.update(hand_position, timestamp_seconds)
        next_position = self._mapper.move(
            hand_position=hand_position,
            current_position=self._session.position,
            window_width=self._session.width,
            window_height=self._session.height,
            gain_multiplier=self._velocity_gain.multiplier_for(velocity),
        )
        self._session = GripSession(
            handle=self._session.handle,
            position=next_position,
            width=self._session.width,
            height=self._session.height,
        )
        return next_position

    def release(self) -> None:
        """Discard every per-grip state; this operation is safe to repeat."""

        self._session = None
        self._mapper.reset()
        self._velocity_tracker.reset()
