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


def test_rejects_unknown_phrasing() -> None:
    assert parse_command("please organize my desktop") is None