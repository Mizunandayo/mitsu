"""Index-middle pointer control with a deliberate downward finger press."""

from __future__ import annotations

from dataclasses import dataclass
from math import hypot

from mitsu.gestures.pinch import HandLandmarks
from mitsu.perception.one_euro import Point2D


@dataclass(frozen=True, slots=True)
class AirClickReading:
    """Pointer-pose state and one-shot pointer action edges."""

    is_pointing: bool
    is_click_pose: bool
    blocks_window_grip: bool
    click_triggered: bool
    back_triggered: bool
    forward_triggered: bool


class AirClickDetector:
    """Click by lowering close index-middle fingertips toward the wrist."""

    def __init__(
        self,
        *,
        pointer_extension_ratio: float,
        fingers_close_ratio: float,
        fingers_release_ratio: float,
        minimum_press_downward_ratio: float,
        minimum_click_pose_frames: int,
        ring_extension_ratio: float,
        minimum_forward_pose_frames: int,
        pinky_extension_ratio: float,
        minimum_back_pose_frames: int,
    ) -> None:
        if pointer_extension_ratio <= 1.0:
            raise ValueError("pointer_extension_ratio must exceed one")
        if not 0.0 < fingers_close_ratio < fingers_release_ratio < 1.0:
            raise ValueError("finger thresholds must satisfy 0 < close < release < 1")
        if minimum_press_downward_ratio <= 0.0:
            raise ValueError("press downward threshold must be positive")
        if minimum_click_pose_frames < 2:
            raise ValueError("click pose requires at least two frames")
        if ring_extension_ratio <= 1.0 or pinky_extension_ratio <= 1.0:
            raise ValueError("side-button extension ratios must exceed one")
        if minimum_forward_pose_frames < 2 or minimum_back_pose_frames < 2:
            raise ValueError("side-button poses require at least two frames")

        self._pointer_extension_ratio = pointer_extension_ratio
        self._fingers_close_ratio = fingers_close_ratio
        self._fingers_release_ratio = fingers_release_ratio
        self._minimum_press_downward_ratio = minimum_press_downward_ratio
        self._minimum_click_pose_frames = minimum_click_pose_frames
        self._ring_extension_ratio = ring_extension_ratio
        self._minimum_forward_pose_frames = minimum_forward_pose_frames
        self._pinky_extension_ratio = pinky_extension_ratio
        self._minimum_back_pose_frames = minimum_back_pose_frames
        self.reset()

    def reset(self) -> None:
        """Clear all action latches after tracking loss or a window drag."""

        self._fingers_are_close = False
        self._click_pose_frames = 0
        self._press_baseline_heights: tuple[float, float] | None = None
        self._awaiting_press_release = False
        self._back_pose_frames = 0
        self._back_armed = True
        self._forward_pose_frames = 0
        self._forward_armed = True

    def update(
        self,
        landmarks: HandLandmarks | None,
        _timestamp_seconds: float,
    ) -> AirClickReading:
        """Return actions for a stable two-finger pose and downward press."""

        if landmarks is None or landmarks.middle_tip is None:
            self.reset()
            return self._empty_reading()

        palm_span = self._distance(landmarks.wrist, landmarks.middle_mcp)
        if palm_span <= 1e-6:
            self.reset()
            return self._empty_reading()

        finger_ratio = (
            self._distance(landmarks.index_tip, landmarks.middle_tip) / palm_span
        )
        if self._fingers_are_close:
            self._fingers_are_close = finger_ratio < self._fingers_release_ratio
        else:
            self._fingers_are_close = finger_ratio <= self._fingers_close_ratio

        index_extension = self._distance(landmarks.index_tip, landmarks.wrist)
        is_pointing = index_extension / palm_span >= self._pointer_extension_ratio
        # A full fist is rejected separately by the app, so this close pair can
        # be slightly curled without becoming a window-grab gesture.
        is_click_pose = self._fingers_are_close
        click_triggered = self._downward_press_click(
            landmarks,
            palm_span,
            is_click_pose,
        )
        back_triggered, forward_triggered = self._side_buttons(
            landmarks,
            palm_span,
            is_click_pose,
        )

        return AirClickReading(
            is_pointing=is_pointing,
            is_click_pose=is_click_pose,
            blocks_window_grip=is_click_pose,
            click_triggered=click_triggered,
            back_triggered=back_triggered,
            forward_triggered=forward_triggered,
        )

    def _downward_press_click(
        self,
        landmarks: HandLandmarks,
        palm_span: float,
        is_click_pose: bool,
    ) -> bool:
        if not is_click_pose:
            self._clear_click_latch()
            return False

        self._click_pose_frames += 1
        if self._click_pose_frames < self._minimum_click_pose_frames:
            return False

        fingertip_heights = self._fingertip_heights_relative_to_wrist(landmarks)
        if self._press_baseline_heights is None:
            self._press_baseline_heights = fingertip_heights
            return False

        # Image Y grows downward. Measuring fingertip height relative to the
        # wrist cancels whole-hand movement. Use the smaller dip so both the
        # index and middle fingertips must move down for a click.
        index_press_ratio = (
            fingertip_heights[0] - self._press_baseline_heights[0]
        ) / palm_span
        middle_press_ratio = (
            fingertip_heights[1] - self._press_baseline_heights[1]
        ) / palm_span
        press_ratio = min(index_press_ratio, middle_press_ratio)
        if self._awaiting_press_release:
            if press_ratio <= self._minimum_press_downward_ratio * 0.35:
                self._awaiting_press_release = False
                self._press_baseline_heights = fingertip_heights
            return False

        if press_ratio >= self._minimum_press_downward_ratio:
            self._awaiting_press_release = True
            return True

        return False

    def _side_buttons(
        self,
        landmarks: HandLandmarks,
        palm_span: float,
        is_click_pose: bool,
    ) -> tuple[bool, bool]:
        is_ring_raised = self._is_finger_raised(
            landmarks.ring_mcp,
            landmarks.ring_tip,
            landmarks.wrist,
            palm_span,
            self._ring_extension_ratio,
        )
        is_pinky_raised = self._is_finger_raised(
            landmarks.pinky_mcp,
            landmarks.pinky_tip,
            landmarks.wrist,
            palm_span,
            self._pinky_extension_ratio,
        )
        is_back_pose = is_click_pose and is_pinky_raised and not is_ring_raised
        is_forward_pose = is_click_pose and is_ring_raised and not is_pinky_raised

        self._back_pose_frames = self._advance_side_pose(
            is_back_pose,
            self._back_pose_frames,
            "back",
        )
        self._forward_pose_frames = self._advance_side_pose(
            is_forward_pose,
            self._forward_pose_frames,
            "forward",
        )
        back_triggered = (
            self._back_armed
            and self._back_pose_frames >= self._minimum_back_pose_frames
        )
        forward_triggered = (
            self._forward_armed
            and self._forward_pose_frames >= self._minimum_forward_pose_frames
        )
        if back_triggered:
            self._back_armed = False
        if forward_triggered:
            self._forward_armed = False
        return back_triggered, forward_triggered

    def _advance_side_pose(self, active: bool, frames: int, direction: str) -> int:
        if active:
            return frames + 1
        if direction == "back":
            self._back_armed = True
        else:
            self._forward_armed = True
        return 0

    def _clear_click_latch(self) -> None:
        self._click_pose_frames = 0
        self._press_baseline_heights = None
        self._awaiting_press_release = False

    @staticmethod
    def _fingertip_heights_relative_to_wrist(
        landmarks: HandLandmarks,
    ) -> tuple[float, float]:
        assert landmarks.middle_tip is not None
        return (
            landmarks.index_tip.y - landmarks.wrist.y,
            landmarks.middle_tip.y - landmarks.wrist.y,
        )

    @staticmethod
    def _is_finger_raised(
        metacarpophalangeal_joint: Point2D | None,
        fingertip: Point2D | None,
        wrist: Point2D,
        palm_span: float,
        extension_ratio_threshold: float,
    ) -> bool:
        if metacarpophalangeal_joint is None or fingertip is None:
            return False
        extension_ratio = AirClickDetector._distance(fingertip, wrist) / palm_span
        return (
            extension_ratio >= extension_ratio_threshold
            and fingertip.y < metacarpophalangeal_joint.y
        )

    @staticmethod
    def _empty_reading() -> AirClickReading:
        return AirClickReading(False, False, False, False, False, False)

    @staticmethod
    def _distance(first: Point2D, second: Point2D) -> float:
        return hypot(first.x - second.x, first.y - second.y)
