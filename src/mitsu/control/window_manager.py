"""Least-privilege Win32 top-level window discovery and movement."""

from __future__ import annotations

import ctypes
import os
from dataclasses import dataclass
from pathlib import Path

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
    """An eligible user-facing window."""

    handle: int
    rect: WindowRect
    title: str


class WindowManager:
    """Control eligible user windows without input injection."""

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

        return self._target_from_handle(root_handle)

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
        win32gui.SetWindowPos(handle, 0, position.x, position.y, 0, 0, flags)

    def prepare_for_drag(self, handle: int) -> WindowRect:
        """Restore a maximized window after an explicit pinch before dragging."""

        if not self._is_eligible(handle):
            raise RuntimeError("Refusing to prepare an ineligible window")

        if self._is_maximized(handle):
            win32gui.ShowWindow(handle, win32con.SW_RESTORE)

        if not win32gui.IsWindow(handle):
            raise RuntimeError("Window closed while preparing for drag")

        return self._get_rect(handle)

    def find_window(self, query: str) -> WindowTarget | None:
        """Resolve an app by title or executable name, foreground match first."""

        normalized_query = query.casefold().strip()
        if not normalized_query:
            return None

        matches: list[WindowTarget] = []

        def collect(handle: int, _context: object) -> None:
            if not self._is_voice_eligible(handle):
                return

            title = win32gui.GetWindowText(handle)
            process_name = self._process_name(handle)
            if (
                normalized_query in title.casefold()
                or normalized_query in process_name.casefold()
            ):
                matches.append(self._target_from_handle(handle))

        win32gui.EnumWindows(collect, None)

        if not matches:
            return None

        foreground = win32gui.GetForegroundWindow()
        return next((item for item in matches if item.handle == foreground), matches[0])

    def restore_and_focus(self, handle: int) -> WindowTarget:
        """Restore an explicit voice target and bring it to the foreground."""

        if not self._is_voice_eligible(handle):
            raise RuntimeError("Refusing to restore an ineligible window")

        if win32gui.IsIconic(handle):
            win32gui.ShowWindow(handle, win32con.SW_RESTORE)

        win32gui.SetForegroundWindow(handle)
        return self._target_from_handle(handle)

    def _is_eligible(self, handle: int) -> bool:
        try:
            if not self._is_common_window_candidate(handle):
                return False
            return not win32gui.IsIconic(handle)
        except pywintypes.error:
            return False

    def _is_voice_eligible(self, handle: int) -> bool:
        """Allow minimized windows while preserving all system exclusions."""

        try:
            return self._is_common_window_candidate(handle)
        except pywintypes.error:
            return False

    def _is_common_window_candidate(self, handle: int) -> bool:
        if not handle or not win32gui.IsWindow(handle):
            return False
        if not win32gui.IsWindowVisible(handle) and not win32gui.IsIconic(handle):
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

    @staticmethod
    def _is_maximized(handle: int) -> bool:
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

    def _target_from_handle(self, handle: int) -> WindowTarget:
        return WindowTarget(
            handle=handle,
            rect=self._get_rect(handle),
            title=win32gui.GetWindowText(handle),
        )

    @staticmethod
    def _process_name(handle: int) -> str:
        """Read only executable metadata using limited process-query access."""

        _, process_id = win32process.GetWindowThreadProcessId(handle)
        kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        process_handle = kernel32.OpenProcess(0x1000, False, process_id)
        if not process_handle:
            return ""

        try:
            size = ctypes.c_uint(32_768)
            buffer = ctypes.create_unicode_buffer(size.value)
            success = kernel32.QueryFullProcessImageNameW(
                process_handle,
                0,
                buffer,
                ctypes.byref(size),
            )
            return Path(buffer.value).stem if success else ""
        finally:
            kernel32.CloseHandle(process_handle)
