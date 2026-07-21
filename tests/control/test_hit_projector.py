from __future__ import annotations

from mitsu.control.coordinate_mapper import (
    CalibratedPointerProjector,
    HitTestProjector,
    ScreenBounds,
    ScreenPoint,
)
from mitsu.perception.one_euro import Point2D


def test_projector_maps_normalized_points_to_physical_screen_coordinates() -> None:
    projector = HitTestProjector(ScreenBounds(0, 0, 1920, 1080))

    assert projector.project(Point2D(0.0, 0.0)) == ScreenPoint(0, 0)
    assert projector.project(Point2D(1.0, 1.0)) == ScreenPoint(1919, 1079)


def test_projector_clamps_invalid_normalized_coordinates() -> None:
    projector = HitTestProjector(ScreenBounds(-2560, 0, 0, 1600))

    assert projector.project(Point2D(-2.0, 3.0)) == ScreenPoint(-2560, 1599)


def test_calibrated_pointer_maps_camera_region_to_one_monitor() -> None:
    projector = CalibratedPointerProjector(
        ScreenBounds(0, 0, 1920, 1080),
        camera_left=0.2,
        camera_top=0.1,
        camera_right=0.8,
        camera_bottom=0.9,
    )

    assert projector.project(Point2D(0.2, 0.1)) == ScreenPoint(0, 0)
    assert projector.project(Point2D(0.8, 0.9)) == ScreenPoint(1919, 1079)
    assert projector.project(Point2D(0.5, 0.5)) == ScreenPoint(960, 540)
