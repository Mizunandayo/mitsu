"""Tests for safe microphone enumeration and selection."""

import numpy as np
import pytest
from pytest import MonkeyPatch

from mitsu.voice.audio_capture import AudioInputDevice, PushToTalkCapture


def _capture() -> PushToTalkCapture:
    return PushToTalkCapture(
        sample_rate_hz=16_000,
        maximum_duration_seconds=6.0,
        minimum_signal_rms=0.003,
    )


def test_input_devices_excludes_output_only_devices(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setattr(
        "mitsu.voice.audio_capture.sd.query_devices",
        lambda: [
            {"name": "Speakers", "max_input_channels": 0},
            {"name": "Microphone", "max_input_channels": 1},
        ],
    )

    assert PushToTalkCapture.input_devices() == (
        AudioInputDevice(index=1, name="Microphone"),
    )


def test_select_device_rejects_an_unavailable_index(monkeypatch: MonkeyPatch) -> None:
    capture = _capture()
    monkeypatch.setattr(
        PushToTalkCapture,
        "input_devices",
        staticmethod(lambda: (AudioInputDevice(index=4, name="Microphone"),)),
    )

    with pytest.raises(ValueError, match="no longer available"):
        capture.select_device(7)


def test_select_device_accepts_default_or_a_known_device(
    monkeypatch: MonkeyPatch,
) -> None:
    capture = _capture()
    monkeypatch.setattr(
        PushToTalkCapture,
        "input_devices",
        staticmethod(lambda: (AudioInputDevice(index=4, name="Microphone"),)),
    )

    capture.select_device(4)
    assert capture.device_index == 4
    capture.select_device(None)
    assert capture.device_index is None


def test_rms_reports_silence_and_signal() -> None:
    assert PushToTalkCapture._rms(np.zeros(32, dtype=np.float32)) == 0.0
    assert PushToTalkCapture._rms(np.ones(32, dtype=np.float32)) == 1.0
