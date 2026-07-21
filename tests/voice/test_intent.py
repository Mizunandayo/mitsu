from __future__ import annotations

from mitsu.voice.intent import parse_command
from mitsu.voice.types import IntentAction, MonitorDestination


def test_parses_show_command() -> None:
    intent = parse_command("show Discord")

    assert intent is not None
    assert intent.action is IntentAction.SHOW
    assert intent.app_name == "Discord"
    assert intent.destination is None


def test_parses_grab_command_with_destination() -> None:
    intent = parse_command("grab VS Code on the left monitor")

    assert intent is not None
    assert intent.action is IntentAction.GRAB
    assert intent.app_name == "VS Code"
    assert intent.destination is MonitorDestination.LEFT


def test_parses_show_command_with_vertical_destination() -> None:
    intent = parse_command("show Discord on the up monitor")

    assert intent is not None
    assert intent.action is IntentAction.SHOW
    assert intent.app_name == "Discord"
    assert intent.destination is MonitorDestination.UP


def test_parses_polite_upper_monitor_request() -> None:
    intent = parse_command("Please show Discord on the upper monitor")

    assert intent is not None
    assert intent.action is IntentAction.SHOW
    assert intent.app_name == "Discord"
    assert intent.destination is MonitorDestination.UP


def test_parses_natural_request_prefix_and_monitor_above() -> None:
    intent = parse_command(
        "Mitsu, could you please bring up Discord on the monitor above"
    )

    assert intent is not None
    assert intent.action is IntentAction.SHOW
    assert intent.app_name == "Discord"
    assert intent.destination is MonitorDestination.UP


def test_parses_lower_display_and_move_synonym() -> None:
    intent = parse_command("I want you to send Discord to my bottom display")

    assert intent is not None
    assert intent.action is IntentAction.GRAB
    assert intent.app_name == "Discord"
    assert intent.destination is MonitorDestination.DOWN


def test_parses_a_wake_word_and_polite_prefix() -> None:
    intent = parse_command("Hey Mitsu, please show Discord on the left screen")

    assert intent is not None
    assert intent.action is IntentAction.SHOW
    assert intent.app_name == "Discord"
    assert intent.destination is MonitorDestination.LEFT


def test_parses_bring_up_as_show() -> None:
    intent = parse_command("Mitsu, bring up Paint")

    assert intent is not None
    assert intent.action is IntentAction.SHOW
    assert intent.app_name == "Paint"


def test_parses_current_screen_as_a_show_command() -> None:
    intent = parse_command("Can you show Discord on my screen")

    assert intent is not None
    assert intent.action is IntentAction.SHOW
    assert intent.app_name == "Discord"
    assert intent.destination is None


def test_rejects_unknown_phrasing() -> None:
    assert parse_command("please organize my desktop") is None
