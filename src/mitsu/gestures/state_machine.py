"""Pure fusion state machine for hand and voice window control."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class GestureState(Enum):
    """The lifecycle of an active window interaction."""

    IDLE = auto()
    TRACKING = auto()
    GRIPPED = auto()
    RELEASING = auto()


class GripSource(Enum):
    """The source that selected the active window target."""

    HAND = auto()
    VOICE = auto()


class GestureEffect(Enum):
    """Side effects requested from the app composition layer."""

    BEGIN_HAND_GRIP = auto()
    BEGIN_VOICE_GRIP = auto()
    MOVE_GRIPPED_WINDOW = auto()
    RELEASE_GRIPPED_WINDOW = auto()


@dataclass(frozen=True, slots=True)
class GestureInput:
    """A normalized frame-level hand observation."""

    hand_present: bool
    is_pinched: bool
    target_available: bool


@dataclass(frozen=True, slots=True)
class GestureTransition:
    """A deterministic transition and requested application effects."""

    previous_state: GestureState
    current_state: GestureState
    effects: tuple[GestureEffect, ...]


class GestureStateMachine:
    """Fuse hand grip and voice target-lock into one interaction lifecycle."""

    def __init__(self) -> None:
        self._state = GestureState.IDLE
        self._grip_source: GripSource | None = None
        self._voice_has_seen_hand = False

    @property
    def state(self) -> GestureState:
        """Return the current interaction state."""

        return self._state

    @property
    def grip_source(self) -> GripSource | None:
        """Return how the current target was selected."""

        return self._grip_source

    def begin_voice_grip(self) -> GestureTransition:
        """Lock a named target without requiring hand hit-testing."""

        if self._state is GestureState.GRIPPED:
            raise RuntimeError("Cannot replace an active grip")

        previous_state = self._state
        self._state = GestureState.GRIPPED
        self._grip_source = GripSource.VOICE
        self._voice_has_seen_hand = False

        return GestureTransition(
            previous_state=previous_state,
            current_state=self._state,
            effects=(GestureEffect.BEGIN_VOICE_GRIP,),
        )

    def reset(self) -> GestureTransition:
        """Safely clear all active interaction state."""

        previous_state = self._state
        effects: tuple[GestureEffect, ...] = ()

        if self._state is GestureState.GRIPPED:
            effects = (GestureEffect.RELEASE_GRIPPED_WINDOW,)

        self._state = GestureState.IDLE
        self._grip_source = None
        self._voice_has_seen_hand = False

        return GestureTransition(previous_state, self._state, effects)

    def step(self, observation: GestureInput) -> GestureTransition:
        """Advance one frame without performing I/O or Win32 calls."""

        previous_state = self._state
        effects: tuple[GestureEffect, ...] = ()

        if self._state is GestureState.IDLE:
            if observation.hand_present:
                self._state = GestureState.TRACKING

        elif self._state is GestureState.TRACKING:
            if not observation.hand_present:
                self._state = GestureState.IDLE
            elif observation.is_pinched and observation.target_available:
                self._state = GestureState.GRIPPED
                self._grip_source = GripSource.HAND
                effects = (GestureEffect.BEGIN_HAND_GRIP,)

        elif self._state is GestureState.GRIPPED:
            if self._grip_source is GripSource.HAND:
                if not observation.hand_present or not observation.is_pinched:
                    self._state = GestureState.RELEASING
                    effects = (GestureEffect.RELEASE_GRIPPED_WINDOW,)
                else:
                    effects = (GestureEffect.MOVE_GRIPPED_WINDOW,)

            elif self._grip_source is GripSource.VOICE:
                if observation.hand_present:
                    self._voice_has_seen_hand = True
                    effects = (GestureEffect.MOVE_GRIPPED_WINDOW,)
                elif self._voice_has_seen_hand:
                    self._state = GestureState.RELEASING
                    effects = (GestureEffect.RELEASE_GRIPPED_WINDOW,)

        elif self._state is GestureState.RELEASING:
            self._state = (
                GestureState.TRACKING
                if observation.hand_present
                else GestureState.IDLE
            )
            self._grip_source = None
            self._voice_has_seen_hand = False

        return GestureTransition(previous_state, self._state, effects)