from __future__ import annotations

import pytest

from mitsu.control.coordinate_mapper import ScreenBounds
from mitsu.control.monitor_layout import Monitor, MonitorLayout


def test_virtual_bounds_span_mixed_resolution_dual_monitor_layout() -> None:
    layout = MonitorLayout(
        monitors=(
            Monitor(
                device_name=r"\\.\DISPLAY1",
                bounds=ScreenBounds(-2560, 0, 0, 1600),
                dpi_x=192,
                dpi_y=192,
                is_primary=False,
            ),
            Monitor(
                device_name=r"\\.\DISPLAY2",
                bounds=ScreenBounds(0, 0, 1920, 1080),
                dpi_x=96,
                dpi_y=96,
                is_primary=True,
            ),
        )
    )

    assert layout.virtual_bounds == ScreenBounds(-2560, 0, 1920, 1600)
    assert layout.primary_monitor.device_name == r"\\.\DISPLAY2"


def test_monitor_at_uses_physical_virtual_desktop_coordinates() -> None:
    layout = MonitorLayout(
        monitors=(
            Monitor(
                device_name=r"\\.\DISPLAY1",
                bounds=ScreenBounds(-2560, 0, 0, 1600),
                dpi_x=192,
                dpi_y=192,
                is_primary=False,
            ),
            Monitor(
                device_name=r"\\.\DISPLAY2",
                bounds=ScreenBounds(0, 0, 1920, 1080),
                dpi_x=96,
                dpi_y=96,
                is_primary=True,
            ),
        )
    )

    assert layout.monitor_at(-100, 100) == layout.monitors[0]
    assert layout.monitor_at(100, 100) == layout.monitors[1]
    assert layout.monitor_at(2000, 100) is None


def test_virtual_bounds_supports_mixed_resolution_three_monitor_layout() -> None:
    layout = MonitorLayout(
        monitors=(
            Monitor(
                device_name=r"\\.\DISPLAY1",
                bounds=ScreenBounds(-2560, 0, 0, 1600),
                dpi_x=192,
                dpi_y=192,
                is_primary=False,
            ),
            Monitor(
                device_name=r"\\.\DISPLAY2",
                bounds=ScreenBounds(0, 0, 1920, 1080),
                dpi_x=96,
                dpi_y=96,
                is_primary=True,
            ),
            Monitor(
                device_name=r"\\.\DISPLAY3",
                bounds=ScreenBounds(0, -1440, 2560, 0),
                dpi_x=144,
                dpi_y=144,
                is_primary=False,
            ),
        )
    )

    assert layout.virtual_bounds == ScreenBounds(-2560, -1440, 2560, 1600)
    assert layout.monitor_at(100, -100) == layout.monitors[2]


def test_layout_rejects_multiple_primary_monitors() -> None:
    monitor = Monitor(
        device_name=r"\\.\DISPLAY1",
        bounds=ScreenBounds(0, 0, 1920, 1080),
        dpi_x=96,
        dpi_y=96,
        is_primary=True,
    )

    with pytest.raises(ValueError, match="exactly one monitor"):
        MonitorLayout(monitors=(monitor, monitor))
