"""Least-privilege Win32 top-level hit-testing and movement."""

from __future__ import annotations

import os
from dataclasses import dataclass

import pywintypes
import win32con
import win32gui
import win32process

from mitsu.control.coordinate_mapper import ScreenPoint, WindowPosition


@dataclass(frozen=True, slots=True)
class WindowRect:
    """A top-level window rectangle in physical desktop pixels."""

    position: WindowPosition
    width: int
    height: int




@dataclass(frozen=True, slots=True)
class WindowTarget:
    """An eligible window that MITSU may move."""

    handle: int
    rect: WindowRect
    title: str



class WindowManager:
    """Move only eligible user-facing top-level windows without input injection."""

    _EXCLUDED_CLASSES = frozenset(
        {
            "Progman",
            "WorkerW",
            "Shell_TrayWnd",
            "Shell_SecondaryTrayWnd",
        }
    )

    def __init__(self) -> None:
        self._own_process_id = os.getpid()
    
    def target_at(self, point: ScreenPoint) -> WindowTarget | None:
        """Return the safe top-level target beneath a physical screen point."""

        handle = win32gui.WindowFromPoint((point.x, point.y))
        if not handle:
            return None
        
        root_handle = win32gui.GetAncestor(handle, win32con.GA_ROOT)
        if not self._is_eligible(root_handle):
            return None

        return WindowTarget(
            handle=root_handle,
            rect=self._get_rect(root_handle),
            title=win32gui.GetWindowText(root_handle),
        )

    def move_window(self, handle: int, position: WindowPosition) -> None:
        """Move an eligible window while preserving size, z-order, and focus."""

        if not self._is_eligible(handle):
            raise RuntimeError("Refusing to move an ineligible window")
        
        flags = (
            win32con.SWP_NOSIZE
            | win32con.SWP_NOZORDER
            | win32con.SWP_NOACTIVATE
            | win32con.SWP_NOOWNERZORDER
        )

        win32gui.SetWindowPos(
            handle,
            0,
            position.x,
            position.y,
            0,
            0,
            flags,
        )

    def prepare_for_drag(self, handle: int) -> WindowRect:
        """Restore a maximized target after an explicit pinch and return its rect."""

        if not self._is_eligible(handle):
            raise RuntimeError("Refusing to prepare an ineligible window for dragging")

        if self._is_maximized(handle):
            win32gui.ShowWindow(handle, win32con.SW_RESTORE)

        if not win32gui.IsWindow(handle):
            raise RuntimeError("Window closed while preparing it for dragging")

        return self._get_rect(handle)

    def _is_eligible(self, handle: int) -> bool:
        try:
            if not handle or not win32gui.IsWindow(handle):
                return False
            if not win32gui.IsWindowVisible(handle):
                return False
            if win32gui.IsIconic(handle):
                return False
            if win32gui.GetParent(handle):
                return False
            if win32gui.GetWindow(handle, win32con.GW_OWNER):
                return False
            if win32gui.GetClassName(handle) in self._EXCLUDED_CLASSES:
                return False
            if not win32gui.GetWindowText(handle).strip():
                return False

            _, process_id = win32process.GetWindowThreadProcessId(handle)
            if process_id == self._own_process_id:
                return False

            extended_style = win32gui.GetWindowLong(handle, win32con.GWL_EXSTYLE)
            return not bool(extended_style & win32con.WS_EX_TOOLWINDOW)
        except pywintypes.error:
            return False

    @staticmethod
    def _is_maximized(handle: int) -> bool:
        """Return whether the window placement is maximized."""

        _, show_command, _, _, _ = win32gui.GetWindowPlacement(handle)
        return show_command == win32con.SW_SHOWMAXIMIZED

    @staticmethod
    def _get_rect(handle: int) -> WindowRect:
        left, top, right, bottom = win32gui.GetWindowRect(handle)
        return WindowRect(
            position=WindowPosition(left, top),
            width=right - left,
            height=bottom - top,
        )
