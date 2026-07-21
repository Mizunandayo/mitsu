"""Tests for direction-to-monitor resolution in the application layer."""

from mitsu.app import monitor_for_destination
from mitsu.control.coordinate_mapper import ScreenBounds
from mitsu.control.monitor_layout import Monitor
from mitsu.voice.types import MonitorDestination


def test_resolves_vertical_monitor_destinations_from_physical_bounds() -> None:
    lower_monitor = Monitor(
        device_name=r"\\.\DISPLAY1",
        bounds=ScreenBounds(left=0, top=0, right=1920, bottom=1080),
        dpi_x=96,
        dpi_y=96,
        is_primary=True,
    )
    upper_monitor = Monitor(
        device_name=r"\\.\DISPLAY2",
        bounds=ScreenBounds(left=0, top=-1600, right=2560, bottom=0),
        dpi_x=144,
        dpi_y=144,
        is_primary=False,
    )
    monitors = (lower_monitor, upper_monitor)

    assert monitor_for_destination(MonitorDestination.UP, monitors) is upper_monitor
    assert monitor_for_destination(MonitorDestination.DOWN, monitors) is lower_monitor
