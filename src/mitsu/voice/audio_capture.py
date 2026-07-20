"""Bounded in-memory push-to-talk microphone capture."""

from __future__ import annotations

from collections import deque
from threading import Lock

import numpy as np
import sounddevice as sd

from mitsu.voice.types import AudioClip


class PushToTalkCapture:
    """Capture microphone audio only after an explicit user action."""

    def __init__(
            self,
            sample_rate_hz: int,
            maximum_duration_seconds: float,
    ) -> None:
        self._sample_rate_hz = sample_rate_hz
        self._maximum_samples = int(sample_rate_hz * maximum_duration_seconds)
        self._chunks: deque[np.ndarray] = deque()
        self._lock = Lock()
        self._stream: sd.InputStream | None = None


    @property
    def is_recording(self) -> bool:
        """Return whether a push-to-talk capture is active"""

        return self._stream is not None
    
    def start(self) -> None:
        """Start explicit local microphone capture"""

        if self._stream is not None:
            raise RuntimeError("Voice recording is already active")

        with self._lock:
            self._chunks.clear()

        self._stream = sd.InputStream(
            samplerate=self._sample_rate_hz,
            channels=1,
            dtype="float32",
            callback=self._on_audio,
        )
        self._stream.start()



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
            captured = sum(item.size for item in self._chunks)
            remaining = self._maximum_samples - captured
            if remaining > 0:
                self._chunks.append(chunk[:remaining])