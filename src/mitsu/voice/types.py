"""Typed contracts for MITSU voice commands."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto

import numpy as np


@dataclass(frozen=True, slots=True)
class AudioClip:
    """A mono, in memory microphone recording."""

    samples: np.ndarray
    sample_rate_hz: int



class IntentAction(Enum):
    """Day 3 voice actions"""

    SHOW = auto()
    GRAB = auto()


class MonitorDestination(Enum):
    """Parsed now, executed during Day 4"""

    LEFT = auto()
    RIGHT = auto()



@dataclass(frozen=True, slots=True)
class VoiceIntent:
    """A deterministic fixed-grammar command"""

    action: IntentAction
    app_name: str
    destination: MonitorDestination | None



@dataclass(frozen=True, slots=True)
class Transcription:
    """An OpenAI transcription response."""

    text: str
    latency_ms: float



@dataclass(frozen=True, slots=True)
class VoiceResult:
    """A completed transcription and optional parsed local intent."""

    transcription: Transcription | None
    intent: VoiceIntent | None
    error_message: str | None