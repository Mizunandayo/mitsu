"""Tests for close index-middle pointer control and downward press clicking."""

from mitsu.gestures.air_click import AirClickDetector
from mitsu.gestures.pinch import HandLandmarks
from mitsu.perception.one_euro import Point2D


def _landmarks(
    *,
    fingertip_y: float = 1.5,
    index_tip_y: float | None = None,
    middle_tip_y: float | None = None,
    wrist_y: float = 0.0,
    finger_distance: float = 0.2,
) -> HandLandmarks:
    index_y = fingertip_y if index_tip_y is None else index_tip_y
    middle_y = fingertip_y if middle_tip_y is None else middle_tip_y
    return HandLandmarks(
        wrist=Point2D(0.0, wrist_y),
        middle_mcp=Point2D(0.0, wrist_y + 1.0),
        index_tip=Point2D(-finger_distance / 2.0, index_y),
        middle_tip=Point2D(finger_distance / 2.0, middle_y),
        thumb_tip=Point2D(-0.1, fingertip_y - 0.05),
        ring_mcp=Point2D(0.4, wrist_y + 0.7),
        ring_tip=Point2D(0.4, wrist_y + 0.9),
        pinky_mcp=Point2D(0.7, wrist_y + 0.7),
        pinky_tip=Point2D(0.7, wrist_y + 0.9),
    )


def _detector() -> AirClickDetector:
    return AirClickDetector(
        pointer_extension_ratio=1.35,
        fingers_close_ratio=0.50,
        fingers_release_ratio=0.65,
        minimum_press_downward_ratio=0.06,
        minimum_click_pose_frames=2,
        ring_extension_ratio=1.25,
        minimum_forward_pose_frames=3,
        pinky_extension_ratio=1.25,
        minimum_back_pose_frames=3,
    )


def test_downward_index_middle_press_triggers_one_click() -> None:
    detector = _detector()
    resting = _landmarks(fingertip_y=1.50)
    pressed = _landmarks(fingertip_y=1.62)

    detector.update(resting, 1.0)
    armed = detector.update(resting, 1.1)
    click = detector.update(pressed, 1.2)
    held = detector.update(pressed, 1.3)

    assert armed.is_click_pose
    assert not armed.click_triggered
    assert click.click_triggered
    assert not held.click_triggered


def test_lifting_fingertips_after_a_click_rearms_without_clicking() -> None:
    detector = _detector()
    resting = _landmarks(fingertip_y=1.50)
    pressed = _landmarks(fingertip_y=1.62)

    detector.update(resting, 1.0)
    detector.update(resting, 1.1)
    first_click = detector.update(pressed, 1.2)
    rearm = detector.update(resting, 1.3)
    second_click = detector.update(pressed, 1.4)

    assert first_click.click_triggered
    assert not rearm.click_triggered
    assert second_click.click_triggered


def test_whole_hand_downward_motion_does_not_click() -> None:
    detector = _detector()
    resting = _landmarks(fingertip_y=1.50, wrist_y=0.0)
    moved_hand = _landmarks(fingertip_y=1.80, wrist_y=0.30)

    detector.update(resting, 1.0)
    detector.update(resting, 1.1)
    reading = detector.update(moved_hand, 1.2)

    assert not reading.click_triggered


def test_one_fingertip_dipping_does_not_click() -> None:
    detector = _detector()
    resting = _landmarks(fingertip_y=1.50)
    index_only_dip = _landmarks(index_tip_y=1.62, middle_tip_y=1.50)

    detector.update(resting, 1.0)
    detector.update(resting, 1.1)
    reading = detector.update(index_only_dip, 1.2)

    assert not reading.click_triggered


def test_separated_fingers_cannot_click() -> None:
    detector = _detector()
    resting = _landmarks(finger_distance=1.0)
    pressed = _landmarks(fingertip_y=1.62, finger_distance=1.0)

    detector.update(resting, 1.0)
    detector.update(resting, 1.1)
    reading = detector.update(pressed, 1.2)

    assert not reading.is_click_pose
    assert not reading.click_triggered


def test_raised_pinky_from_the_click_pose_triggers_back_once() -> None:
    detector = _detector()
    landmarks = _landmarks()
    raised_pinky = HandLandmarks(
        wrist=landmarks.wrist,
        middle_mcp=landmarks.middle_mcp,
        index_tip=landmarks.index_tip,
        middle_tip=landmarks.middle_tip,
        thumb_tip=landmarks.thumb_tip,
        ring_mcp=landmarks.ring_mcp,
        ring_tip=landmarks.ring_tip,
        pinky_mcp=landmarks.pinky_mcp,
        pinky_tip=Point2D(0.7, -1.2),
    )

    detector.update(raised_pinky, 1.0)
    detector.update(raised_pinky, 1.1)
    back = detector.update(raised_pinky, 1.2)

    assert back.back_triggered


def test_raised_ring_from_the_click_pose_triggers_forward_once() -> None:
    detector = _detector()
    landmarks = _landmarks()
    raised_ring = HandLandmarks(
        wrist=landmarks.wrist,
        middle_mcp=landmarks.middle_mcp,
        index_tip=landmarks.index_tip,
        middle_tip=landmarks.middle_tip,
        thumb_tip=landmarks.thumb_tip,
        ring_mcp=landmarks.ring_mcp,
        ring_tip=Point2D(0.4, -1.2),
        pinky_mcp=landmarks.pinky_mcp,
        pinky_tip=landmarks.pinky_tip,
    )

    detector.update(raised_ring, 1.0)
    detector.update(raised_ring, 1.1)
    forward = detector.update(raised_ring, 1.2)

    assert forward.forward_triggered
