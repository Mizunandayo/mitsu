"""Tests for whole-hand fist grip recognition."""

from mitsu.gestures.fist import FistGripDetector
from mitsu.perception.one_euro import Point2D


def _points(tip_distance: float) -> tuple[Point2D, ...]:
    points = [Point2D(0.0, 0.0) for _ in range(21)]
    points[9] = Point2D(0.0, 1.0)
    for tip_index in (4, 8, 12, 16, 20):
        points[tip_index] = Point2D(tip_distance, 0.0)
    return tuple(points)


def _detector() -> FistGripDetector:
    return FistGripDetector(
        engage_tip_distance_ratio=1.10,
        release_tip_distance_ratio=1.35,
        release_debounce_frames=3,
    )


def test_closed_fist_engages_a_whole_hand_grip() -> None:
    assert _detector().update(_points(1.0)).is_fist


def test_two_close_fingers_without_a_fist_do_not_engage_grip() -> None:
    assert not _detector().update(_points(1.6)).is_fist


def test_fist_release_requires_multiple_open_frames() -> None:
    detector = _detector()
    detector.update(_points(1.0))

    assert detector.update(_points(1.6)).is_fist
    assert detector.update(_points(1.6)).is_fist
    assert not detector.update(_points(1.6)).is_fist
