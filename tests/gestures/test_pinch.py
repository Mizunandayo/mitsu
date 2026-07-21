from __future__ import annotations

from mitsu.gestures.pinch import HandLandmarks, PinchDetector
from mitsu.perception.one_euro import Point2D


def hand_with_tip_distance(tip_distance: float) -> HandLandmarks:
    return HandLandmarks(
        wrist=Point2D(0.0, 0.0),
        middle_mcp=Point2D(0.0, 1.0),
        thumb_tip=Point2D(0.0, 0.0),
        index_tip=Point2D(tip_distance, 0.0),
    )


def test_pinch_engages_at_the_engagement_threshold() -> None:
    subject = PinchDetector(engage_ratio=0.34, release_ratio=0.46)

    reading = subject.update(hand_with_tip_distance(0.34))

    assert reading.is_pinched is True
    assert reading.ratio == 0.34


def test_pinch_hysteresis_prevents_chatter() -> None:
    subject = PinchDetector(
        engage_ratio=0.34,
        release_ratio=0.46,
        release_debounce_frames=2,
    )
    subject.update(hand_with_tip_distance(0.30))

    assert subject.update(hand_with_tip_distance(0.40)).is_pinched is True
    assert subject.update(hand_with_tip_distance(0.46)).is_pinched is True
    assert subject.update(hand_with_tip_distance(0.46)).is_pinched is False


def test_tracking_loss_resets_latched_pinch() -> None:
    subject = PinchDetector(engage_ratio=0.34, release_ratio=0.46)
    subject.update(hand_with_tip_distance(0.30))

    reading = subject.update(None)

    assert reading.is_pinched is False
    assert reading.ratio is None


def test_single_open_frame_does_not_release_an_active_pinch() -> None:
    subject = PinchDetector(
        engage_ratio=0.34,
        release_ratio=0.46,
        release_debounce_frames=4,
    )
    subject.update(hand_with_tip_distance(0.30))

    reading = subject.update(hand_with_tip_distance(0.60))

    assert reading.is_pinched is True


def test_sustained_open_pinch_releases_after_the_debounce_window() -> None:
    subject = PinchDetector(
        engage_ratio=0.34,
        release_ratio=0.46,
        release_debounce_frames=4,
    )
    subject.update(hand_with_tip_distance(0.30))

    for _ in range(3):
        assert subject.update(hand_with_tip_distance(0.60)).is_pinched is True

    assert subject.update(hand_with_tip_distance(0.60)).is_pinched is False
