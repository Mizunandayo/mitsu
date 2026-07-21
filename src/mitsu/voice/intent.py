"""Fixed local command grammar"""

from __future__ import annotations

import re

from mitsu.voice.types import IntentAction, MonitorDestination, VoiceIntent

_COMMAND = re.compile(
    r"^\s*"
    r"(?P<verb>grab|move|show|open|place)\s+"
    r"(?P<app>[\w .,'&()+-]+?)"
    r"(?:\s+(?:on|to)\s+the\s+(?P<destination>left|right|up|down)"
    r"(?:\s+(?:screen|monitor))?)?"
    r"\s*$",
    re.IGNORECASE,
)

_SPEECH_PREFIX = re.compile(
    r"^\s*(?:(?:hey\s+)?mitsu[,:!\-\s]+)?"
    r"(?:(?:can|could)\s+you\s+)?"
    r"(?:please\s+)?",
    re.IGNORECASE,
)

_BRING_UP = re.compile(r"^bring\s+up\s+", re.IGNORECASE)
_CURRENT_SCREEN_SUFFIX = re.compile(
    r"\s+(?:on|to)\s+(?:my|this)\s+screen\s*[.!?]*$",
    re.IGNORECASE,
)


def parse_command(transcript: str) -> VoiceIntent | None:
    """Parse supported phrasing without guessing unsupported intent."""

    normalized = _SPEECH_PREFIX.sub("", transcript.strip())
    normalized = _BRING_UP.sub("show ", normalized)
    normalized = _CURRENT_SCREEN_SUFFIX.sub("", normalized)
    match = _COMMAND.fullmatch(normalized)
    if match is None:
        return None

    app_name = " ".join(match.group("app").split()).strip(" .")
    if not app_name:
        return None

    action = (
        IntentAction.GRAB
        if match.group("verb").casefold() in {"grab", "move", "place"}
        else IntentAction.SHOW
    )

    destination_text = match.group("destination")
    destination = (
        None
        if destination_text is None
        else MonitorDestination[destination_text.upper()]
    )

    return VoiceIntent(action, app_name, destination)
