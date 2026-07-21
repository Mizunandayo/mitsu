"""Forgiving but deterministic local grammar for window voice commands."""

from __future__ import annotations

import re

from mitsu.voice.types import IntentAction, MonitorDestination, VoiceIntent

_COMMAND = re.compile(
    r"^\s*(?P<verb>grab|move|show|open|place|put|send)\s+"
    r"(?P<app>[\w .,'&()+-]+?)\s*$",
    re.IGNORECASE,
)

_SPEECH_PREFIXES = (
    re.compile(r"^\s*(?:hey\s+)?mitsu\s*[,!:;\-]*\s*", re.IGNORECASE),
    re.compile(
        r"^\s*(?:can|could|would|will)\s+you\s*[,!:;\-]*\s*",
        re.IGNORECASE,
    ),
    re.compile(r"^\s*(?:please|kindly)\s*[,!:;\-]*\s*", re.IGNORECASE),
    re.compile(r"^\s*i\s+(?:want|need)\s+you\s+to\s+", re.IGNORECASE),
)

_SHOW_VERB = re.compile(
    r"^(?:bring(?:\s+up)?|pull\s+up|launch)\s+",
    re.IGNORECASE,
)
_CURRENT_SCREEN_SUFFIX = re.compile(
    r"\s+(?:on|to)\s+(?:my|this)\s+screen\s*[.!?]*$",
    re.IGNORECASE,
)

_DIRECTION_ALIASES = {
    "left": MonitorDestination.LEFT,
    "right": MonitorDestination.RIGHT,
    "up": MonitorDestination.UP,
    "upper": MonitorDestination.UP,
    "top": MonitorDestination.UP,
    "above": MonitorDestination.UP,
    "down": MonitorDestination.DOWN,
    "lower": MonitorDestination.DOWN,
    "bottom": MonitorDestination.DOWN,
    "below": MonitorDestination.DOWN,
}
_DIRECTION_WORDS = "|".join(_DIRECTION_ALIASES)
_LEADING_DESTINATION_SUFFIX = re.compile(
    rf"\s+(?:on|to|onto|in)\s+(?:(?:the|my|this)\s+)?"
    rf"(?P<direction>{_DIRECTION_WORDS})"
    r"(?:\s+(?:screen|monitor|display))?\s*[.!?]*$",
    re.IGNORECASE,
)
_TRAILING_DESTINATION_SUFFIX = re.compile(
    r"\s+(?:on|to|onto|in)\s+(?:(?:the|my|this)\s+)?"
    r"(?:screen|monitor|display)\s+(?P<direction>above|below|up|down)"
    r"\s*[.!?]*$",
    re.IGNORECASE,
)


def parse_command(transcript: str) -> VoiceIntent | None:
    """Parse supported phrasing without guessing unsupported intent."""

    normalized = _remove_speech_prefixes(transcript)
    normalized = _SHOW_VERB.sub("show ", normalized)
    normalized = _CURRENT_SCREEN_SUFFIX.sub("", normalized)
    normalized, destination = _extract_destination(normalized)
    match = _COMMAND.fullmatch(normalized)
    if match is None:
        return None

    app_name = " ".join(match.group("app").split()).strip(" .")
    if not app_name:
        return None

    action = (
        IntentAction.GRAB
        if match.group("verb").casefold() in {"grab", "move", "place", "put", "send"}
        else IntentAction.SHOW
    )

    return VoiceIntent(action, app_name, destination)


def _remove_speech_prefixes(transcript: str) -> str:
    """Remove a bounded set of polite request prefixes in a common order."""

    normalized = transcript.strip()
    for _ in range(4):
        for prefix in _SPEECH_PREFIXES:
            stripped = prefix.sub("", normalized, count=1)
            if stripped != normalized:
                normalized = stripped
                break
        else:
            break
    return normalized


def _extract_destination(text: str) -> tuple[str, MonitorDestination | None]:
    """Split a supported monitor phrase from the app title without guessing."""

    for pattern in (_LEADING_DESTINATION_SUFFIX, _TRAILING_DESTINATION_SUFFIX):
        match = pattern.search(text)
        if match is not None:
            direction = match.group("direction").casefold()
            return text[: match.start()].rstrip(), _DIRECTION_ALIASES[direction]
    return text, None
