
"""Fixed local command grammar"""


from __future__ import annotations

import re

from mitsu.voice.types import IntentAction, MonitorDestination, VoiceIntent

_COMMAND = re.compile(
    r"^\s*"
    r"(?P<verb>grab|move|show|open|place)\s+"
    r"(?P<app>[\w .,'&()+-]+?)"
    r"(?:\s+(?:on|to)\s+the\s+(?P<destination>left|right)"
    r"(?:\s+(?:screen|monitor))?)?"
    r"\s*$",
    re.IGNORECASE,
)




def parse_command(transcript: str) -> VoiceIntent | None:
    """Parse supported phrasing without guessing unsupported intent."""

    match = _COMMAND.fullmatch(transcript)
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
