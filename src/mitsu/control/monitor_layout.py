"""Windows monitor discovery and DPI-consistent virtual desktop layout."""

from __future__ import annotations

import ctypes
import os
from dataclasses import dataclass
from typing import Final

import win32api
from screeninfo import get_monitors

from mitsu.control.coordinate_mapper import ScreenBounds

_MONITORINFOF_PRIMARY: Final[int] = 1
_MDT_EFFECTIVE_DPI: Final[int] = 0
_S_OK: Final[int] = 0


@dataclass(frozen=True, slots=True)
class Monitor:
    """A physical Windows display in per-monitor-DPI-aware coordinates."""

    device_name: str
    bounds: ScreenBounds
    dpi_x: int
    dpi_y: int
    is_primary: bool

    def __post_init__(self) -> None:
        if not self.device_name:
            raise ValueError("device_name must not be empty")
        if self.dpi_x <= 0 or self.dpi_y <= 0:
            raise ValueError("monitor DPI must be positive")


@dataclass(frozen=True, slots=True)
class MonitorLayout:
    """Validated physical monitor topology and its virtual desktop bounds."""

    monitors: tuple[Monitor, ...]

    def __post_init__(self) -> None:
        if not self.monitors:
            raise ValueError("at least one monitor is required")
        if sum(monitor.is_primary for monitor in self.monitors) != 1:
            raise ValueError("exactly one monitor must be primary")

    @property
    def virtual_bounds(self) -> ScreenBounds:
        """Return a physical-pixel bounding box spanning every monitor."""

        return ScreenBounds(
            left=min(monitor.bounds.left for monitor in self.monitors),
            top=min(monitor.bounds.top for monitor in self.monitors),
            right=max(monitor.bounds.right for monitor in self.monitors),
            bottom=max(monitor.bounds.bottom for monitor in self.monitors),
        )

    @property
    def primary_monitor(self) -> Monitor:
        """Return the Windows primary monitor."""

        return next(monitor for monitor in self.monitors if monitor.is_primary)

    def monitor_at(self, x: int, y: int) -> Monitor | None:
        """Return the monitor containing a physical-pixel point."""

        for monitor in self.monitors:
            bounds = monitor.bounds
            if bounds.left <= x < bounds.right and bounds.top <= y < bounds.bottom:
                return monitor
        return None


def discover_monitor_layout(require_consistency: bool) -> MonitorLayout:
    """Discover monitors after per-monitor DPI awareness has been enabled.

    This must only be called after the process enables per-monitor DPI awareness
    V2. The resulting bounds then match GetWindowRect and SetWindowPos physical
    pixels and must not be independently rescaled.
    """

    if os.name != "nt":
        raise OSError("MITSU monitor control is supported only on Windows")

    screeninfo_rectangles = {
        (monitor.x, monitor.y, monitor.x + monitor.width, monitor.y + monitor.height)
        for monitor in get_monitors()
    }

    monitors: list[Monitor] = []
    win32_rectangles: set[tuple[int, int, int, int]] = set()

    for handle, _, rectangle in win32api.EnumDisplayMonitors():
        info = win32api.GetMonitorInfo(handle)
        left, top, right, bottom = rectangle
        bounds = ScreenBounds(left, top, right, bottom)
        win32_rectangles.add((left, top, right, bottom))
        dpi_x, dpi_y = _dpi_for_monitor(int(handle))

        monitors.append(
            Monitor(
                device_name=str(info["Device"]),
                bounds=bounds,
                dpi_x=dpi_x,
                dpi_y=dpi_y,
                is_primary=bool(int(info["Flags"]) & _MONITORINFOF_PRIMARY),
            )
        )

    if require_consistency and screeninfo_rectangles != win32_rectangles:
        raise RuntimeError(
            "screeninfo and Win32 returned different monitor geometries; "
            "refusing to control windows with ambiguous coordinates"
        )

    return MonitorLayout(monitors=tuple(monitors))


def _dpi_for_monitor(monitor_handle: int) -> tuple[int, int]:
    """Return effective monitor DPI through the Windows Shcore API."""

    shcore = ctypes.WinDLL("Shcore", use_last_error=True)
    get_dpi_for_monitor = shcore.GetDpiForMonitor
    get_dpi_for_monitor.argtypes = [
        ctypes.c_void_p,
        ctypes.c_int,
        ctypes.POINTER(ctypes.c_uint),
        ctypes.POINTER(ctypes.c_uint),
    ]
    get_dpi_for_monitor.restype = ctypes.c_long

    dpi_x = ctypes.c_uint()
    dpi_y = ctypes.c_uint()
    result = get_dpi_for_monitor(
        ctypes.c_void_p(monitor_handle),
        _MDT_EFFECTIVE_DPI,
        ctypes.byref(dpi_x),
        ctypes.byref(dpi_y),
    )

    if result != _S_OK:
        raise OSError(
            f"GetDpiForMonitor failed with HRESULT 0x{result & 0xFFFFFFFF:08X}"
        )

    return dpi_x.value, dpi_y.value
