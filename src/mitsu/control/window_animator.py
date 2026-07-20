"""Main-loop-owned eased animation for full voice relocation."""


from __future__ import annotations

from dataclasses import dataclass

from mitsu.control.coordinate_mapper import ScreenBounds, WindowPosition
from mitsu.control.window_manager import WindowRect


@dataclass(frozen=True, slots=True)
class GlideFrame:
    """One frame of a window glide."""

    position: WindowPosition
    is_complete: bool




class WindowGlide:
    """Animate one window position without threads or blocking sleeps"""

    def __init__(self, duration_seconds: float = 0.36) -> None:
        if duration_seconds <= 0.0:
            raise ValueError("duration_seconds must be positive")
        
        self._duration_seconds = duration_seconds
        self._start_time: float | None = None
        self._start_position: WindowPosition | None = None
        self._end_position: WindowPosition | None = None
    
    @property
    def is_active(self) -> bool:
        """Return whether a glide is currently in progress."""

        return self._start_time is not None
    
    def start(
        self,
        window_rect: WindowRect,
        destination_bounds: ScreenBounds,
        timestamp_seconds: float,
    ) -> None:
        """Start an eased glide to the center of a monitor."""

        self._start_time = timestamp_seconds
        self._start_position = window_rect.position
        self._end_position = self._centered_position(
            window_rect.width,
            window_rect.height,
            destination_bounds,
        )

    def update(self, timestamp_seconds: float) -> GlideFrame | None:
        """Return one animation frame or None when no glide is active."""

        if (
            self._start_time is None
            or self._start_position is None
            or self._end_position is None
        ):
            return None
        

        progress = min(
            max((timestamp_seconds - self._start_time) / self._duration_seconds, 0.0),
            1.0,
        )
        eased_progress = 1.0 - (1.0 - progress) ** 3

        position = WindowPosition(
            x=round(
                self._start_position.x
                + (self._end_position.x - self._start_position.x) * eased_progress
            ),
            y=round(
                self._start_position.y
                + (self._end_position.y - self._start_position.y) * eased_progress
            ),
        )

        is_complete = progress >= 1.0
        if is_complete:
            self.stop()
        
        return GlideFrame(position=position, is_complete=is_complete)
    
    def stop(self) -> None:
        """Cancel or finish the active glide."""

        self._start_time = None
        self._start_position = None
        self._end_position = None

    @staticmethod
    def _centered_position(
        window_width: int,
        window_height: int,
        bounds: ScreenBounds,
    ) -> WindowPosition:
        maximum_x = max(bounds.left, bounds.right - window_width)
        maximum_y = max(bounds.top, bounds.bottom - window_height)

        desired_x = bounds.left + (bounds.width - window_width) // 2
        desired_y = bounds.top + (bounds.height - window_height) // 2

        return WindowPosition(
            x=min(max(desired_x, bounds.left), maximum_x),
            y=min(max(desired_y, bounds.top), maximum_y),
        )
