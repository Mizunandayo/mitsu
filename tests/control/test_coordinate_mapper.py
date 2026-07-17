from __future__ import annotations

from mitsu.control.coordinate_mapper import (
    RelativeCoordinateMapper,
    ScreenBounds,
    WindowPosition,
)
from mitsu.perception.one_euro import Point2D


def test_begin_produces_no_initial_window_jump() -> None:
    subject = RelativeCoordinateMapper(
        movement_gain=1000.0,
        minimum_delta_pixels=1.0,
        bounds=ScreenBounds(0, 0, 1920, 1080),
    )

    subject.begin(Point2D(0.2, 0.2))

    assert subject.move(
        Point2D(0.2, 0.2),
        WindowPosition(100, 100),
        500,
        400,
    ) == WindowPosition(100, 100)


def test_relative_hand_motion_moves_window() -> None:
    subject = RelativeCoordinateMapper(
        movement_gain=1000.0,
        minimum_delta_pixels=1.0,
        bounds=ScreenBounds(0, 0, 1920, 1080),
    )
    subject.begin(Point2D(0.2, 0.2))

    position = subject.move(
        Point2D(0.25, 0.18),
        WindowPosition(100, 100),
        500,
        400,
    )

    assert position == WindowPosition(150, 80)


def test_window_is_clamped_inside_single_monitor_bounds() -> None:
    subject = RelativeCoordinateMapper(
        movement_gain=10_000.0,
        minimum_delta_pixels=0.0,
        bounds=ScreenBounds(0, 0, 1920, 1080),
    )
    subject.begin(Point2D(0.0, 0.0))

    position = subject.move(
        Point2D(1.0, 1.0),
        WindowPosition(100, 100),
        500,
        400,
    )

    assert position == WindowPosition(1420, 680)


def test_subthreshold_motion_is_ignored() -> None:
    subject = RelativeCoordinateMapper(
        movement_gain=1000.0,
        minimum_delta_pixels=2.0,
        bounds=ScreenBounds(0, 0, 1920, 1080),
    )
    subject.begin(Point2D(0.1, 0.1))

    position = subject.move(
        Point2D(0.101, 0.099),
        WindowPosition(100, 100),
        500,
        400,
    )

    assert position == WindowPosition(100, 100)


def test_mapper_supports_a_negative_left_virtual_desktop_coordinate() -> None:
    subject = RelativeCoordinateMapper(
        movement_gain=1000.0,
        minimum_delta_pixels=0.0,
        bounds=ScreenBounds(-2560, 0, 1920, 1600),
    )
    subject.begin(Point2D(0.5, 0.5))

    position = subject.move(
        Point2D(0.0, 0.5),
        WindowPosition(100, 100),
        500,
        400,
    )

    assert position == WindowPosition(-400, 100)


def test_velocity_multiplier_expands_relative_motion() -> None:
    subject = RelativeCoordinateMapper(
        movement_gain=1000.0,
        minimum_delta_pixels=0.0,
        bounds=ScreenBounds(-2560, 0, 1920, 1600),
    )
    subject.begin(Point2D(0.0, 0.0))

    position = subject.move(
        Point2D(0.1, 0.0),
        WindowPosition(0, 100),
        500,
        400,
        gain_multiplier=2.5,
    )

    assert position == WindowPosition(250, 100)
