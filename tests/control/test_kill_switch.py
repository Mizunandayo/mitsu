"""Tests for the global automation emergency stop."""

from mitsu.control.kill_switch import VK_CONTROL, VK_F12, VK_SHIFT, KillSwitch


def test_kill_switch_triggers_once_for_each_key_press() -> None:
    keys = {
        VK_CONTROL: 0x8000,
        VK_SHIFT: 0x8000,
        VK_F12: 0x8000,
    }
    switch = KillSwitch(key_state_reader=lambda key: keys.get(key, 0))

    assert switch.poll()
    assert not switch.poll()

    keys[VK_F12] = 0
    assert not switch.poll()

    keys[VK_F12] = 0x8000
    assert switch.poll()


def test_kill_switch_requires_the_full_key_chord() -> None:
    keys = {
        VK_CONTROL: 0x8000,
        VK_SHIFT: 0x8000,
        VK_F12: 0,
    }
    switch = KillSwitch(key_state_reader=lambda key: keys.get(key, 0))

    assert not switch.poll()
