"""Bounded in-memory push-to-talk microphone capture."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from threading import Lock

import numpy as np
import sounddevice as sd

from mitsu.voice.types import AudioClip


@dataclass(frozen=True, slots=True)
class AudioInputDevice:
    """One input-capable PortAudio device exposed to the user."""

    index: int
    name: str


class PushToTalkCapture:
    """Capture microphone audio only after an explicit user action."""

    def __init__(
        self,
        sample_rate_hz: int,
        maximum_duration_seconds: float,
        minimum_signal_rms: float,
    ) -> None:
        if minimum_signal_rms <= 0.0:
            raise ValueError("minimum_signal_rms must be positive")
        self._sample_rate_hz = sample_rate_hz
        self._maximum_samples = int(sample_rate_hz * maximum_duration_seconds)
        self._minimum_signal_rms = minimum_signal_rms
        self._chunks: deque[np.ndarray] = deque()
        self._lock = Lock()
        self._stream: sd.InputStream | None = None
        self._latest_rms = 0.0
        self._device_index: int | None = None

    @property
    def is_recording(self) -> bool:
        """Return whether a push-to-talk capture is active"""

        return self._stream is not None

    @property
    def signal_rms(self) -> float:
        """Return the most recent microphone level without persisting audio."""

        with self._lock:
            return self._latest_rms

    @property
    def device_index(self) -> int | None:
        """Return the selected device, or None for the Windows default."""

        return self._device_index

    @staticmethod
    def input_devices() -> tuple[AudioInputDevice, ...]:
        """Enumerate usable input devices without opening an audio stream."""

        try:
            devices = sd.query_devices()
        except sd.PortAudioError as error:
            raise RuntimeError("Could not enumerate microphone devices") from error

        return tuple(
            AudioInputDevice(index=index, name=str(device["name"]))
            for index, device in enumerate(devices)
            if int(device["max_input_channels"]) > 0
        )

    def select_device(self, device_index: int | None) -> None:
        """Select a microphone for the next capture; never switch mid-recording."""

        if self._stream is not None:
            raise RuntimeError("Stop recording before changing microphone")
        if device_index is not None:
            available = {device.index for device in self.input_devices()}
            if device_index not in available:
                raise ValueError("Selected microphone is no longer available")
        self._device_index = device_index

    def start(self) -> None:
        """Start explicit local microphone capture"""

        if self._stream is not None:
            raise RuntimeError("Voice recording is already active")

        with self._lock:
            self._chunks.clear()
            self._latest_rms = 0.0

        try:
            self._stream = sd.InputStream(
                device=self._device_index,
                samplerate=self._sample_rate_hz,
                channels=1,
                dtype="float32",
                callback=self._on_audio,
            )
            self._stream.start()
        except sd.PortAudioError as error:
            self._stream = None
            raise RuntimeError("Could not open the selected microphone") from error

    def stop(self) -> AudioClip:
        """Stop capture and return the clip without persisting it."""

        if self._stream is None:
            raise RuntimeError("Voice recording is not active")

        stream = self._stream
        self._stream = None
        stream.stop()
        stream.close()

        with self._lock:
            chunks = tuple(self._chunks)
            self._chunks.clear()

        if not chunks:
            raise RuntimeError("No audio was captured")

        samples = np.concatenate(chunks).reshape(-1)
        if samples.size == 0:
            raise RuntimeError("No audio was captured")
        if self._rms(samples) < self._minimum_signal_rms:
            raise RuntimeError(
                "No speech detected; check the Windows default microphone"
            )

        return AudioClip(samples=samples, sample_rate_hz=self._sample_rate_hz)

    def close(self) -> None:
        """Close capture and discard all buffered speech."""

        if self._stream is not None:
            stream = self._stream
            self._stream = None
            stream.stop()
            stream.close()

        with self._lock:
            self._chunks.clear()
            self._latest_rms = 0.0

    def _on_audio(
        self,
        input_data: np.ndarray,
        _frames: int,
        _time: object,
        status: sd.CallbackFlags,
    ) -> None:
        if status:
            return

        chunk = input_data.copy().reshape(-1)

        with self._lock:
            self._latest_rms = self._rms(chunk)
            captured = sum(item.size for item in self._chunks)
            remaining = self._maximum_samples - captured
            if remaining > 0:
                self._chunks.append(chunk[:remaining])

    @staticmethod
    def _rms(samples: np.ndarray) -> float:
        """Return a bounded root-mean-square signal level."""

        return float(np.sqrt(np.mean(np.square(samples, dtype=np.float64))))
