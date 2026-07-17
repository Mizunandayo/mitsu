"""MediaPipe Tasks Hand Landmarker adapter in VIDEO mode."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import cv2
import mediapipe as mp
import numpy as np
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

from mitsu.gestures.pinch import HandLandmarks
from mitsu.perception.one_euro import Point2D


@dataclass(frozen=True, slots=True)
class TrackedHand:
    """The landmarks MITSU needs from one detected hand."""

    control_point: Point2D
    pinch_landmarks: HandLandmarks
    display_points: tuple[Point2D, ...]




class HandTracker:
    """Detect at most one hand from mirrored BGR camera frames."""

    def __init__(self, model_path: Path) -> None:
        options = vision.HandLandmarkerOptions(
            base_options=python.BaseOptions(model_asset_path=str(model_path)),
            running_mode=vision.RunningMode.VIDEO,
            num_hands=1,
            min_hand_detection_confidence=0.6,
            min_hand_presence_confidence=0.6,
            min_tracking_confidence=0.6,
        )
        self._landmarker = vision.HandLandmarker.create_from_options(options)
        

    def detect(
            self,
            bgr_frame: np.ndarray,
            timestamp_milliseconds: int,
    ) -> TrackedHand | None:
        """Return landmarks for one hand, or None if no hand is detected."""

        rgb_frame = cv2.cvtColor(bgr_frame, cv2.COLOR_BGR2RGB)
        image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        result = self._landmarker.detect_for_video(image, timestamp_milliseconds)

        if not result.hand_landmarks:
            return None
        
        landmarks = result.hand_landmarks[0]
        points = tuple(Point2D(point.x, point.y) for point in landmarks)

        return TrackedHand(
            control_point=points[8],  
            pinch_landmarks=HandLandmarks(
                wrist=points[0],
                thumb_tip=points[4],
                index_tip=points[8],
                middle_mcp=points[9],
            ),
            display_points=points,
        )
    
    def close(self) -> None:
        """Release MediaPipe task resources."""

        self._landmarker.close()
    

    def __enter__(self) -> HandTracker:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
        
