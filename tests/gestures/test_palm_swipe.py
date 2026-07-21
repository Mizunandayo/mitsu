"""Tests for guarded open-palm minimization gestures."""

from mitsu.gestures.palm_swipe import PalmSwipeDetector
from mitsu.perception.one_euro import Point2D


def _open_palm(center_y: float) -> tuple[Point2D, ...]:
    points = [Point2D(0.0, 0.0) for _ in range(21)]
    points[0] = Point2D(0.0, center_y)
    points[9] = Point2D(0.0, center_y + 1.0)
    points[8] = Point2D(-0.4, center_y + 1.5)
    points[12] = Point2D(0.0, center_y + 1.7)
    points[16] = Point2D(0.4, center_y + 1.5)
    points[20] = Point2D(0.7, center_y + 1.35)
    return tuple(points)


def _palm_folded_down(wrist_offset: float) -> tuple[Point2D, ...]:
    points = list(_open_palm(0.0))
    points[0] = Point2D(0.0, wrist_offset)
    return tuple(points)


def test_open_palm_wrist_fold_triggers_minimize_once() -> None:
    detector = PalmSwipeDetector(
        open_palm_extension_ratio=1.30,
        minimum_open_palm_frames=2,
        minimum_downward_distance_ratio=0.14,
        downward_velocity_ratio_per_second=1.1,
    )

    first = detector.update(_palm_folded_down(0.0), 1.0)
    fold = detector.update(_palm_folded_down(0.2), 1.1)
    held = detector.update(_palm_folded_down(0.2), 1.2)

    assert first.is_open_palm
    assert not first.minimize_triggered
    assert fold.minimize_triggered
    assert not held.minimize_triggered


def test_unfolding_never_triggers_a_second_desktop_action() -> None:
    detector = PalmSwipeDetector(
        open_palm_extension_ratio=1.30,
        minimum_open_palm_frames=2,
        minimum_downward_distance_ratio=0.14,
        downward_velocity_ratio_per_second=1.1,
    )

    detector.update(_palm_folded_down(0.0), 1.0)
    minimized = detector.update(_palm_folded_down(0.2), 1.1)
    unfolding = detector.update(_palm_folded_down(0.0), 1.2)

    assert minimized.minimize_triggered
    assert not unfolding.minimize_triggered


def test_fold_motion_before_open_palm_is_stable_is_ignored() -> None:
    detector = PalmSwipeDetector(
        open_palm_extension_ratio=1.30,
        minimum_open_palm_frames=3,
        minimum_downward_distance_ratio=0.14,
        downward_velocity_ratio_per_second=1.1,
    )

    detector.update(_palm_folded_down(0.0), 1.0)
    early_motion = detector.update(_palm_folded_down(0.2), 1.1)
    detector.update(_palm_folded_down(0.0), 1.2)
    deliberate_fold = detector.update(_palm_folded_down(0.2), 1.3)

    assert not early_motion.minimize_triggered
    assert deliberate_fold.minimize_triggered


def test_whole_hand_downward_translation_never_triggers_minimize() -> None:
    detector = PalmSwipeDetector(
        open_palm_extension_ratio=1.30,
        minimum_open_palm_frames=2,
        minimum_downward_distance_ratio=0.14,
        downward_velocity_ratio_per_second=1.1,
    )

    detector.update(_open_palm(0.0), 1.0)
    translation = detector.update(_open_palm(0.3), 1.1)

    assert not translation.minimize_triggered


def test_relaxed_open_palm_is_recognized_by_the_runtime_threshold() -> None:
    detector = PalmSwipeDetector(
        open_palm_extension_ratio=1.20,
        minimum_open_palm_frames=2,
        minimum_downward_distance_ratio=0.14,
        downward_velocity_ratio_per_second=1.1,
    )

    points = list(_open_palm(0.0))
    points[8] = Point2D(-0.35, 1.2)
    points[12] = Point2D(0.0, 1.25)
    points[16] = Point2D(0.35, 1.2)
    points[20] = Point2D(0.55, 1.1)

    reading = detector.update(tuple(points), 1.0)

    assert reading.is_open_palm
    assert not reading.minimize_triggered


def test_wide_open_palm_requires_a_stricter_extension_threshold() -> None:
    detector = PalmSwipeDetector(
        open_palm_extension_ratio=1.20,
        minimum_open_palm_frames=2,
        minimum_downward_distance_ratio=0.14,
        downward_velocity_ratio_per_second=1.1,
    )

    relaxed_points = list(_open_palm(0.0))
    relaxed_points[8] = Point2D(-0.35, 1.2)
    relaxed_points[12] = Point2D(0.0, 1.25)
    relaxed_points[16] = Point2D(0.35, 1.2)
    relaxed_points[20] = Point2D(0.55, 1.1)

    assert detector.is_open_palm(tuple(relaxed_points))
    assert not detector.is_open_palm(
        tuple(relaxed_points),
        minimum_extension_ratio=1.30,
    )
    assert detector.is_open_palm(
        _open_palm(0.0),
        minimum_extension_ratio=1.30,
    )
