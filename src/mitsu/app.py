"""MITSU Day-2 local hand-driven window movement application."""

from __future__ import annotations

from pathlib import Path

import cv2
from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication

from mitsu.config import load_settings
from mitsu.control.coordinate_mapper import HitTestProjector, ScreenPoint
from mitsu.control.drag_runtime import DragRuntime
from mitsu.control.target_latch import TargetLatch
from mitsu.control.window_manager import WindowManager
from mitsu.gestures.pinch import PinchDetector
from mitsu.gestures.state_machine import (
    GestureEffect,
    GestureInput,
    GestureState,
    GestureStateMachine,
)
from mitsu.logging_setup import configure_logging
from mitsu.overlay.debug_overlay import DebugOverlay
from mitsu.overlay.live_pointer import LivePointerOverlay
from mitsu.perception.camera import Camera
from mitsu.perception.hand_tracker import HandTracker
from mitsu.perception.one_euro import OneEuroFilter
from mitsu.security import enable_per_monitor_dpi_awareness, verify_model_integrity
from mitsu.voice.asr import OpenAITranscriber
from mitsu.voice.audio_capture import PushToTalkCapture
from mitsu.voice.service import VoiceService


def main() -> int:
    """Run the local Day-2 cross-monitor drag loop."""

    project_root = Path(__file__).resolve().parents[2]
    load_dotenv(project_root / ".env")
    logger = configure_logging()

    try:
        enable_per_monitor_dpi_awareness()

        settings = load_settings(project_root / "config" / "default.toml")
        model_path = project_root / "models" / "hand_landmarker.task"
        pin_path = project_root / "models" / "hand_landmarker.task.sha256"
        verify_model_integrity(model_path, pin_path)

        runtime = DragRuntime.discover(settings)
        projector = HitTestProjector(runtime.layout.virtual_bounds)
        target_latch = TargetLatch(grace_period_seconds=0.18)
        window_manager = WindowManager()
        voice_capture = PushToTalkCapture(
            sample_rate_hz=settings.voice.sample_rate_hz,
            maximum_duration_seconds=settings.voice.maximum_recording_seconds,
        )
        voice_service = VoiceService(
            OpenAITranscriber.from_environment(
                model=settings.voice.transcription_model,
                language=settings.voice.language,
                prompt=settings.voice.transcription_prompt,
            )
        )
        voice_status = "Ready"
        state_machine = GestureStateMachine()
        pinch_detector = PinchDetector(
            settings.gesture.pinch.engage_ratio,
            settings.gesture.pinch.release_ratio,
        )
        smoothing_filter = OneEuroFilter(
            settings.filter.minimum_cutoff_hz,
            settings.filter.beta,
            settings.filter.derivative_cutoff_hz,
        )
        overlay = DebugOverlay(
            project_root / "assets" / "fonts" / "Poppins-SemiBold.ttf"
        )
        qt_application = QApplication.instance() or QApplication([])
        live_pointer = LivePointerOverlay(
            project_root / "assets" / "fonts" / "Poppins-SemiBold.ttf"
        )

        logger.info(
            "MITSU started with virtual desktop bounds %s",
            runtime.layout.virtual_bounds,
        )

        with Camera() as camera, HandTracker(model_path) as hand_tracker:
            cv2.namedWindow("MITSU Debug", cv2.WINDOW_NORMAL)

            while True:
                frame = camera.read()
                tracked_hand = hand_tracker.detect(
                    frame.bgr,
                    frame.timestamp_milliseconds,
                )

                filtered_point = None
                pinch_reading = pinch_detector.update(
                    None if tracked_hand is None else tracked_hand.pinch_landmarks
                )

                if tracked_hand is None:
                    smoothing_filter.reset()
                else:
                    filtered_point = smoothing_filter.filter(
                        tracked_hand.control_point,
                        frame.timestamp_seconds,
                    )

                candidate = None
                projected_point: ScreenPoint | None = (
                    None
                    if filtered_point is None
                    else projector.project(filtered_point)
                )
                if (
                    projected_point is not None
                    and state_machine.state is GestureState.TRACKING
                ):
                    live_candidate = window_manager.target_at(projected_point)
                    candidate = target_latch.resolve(
                        live_candidate,
                        pinch_reading.is_pinched,
                        frame.timestamp_seconds,
                    )

                transition = state_machine.step(
                    GestureInput(
                        hand_present=tracked_hand is not None,
                        is_pinched=pinch_reading.is_pinched,
                        target_available=candidate is not None,
                    )
                )

                for effect in transition.effects:
                    if effect is GestureEffect.BEGIN_GRIP:
                        assert candidate is not None
                        assert filtered_point is not None
                        prepared_rect = window_manager.prepare_for_drag(
                            candidate.handle
                        )
                        runtime.begin_grip(
                            handle=candidate.handle,
                            position=prepared_rect.position,
                            width=prepared_rect.width,
                            height=prepared_rect.height,
                            hand_position=filtered_point,
                            timestamp_seconds=frame.timestamp_seconds,
                        )
                        target_latch.clear()

                    elif effect is GestureEffect.MOVE_GRIPPED_WINDOW:
                        assert filtered_point is not None
                        handle = runtime.active_handle
                        assert handle is not None

                        next_position = runtime.move(
                            filtered_point,
                            frame.timestamp_seconds,
                        )
                        window_manager.move_window(handle, next_position)

                    elif effect is GestureEffect.RELEASE_GRIPPED_WINDOW:
                        runtime.release()
                        target_latch.clear()

                if tracked_hand is None:
                    target_latch.clear()

                voice_result = voice_service.poll()
                if voice_result is not None:
                    if voice_result.error_message is not None:
                        voice_status = f"Error: {voice_result.error_message}"
                    elif voice_result.intent is None:
                        voice_status = "Command not recognized"
                    else:
                        target = window_manager.find_window(
                            voice_result.intent.app_name
                        )
                        if target is None:
                            voice_status = f"Not found: {voice_result.intent.app_name}"
                        elif voice_result.intent.destination is not None:
                            voice_status = "Destination movement is Day 4"
                        else:
                            try:
                                restored = window_manager.restore_and_focus(
                                    target.handle
                                )
                                voice_status = f"Showing: {restored.title}"
                            except RuntimeError:
                                voice_status = "Target changed before action"

                if projected_point is None:
                    live_pointer.hide()
                else:
                    live_pointer.show_at(
                        projected_point,
                        None if candidate is None else candidate.title,
                    )
                qt_application.processEvents()

                rendered = overlay.draw(
                    frame.bgr,
                    tracked_hand,
                    state_machine.state,
                    runtime.active_handle,
                    None if candidate is None else candidate.title,
                    projected_point,
                    voice_status,
                )
                cv2.imshow("MITSU Debug", rendered)

                key = cv2.waitKey(1) & 0xFF
                if key == ord("v"):
                    try:
                        if voice_capture.is_recording:
                            clip = voice_capture.stop()
                            voice_status = (
                                "Transcribing..."
                                if voice_service.submit(clip)
                                else "Command already processing"
                            )
                        else:
                            voice_capture.start()
                            voice_status = "Recording - press V to send"
                    except RuntimeError as error:
                        voice_status = f"Audio error: {type(error).__name__}"
                if key in (ord("q"), 27):
                    break

    except Exception:
        logger.exception("MITSU stopped because of an unrecoverable error")
        return 1
    finally:
        if "runtime" in locals():
            runtime.release()
        if "live_pointer" in locals():
            live_pointer.close()
        if "voice_capture" in locals():
            voice_capture.close()
        if "voice_service" in locals():
            voice_service.close()
        cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
