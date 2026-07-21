"""MITSU Day-2 local hand-driven window movement application."""

from __future__ import annotations

import os
import time
from pathlib import Path

import cv2
from dotenv import load_dotenv
from PySide6.QtWidgets import QApplication

from mitsu.cognition.cloud_reasoner import OpenAIReasoner
from mitsu.cognition.tool_registry import ToolRegistry
from mitsu.config import load_settings
from mitsu.control.coordinate_mapper import (
    CalibratedPointerProjector,
    HitTestProjector,
    ScreenPoint,
)
from mitsu.control.drag_runtime import DragRuntime
from mitsu.control.kill_switch import KillSwitch
from mitsu.control.monitor_layout import Monitor
from mitsu.control.mouse_controller import MouseController
from mitsu.control.target_latch import TargetLatch
from mitsu.control.window_animator import WindowGlide
from mitsu.control.window_manager import WindowManager
from mitsu.gestures.air_click import AirClickDetector
from mitsu.gestures.fist import FistGripDetector
from mitsu.gestures.palm_swipe import PalmSwipeDetector, PalmSwipeReading
from mitsu.gestures.pinch import PinchDetector, PinchReading
from mitsu.gestures.state_machine import (
    GestureEffect,
    GestureInput,
    GestureState,
    GestureStateMachine,
)
from mitsu.gestures.three_finger_swipe import ThreeFingerMinimizeDetector
from mitsu.gestures.v_sign import VSignDetector
from mitsu.logging_setup import configure_logging
from mitsu.observability.metrics import JitterMeter, RollingMetric
from mitsu.overlay.debug_overlay import DebugOverlay
from mitsu.overlay.live_pointer import LivePointerOverlay
from mitsu.overlay.microphone_selector import MicrophoneSelector
from mitsu.overlay.window_shelf import WindowShelf
from mitsu.perception.camera import Camera
from mitsu.perception.hand_tracker import HandTracker
from mitsu.perception.one_euro import OneEuroFilter
from mitsu.security import enable_per_monitor_dpi_awareness, verify_model_integrity
from mitsu.voice.asr import OpenAITranscriber
from mitsu.voice.audio_capture import PushToTalkCapture
from mitsu.voice.service import VoiceService
from mitsu.voice.types import MonitorDestination


def monitor_for_destination(
    destination: MonitorDestination,
    monitors: tuple[object, ...],
) -> Monitor:
    """Resolve a voice direction against physical monitor positions at startup."""

    if destination is MonitorDestination.LEFT:
        return min(monitors, key=lambda monitor: monitor.bounds.left)

    if destination is MonitorDestination.RIGHT:
        return max(monitors, key=lambda monitor: monitor.bounds.right)

    if destination is MonitorDestination.UP:
        return min(monitors, key=lambda monitor: monitor.bounds.top)

    return max(monitors, key=lambda monitor: monitor.bounds.bottom)


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
        hit_test_projector = HitTestProjector(runtime.layout.primary_monitor.bounds)
        pointer_projector = CalibratedPointerProjector(
            runtime.layout.primary_monitor.bounds,
            camera_left=settings.pointer.camera_left,
            camera_top=settings.pointer.camera_top,
            camera_right=settings.pointer.camera_right,
            camera_bottom=settings.pointer.camera_bottom,
        )
        target_latch = TargetLatch(grace_period_seconds=0.18)
        window_manager = WindowManager()
        mouse_controller = MouseController()
        kill_switch = KillSwitch()
        window_glide = WindowGlide()
        glide_handle: int | None = None

        def move_window_to_destination(handle: int, destination: str) -> bool:
            """Start a bounded glide for a validated left/right tool request."""

            nonlocal glide_handle

            try:
                requested_destination = MonitorDestination[destination.upper()]
            except KeyError:
                return False

            target = window_manager.find_window_by_handle(handle)
            if target is None:
                return False

            monitor = monitor_for_destination(
                requested_destination,
                runtime.layout.monitors,
            )
            window_glide.start(
                target.rect,
                monitor.bounds,
                time.perf_counter(),
            )
            glide_handle = target.handle
            return True

        tool_registry = ToolRegistry(
            window_manager=window_manager,
            move_to_destination=move_window_to_destination,
        )
        cloud_reasoner = OpenAIReasoner.from_environment(
            settings=settings.cloud,
            tool_registry=tool_registry,
        )
        perception_latency_ms = RollingMetric(settings.observability.maximum_samples)
        voice_latency_ms = RollingMetric(settings.observability.maximum_samples)
        jitter_meter = JitterMeter(settings.observability.maximum_samples)
        voice_locked_target = None
        voice_capture = PushToTalkCapture(
            sample_rate_hz=settings.voice.sample_rate_hz,
            maximum_duration_seconds=settings.voice.maximum_recording_seconds,
            minimum_signal_rms=settings.voice.minimum_signal_rms,
        )
        try:
            microphone_devices = voice_capture.input_devices()
        except RuntimeError as error:
            microphone_devices = ()
            microphone_enumeration_error = str(error)
        else:
            microphone_enumeration_error = None
        microphone_names = {device.index: device.name for device in microphone_devices}
        api_key_available = bool(os.getenv("OPENAI_API_KEY", "").strip())
        voice_service = (
            VoiceService(
                OpenAITranscriber.from_environment(
                    model=settings.voice.transcription_model,
                    language=settings.voice.language,
                    prompt=settings.voice.transcription_prompt,
                )
            )
            if api_key_available
            else None
        )
        voice_status = "Ready" if api_key_available else "Local controls ready"
        state_machine = GestureStateMachine()
        pinch_detector = PinchDetector(
            settings.gesture.pinch.engage_ratio,
            settings.gesture.pinch.release_ratio,
            settings.gesture.pinch.release_debounce_frames,
        )
        fist_detector = FistGripDetector(
            engage_tip_distance_ratio=(settings.gesture.fist.engage_tip_distance_ratio),
            release_tip_distance_ratio=(
                settings.gesture.fist.release_tip_distance_ratio
            ),
            release_debounce_frames=settings.gesture.fist.release_debounce_frames,
        )
        air_click_detector = AirClickDetector(
            pointer_extension_ratio=settings.click.pointer_extension_ratio,
            fingers_close_ratio=settings.click.fingers_close_ratio,
            fingers_release_ratio=settings.click.fingers_release_ratio,
            minimum_press_downward_ratio=(settings.click.minimum_press_downward_ratio),
            minimum_click_pose_frames=settings.click.minimum_click_pose_frames,
            ring_extension_ratio=settings.click.ring_extension_ratio,
            minimum_forward_pose_frames=settings.click.minimum_forward_pose_frames,
            pinky_extension_ratio=settings.click.pinky_extension_ratio,
            minimum_back_pose_frames=settings.click.minimum_back_pose_frames,
        )
        palm_swipe_detector = PalmSwipeDetector(
            open_palm_extension_ratio=settings.minimize.open_palm_extension_ratio,
            minimum_open_palm_frames=settings.minimize.minimum_open_palm_frames,
            minimum_downward_distance_ratio=(
                settings.minimize.minimum_downward_distance_ratio
            ),
            downward_velocity_ratio_per_second=(
                settings.minimize.downward_velocity_ratio_per_second
            ),
        )
        minimize_detector = ThreeFingerMinimizeDetector(
            triad_close_ratio=settings.minimize.triad_close_ratio,
            triad_extension_ratio=settings.minimize.triad_extension_ratio,
            folded_pinky_extension_ratio=(
                settings.minimize.folded_pinky_extension_ratio
            ),
            minimum_thumb_index_ratio=settings.minimize.minimum_thumb_index_ratio,
            minimum_pose_frames=settings.minimize.minimum_pose_frames,
            minimum_downward_distance_ratio=(
                settings.minimize.minimum_downward_distance_ratio
            ),
            downward_velocity_ratio_per_second=(
                settings.minimize.downward_velocity_ratio_per_second
            ),
        )
        v_sign_detector = VSignDetector(
            extension_ratio=settings.gesture.v_sign.extension_ratio,
            folded_finger_ratio=settings.gesture.v_sign.folded_finger_ratio,
            minimum_finger_gap_ratio=(settings.gesture.v_sign.minimum_finger_gap_ratio),
            minimum_hold_frames=settings.gesture.v_sign.minimum_hold_frames,
        )
        smoothing_filter = OneEuroFilter(
            settings.filter.minimum_cutoff_hz,
            settings.filter.beta,
            settings.filter.derivative_cutoff_hz,
        )
        overlay = DebugOverlay(
            project_root / "assets" / "fonts" / "Poppins-SemiBold.ttf"
        )
        debug_overlay_interval_seconds = 1.0 / 15.0
        next_debug_overlay_at = 0.0
        qt_application = QApplication.instance() or QApplication([])
        live_pointer = LivePointerOverlay(
            project_root / "assets" / "fonts" / "Poppins-SemiBold.ttf"
        )
        window_shelf = WindowShelf(
            project_root / "assets" / "fonts" / "Poppins-SemiBold.ttf"
        )
        microphone_selector = MicrophoneSelector(
            project_root / "assets" / "fonts" / "Poppins-SemiBold.ttf"
        )
        microphone_status = "Windows default microphone"
        shelf_opened_at: float | None = None
        shelf_timeout_seconds = 8.0

        logger.info(
            "MITSU started with %d monitor(s); virtual desktop bounds %s",
            len(runtime.layout.monitors),
            runtime.layout.virtual_bounds,
        )
        for index, monitor in enumerate(runtime.layout.monitors, start=1):
            logger.info(
                "Monitor %d: device=%s primary=%s position=(%d,%d) "
                "resolution=%dx%d dpi=%dx%d",
                index,
                monitor.device_name,
                monitor.is_primary,
                monitor.bounds.left,
                monitor.bounds.top,
                monitor.bounds.width,
                monitor.bounds.height,
                monitor.dpi_x,
                monitor.dpi_y,
            )

        with Camera() as camera, HandTracker(model_path) as hand_tracker:
            cv2.namedWindow("MITSU Debug", cv2.WINDOW_NORMAL)

            while True:
                if kill_switch.poll():
                    logger.warning(
                        "Kill switch activated; stopping automated window movement."
                    )
                    runtime.release()
                    window_glide.stop()
                    state_machine.reset()
                    target_latch.clear()
                    voice_locked_target = None
                    voice_status = "Automation stopped by kill switch"
                    break

                frame_started = time.perf_counter()
                frame = camera.read()
                if voice_capture.is_recording:
                    voice_status = (
                        f"Recording input: {voice_capture.signal_rms * 100:.1f}%"
                        " - press V to send"
                    )
                tracked_hand = hand_tracker.detect(
                    frame.bgr,
                    frame.timestamp_milliseconds,
                )

                filtered_point = None
                display_points = (
                    None if tracked_hand is None else tracked_hand.display_points
                )
                thumb_pinch_reading = pinch_detector.update(
                    None if tracked_hand is None else tracked_hand.pinch_landmarks
                )
                fist_reading = fist_detector.update(display_points)
                pinch_reading = PinchReading(
                    is_pinched=(thumb_pinch_reading.is_pinched or fist_reading.is_fist),
                    ratio=thumb_pinch_reading.ratio,
                )
                air_click_reading = air_click_detector.update(
                    None if tracked_hand is None else tracked_hand.pinch_landmarks,
                    frame.timestamp_seconds,
                )
                is_wide_open_palm = palm_swipe_detector.is_open_palm(
                    display_points,
                    minimum_extension_ratio=(
                        settings.minimize.maximize_open_palm_extension_ratio
                    ),
                )
                minimize_reading = minimize_detector.update(
                    display_points,
                    frame.timestamp_seconds,
                )
                v_sign_reading = v_sign_detector.update(display_points)
                if (
                    air_click_reading.blocks_window_grip
                    and not fist_reading.is_fist
                    and not minimize_reading.is_three_finger_pose
                    and state_machine.state is not GestureState.GRIPPED
                ):
                    # Any close index-middle pose exclusively owns this frame.
                    # It blocks new thumb-index window grips even when the
                    # hand is too curled to qualify as a pointer/click pose.
                    pinch_detector.reset()
                    pinch_reading = PinchReading(
                        is_pinched=False,
                        ratio=pinch_reading.ratio,
                    )
                if state_machine.state in {
                    GestureState.GRIPPED,
                    GestureState.RELEASING,
                }:
                    # While dragging, a thumb-index pinch can have four
                    # extended fingertips and resemble an open palm. Only the
                    # stricter wide-open pose may end this latched interaction.
                    palm_swipe_detector.reset()
                    palm_swipe_reading = PalmSwipeReading(
                        is_open_palm=is_wide_open_palm,
                        minimize_triggered=False,
                    )
                else:
                    palm_swipe_reading = palm_swipe_detector.update(
                        display_points,
                        frame.timestamp_seconds,
                    )
                if palm_swipe_reading.is_open_palm:
                    # An open palm owns the gesture stream. It can only
                    # produce a guarded downward minimize; it must never be
                    # reinterpreted as a click or thumb-index window grip.
                    pinch_detector.reset()
                    fist_detector.reset()
                    air_click_detector.reset()
                    minimize_detector.reset()
                    pinch_reading = PinchReading(
                        is_pinched=False,
                        ratio=pinch_reading.ratio,
                    )

                if tracked_hand is None:
                    smoothing_filter.reset()
                else:
                    filtered_point = smoothing_filter.filter(
                        tracked_hand.control_point,
                        frame.timestamp_seconds,
                    )
                    jitter_meter.record(
                        raw_x=tracked_hand.control_point.x,
                        raw_y=tracked_hand.control_point.y,
                        filtered_x=filtered_point.x,
                        filtered_y=filtered_point.y,
                    )

                candidate = None
                hit_test_point: ScreenPoint | None = (
                    None
                    if filtered_point is None
                    else hit_test_projector.project(filtered_point)
                )
                pointer_point: ScreenPoint | None = (
                    None
                    if filtered_point is None
                    else pointer_projector.project(filtered_point)
                )
                if (
                    hit_test_point is not None
                    and state_machine.state is GestureState.TRACKING
                ):
                    live_candidate = window_manager.target_at(hit_test_point)
                    candidate = target_latch.resolve(
                        live_candidate,
                        pinch_reading.is_pinched,
                        frame.timestamp_seconds,
                    )

                if (
                    v_sign_reading.activated
                    and runtime.active_handle is None
                    and not window_shelf.active
                ):
                    minimized_windows = window_manager.minimized_windows()
                    if not minimized_windows:
                        voice_status = "No minimized windows"
                    else:
                        window_shelf.present(
                            minimized_windows,
                            runtime.layout.primary_monitor.bounds,
                        )
                        shelf_opened_at = frame.timestamp_seconds
                        voice_status = "Choose a minimized window"

                if (
                    window_shelf.active
                    and shelf_opened_at is not None
                    and frame.timestamp_seconds - shelf_opened_at
                    >= shelf_timeout_seconds
                ):
                    window_shelf.dismiss()
                    shelf_opened_at = None
                    voice_status = "Window shelf timed out"

                shelf_click_consumed = False
                if (
                    window_shelf.active
                    and pointer_point is not None
                    and air_click_reading.click_triggered
                ):
                    shelf_click_consumed = True
                    selected_handle = window_shelf.selection_at(pointer_point)
                    if selected_handle is None:
                        voice_status = "Point at a minimized window"
                    else:
                        try:
                            restored = window_manager.restore_and_focus(selected_handle)
                        except RuntimeError:
                            voice_status = "Selected window is no longer available"
                        else:
                            voice_status = f"Showing: {restored.title}"
                        window_shelf.dismiss()
                        shelf_opened_at = None

                cursor_point: ScreenPoint | None = None
                if (
                    settings.click.enabled
                    and pointer_point is not None
                    and (
                        air_click_reading.is_pointing
                        or air_click_reading.blocks_window_grip
                    )
                    and not fist_reading.is_fist
                    and not palm_swipe_reading.is_open_palm
                    and not minimize_reading.is_three_finger_pose
                    and not window_shelf.active
                    and not shelf_click_consumed
                    and not pinch_reading.is_pinched
                    and state_machine.state is not GestureState.GRIPPED
                ):
                    if mouse_controller.move_to(pointer_point):
                        cursor_point = (
                            mouse_controller.current_position() or pointer_point
                        )
                        if air_click_reading.back_triggered:
                            mouse_controller.back_button()
                        elif air_click_reading.forward_triggered:
                            mouse_controller.forward_button()
                        elif air_click_reading.click_triggered:
                            mouse_controller.left_click()
                    else:
                        voice_status = "Pointer control unavailable"

                transition = state_machine.step(
                    GestureInput(
                        hand_present=tracked_hand is not None,
                        is_pinched=pinch_reading.is_pinched,
                        target_available=candidate is not None,
                    )
                )

                for effect in transition.effects:
                    if effect is GestureEffect.BEGIN_HAND_GRIP:
                        air_click_detector.reset()
                        palm_swipe_detector.reset()
                        minimize_detector.reset()
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
                        active_handle = runtime.active_handle
                        if is_wide_open_palm and active_handle is not None:
                            try:
                                window_manager.maximize_window(active_handle)
                            except RuntimeError:
                                logger.info(
                                    "Release target changed before maximization."
                                )
                        runtime.release()
                        target_latch.clear()

                if tracked_hand is None:
                    target_latch.clear()

                if (
                    settings.minimize.enabled
                    and minimize_reading.minimize_triggered
                    and not pinch_reading.is_pinched
                    and state_machine.state is GestureState.TRACKING
                ):
                    minimize_target = (
                        None
                        if hit_test_point is None
                        else window_manager.target_at(hit_test_point)
                    )
                    if minimize_target is None:
                        voice_status = "Point at an app window to minimize"
                    else:
                        try:
                            minimized = window_manager.minimize_window(
                                minimize_target.handle
                            )
                        except RuntimeError:
                            voice_status = "Selected window is no longer available"
                        else:
                            voice_status = f"Minimized: {minimized.title}"

                if glide_handle is not None:
                    glide_frame = window_glide.update(time.perf_counter())
                    if glide_frame is not None:
                        try:
                            window_manager.move_window(
                                glide_handle,
                                glide_frame.position,
                            )
                        except RuntimeError:
                            window_glide.stop()
                            glide_handle = None
                        else:
                            if glide_frame.is_complete:
                                glide_handle = None

                perception_latency_ms.record(
                    (time.perf_counter() - frame_started) * 1000.0
                )

                voice_result = None if voice_service is None else voice_service.poll()
                if voice_result is not None:
                    if voice_result.transcription is not None:
                        voice_latency_ms.record(voice_result.transcription.latency_ms)
                    if voice_result.error_message is not None:
                        voice_status = f"Error: {voice_result.error_message}"
                    elif voice_result.intent is None:
                        if voice_result.transcription is None:
                            voice_status = "Command not recognized"
                        else:
                            cloud_result = cloud_reasoner.resolve(
                                voice_result.transcription.text
                            )
                            heard = voice_result.transcription.text.strip()
                            voice_status = (
                                f"Heard: {heard[:36]} | {cloud_result.message}"
                            )
                    else:
                        target = window_manager.find_window(
                            voice_result.intent.app_name
                        )
                        if target is None:
                            voice_status = f"Not found: {voice_result.intent.app_name}"
                        else:
                            try:
                                restored = window_manager.restore_and_focus(
                                    target.handle
                                )
                                if voice_result.intent.destination is None:
                                    voice_status = f"Showing: {restored.title}"
                                elif move_window_to_destination(
                                    restored.handle,
                                    voice_result.intent.destination.name.casefold(),
                                ):
                                    voice_status = f"Moving: {restored.title}"
                                else:
                                    voice_status = "Destination movement was rejected"
                            except RuntimeError:
                                voice_status = "Target changed before action"

                display_point = cursor_point
                if display_point is None:
                    # Keep this marker visible whenever a hand is tracked.
                    # Outside click control it represents calibrated hand
                    # position; during click control it is the Windows cursor
                    # coordinate sent in the same frame.
                    display_point = pointer_point

                if display_point is None:
                    live_pointer.hide()
                else:
                    live_pointer.show_at(
                        display_point,
                        None if candidate is None else candidate.title,
                    )
                qt_application.processEvents()
                selection_ready, selected_microphone = (
                    microphone_selector.take_selection()
                )
                if selection_ready:
                    try:
                        voice_capture.select_device(selected_microphone)
                    except (RuntimeError, ValueError) as error:
                        voice_status = f"Microphone error: {error}"
                    else:
                        microphone_status = (
                            "Windows default microphone"
                            if selected_microphone is None
                            else microphone_names.get(
                                selected_microphone,
                                f"Microphone {selected_microphone}",
                            )
                        )
                        voice_status = "Microphone selected"

                if frame.timestamp_seconds >= next_debug_overlay_at:
                    rendered = overlay.draw(
                        frame.bgr,
                        tracked_hand,
                        state_machine.state,
                        runtime.active_handle,
                        None if candidate is None else candidate.title,
                        display_point,
                        voice_status,
                        microphone_status,
                    )
                    cv2.imshow("MITSU Debug", rendered)
                    next_debug_overlay_at = (
                        frame.timestamp_seconds + debug_overlay_interval_seconds
                    )

                key = cv2.waitKey(1) & 0xFF
                if key in (ord("v"), ord("V")):
                    try:
                        if voice_service is None:
                            voice_status = "Voice requires OPENAI_API_KEY"
                        elif voice_capture.is_recording:
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
                        voice_status = f"Audio error: {error}"
                if key in (ord("m"), ord("M")):
                    if voice_capture.is_recording:
                        voice_status = "Stop recording before changing microphone"
                    elif microphone_enumeration_error is not None:
                        voice_status = (
                            f"Microphone error: {microphone_enumeration_error}"
                        )
                    else:
                        microphone_selector.present(
                            microphone_devices,
                            voice_capture.device_index,
                        )
                        qt_application.processEvents()
                        voice_status = "Choose a microphone"
                if key in (ord("q"), 27):
                    break

    except Exception:
        logger.exception("MITSU stopped because of an unrecoverable error")
        return 1
    finally:
        if "runtime" in locals():
            runtime.release()
        if "perception_latency_ms" in locals():
            perception_summary = perception_latency_ms.summary()
            if perception_summary is not None:
                logger.info(
                    "Perception latency: n=%d p50=%.2fms p95=%.2fms",
                    perception_summary.count,
                    perception_summary.p50,
                    perception_summary.p95,
                )
        if "voice_latency_ms" in locals():
            voice_summary = voice_latency_ms.summary()
            if voice_summary is not None:
                logger.info(
                    "Voice latency: n=%d p50=%.2fms p95=%.2fms",
                    voice_summary.count,
                    voice_summary.p50,
                    voice_summary.p95,
                )
        if "jitter_meter" in locals():
            raw_jitter = jitter_meter.raw_standard_deviation()
            filtered_jitter = jitter_meter.filtered_standard_deviation()
            if raw_jitter is not None and filtered_jitter is not None:
                logger.info(
                    "Hand jitter: raw=%.6f filtered=%.6f",
                    raw_jitter,
                    filtered_jitter,
                )
        if "live_pointer" in locals():
            live_pointer.close()
        if "window_shelf" in locals():
            window_shelf.close()
        if "microphone_selector" in locals():
            microphone_selector.close()
        if "voice_capture" in locals():
            voice_capture.close()
        if locals().get("voice_service") is not None:
            voice_service.close()
        cv2.destroyAllWindows()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
