from __future__ import annotations
import pytest
from mitsu.perception.one_euro import OneEuroFilter, Point2D



def test_first_sample_is_returned_unchanged() -> None:
    subject = OneEuroFilter(1.2, 0.015, 1.0)

    assert subject.filter(Point2D(0.2, 0.3), 1.0) == Point2D(0.2, 0.3)


def test_filter_smooths_a_position_step() -> None:
    subject = OneEuroFilter(1.2, 0.0, 1.0)
    subject.filter(Point2D(0.0, 0.0), 0.0)

    filtered = subject.filter(Point2D(1.0, 1.0), 0.1)

    assert 0.0 < filtered.x < 1.0
    assert 0.0 < filtered.y < 1.0



def test_filter_rejects_non_monotonic_timestamps() -> None:
    subject = OneEuroFilter(1.2, 0.015, 1.0)
    subject.filter(Point2D(0.0, 0.0), 1.0)

    with pytest.raises(ValueError, match="strictly increasing"):
        subject.filter(Point2D(0.1, 0.1), 1.0)




def test_reset_makes_next_sample_a_new_initial_value() -> None:
    subject = OneEuroFilter(1.2, 0.015, 1.0)
    subject.filter(Point2D(0.0, 0.0), 0.0)
    subject.reset()

    assert subject.filter(Point2D(0.9, 0.8), 2.0) == Point2D(0.9, 0.8)