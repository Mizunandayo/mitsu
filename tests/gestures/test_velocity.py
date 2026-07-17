from __future__ import annotations

import pytest

from mitsu.gestures.velocity import HandVelocity, HandVelocityTracker, VelocityGain
from mitsu.perception.one_euro import Point2D


def test_first_velocity_sample_is_zero() -> None:
    tracker = HandVelocityTracker(smoothing_alpha=1.0)
    velocity = tracker.update(Point2D(0.2, 0.3), 1.0)

    assert velocity == HandVelocity(0.0, 0.0)


def test_velocity_is_measured_from_position_delta_and_time() -> None:
    tracker = HandVelocityTracker(smoothing_alpha=1.0)
    tracker.update(Point2D(0.0, 0.0), 0.0)

    velocity = tracker.update(Point2D(0.2, -0.1), 0.5)

    assert velocity == HandVelocity(0.4, -0.2)


def test_velocity_is_smoothed() -> None:
    tracker = HandVelocityTracker(smoothing_alpha=0.5)
    tracker.update(Point2D(0.0, 0.0), 0.0)

    velocity = tracker.update(Point2D(1.0, 0.0), 1.0)

    assert velocity == HandVelocity(0.5, 0.0)


def test_velocity_rejects_non_monotonic_timestamps() -> None:
    tracker = HandVelocityTracker(smoothing_alpha=1.0)
    tracker.update(Point2D(0.0, 0.0), 1.0)

    with pytest.raises(ValueError, match="strictly increasing"):
        tracker.update(Point2D(0.1, 0.0), 1.0)


def test_gain_is_one_below_activation_speed() -> None:
    gain = VelocityGain(activation_speed=0.35, maximum_gain_multiplier=2.5)

    assert gain.multiplier_for(HandVelocity(0.2, 0.0)) == 1.0


def test_gain_reaches_configured_cap() -> None:
    gain = VelocityGain(activation_speed=0.35, maximum_gain_multiplier=2.5)

    assert gain.multiplier_for(HandVelocity(0.70, 0.0)) == 2.5
    assert gain.multiplier_for(HandVelocity(4.0, 0.0)) == 2.5
