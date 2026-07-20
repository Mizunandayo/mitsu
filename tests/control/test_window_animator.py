from __future__ import annotations

from mitsu.control.coordinate_mapper import ScreenBounds, WindowPosition
from mitsu.control.window_animator import GlideFrame, WindowGlide
from mitsu.control.window_manager import WindowRect


def test_glide_starts_at_current_position() -> None:
    glide = WindowGlide(duration_seconds=1.0)
    rect = WindowRect(WindowPosition(100, 100), 500, 400)
    bounds = ScreenBounds(0, 0, 1920, 1080)

    glide.start(rect, bounds, timestamp_seconds=10.0)
    frame = glide.update(timestamp_seconds=10.0)

    assert frame == GlideFrame(WindowPosition(100, 100), False)


def test_glide_finishes_centered_on_destination_monitor() -> None:
    glide = WindowGlide(duration_seconds=1.0)
    rect = WindowRect(WindowPosition(100, 100), 500, 400)
    bounds = ScreenBounds(-2560, 0, 0, 1600)

    glide.start(rect, bounds, timestamp_seconds=10.0)
    frame = glide.update(timestamp_seconds=11.0)

    assert frame is not None
    assert frame.position == WindowPosition(-1530, 600)
    assert frame.is_complete is True


def test_glide_is_inactive_after_completion() -> None:
    glide = WindowGlide(duration_seconds=0.2)
    rect = WindowRect(WindowPosition(0, 0), 500, 400)
    bounds = ScreenBounds(0, 0, 1920, 1080)

    glide.start(rect, bounds, timestamp_seconds=0.0)
    glide.update(timestamp_seconds=0.2)

    assert glide.is_active is False