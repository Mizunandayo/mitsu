"""Pure gesture state machine for the Day-1 drag interaction."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, auto


class GestureState(Enum):
    """The lifecycle of one hand-driven drag."""

    IDLE = auto()
    TRACKING = auto()
    GRIPPED = auto()
    RELEASING = auto()


class GestureEffect(Enum):
    """Side effects requested from the application composition layer."""

    BEGIN_GRIP = auto()
    MOVE_GRIPPED_WINDOW = auto()
    RELEASE_GRIPPED_WINDOW = auto()


@dataclass(frozen=True, slots=True)
class GestureInput:
    """A normalized frame-level gesture observation."""

    hand_present: bool
    is_pinched: bool
    target_available: bool


@dataclass(frozen=True, slots=True)
class GestureTransition:
    """A deterministic state transition and requested application effects."""

    previous_state: GestureState
    current_state: GestureState
    effects: tuple[GestureEffect, ...]


class GestureStateMachine:
    """Translate stable pinch observations into drag lifecycle effects."""

    def __init__(self) -> None:
        self._state = GestureState.IDLE

    @property
    def state(self) -> GestureState:
        """Return the current state."""

        return self._state

    def reset(self) -> GestureTransition:
        """Safely end a drag if the application is interrupted."""

        previous_state = self._state
        effects: tuple[GestureEffect, ...] = ()

        if previous_state is GestureState.GRIPPED:
            effects = (GestureEffect.RELEASE_GRIPPED_WINDOW,)

        self._state = GestureState.IDLE
        return GestureTransition(previous_state, self._state, effects)

    def step(self, observation: GestureInput) -> GestureTransition:
        """Advance one frame without performing OS operations."""

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
                effects = (GestureEffect.BEGIN_GRIP,)

        elif self._state is GestureState.GRIPPED:
            if not observation.hand_present or not observation.is_pinched:
                self._state = GestureState.RELEASING
                effects = (GestureEffect.RELEASE_GRIPPED_WINDOW,)
            else:
                effects = (GestureEffect.MOVE_GRIPPED_WINDOW,)

        elif self._state is GestureState.RELEASING:
            self._state = (
                GestureState.TRACKING if observation.hand_present else GestureState.IDLE
            )

        return GestureTransition(previous_state, self._state, effects)
