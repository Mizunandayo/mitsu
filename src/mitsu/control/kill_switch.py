from __future__ import annotations

import ctypes
from collections.abc import Callable

VK_CONTROL = 0x11
VK_SHIFT = 0x10
VK_F12 = 0x7B


KeyStateReader = Callable[[int], int]


class KillSwitch:
    """Edge-triggered global emergency stop: Ctrl + Shift + F12."""

    def __init__(self, key_state_reader: KeyStateReader | None = None) -> None:
        self._key_state_reader = key_state_reader or self._windows_key_state
        self._was_pressed = False

    def poll(self) -> bool:
        pressed = (
            self._is_down(VK_CONTROL)
            and self._is_down(VK_SHIFT)
            and self._is_down(VK_F12)
        )

        triggered = pressed and not self._was_pressed
        self._was_pressed = pressed
        return triggered

    def _is_down(self, virtual_key: int) -> bool:
        return bool(self._key_state_reader(virtual_key) & 0x8000)

    @staticmethod
    def _windows_key_state(virtual_key: int) -> int:
        user32 = ctypes.WinDLL("user32", use_last_error=True)
        return int(user32.GetAsyncKeyState(virtual_key))
