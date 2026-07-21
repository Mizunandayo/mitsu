"""Tests for explicit, coalesced pointer and click control."""

import pywintypes
import win32con
from pytest import MonkeyPatch

from mitsu.control.coordinate_mapper import ScreenPoint
from mitsu.control.mouse_controller import MouseController


def test_mouse_controller_coalesces_identical_moves(
    monkeypatch: MonkeyPatch,
) -> None:
    controller = MouseController()
    calls: list[tuple[int, int]] = []
    point = ScreenPoint(100, 200)

    monkeypatch.setattr(
        "mitsu.control.mouse_controller.win32api.SetCursorPos",
        lambda position: calls.append(position),
    )

    assert controller.move_to(point)
    assert controller.move_to(point)

    assert calls == [(100, 200)]


def test_mouse_controller_sends_a_complete_left_click(
    monkeypatch: MonkeyPatch,
) -> None:
    controller = MouseController()
    flags: list[int] = []

    monkeypatch.setattr(
        "mitsu.control.mouse_controller.win32api.mouse_event",
        lambda flag, _x, _y, _data, _extra: flags.append(flag),
    )

    assert controller.left_click()

    assert flags == [win32con.MOUSEEVENTF_LEFTDOWN, win32con.MOUSEEVENTF_LEFTUP]


def test_mouse_controller_sends_a_complete_back_button_click(
    monkeypatch: MonkeyPatch,
) -> None:
    controller = MouseController()
    calls: list[tuple[int, int]] = []

    monkeypatch.setattr(
        "mitsu.control.mouse_controller.win32api.mouse_event",
        lambda flag, _x, _y, data, _extra: calls.append((flag, data)),
    )

    assert controller.back_button()

    assert calls == [
        (win32con.MOUSEEVENTF_XDOWN, 0x0001),
        (win32con.MOUSEEVENTF_XUP, 0x0001),
    ]


def test_mouse_controller_sends_a_complete_forward_button_click(
    monkeypatch: MonkeyPatch,
) -> None:
    controller = MouseController()
    calls: list[tuple[int, int]] = []

    monkeypatch.setattr(
        "mitsu.control.mouse_controller.win32api.mouse_event",
        lambda flag, _x, _y, data, _extra: calls.append((flag, data)),
    )

    assert controller.forward_button()

    assert calls == [
        (win32con.MOUSEEVENTF_XDOWN, 0x0002),
        (win32con.MOUSEEVENTF_XUP, 0x0002),
    ]


def test_mouse_controller_recovers_from_set_cursor_position_failure(
    monkeypatch: MonkeyPatch,
) -> None:
    controller = MouseController()

    monkeypatch.setattr(
        "mitsu.control.mouse_controller.win32api.SetCursorPos",
        lambda _position: (_ for _ in ()).throw(
            pywintypes.error(0, "SetCursorPos", "No error message is available")
        ),
    )

    assert not controller.move_to(ScreenPoint(100, 200))


def test_mouse_controller_reads_the_physical_cursor_position(
    monkeypatch: MonkeyPatch,
) -> None:
    monkeypatch.setattr(
        "mitsu.control.mouse_controller.win32api.GetCursorPos",
        lambda: (123, 456),
    )

    assert MouseController.current_position() == ScreenPoint(123, 456)
