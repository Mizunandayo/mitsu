"""Bounded explicit pointer movement and click control for Windows."""

from __future__ import annotations

import pywintypes
import win32api
import win32con

from mitsu.control.coordinate_mapper import ScreenPoint

_XBUTTON1 = 0x0001
_XBUTTON2 = 0x0002


class MouseController:
    """Move the system pointer and send explicit, bounded mouse actions."""

    def __init__(self) -> None:
        self._last_position: ScreenPoint | None = None

    def move_to(self, point: ScreenPoint) -> bool:
        """Move only when changed, returning false for a recoverable Win32 error."""

        if point == self._last_position:
            return True

        try:
            win32api.SetCursorPos((point.x, point.y))
        except pywintypes.error:
            self._last_position = None
            return False

        self._last_position = point
        return True

    @staticmethod
    def current_position() -> ScreenPoint | None:
        """Return Windows' physical cursor coordinates, if they are available."""

        try:
            x, y = win32api.GetCursorPos()
        except pywintypes.error:
            return None
        return ScreenPoint(x=int(x), y=int(y))

    def left_click(self) -> bool:
        """Send one explicit left-click, returning false for a Win32 error."""

        return self._mouse_event_pair(
            win32con.MOUSEEVENTF_LEFTDOWN,
            win32con.MOUSEEVENTF_LEFTUP,
            0,
        )

    def back_button(self) -> bool:
        """Send one standard mouse Back event, returning false for a Win32 error."""

        return self._mouse_event_pair(
            win32con.MOUSEEVENTF_XDOWN,
            win32con.MOUSEEVENTF_XUP,
            _XBUTTON1,
        )

    def forward_button(self) -> bool:
        """Send one standard mouse Forward event, returning false for a Win32 error."""

        return self._mouse_event_pair(
            win32con.MOUSEEVENTF_XDOWN,
            win32con.MOUSEEVENTF_XUP,
            _XBUTTON2,
        )

    @staticmethod
    def _mouse_event_pair(down_flag: int, up_flag: int, data: int) -> bool:
        try:
            win32api.mouse_event(down_flag, 0, 0, data, 0)
            win32api.mouse_event(up_flag, 0, 0, data, 0)
        except pywintypes.error:
            return False
        return True
