"""Tests for index-middle-ring minimization downstrokes."""

from mitsu.gestures.three_finger_swipe import ThreeFingerMinimizeDetector
from mitsu.perception.one_euro import Point2D


def _pose(centroid_y: float) -> tuple[Point2D, ...]:
    points = [Point2D(0.0, 0.0) for _ in range(21)]
    points[9] = Point2D(0.0, 1.0)
    points[4] = Point2D(-1.0, 0.0)
    points[8] = Point2D(-0.22, centroid_y)
    points[12] = Point2D(0.0, centroid_y)
    points[16] = Point2D(0.22, centroid_y)
    points[20] = Point2D(0.2, 0.7)
    return tuple(points)


def _detector() -> ThreeFingerMinimizeDetector:
    return ThreeFingerMinimizeDetector(
        triad_close_ratio=0.70,
        triad_extension_ratio=1.20,
        folded_pinky_extension_ratio=1.20,
        minimum_thumb_index_ratio=0.45,
        minimum_pose_frames=2,
        minimum_downward_distance_ratio=0.14,
        downward_velocity_ratio_per_second=0.80,
    )


def test_stable_three_finger_downstroke_triggers_once() -> None:
    detector = _detector()

    first = detector.update(_pose(1.4), 1.0)
    stroke = detector.update(_pose(1.6), 1.1)
    held = detector.update(_pose(1.8), 1.2)

    assert first.is_three_finger_pose
    assert not first.minimize_triggered
    assert stroke.minimize_triggered
    assert not held.minimize_triggered


def test_open_hand_cannot_trigger_three_finger_minimize() -> None:
    detector = _detector()
    points = list(_pose(1.4))
    points[20] = Point2D(0.7, 1.35)

    reading = detector.update(tuple(points), 1.0)

    assert not reading.is_three_finger_pose
    assert not reading.minimize_triggered


def test_thumb_index_pinch_cannot_trigger_three_finger_minimize() -> None:
    detector = _detector()
    points = list(_pose(1.4))
    points[4] = Point2D(-0.2, 1.4)

    assert not detector.update(tuple(points), 1.0).is_three_finger_pose
