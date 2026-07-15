from __future__ import annotations
from mitsu.gestures.state_machine import (
    GestureEffect,
    GestureInput,
    GestureState,
    GestureStateMachine,
)



def test_hand_appearance_transitions_idle_to_tracking() -> None:
    subject = GestureStateMachine()

    transition = subject.step(GestureInput(True, False, False))

    assert transition.current_state is GestureState.TRACKING
    assert transition.effects == ()


def test_pinch_with_target_starts_grip_then_moves() -> None:
    subject = GestureStateMachine()
    subject.step(GestureInput(True, False, False))

    grip = subject.step(GestureInput(True, True, True))
    move = subject.step(GestureInput(True, True, True))

    assert grip.current_state is GestureState.GRIPPED
    assert grip.effects == (GestureEffect.BEGIN_GRIP,)
    assert move.effects == (GestureEffect.MOVE_GRIPPED_WINDOW,)


def test_pinch_without_target_does_not_grip() -> None:
    subject = GestureStateMachine()
    subject.step(GestureInput(True, False, False))

    transition = subject.step(GestureInput(True, True, False))

    assert transition.current_state is GestureState.TRACKING
    assert transition.effects == ()


def test_release_emits_one_release_effect() -> None:
    subject = GestureStateMachine()
    subject.step(GestureInput(True, False, False))
    subject.step(GestureInput(True, True, True))

    release = subject.step(GestureInput(True, False, True))
    settle = subject.step(GestureInput(True, False, False))

    assert release.current_state is GestureState.RELEASING
    assert release.effects == (GestureEffect.RELEASE_GRIPPED_WINDOW,)
    assert settle.current_state is GestureState.TRACKING
    assert settle.effects == ()


def test_tracking_loss_during_drag_releases_window() -> None:
    subject = GestureStateMachine()
    subject.step(GestureInput(True, False, False))
    subject.step(GestureInput(True, True, True))

    transition = subject.step(GestureInput(False, False, False))

    assert transition.current_state is GestureState.RELEASING
    assert transition.effects == (GestureEffect.RELEASE_GRIPPED_WINDOW,)