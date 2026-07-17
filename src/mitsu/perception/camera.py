"""Mirrored OpenCV camera capture for local hand perception."""


from __future__ import annotations

import time
from dataclasses import dataclass

import cv2
import numpy as np


@dataclass(frozen=True, slots=True)
class CameraFrame:
    """A mirrored BGR frame and monotonically increasing timestamps."""

    bgr: np.ndarray
    timestamp_seconds: float
    timestamp_milliseconds: int


class Camera:
    """Own one local webcam capture device."""

    def __init__(self, device_index: int = 0) -> None:
        self._capture = cv2.VideoCapture(device_index, cv2.CAP_DSHOW)
        self._capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        if not self._capture.isOpened():
            self._capture.release()
            raise RuntimeError(f"Could not open camera device {device_index}")

        self._last_timestamp_milliseconds = -1

    def read(self) -> CameraFrame:
        """Read and mirror one camera frame before landmark inference."""

        success, frame = self._capture.read()
        if not success or frame is None:
            raise RuntimeError("Camera frame capture failed")

        timestamp_seconds = time.perf_counter()
        timestamp_milliseconds = max(
            int(timestamp_seconds * 1000),
            self._last_timestamp_milliseconds + 1,
        )
        self._last_timestamp_milliseconds = timestamp_milliseconds

        return CameraFrame(
            bgr=cv2.flip(frame, 1),
            timestamp_seconds=timestamp_seconds,
            timestamp_milliseconds=timestamp_milliseconds,
        )

    def close(self) -> None:
        """Release the camera device."""

        self._capture.release()

    def __enter__(self) -> Camera:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()