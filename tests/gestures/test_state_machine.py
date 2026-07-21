from __future__ import annotations

import pytest

from mitsu.gestures.state_machine import (
    GestureEffect,
    GestureInput,
    GestureState,
    GestureStateMachine,
    GripSource,
)


def test_hand_appearance_transitions_idle_to_tracking() -> None:
    subject = GestureStateMachine()

    transition = subject.step(GestureInput(True, False, False))

    assert transition.current_state is GestureState.TRACKING
    assert transition.effects == ()


def test_hand_pinch_starts_and_moves_grip() -> None:
    subject = GestureStateMachine()
    subject.step(GestureInput(True, False, False))

    begin = subject.step(GestureInput(True, True, True))
    move = subject.step(GestureInput(True, True, True))

    assert begin.effects == (GestureEffect.BEGIN_HAND_GRIP,)
    assert subject.grip_source is GripSource.HAND
    assert move.effects == (GestureEffect.MOVE_GRIPPED_WINDOW,)


def test_hand_release_releases_grip() -> None:
    subject = GestureStateMachine()
    subject.step(GestureInput(True, False, False))
    subject.step(GestureInput(True, True, True))

    release = subject.step(GestureInput(True, False, True))

    assert release.current_state is GestureState.RELEASING
    assert release.effects == (GestureEffect.RELEASE_GRIPPED_WINDOW,)


def test_voice_lock_enters_gripped_state_without_a_hand() -> None:
    subject = GestureStateMachine()

    transition = subject.begin_voice_grip()

    assert transition.current_state is GestureState.GRIPPED
    assert transition.effects == (GestureEffect.BEGIN_VOICE_GRIP,)
    assert subject.grip_source is GripSource.VOICE


def test_voice_grip_waits_for_hand_before_movement() -> None:
    subject = GestureStateMachine()
    subject.begin_voice_grip()

    transition = subject.step(GestureInput(False, False, False))

    assert transition.current_state is GestureState.GRIPPED
    assert transition.effects == ()


def test_voice_grip_moves_when_hand_arrives() -> None:
    subject = GestureStateMachine()
    subject.begin_voice_grip()

    transition = subject.step(GestureInput(True, False, False))

    assert transition.effects == (GestureEffect.MOVE_GRIPPED_WINDOW,)


def test_voice_grip_releases_when_hand_leaves_after_movement() -> None:
    subject = GestureStateMachine()
    subject.begin_voice_grip()
    subject.step(GestureInput(True, False, False))

    transition = subject.step(GestureInput(False, False, False))

    assert transition.current_state is GestureState.RELEASING
    assert transition.effects == (GestureEffect.RELEASE_GRIPPED_WINDOW,)


def test_voice_lock_cannot_replace_active_grip() -> None:
    subject = GestureStateMachine()
    subject.begin_voice_grip()

    with pytest.raises(RuntimeError, match="active grip"):
        subject.begin_voice_grip()
