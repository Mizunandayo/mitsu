"""Tests for minimized-window shelf V-sign activation."""

from mitsu.gestures.v_sign import VSignDetector
from mitsu.perception.one_euro import Point2D


def _v_sign() -> tuple[Point2D, ...]:
    points = [Point2D(0.0, 0.0) for _ in range(21)]
    points[9] = Point2D(0.0, 1.0)
    points[8] = Point2D(-0.5, 1.5)
    points[12] = Point2D(0.5, 1.5)
    points[16] = Point2D(0.2, 0.7)
    points[20] = Point2D(0.4, 0.7)
    return tuple(points)


def _detector() -> VSignDetector:
    return VSignDetector(
        extension_ratio=1.25,
        folded_finger_ratio=1.20,
        minimum_finger_gap_ratio=0.45,
        minimum_hold_frames=3,
    )


def test_stable_v_sign_activates_once() -> None:
    detector = _detector()

    first = detector.update(_v_sign())
    second = detector.update(_v_sign())
    third = detector.update(_v_sign())
    held = detector.update(_v_sign())

    assert first.is_v_sign
    assert not second.activated
    assert third.activated
    assert not held.activated


def test_close_index_middle_click_pose_is_not_a_v_sign() -> None:
    detector = _detector()
    points = list(_v_sign())
    points[12] = Point2D(-0.3, 1.5)

    assert not detector.update(tuple(points)).is_v_sign
