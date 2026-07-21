"""Tests for low-overhead, least-privilege native window movement."""

import win32con
from pytest import MonkeyPatch

from mitsu.control.coordinate_mapper import WindowPosition
from mitsu.control.window_manager import WindowManager


def test_move_window_coalesces_identical_positions(
    monkeypatch: MonkeyPatch,
) -> None:
    manager = WindowManager()
    calls: list[tuple[object, ...]] = []
    position = WindowPosition(100, 200)

    monkeypatch.setattr(manager, "_is_eligible", lambda _handle: True)
    monkeypatch.setattr(
        "mitsu.control.window_manager.win32gui.SetWindowPos",
        lambda *arguments: calls.append(arguments),
    )

    manager.move_window(123, position)
    manager.move_window(123, position)

    assert len(calls) == 1


def test_maximize_window_requires_an_eligible_target(
    monkeypatch: MonkeyPatch,
) -> None:
    manager = WindowManager()
    calls: list[tuple[object, ...]] = []

    monkeypatch.setattr(manager, "_is_eligible", lambda _handle: True)
    monkeypatch.setattr(
        "mitsu.control.window_manager.win32gui.ShowWindow",
        lambda *arguments: calls.append(arguments),
    )

    manager.maximize_window(123)

    assert calls == [(123, win32con.SW_MAXIMIZE)]


def test_minimize_foreground_window_rejects_ineligible_foreground_target(
    monkeypatch: MonkeyPatch,
) -> None:
    manager = WindowManager()

    monkeypatch.setattr(
        "mitsu.control.window_manager.win32gui.GetForegroundWindow",
        lambda: 123,
    )
    monkeypatch.setattr(manager, "_is_eligible", lambda _handle: False)

    assert manager.minimize_foreground_window() is None


def test_minimize_window_requires_an_eligible_hand_selected_target(
    monkeypatch: MonkeyPatch,
) -> None:
    manager = WindowManager()

    monkeypatch.setattr(manager, "_is_eligible", lambda _handle: False)

    try:
        manager.minimize_window(123)
    except RuntimeError as error:
        assert "ineligible" in str(error)
    else:
        raise AssertionError("Expected ineligible window minimization to fail")
