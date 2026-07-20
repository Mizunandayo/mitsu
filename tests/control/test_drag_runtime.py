from __future__ import annotations

import pytest

from mitsu.config import Settings
from mitsu.control.coordinate_mapper import ScreenBounds, WindowPosition
from mitsu.control.drag_runtime import DragRuntime
from mitsu.control.monitor_layout import Monitor, MonitorLayout
from mitsu.perception.one_euro import Point2D


def test_runtime_moves_an_active_window_across_virtual_desktop() -> None:
    runtime = DragRuntime(_settings(), _dual_monitor_layout())
    runtime.begin_grip(
        handle=100,
        position=WindowPosition(100, 100),
        width=500,
        height=400,
        hand_position=Point2D(0.5, 0.5),
        timestamp_seconds=1.0,
    )

    next_position = runtime.move(Point2D(0.0, 0.5), 2.0)

    assert next_position.x < 0
    assert runtime.active_handle == 100


def test_release_clears_runtime_state_and_is_idempotent() -> None:
    runtime = DragRuntime(_settings(), _dual_monitor_layout())
    runtime.begin_grip(
        handle=100,
        position=WindowPosition(100, 100),
        width=500,
        height=400,
        hand_position=Point2D(0.5, 0.5),
        timestamp_seconds=1.0,
    )

    runtime.release()
    runtime.release()

    assert runtime.active_handle is None
    with pytest.raises(RuntimeError, match="active grip"):
        runtime.move(Point2D(0.6, 0.5), 2.0)


def test_runtime_rejects_overlapping_grips() -> None:
    runtime = DragRuntime(_settings(), _dual_monitor_layout())
    runtime.begin_grip(
        handle=100,
        position=WindowPosition(100, 100),
        width=500,
        height=400,
        hand_position=Point2D(0.5, 0.5),
        timestamp_seconds=1.0,
    )

    with pytest.raises(RuntimeError, match="another grip"):
        runtime.begin_grip(
            handle=200,
            position=WindowPosition(200, 200),
            width=500,
            height=400,
            hand_position=Point2D(0.5, 0.5),
            timestamp_seconds=2.0,
        )


def _settings() -> Settings:
    return Settings.model_validate(
        {
            "gesture": {
                "movement_gain": 1800.0,
                "minimum_delta_pixels": 0.0,
                "pinch": {"engage_ratio": 0.34, "release_ratio": 0.46},
                "velocity": {
                    "smoothing_alpha": 1.0,
                    "activation_speed": 0.35,
                    "maximum_gain_multiplier": 1.0,
                },
            },
            "filter": {
                "minimum_cutoff_hz": 1.2,
                "beta": 0.015,
                "derivative_cutoff_hz": 1.0,
            },
            "window": {
                "single_monitor_only": False,
                "require_monitor_consistency": True,
            },
            "voice": {
                "sample_rate_hz": 16_000,
                "maximum_recording_seconds": 6.0,
                "language": "en",
                "transcription_model": "gpt-4o-mini-transcribe",
                "transcription_prompt": "MITSU desktop window commands.",
            },
        }
    )


def _dual_monitor_layout() -> MonitorLayout:
    return MonitorLayout(
        monitors=(
            Monitor(
                device_name=r"\\.\DISPLAY1",
                bounds=ScreenBounds(-2560, 0, 0, 1600),
                dpi_x=192,
                dpi_y=192,
                is_primary=False,
            ),
            Monitor(
                device_name=r"\\.\DISPLAY2",
                bounds=ScreenBounds(0, 0, 1920, 1080),
                dpi_x=96,
                dpi_y=96,
                is_primary=True,
            ),
        )
    )
